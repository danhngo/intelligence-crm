import { useQuery, useMutation, useQueryClient } from 'react-query';
import { apiClient } from '@/lib/api-client';
import { 
  Contact, 
  ContactCreate, 
  DashboardMetrics, 
  AnalyticsEvent,
  MessageAnalytics,
  ConversationAnalytics,
  Workflow,
  Message,
  User 
} from '@/types/api';

// Auth Hooks
export const useCurrentUser = () => {
  return useQuery('currentUser', () => apiClient.getCurrentUser(), {
    retry: false,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useLogin = () => {
  return useMutation(apiClient.login);
};

// Dashboard Hooks
export const useDashboardMetrics = () => {
  return useQuery<DashboardMetrics>('dashboardMetrics', () => apiClient.getDashboardMetrics(), {
    refetchInterval: 30000, // Refetch every 30 seconds
  });
};

// Analytics Hooks
export const useAnalyticsEvents = (params?: any) => {
  return useQuery<AnalyticsEvent[]>(['analyticsEvents', params], () => 
    apiClient.getEvents(params), {
    keepPreviousData: true,
  });
};

export const useMessageAnalytics = (params?: any) => {
  return useQuery<MessageAnalytics[]>(['messageAnalytics', params], () => 
    apiClient.getMessageAnalytics(params), {
    keepPreviousData: true,
  });
};

export const useConversationAnalytics = (params?: any) => {
  return useQuery<ConversationAnalytics[]>(['conversationAnalytics', params], () => 
    apiClient.getConversationAnalytics(params), {
    keepPreviousData: true,
  });
};

export const useCreateEvent = () => {
  const queryClient = useQueryClient();
  
  return useMutation(apiClient.createEvent, {
    onSuccess: () => {
      queryClient.invalidateQueries('analyticsEvents');
      queryClient.invalidateQueries('dashboardMetrics');
    },
  });
};

// Contact Hooks
export const useContacts = (params?: any) => {
  return useQuery<Contact[]>(['contacts', params], () => 
    apiClient.getContacts(params), {
    keepPreviousData: true,
  });
};

export const useContact = (id: string) => {
  return useQuery<Contact>(['contact', id], () => 
    apiClient.getContact(id), {
    enabled: !!id,
  });
};

export const useCreateContact = () => {
  const queryClient = useQueryClient();
  
  return useMutation(apiClient.createContact, {
    onSuccess: () => {
      queryClient.invalidateQueries('contacts');
      queryClient.invalidateQueries('dashboardMetrics');
    },
  });
};

export const useUpdateContact = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    ({ id, contact }: { id: string; contact: Partial<ContactCreate> }) =>
      apiClient.updateContact(id, contact),
    {
      onSuccess: (_, { id }) => {
        queryClient.invalidateQueries('contacts');
        queryClient.invalidateQueries(['contact', id]);
        queryClient.invalidateQueries('dashboardMetrics');
      },
    }
  );
};

export const useDeleteContact = () => {
  const queryClient = useQueryClient();
  
  return useMutation(apiClient.deleteContact, {
    onSuccess: () => {
      queryClient.invalidateQueries('contacts');
      queryClient.invalidateQueries('dashboardMetrics');
    },
  });
};

// Workflow Hooks
export const useWorkflows = () => {
  return useQuery<Workflow[]>('workflows', () => apiClient.getWorkflows());
};

export const useWorkflow = (id: string) => {
  return useQuery<Workflow>(['workflow', id], () => 
    apiClient.getWorkflow(id), {
    enabled: !!id,
  });
};

export const useCreateWorkflow = () => {
  const queryClient = useQueryClient();
  
  return useMutation(apiClient.createWorkflow, {
    onSuccess: () => {
      queryClient.invalidateQueries('workflows');
    },
  });
};

export const useExecuteWorkflow = () => {
  const queryClient = useQueryClient();
  
  return useMutation(
    ({ id, params }: { id: string; params?: any }) =>
      apiClient.executeWorkflow(id, params),
    {
      onSuccess: () => {
        queryClient.invalidateQueries('workflows');
      },
    }
  );
};

// Message Hooks
export const useMessages = (params?: any) => {
  return useQuery<Message[]>(['messages', params], () => 
    apiClient.getMessages(params), {
    keepPreviousData: true,
    refetchInterval: 5000, // Refetch every 5 seconds for real-time updates
  });
};

export const useSendMessage = () => {
  const queryClient = useQueryClient();
  
  return useMutation(apiClient.sendMessage, {
    onSuccess: () => {
      queryClient.invalidateQueries('messages');
      queryClient.invalidateQueries('messageAnalytics');
    },
  });
};

// AI Hooks
export const useGenerateInsights = () => {
  return useMutation(apiClient.generateInsights);
};

export const useRecommendations = (contactId: string) => {
  return useQuery(['recommendations', contactId], () => 
    apiClient.getRecommendations(contactId), {
    enabled: !!contactId,
  });
};
