"""Messages API endpoints."""

from typing import List, Dict, Any, Optional
from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


class Message(BaseModel):
    """Message model."""
    id: str
    content: str
    sender: str
    recipient: str
    channel: str
    status: str
    created_at: str
    sent_at: Optional[str] = None
    delivered_at: Optional[str] = None
    metadata: Dict[str, Any] = {}


class MessageTemplate(BaseModel):
    """Message template model."""
    id: str
    name: str
    channel: str
    template: str
    variables: List[str]
    description: str = ""


@router.get("/", response_model=List[Message])
async def list_messages(
    limit: int = Query(50, le=100),
    offset: int = Query(0, ge=0),
    channel: Optional[str] = None,
    status: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
) -> List[Message]:
    """List messages with optional filters."""
    # Mock implementation
    import datetime
    
    messages = []
    for i in range(min(limit, 10)):
        msg_id = f"msg-{offset + i + 1}"
        messages.append(Message(
            id=msg_id,
            content=f"Sample message content {i + 1}",
            sender="system",
            recipient=f"user-{i + 1}@example.com",
            channel=channel or ("email" if i % 2 == 0 else "sms"),
            status=status or ("delivered" if i % 3 != 0 else "pending"),
            created_at=datetime.datetime.utcnow().isoformat(),
            sent_at=datetime.datetime.utcnow().isoformat() if i % 3 != 0 else None,
            delivered_at=datetime.datetime.utcnow().isoformat() if i % 4 != 0 else None,
            metadata={"priority": "normal", "campaign": f"campaign-{i % 3 + 1}"}
        ))
    
    return messages


@router.get("/{message_id}", response_model=Message)
async def get_message(
    message_id: str,
    db: AsyncSession = Depends(get_db)
) -> Message:
    """Get a specific message by ID."""
    # Mock implementation
    import datetime
    
    return Message(
        id=message_id,
        content="Sample message content",
        sender="system",
        recipient="user@example.com",
        channel="email",
        status="delivered",
        created_at=datetime.datetime.utcnow().isoformat(),
        sent_at=datetime.datetime.utcnow().isoformat(),
        delivered_at=datetime.datetime.utcnow().isoformat(),
        metadata={"priority": "normal"}
    )


@router.get("/templates/", response_model=List[MessageTemplate])
async def list_templates(
    channel: Optional[str] = None,
    db: AsyncSession = Depends(get_db)
) -> List[MessageTemplate]:
    """List message templates."""
    # Mock implementation
    templates = [
        MessageTemplate(
            id="welcome-email",
            name="Welcome Email",
            channel="email",
            template="Welcome {{name}} to our CRM system! Your account is now active.",
            variables=["name"],
            description="Welcome email for new users"
        ),
        MessageTemplate(
            id="reminder-sms",
            name="Appointment Reminder",
            channel="sms",
            template="Hi {{name}}, reminder: appointment on {{date}} at {{time}}",
            variables=["name", "date", "time"],
            description="SMS reminder for appointments"
        ),
        MessageTemplate(
            id="follow-up-email",
            name="Follow-up Email",
            channel="email",
            template="Hi {{name}}, following up on {{subject}}. Next steps: {{action}}",
            variables=["name", "subject", "action"],
            description="Follow-up email template"
        )
    ]
    
    if channel:
        templates = [t for t in templates if t.channel == channel]
    
    return templates


@router.post("/templates/{template_id}/render")
async def render_template(
    template_id: str,
    variables: Dict[str, Any],
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Render a message template with variables."""
    # Mock implementation
    templates = {
        "welcome-email": "Welcome {{name}} to our CRM system! Your account is now active.",
        "reminder-sms": "Hi {{name}}, reminder: appointment on {{date}} at {{time}}",
        "follow-up-email": "Hi {{name}}, following up on {{subject}}. Next steps: {{action}}"
    }
    
    if template_id not in templates:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Template not found")
    
    template = templates[template_id]
    
    # Simple template rendering (in production, use proper template engine)
    rendered = template
    for key, value in variables.items():
        rendered = rendered.replace(f"{{{{{key}}}}}", str(value))
    
    return {
        "template_id": template_id,
        "rendered_content": rendered,
        "variables_used": list(variables.keys())
    }
