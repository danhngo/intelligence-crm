"""Initial database migration for contacts.

Revision ID: ${revision}
Revises: 
Create Date: ${create_date}
"""

from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = str(uuid4())
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create contacts table
    op.create_table(
        "contacts",
        sa.Column("id", sa.String(36), primary_key=True),
        sa.Column("tenant_id", sa.String(36), nullable=False),
        
        # Basic information
        sa.Column("first_name", sa.String(100), nullable=False),
        sa.Column("last_name", sa.String(100), nullable=True),
        sa.Column("organization", sa.String(200), nullable=True),
        sa.Column("title", sa.String(100), nullable=True),
        
        # Contact information
        sa.Column("email", sa.String(255), nullable=True),
        sa.Column("phone", sa.String(50), nullable=True),
        sa.Column("mobile", sa.String(50), nullable=True),
        
        # Address
        sa.Column("address_line1", sa.String(200), nullable=True),
        sa.Column("address_line2", sa.String(200), nullable=True),
        sa.Column("city", sa.String(100), nullable=True),
        sa.Column("state", sa.String(100), nullable=True),
        sa.Column("postal_code", sa.String(20), nullable=True),
        sa.Column("country", sa.String(100), nullable=True),
        
        # Additional fields
        sa.Column("description", sa.String(1000), nullable=True),
        sa.Column("website", sa.String(255), nullable=True),
        sa.Column("linkedin", sa.String(255), nullable=True),
        sa.Column("twitter", sa.String(255), nullable=True),
        
        # Lead information
        sa.Column("lead_score", sa.Float, nullable=True),
        sa.Column("lead_status", sa.String(50), nullable=True),
        sa.Column("lead_source", sa.String(100), nullable=True),
        
        # Tags
        sa.Column("tags", sa.String(500), nullable=True),
        
        # Preferences
        sa.Column("preferred_contact_method", sa.String(20), nullable=True),
        sa.Column("opt_out", sa.Boolean, default=False),
        
        # Metadata
        sa.Column("owner_id", sa.String(36), nullable=True),
        sa.Column("created_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("updated_at", sa.DateTime(timezone=True), nullable=False),
        sa.Column("deleted_at", sa.DateTime(timezone=True), nullable=True),
        sa.Column("is_deleted", sa.Boolean, default=False),
    )
    
    # Create indexes
    op.create_index("ix_contacts_tenant_id", "contacts", ["tenant_id"])
    op.create_index("ix_contacts_email", "contacts", ["email"])
    op.create_index("ix_contacts_owner_id", "contacts", ["owner_id"])


def downgrade() -> None:
    # Drop indexes
    op.drop_index("ix_contacts_owner_id")
    op.drop_index("ix_contacts_email")
    op.drop_index("ix_contacts_tenant_id")
    
    # Drop table
    op.drop_table("contacts")
