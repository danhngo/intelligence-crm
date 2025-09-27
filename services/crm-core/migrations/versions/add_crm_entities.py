"""Add CRM entities - companies, leads, deals, activities

Revision ID: ${revision}
Revises: ${down_revision}
Create Date: ${create_date}

"""
from typing import Sequence, Union
from uuid import uuid4

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic
revision = str(uuid4())
down_revision = str(uuid4())  # This should reference the actual init_contacts revision ID
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Upgrade database schema."""
    
    # Create companies table
    op.create_table('companies',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('tenant_id', sa.String(36), nullable=False, index=True),
        sa.Column('name', sa.String(200), nullable=False, index=True),
        sa.Column('legal_name', sa.String(200), nullable=True),
        sa.Column('industry', sa.String(100), nullable=True),
        sa.Column('company_type', sa.String(50), nullable=True),
        sa.Column('website', sa.String(255), nullable=True),
        sa.Column('email', sa.String(255), nullable=True),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('address_line1', sa.String(200), nullable=True),
        sa.Column('address_line2', sa.String(200), nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('state', sa.String(100), nullable=True),
        sa.Column('postal_code', sa.String(20), nullable=True),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('employee_count', sa.Integer, nullable=True),
        sa.Column('annual_revenue', sa.Float, nullable=True),
        sa.Column('founded_year', sa.Integer, nullable=True),
        sa.Column('linkedin', sa.String(255), nullable=True),
        sa.Column('twitter', sa.String(255), nullable=True),
        sa.Column('facebook', sa.String(255), nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('tags', sa.String(500), nullable=True),
        sa.Column('status', sa.String(50), nullable=True),
        sa.Column('company_score', sa.Float, nullable=True),
        sa.Column('owner_id', sa.String(36), nullable=True, index=True),
        sa.Column('parent_company_id', sa.String(36), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_deleted', sa.Boolean, default=False),
        sa.ForeignKeyConstraint(['parent_company_id'], ['companies.id'])
    )
    
    # Create leads table
    op.create_table('leads',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('tenant_id', sa.String(36), nullable=False, index=True),
        sa.Column('first_name', sa.String(100), nullable=False),
        sa.Column('last_name', sa.String(100), nullable=True),
        sa.Column('title', sa.String(100), nullable=True),
        sa.Column('email', sa.String(255), nullable=True, index=True),
        sa.Column('phone', sa.String(50), nullable=True),
        sa.Column('mobile', sa.String(50), nullable=True),
        sa.Column('company', sa.String(200), nullable=True),
        sa.Column('company_id', sa.String(36), nullable=True),
        sa.Column('address_line1', sa.String(200), nullable=True),
        sa.Column('address_line2', sa.String(200), nullable=True),
        sa.Column('city', sa.String(100), nullable=True),
        sa.Column('state', sa.String(100), nullable=True),
        sa.Column('postal_code', sa.String(20), nullable=True),
        sa.Column('country', sa.String(100), nullable=True),
        sa.Column('status', sa.String(50), nullable=False, default='new'),
        sa.Column('source', sa.String(100), nullable=True),
        sa.Column('lead_score', sa.Float, nullable=True),
        sa.Column('budget', sa.Float, nullable=True),
        sa.Column('interest_level', sa.String(20), nullable=True),
        sa.Column('expected_close_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('last_contact_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('linkedin', sa.String(255), nullable=True),
        sa.Column('twitter', sa.String(255), nullable=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('tags', sa.String(500), nullable=True),
        sa.Column('owner_id', sa.String(36), nullable=True, index=True),
        sa.Column('converted_contact_id', sa.String(36), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_deleted', sa.Boolean, default=False),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id']),
        sa.ForeignKeyConstraint(['converted_contact_id'], ['contacts.id'])
    )
    
    # Create deals table
    op.create_table('deals',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('tenant_id', sa.String(36), nullable=False, index=True),
        sa.Column('name', sa.String(200), nullable=False, index=True),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('amount', sa.Float, nullable=True),
        sa.Column('currency', sa.String(3), nullable=False, default='USD'),
        sa.Column('stage', sa.String(50), nullable=False, default='prospecting'),
        sa.Column('probability', sa.Float, nullable=True),
        sa.Column('expected_close_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('actual_close_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('contact_id', sa.String(36), nullable=True),
        sa.Column('company_id', sa.String(36), nullable=True),
        sa.Column('lead_id', sa.String(36), nullable=True),
        sa.Column('source', sa.String(100), nullable=True),
        sa.Column('deal_type', sa.String(50), nullable=True),
        sa.Column('product_category', sa.String(100), nullable=True),
        sa.Column('competitors', sa.String(500), nullable=True),
        sa.Column('risk_factors', sa.Text, nullable=True),
        sa.Column('tags', sa.String(500), nullable=True),
        sa.Column('owner_id', sa.String(36), nullable=True, index=True),
        sa.Column('team_members', sa.String(500), nullable=True),
        sa.Column('forecast_category', sa.String(20), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_deleted', sa.Boolean, default=False),
        sa.ForeignKeyConstraint(['contact_id'], ['contacts.id']),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id']),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id'])
    )
    
    # Create activities table
    op.create_table('activities',
        sa.Column('id', sa.String(36), primary_key=True),
        sa.Column('tenant_id', sa.String(36), nullable=False, index=True),
        sa.Column('subject', sa.String(200), nullable=False),
        sa.Column('description', sa.Text, nullable=True),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('status', sa.String(50), nullable=False, default='open'),
        sa.Column('priority', sa.String(20), nullable=False, default='normal'),
        sa.Column('due_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('start_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('end_time', sa.DateTime(timezone=True), nullable=True),
        sa.Column('duration_minutes', sa.Integer, nullable=True),
        sa.Column('completed', sa.Boolean, nullable=False, default=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('contact_id', sa.String(36), nullable=True),
        sa.Column('company_id', sa.String(36), nullable=True),
        sa.Column('lead_id', sa.String(36), nullable=True),
        sa.Column('deal_id', sa.String(36), nullable=True),
        sa.Column('owner_id', sa.String(36), nullable=True, index=True),
        sa.Column('assigned_to_id', sa.String(36), nullable=True, index=True),
        sa.Column('location', sa.String(200), nullable=True),
        sa.Column('meeting_url', sa.String(500), nullable=True),
        sa.Column('attendees', sa.String(1000), nullable=True),
        sa.Column('email_from', sa.String(255), nullable=True),
        sa.Column('email_to', sa.String(1000), nullable=True),
        sa.Column('email_cc', sa.String(1000), nullable=True),
        sa.Column('email_bcc', sa.String(1000), nullable=True),
        sa.Column('reminder_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('reminder_sent', sa.Boolean, nullable=False, default=False),
        sa.Column('outcome', sa.String(100), nullable=True),
        sa.Column('follow_up_required', sa.Boolean, nullable=False, default=False),
        sa.Column('follow_up_date', sa.DateTime(timezone=True), nullable=True),
        sa.Column('tags', sa.String(500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('deleted_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_deleted', sa.Boolean, default=False),
        sa.ForeignKeyConstraint(['contact_id'], ['contacts.id']),
        sa.ForeignKeyConstraint(['company_id'], ['companies.id']),
        sa.ForeignKeyConstraint(['lead_id'], ['leads.id']),
        sa.ForeignKeyConstraint(['deal_id'], ['deals.id'])
    )
    
    # Create indexes
    op.create_index('ix_companies_tenant_name', 'companies', ['tenant_id', 'name'])
    op.create_index('ix_leads_tenant_email', 'leads', ['tenant_id', 'email'])
    op.create_index('ix_leads_tenant_status', 'leads', ['tenant_id', 'status'])
    op.create_index('ix_deals_tenant_stage', 'deals', ['tenant_id', 'stage'])
    op.create_index('ix_deals_expected_close', 'deals', ['expected_close_date'])
    op.create_index('ix_activities_tenant_type', 'activities', ['tenant_id', 'type'])
    op.create_index('ix_activities_tenant_status', 'activities', ['tenant_id', 'status'])
    op.create_index('ix_activities_due_date', 'activities', ['due_date'])


def downgrade() -> None:
    """Downgrade database schema."""
    # Drop tables in reverse order due to foreign key constraints
    op.drop_table('activities')
    op.drop_table('deals')
    op.drop_table('leads')
    op.drop_table('companies')