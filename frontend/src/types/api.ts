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
  full_name: string;
  is_active: boolean;
  is_superuser: boolean;
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

// Contact Types
export interface Contact {
  id: string;
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  company?: string;
  position?: string;
  status: 'active' | 'inactive' | 'prospect';
  tags?: string[];
  notes?: string;
  created_at: string;
  updated_at: string;
  owner_id?: string;
}

export interface ContactCreate {
  first_name: string;
  last_name: string;
  email: string;
  phone?: string;
  company?: string;
  position?: string;
  status?: 'active' | 'inactive' | 'prospect';
  tags?: string[];
  notes?: string;
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
  token_type: string;
  user: User;
}
