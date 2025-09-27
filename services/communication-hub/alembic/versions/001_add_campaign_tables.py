"""Add campaign and email tracking tables

Revision ID: 001_add_campaign_tables
Revises: 
Create Date: 2024-09-25 20:45:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001_add_campaign_tables'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # Create campaigns table
    op.create_table('campaigns',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('type', sa.Enum('EMAIL', 'SMS', 'WHATSAPP', 'MULTI_CHANNEL', name='campaigntype'), nullable=False),
        sa.Column('status', sa.Enum('DRAFT', 'SCHEDULED', 'RUNNING', 'PAUSED', 'COMPLETED', 'CANCELLED', name='campaignstatus'), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('created_by', sa.UUID(), nullable=False),
        sa.Column('scheduled_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('started_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('target_segments', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('contact_list_ids', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('template_id', sa.UUID(), nullable=True),
        sa.Column('subject_line', sa.String(length=255), nullable=True),
        sa.Column('sender_name', sa.String(length=100), nullable=True),
        sa.Column('sender_email', sa.String(length=255), nullable=True),
        sa.Column('tracking_enabled', sa.Boolean(), nullable=False),
        sa.Column('click_tracking_enabled', sa.Boolean(), nullable=False),
        sa.Column('open_tracking_enabled', sa.Boolean(), nullable=False),
        sa.Column('unsubscribe_enabled', sa.Boolean(), nullable=False),
        sa.Column('total_recipients', sa.Integer(), nullable=False),
        sa.Column('sent_count', sa.Integer(), nullable=False),
        sa.Column('delivered_count', sa.Integer(), nullable=False),
        sa.Column('opened_count', sa.Integer(), nullable=False),
        sa.Column('clicked_count', sa.Integer(), nullable=False),
        sa.Column('bounced_count', sa.Integer(), nullable=False),
        sa.Column('complained_count', sa.Integer(), nullable=False),
        sa.Column('unsubscribed_count', sa.Integer(), nullable=False),
        sa.Column('config', sa.JSON(), nullable=False),
        sa.Column('extra_data', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_campaigns_tenant_id'), 'campaigns', ['tenant_id'], unique=False)
    
    # Create campaign_messages table
    op.create_table('campaign_messages',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('campaign_id', sa.UUID(), nullable=False),
        sa.Column('message_id', sa.UUID(), nullable=True),
        sa.Column('recipient_email', sa.String(length=255), nullable=False),
        sa.Column('recipient_contact_id', sa.UUID(), nullable=True),
        sa.Column('subject_line', sa.String(length=255), nullable=False),
        sa.Column('html_content', sa.Text(), nullable=True),
        sa.Column('text_content', sa.Text(), nullable=True),
        sa.Column('tracking_id', sa.String(length=255), nullable=False),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('delivered_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('error_message', sa.Text(), nullable=True),
        sa.Column('retry_count', sa.Integer(), nullable=False),
        sa.Column('personalization_data', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tracking_id')
    )
    op.create_index(op.f('ix_campaign_messages_campaign_id'), 'campaign_messages', ['campaign_id'], unique=False)
    op.create_index(op.f('ix_campaign_messages_recipient_email'), 'campaign_messages', ['recipient_email'], unique=False)
    op.create_index(op.f('ix_campaign_messages_tracking_id'), 'campaign_messages', ['tracking_id'], unique=False)
    
    # Create email_tracking_events table
    op.create_table('email_tracking_events',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('campaign_id', sa.UUID(), nullable=True),
        sa.Column('campaign_message_id', sa.UUID(), nullable=True),
        sa.Column('message_id', sa.UUID(), nullable=True),
        sa.Column('event_type', sa.Enum('SENT', 'DELIVERED', 'OPENED', 'CLICKED', 'BOUNCED', 'COMPLAINED', 'UNSUBSCRIBED', name='emaileventtype'), nullable=False),
        sa.Column('tracking_id', sa.String(length=255), nullable=False),
        sa.Column('recipient_email', sa.String(length=255), nullable=False),
        sa.Column('event_timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('url', sa.Text(), nullable=True),
        sa.Column('link_id', sa.String(length=255), nullable=True),
        sa.Column('user_agent', sa.Text(), nullable=True),
        sa.Column('ip_address', postgresql.INET(), nullable=True),
        sa.Column('country', sa.String(length=2), nullable=True),
        sa.Column('region', sa.String(length=100), nullable=True),
        sa.Column('city', sa.String(length=100), nullable=True),
        sa.Column('device_type', sa.String(length=50), nullable=True),
        sa.Column('client_name', sa.String(length=100), nullable=True),
        sa.Column('client_version', sa.String(length=50), nullable=True),
        sa.Column('extra_data', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['campaign_id'], ['campaigns.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['campaign_message_id'], ['campaign_messages.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['message_id'], ['messages.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_email_tracking_events_campaign_id'), 'email_tracking_events', ['campaign_id'], unique=False)
    op.create_index(op.f('ix_email_tracking_events_campaign_message_id'), 'email_tracking_events', ['campaign_message_id'], unique=False)
    op.create_index(op.f('ix_email_tracking_events_event_type'), 'email_tracking_events', ['event_type'], unique=False)
    op.create_index(op.f('ix_email_tracking_events_tracking_id'), 'email_tracking_events', ['tracking_id'], unique=False)
    op.create_index(op.f('ix_email_tracking_events_recipient_email'), 'email_tracking_events', ['recipient_email'], unique=False)
    op.create_index(op.f('ix_email_tracking_events_event_timestamp'), 'email_tracking_events', ['event_timestamp'], unique=False)
    
    # Create email_templates table
    op.create_table('email_templates',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('created_by', sa.UUID(), nullable=False),
        sa.Column('subject_template', sa.String(length=255), nullable=False),
        sa.Column('html_template', sa.Text(), nullable=True),
        sa.Column('text_template', sa.Text(), nullable=True),
        sa.Column('variables', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('sample_data', sa.JSON(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('category', sa.String(length=100), nullable=True),
        sa.Column('tags', postgresql.ARRAY(sa.String()), nullable=False),
        sa.Column('usage_count', sa.Integer(), nullable=False),
        sa.Column('last_used_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('extra_data', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_email_templates_tenant_id'), 'email_templates', ['tenant_id'], unique=False)
    
    # Create contact_segments table
    op.create_table('contact_segments',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('created_by', sa.UUID(), nullable=False),
        sa.Column('criteria', sa.JSON(), nullable=False),
        sa.Column('contact_count', sa.Integer(), nullable=False),
        sa.Column('last_calculated_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('is_dynamic', sa.Boolean(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('extra_data', sa.JSON(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_contact_segments_tenant_id'), 'contact_segments', ['tenant_id'], unique=False)


def downgrade():
    # Drop tables in reverse order
    op.drop_index(op.f('ix_contact_segments_tenant_id'), table_name='contact_segments')
    op.drop_table('contact_segments')
    
    op.drop_index(op.f('ix_email_templates_tenant_id'), table_name='email_templates')
    op.drop_table('email_templates')
    
    op.drop_index(op.f('ix_email_tracking_events_event_timestamp'), table_name='email_tracking_events')
    op.drop_index(op.f('ix_email_tracking_events_recipient_email'), table_name='email_tracking_events')
    op.drop_index(op.f('ix_email_tracking_events_tracking_id'), table_name='email_tracking_events')
    op.drop_index(op.f('ix_email_tracking_events_event_type'), table_name='email_tracking_events')
    op.drop_index(op.f('ix_email_tracking_events_campaign_message_id'), table_name='email_tracking_events')
    op.drop_index(op.f('ix_email_tracking_events_campaign_id'), table_name='email_tracking_events')
    op.drop_table('email_tracking_events')
    
    op.drop_index(op.f('ix_campaign_messages_tracking_id'), table_name='campaign_messages')
    op.drop_index(op.f('ix_campaign_messages_recipient_email'), table_name='campaign_messages')
    op.drop_index(op.f('ix_campaign_messages_campaign_id'), table_name='campaign_messages')
    op.drop_table('campaign_messages')
    
    op.drop_index(op.f('ix_campaigns_tenant_id'), table_name='campaigns')
    op.drop_table('campaigns')
    
    # Drop enums
    op.execute('DROP TYPE IF EXISTS emaileventtype')
    op.execute('DROP TYPE IF EXISTS campaignstatus')
    op.execute('DROP TYPE IF EXISTS campaigntype')
