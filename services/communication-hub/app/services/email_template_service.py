"""Email template service for template management."""

import logging
from typing import Any, Dict, List, Optional
from uuid import UUID

from jinja2 import Environment, BaseLoader, TemplateError
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.campaign import EmailTemplate
from app.schemas.campaign import (
    EmailTemplateCreate,
    EmailTemplateList,
    EmailTemplateUpdate
)

logger = logging.getLogger(__name__)


class EmailTemplateService:
    """Service for email template management."""

    def __init__(self, db: AsyncSession):
        self.db = db
        self.jinja_env = Environment(loader=BaseLoader())

    async def create_template(
        self,
        template: EmailTemplateCreate,
        tenant_id: UUID,
        created_by: UUID
    ) -> EmailTemplate:
        """Create a new email template."""
        db_template = EmailTemplate(
            **template.model_dump(),
            tenant_id=tenant_id,
            created_by=created_by
        )
        
        self.db.add(db_template)
        await self.db.commit()
        await self.db.refresh(db_template)
        
        logger.info(f"Created email template {db_template.id} for tenant {tenant_id}")
        return db_template

    async def list_templates(
        self,
        tenant_id: UUID,
        skip: int = 0,
        limit: int = 20,
        category: Optional[str] = None,
        search: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> EmailTemplateList:
        """List email templates with filtering."""
        query = select(EmailTemplate).where(EmailTemplate.tenant_id == tenant_id)
        
        # Apply filters
        if category:
            query = query.where(EmailTemplate.category == category)
        if search:
            query = query.where(
                EmailTemplate.name.ilike(f"%{search}%") |
                EmailTemplate.description.ilike(f"%{search}%")
            )
        if is_active is not None:
            query = query.where(EmailTemplate.is_active == is_active)
        
        # Get total count
        count_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(count_query)
        total = total_result.scalar()
        
        # Apply pagination and ordering
        query = query.order_by(EmailTemplate.created_at.desc()).offset(skip).limit(limit)
        result = await self.db.execute(query)
        templates = result.scalars().all()
        
        return EmailTemplateList(
            items=templates,
            total=total,
            skip=skip,
            limit=limit
        )

    async def get_template(self, template_id: UUID, tenant_id: UUID) -> Optional[EmailTemplate]:
        """Get a specific email template."""
        query = select(EmailTemplate).where(
            EmailTemplate.id == template_id,
            EmailTemplate.tenant_id == tenant_id
        )
        result = await self.db.execute(query)
        return result.scalar_one_or_none()

    async def update_template(
        self,
        template_id: UUID,
        template_update: EmailTemplateUpdate,
        tenant_id: UUID
    ) -> Optional[EmailTemplate]:
        """Update an email template."""
        template = await self.get_template(template_id, tenant_id)
        if not template:
            return None
        
        # Update fields
        update_data = template_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(template, field, value)
        
        await self.db.commit()
        await self.db.refresh(template)
        
        logger.info(f"Updated email template {template_id}")
        return template

    async def delete_template(self, template_id: UUID, tenant_id: UUID) -> bool:
        """Delete an email template."""
        template = await self.get_template(template_id, tenant_id)
        if not template:
            return False
        
        await self.db.delete(template)
        await self.db.commit()
        
        logger.info(f"Deleted email template {template_id}")
        return True

    async def preview_template(
        self,
        template_id: UUID,
        tenant_id: UUID,
        data: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Preview template with provided data."""
        template = await self.get_template(template_id, tenant_id)
        if not template:
            return None
        
        try:
            # Render subject
            subject_template = self.jinja_env.from_string(template.subject_template)
            rendered_subject = subject_template.render(**data)
            
            # Render HTML content
            rendered_html = None
            if template.html_template:
                html_template = self.jinja_env.from_string(template.html_template)
                rendered_html = html_template.render(**data)
            
            # Render text content
            rendered_text = None
            if template.text_template:
                text_template = self.jinja_env.from_string(template.text_template)
                rendered_text = text_template.render(**data)
            
            return {
                "subject": rendered_subject,
                "html_content": rendered_html,
                "text_content": rendered_text,
                "variables_used": template.variables,
                "data_provided": list(data.keys())
            }
            
        except TemplateError as e:
            logger.error(f"Template rendering error for {template_id}: {e}")
            raise ValueError(f"Template rendering error: {str(e)}")

    async def duplicate_template(
        self,
        template_id: UUID,
        new_name: str,
        tenant_id: UUID,
        created_by: UUID
    ) -> Optional[EmailTemplate]:
        """Duplicate an existing template."""
        original = await self.get_template(template_id, tenant_id)
        if not original:
            return None
        
        # Create new template with copied data
        new_template = EmailTemplate(
            name=new_name,
            description=f"Copy of {original.name}",
            subject_template=original.subject_template,
            html_template=original.html_template,
            text_template=original.text_template,
            variables=original.variables.copy() if original.variables else [],
            sample_data=original.sample_data.copy() if original.sample_data else {},
            category=original.category,
            tags=original.tags.copy() if original.tags else [],
            extra_data=original.extra_data.copy() if original.extra_data else {},
            tenant_id=tenant_id,
            created_by=created_by
        )
        
        self.db.add(new_template)
        await self.db.commit()
        await self.db.refresh(new_template)
        
        logger.info(f"Duplicated template {template_id} as {new_template.id}")
        return new_template

    def extract_variables(self, template_content: str) -> List[str]:
        """Extract template variables from Jinja2 template."""
        try:
            template = self.jinja_env.from_string(template_content)
            return list(template.environment.parse(template_content).find_all(
                lambda node: hasattr(node, 'name')
            ))
        except Exception as e:
            logger.error(f"Error extracting variables: {e}")
            return []
