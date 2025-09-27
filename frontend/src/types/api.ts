// API Response Types
export interface ApiResponse<T = any> {
  success: boolean;
  data: T;
  message?: string;
}

// User Types
export interface User {
  id: string;
  email: string;
  first_name: string;
  last_name: string;
  is_active: boolean;
  is_superuser: boolean;
  email_verified: boolean;
  last_login: string | null;
  created_at: string;
  updated_at: string;
}

export interface UserCreate {
  email: string;
  password: string;
  full_name: string;
}

export interface UserUpdate {
  email?: string;
  full_name?: string;
  is_active?: boolean;
}

// Contact types
export interface Contact {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  organization?: string;
  title?: string;
  lead_status: 'prospect' | 'qualified' | 'customer' | 'inactive';
  preferred_contact_method?: 'email' | 'phone' | 'sms';
  tags: string[];
  notes?: string;
  last_contacted?: string;
  created_at: string;
  updated_at: string;
}

export interface ContactCreate {
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  organization?: string;
  title?: string;
  lead_status?: 'prospect' | 'qualified' | 'customer' | 'inactive';
  preferred_contact_method?: 'email' | 'phone' | 'sms';
  tags?: string[];
  notes?: string;
}

// Campaign types
export type CampaignType = 'EMAIL' | 'SMS' | 'WHATSAPP' | 'MULTI_CHANNEL';
export type CampaignStatus = 'DRAFT' | 'SCHEDULED' | 'RUNNING' | 'PAUSED' | 'COMPLETED' | 'CANCELLED';
export type EmailEventType = 'SENT' | 'DELIVERED' | 'OPENED' | 'CLICKED' | 'BOUNCED' | 'COMPLAINED' | 'UNSUBSCRIBED';

export interface Campaign {
  id: string;
  name: string;
  description?: string;
  type: CampaignType;
  status: CampaignStatus;
  tenant_id: string;
  created_by: string;
  scheduled_at?: string;
  started_at?: string;
  completed_at?: string;
  target_segments: string[];
  contact_list_ids: string[];
  template_id?: string;
  subject_line?: string;
  sender_name?: string;
  sender_email?: string;
  tracking_enabled: boolean;
  click_tracking_enabled: boolean;
  open_tracking_enabled: boolean;
  unsubscribe_enabled: boolean;
  total_recipients: number;
  sent_count: number;
  delivered_count: number;
  opened_count: number;
  clicked_count: number;
  bounced_count: number;
  complained_count: number;
  unsubscribed_count: number;
  config: Record<string, any>;
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface CampaignCreate {
  name: string;
  description?: string;
  type: CampaignType;
  scheduled_at?: string;
  target_segments?: string[];
  contact_list_ids?: string[];
  template_id?: string;
  subject_line?: string;
  sender_name?: string;
  sender_email?: string;
  tracking_enabled?: boolean;
  click_tracking_enabled?: boolean;
  open_tracking_enabled?: boolean;
  unsubscribe_enabled?: boolean;
  config?: Record<string, any>;
  metadata?: Record<string, any>;
}

export interface CampaignUpdate {
  name?: string;
  description?: string;
  status?: CampaignStatus;
  scheduled_at?: string;
  target_segments?: string[];
  contact_list_ids?: string[];
  template_id?: string;
  subject_line?: string;
  sender_name?: string;
  sender_email?: string;
  tracking_enabled?: boolean;
  click_tracking_enabled?: boolean;
  open_tracking_enabled?: boolean;
  unsubscribe_enabled?: boolean;
  config?: Record<string, any>;
  metadata?: Record<string, any>;
}

export interface CampaignStats {
  campaign_id: string;
  sent_count: number;
  delivered_count: number;
  unique_opens_count: number;
  total_opens_count: number;
  unique_clicks_count: number;
  total_clicks_count: number;
  bounce_count: number;
  unsubscribe_count: number;
  complaint_count: number;
}

export interface EmailTrackingEvent {
  id: string;
  campaign_id: string;
  message_id: string;
  recipient_email: string;
  event_type: 'SENT' | 'DELIVERED' | 'OPEN' | 'CLICK' | 'BOUNCE' | 'UNSUBSCRIBE' | 'COMPLAINT';
  created_at: string;
  ip_address?: string;
  user_agent?: string;
  url?: string;
  metadata?: Record<string, any>;
}

export interface EmailTemplate {
  id: string;
  name: string;
  description?: string;
  subject: string;
  html_content: string;
  text_content?: string;
  variables: string[];
  category?: string;
  is_active: boolean;
  tenant_id: string;
  created_by: string;
  metadata?: Record<string, any>;
  created_at: string;
  updated_at: string;
}

export interface EmailTemplateCreate {
  name: string;
  description?: string;
  subject: string;
  html_content: string;
  text_content?: string;
  variables?: string[];
  category?: string;
  is_active?: boolean;
  metadata?: Record<string, any>;
}

export interface ContactSegment {
  id: string;
  name: string;
  description?: string;
  tenant_id: string;
  created_by: string;
  criteria: Record<string, any>;
  contact_count: number;
  last_calculated_at?: string;
  is_dynamic: boolean;
  is_active: boolean;
  metadata: Record<string, any>;
  created_at: string;
  updated_at: string;
}

// Analytics Types
export interface AnalyticsEvent {
  id: string;
  event_type: string;
  user_id?: string;
  contact_id?: string;
  properties: Record<string, any>;
  timestamp: string;
}

export interface MessageAnalytics {
  id: string;
  channel: string;
  message_type: string;
  sentiment_score: number;
  response_time: number;
  user_id?: string;
  contact_id?: string;
  timestamp: string;
}

export interface ConversationAnalytics {
  id: string;
  conversation_id: string;
  channel: string;
  duration: number;
  message_count: number;
  satisfaction_score?: number;
  resolution_status: string;
  timestamp: string;
}

export interface DashboardMetrics {
  total_contacts: number;
  active_users: number;
  total_conversations: number;
  avg_response_time: number;
  satisfaction_score: number;
  conversion_rate: number;
}

// Workflow Types
export interface Workflow {
  id: string;
  name: string;
  description?: string;
  status: 'active' | 'inactive' | 'draft';
  trigger_type: string;
  actions: WorkflowAction[];
  created_at: string;
  updated_at: string;
}

export interface WorkflowAction {
  id: string;
  type: string;
  parameters: Record<string, any>;
  order: number;
}

export interface WorkflowExecution {
  id: string;
  workflow_id: string;
  status: 'running' | 'completed' | 'failed';
  started_at: string;
  completed_at?: string;
  error_message?: string;
}

// Message Types
export interface Message {
  id: string;
  content: string;
  channel: string;
  direction: 'inbound' | 'outbound';
  contact_id?: string;
  user_id?: string;
  metadata?: Record<string, any>;
  timestamp: string;
}

// Channel Types
export interface Channel {
  id: string;
  name: string;
  type: 'email' | 'sms' | 'whatsapp' | 'webchat' | 'phone';
  configuration: Record<string, any>;
  is_active: boolean;
  created_at: string;
}

// Auth Types
export interface LoginRequest {
  email: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}
