import { useMutation, useQuery, useQueryClient } from 'react-query';
import type { 
  Campaign, 
  CampaignCreate, 
  CampaignUpdate,
  CampaignStats,
  EmailTrackingEvent,
  EmailTemplate,
  EmailTemplateCreate,
  ContactSegment
} from '@/types/api';

const COMMUNICATION_HUB_BASE_URL = 'http://localhost:8004/api/v1';

// Helper function to get auth headers
const getAuthHeaders = () => ({
  'Content-Type': 'application/json',
  'Authorization': `Bearer ${localStorage.getItem('token')}`,
});

// Campaign Hooks
export const useCampaigns = (params?: {
  skip?: number;
  limit?: number;
  status?: string;
  campaign_type?: string;
  search?: string;
}) => {
  return useQuery<Campaign[]>(['campaigns', params], async (): Promise<Campaign[]> => {
    const searchParams = new URLSearchParams();
    if (params?.skip) searchParams.append('skip', params.skip.toString());
    if (params?.limit) searchParams.append('limit', params.limit.toString());
    if (params?.status) searchParams.append('status', params.status);
    if (params?.campaign_type) searchParams.append('campaign_type', params.campaign_type);
    if (params?.search) searchParams.append('search', params.search);
    
    const response = await fetch(`${COMMUNICATION_HUB_BASE_URL}/campaigns?${searchParams}`, {
      headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch campaigns');
    }
    
    const data = await response.json();
    return data.items || [];
  }, {
    keepPreviousData: true,
  });
};

export const useCampaign = (campaignId: string) => {
  return useQuery<Campaign>(['campaign', campaignId], async (): Promise<Campaign> => {
    const response = await fetch(`${COMMUNICATION_HUB_BASE_URL}/campaigns/${campaignId}`, {
      headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch campaign');
    }
    
    return response.json();
  }, {
    enabled: !!campaignId,
  });
};

export const useCreateCampaign = () => {
  const queryClient = useQueryClient();
  
  return useMutation(async (campaign: CampaignCreate): Promise<Campaign> => {
    const response = await fetch(`${COMMUNICATION_HUB_BASE_URL}/campaigns`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(campaign),
    });
    
    if (!response.ok) {
      throw new Error('Failed to create campaign');
    }
    
    return response.json();
  }, {
    onSuccess: () => {
      queryClient.invalidateQueries('campaigns');
    },
  });
};

export const useUpdateCampaign = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    async ({ campaignId, updates }: { campaignId: string; updates: CampaignUpdate }): Promise<Campaign> => {
      const response = await fetch(`${COMMUNICATION_HUB_BASE_URL}/campaigns/${campaignId}`, {
        method: 'PUT',
        headers: getAuthHeaders(),
        body: JSON.stringify(updates),
      });
      
      if (!response.ok) {
        throw new Error('Failed to update campaign');
      }
      
      return response.json();
    },
    {
      onSuccess: (_, { campaignId }) => {
        queryClient.invalidateQueries('campaigns');
        queryClient.invalidateQueries(['campaign', campaignId]);
      },
    }
  );
};

export const useDeleteCampaign = () => {
  const queryClient = useQueryClient();
  
  return useMutation(async (campaignId: string) => {
    const response = await fetch(`${COMMUNICATION_HUB_BASE_URL}/campaigns/${campaignId}`, {
      method: 'DELETE',
      headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to delete campaign');
    }
    
    return response.json();
  }, {
    onSuccess: () => {
      queryClient.invalidateQueries('campaigns');
    },
  });
};

export const useStartCampaign = () => {
  const queryClient = useQueryClient();
  
  return useMutation(async (campaignId: string): Promise<Campaign> => {
    const response = await fetch(`${COMMUNICATION_HUB_BASE_URL}/campaigns/${campaignId}/start`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to start campaign');
    }
    
    return response.json();
  }, {
    onSuccess: (_, campaignId) => {
      queryClient.invalidateQueries('campaigns');
      queryClient.invalidateQueries(['campaign', campaignId]);
    },
  });
};

export const usePauseCampaign = () => {
  const queryClient = useQueryClient();
  
  return useMutation(async (campaignId: string): Promise<Campaign> => {
    const response = await fetch(`${COMMUNICATION_HUB_BASE_URL}/campaigns/${campaignId}/pause`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to pause campaign');
    }
    
    return response.json();
  }, {
    onSuccess: (_, campaignId) => {
      queryClient.invalidateQueries('campaigns');
      queryClient.invalidateQueries(['campaign', campaignId]);
    },
  });
};

export const useStopCampaign = () => {
  const queryClient = useQueryClient();
  
  return useMutation(async (campaignId: string): Promise<Campaign> => {
    const response = await fetch(`${COMMUNICATION_HUB_BASE_URL}/campaigns/${campaignId}/stop`, {
      method: 'POST',
      headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to stop campaign');
    }
    
    return response.json();
  }, {
    onSuccess: (_, campaignId) => {
      queryClient.invalidateQueries('campaigns');
      queryClient.invalidateQueries(['campaign', campaignId]);
    },
  });
};

export const useCampaignStats = (campaignId: string) => {
  return useQuery<CampaignStats>(['campaign-stats', campaignId], async (): Promise<CampaignStats> => {
    const response = await fetch(`${COMMUNICATION_HUB_BASE_URL}/campaigns/${campaignId}/stats`, {
      headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch campaign stats');
    }
    
    return response.json();
  }, {
    enabled: !!campaignId,
    refetchInterval: 30000, // Refresh every 30 seconds
  });
};

export const useCampaignEvents = (campaignId: string, params?: {
  skip?: number;
  limit?: number;
  event_type?: string;
}) => {
  return useQuery<EmailTrackingEvent[]>(['campaign-events', campaignId, params], async (): Promise<EmailTrackingEvent[]> => {
    const searchParams = new URLSearchParams();
    if (params?.skip) searchParams.append('skip', params.skip.toString());
    if (params?.limit) searchParams.append('limit', params.limit.toString());
    if (params?.event_type) searchParams.append('event_type', params.event_type);
    
    const response = await fetch(`${COMMUNICATION_HUB_BASE_URL}/campaigns/${campaignId}/events?${searchParams}`, {
      headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch campaign events');
    }
    
    const data = await response.json();
    return data.items || [];
  }, {
    enabled: !!campaignId,
    refetchInterval: 10000, // Refresh every 10 seconds
  });
};

// Email Template Hooks
export const useEmailTemplates = (params?: {
  skip?: number;
  limit?: number;
  category?: string;
  search?: string;
  is_active?: boolean;
}) => {
  return useQuery<EmailTemplate[]>(['email-templates', params], async (): Promise<EmailTemplate[]> => {
    const searchParams = new URLSearchParams();
    if (params?.skip) searchParams.append('skip', params.skip.toString());
    if (params?.limit) searchParams.append('limit', params.limit.toString());
    if (params?.category) searchParams.append('category', params.category);
    if (params?.search) searchParams.append('search', params.search);
    if (params?.is_active !== undefined) searchParams.append('is_active', params.is_active.toString());
    
    const response = await fetch(`${COMMUNICATION_HUB_BASE_URL}/templates?${searchParams}`, {
      headers: getAuthHeaders(),
    });
    
    if (!response.ok) {
      throw new Error('Failed to fetch email templates');
    }
    
    const data = await response.json();
    return data.items || [];
  });
};

export const useCreateEmailTemplate = () => {
  const queryClient = useQueryClient();
  
  return useMutation(async (template: EmailTemplateCreate): Promise<EmailTemplate> => {
    const response = await fetch(`${COMMUNICATION_HUB_BASE_URL}/templates`, {
      method: 'POST',
      headers: getAuthHeaders(),
      body: JSON.stringify(template),
    });
    
    if (!response.ok) {
      throw new Error('Failed to create email template');
    }
    
    return response.json();
  }, {
    onSuccess: () => {
      queryClient.invalidateQueries('email-templates');
    },
  });
};

// Contact Segment Hooks
export const useContactSegments = () => {
  return useQuery<ContactSegment[]>('contact-segments', async (): Promise<ContactSegment[]> => {
    // TODO: Implement actual API call when segments endpoint is ready
    // For now, return mock data
    return [
      {
        id: '1',
        name: 'Active Prospects',
        description: 'Contacts with prospect status who have engaged recently',
        tenant_id: '1',
        created_by: '1',
        criteria: { lead_status: 'prospect', last_contacted: 'within_30_days' },
        contact_count: 150,
        last_calculated_at: new Date().toISOString(),
        is_dynamic: true,
        is_active: true,
        metadata: {},
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
      {
        id: '2',
        name: 'Qualified Leads',
        description: 'Contacts that have been qualified as sales ready',
        tenant_id: '1',
        created_by: '1',
        criteria: { lead_status: 'qualified' },
        contact_count: 75,
        last_calculated_at: new Date().toISOString(),
        is_dynamic: true,
        is_active: true,
        metadata: {},
        created_at: new Date().toISOString(),
        updated_at: new Date().toISOString(),
      },
    ];
  });
};
