'use client'

import { useState } from 'react'

interface Endpoint {
  method: string
  path: string
  description: string
  parameters?: string[]
  requestBody?: string
  response?: string
}

interface ServiceAPI {
  name: string
  baseUrl: string
  version: string
  description: string
  endpoints: Endpoint[]
}

const API_SERVICES: ServiceAPI[] = [
  {
    name: 'User Management API',
    baseUrl: 'http://localhost:8002',
    version: '1.0.0',
    description: 'Authentication and user management service',
    endpoints: [
      {
        method: 'POST',
        path: '/api/v1/auth/login',
        description: 'User login authentication',
        requestBody: '{ "username": "string", "password": "string" }',
        response: '{ "access_token": "string", "token_type": "bearer", "expires_in": number }'
      },
      {
        method: 'POST',
        path: '/api/v1/auth/refresh',
        description: 'Refresh access token',
        response: '{ "access_token": "string", "token_type": "bearer" }'
      },
      {
        method: 'POST',
        path: '/api/v1/auth/register',
        description: 'Register new user',
        requestBody: '{ "email": "string", "password": "string", "full_name": "string" }',
        response: '{ "id": "uuid", "email": "string", "full_name": "string", "is_active": boolean }'
      },
      {
        method: 'GET',
        path: '/api/v1/users/me',
        description: 'Get current user profile',
        response: '{ "id": "uuid", "email": "string", "full_name": "string", "is_active": boolean }'
      },
      {
        method: 'PUT',
        path: '/api/v1/users/me',
        description: 'Update current user profile',
        requestBody: '{ "email": "string", "full_name": "string" }',
        response: '{ "id": "uuid", "email": "string", "full_name": "string", "is_active": boolean }'
      },
      {
        method: 'GET',
        path: '/api/v1/users/',
        description: 'List all users (admin only)',
        parameters: ['skip: number', 'limit: number'],
        response: '[{ "id": "uuid", "email": "string", "full_name": "string", "is_active": boolean }]'
      },
      {
        method: 'POST',
        path: '/api/v1/users/',
        description: 'Create new user (admin only)',
        requestBody: '{ "email": "string", "password": "string", "full_name": "string" }',
        response: '{ "id": "uuid", "email": "string", "full_name": "string", "is_active": boolean }'
      },
      {
        method: 'GET',
        path: '/api/v1/users/{user_id}',
        description: 'Get user by ID',
        parameters: ['user_id: uuid'],
        response: '{ "id": "uuid", "email": "string", "full_name": "string", "is_active": boolean }'
      },
      {
        method: 'PUT',
        path: '/api/v1/users/{user_id}',
        description: 'Update user by ID (admin only)',
        parameters: ['user_id: uuid'],
        requestBody: '{ "email": "string", "full_name": "string", "is_active": boolean }',
        response: '{ "id": "uuid", "email": "string", "full_name": "string", "is_active": boolean }'
      },
      {
        method: 'DELETE',
        path: '/api/v1/users/{user_id}',
        description: 'Delete user by ID (admin only)',
        parameters: ['user_id: uuid'],
        response: '{ "id": "uuid", "email": "string", "full_name": "string", "is_active": boolean }'
      }
    ]
  },
  {
    name: 'CRM Core API',
    baseUrl: 'http://localhost:8000',
    version: '1.0.0',
    description: 'Customer relationship management core functionality',
    endpoints: [
      {
        method: 'POST',
        path: '/api/v1/contacts',
        description: 'Create new contact',
        requestBody: '{ "name": "string", "email": "string", "phone": "string", "company": "string" }',
        response: '{ "id": "uuid", "name": "string", "email": "string", "phone": "string", "company": "string", "created_at": "datetime" }'
      },
      {
        method: 'GET',
        path: '/api/v1/contacts',
        description: 'List all contacts',
        parameters: ['skip: number', 'limit: number'],
        response: '{ "contacts": [Contact], "total": number, "page": number, "pages": number }'
      },
      {
        method: 'GET',
        path: '/api/v1/contacts/{contact_id}',
        description: 'Get contact by ID',
        parameters: ['contact_id: uuid'],
        response: '{ "id": "uuid", "name": "string", "email": "string", "phone": "string", "company": "string", "created_at": "datetime" }'
      },
      {
        method: 'PATCH',
        path: '/api/v1/contacts/{contact_id}',
        description: 'Update contact partially',
        parameters: ['contact_id: uuid'],
        requestBody: '{ "name"?: "string", "email"?: "string", "phone"?: "string", "company"?: "string" }',
        response: '{ "id": "uuid", "name": "string", "email": "string", "phone": "string", "company": "string", "created_at": "datetime" }'
      },
      {
        method: 'DELETE',
        path: '/api/v1/contacts/{contact_id}',
        description: 'Delete contact by ID',
        parameters: ['contact_id: uuid'],
        response: 'HTTP 204 No Content'
      }
    ]
  },
  {
    name: 'Workflow Engine API',
    baseUrl: 'http://localhost:8001',
    version: '0.1.0',
    description: 'Business process automation and workflow management',
    endpoints: [
      {
        method: 'GET',
        path: '/api/v1/workflows/types',
        description: 'Get available workflow types',
        response: '[{ "name": "string", "description": "string", "input_schema": object }]'
      },
      {
        method: 'GET',
        path: '/api/v1/workflows/',
        description: 'List all workflows',
        parameters: ['limit: number', 'offset: number'],
        response: '[{ "id": "uuid", "name": "string", "type": "string", "status": "string", "created_at": "datetime" }]'
      },
      {
        method: 'POST',
        path: '/api/v1/workflows/',
        description: 'Create new workflow',
        requestBody: '{ "name": "string", "type": "string", "configuration": object }',
        response: '{ "id": "uuid", "name": "string", "type": "string", "status": "string", "created_at": "datetime" }'
      },
      {
        method: 'POST',
        path: '/api/v1/workflows/workflows',
        description: 'Create workflow definition',
        requestBody: '{ "name": "string", "description": "string", "steps": [WorkflowStep] }',
        response: '{ "id": "uuid", "name": "string", "description": "string", "status": "string" }'
      },
      {
        method: 'GET',
        path: '/api/v1/workflows/workflows',
        description: 'List workflow definitions',
        response: '[{ "id": "uuid", "name": "string", "description": "string", "status": "string" }]'
      },
      {
        method: 'GET',
        path: '/api/v1/workflows/workflows/{workflow_id}',
        description: 'Get workflow by ID',
        parameters: ['workflow_id: uuid'],
        response: '{ "id": "uuid", "name": "string", "description": "string", "steps": [WorkflowStep] }'
      },
      {
        method: 'PUT',
        path: '/api/v1/workflows/workflows/{workflow_id}',
        description: 'Update workflow definition',
        parameters: ['workflow_id: uuid'],
        requestBody: '{ "name": "string", "description": "string", "steps": [WorkflowStep] }',
        response: '{ "id": "uuid", "name": "string", "description": "string", "status": "string" }'
      },
      {
        method: 'POST',
        path: '/api/v1/workflows/workflows/{workflow_id}/execute',
        description: 'Execute workflow',
        parameters: ['workflow_id: uuid'],
        requestBody: '{ "input_data": object }',
        response: '{ "execution_id": "uuid", "status": "string", "started_at": "datetime" }'
      },
      {
        method: 'GET',
        path: '/api/v1/workflows/executions',
        description: 'List workflow executions',
        parameters: ['workflow_id?: uuid', 'status?: string'],
        response: '[{ "id": "uuid", "workflow_id": "uuid", "status": "string", "started_at": "datetime" }]'
      },
      {
        method: 'GET',
        path: '/api/v1/workflows/executions/{execution_id}',
        description: 'Get execution details',
        parameters: ['execution_id: uuid'],
        response: '{ "id": "uuid", "workflow_id": "uuid", "status": "string", "result": object, "logs": [string] }'
      },
      {
        method: 'GET',
        path: '/api/v1/workflows/executions/{execution_id}/logs',
        description: 'Get execution logs',
        parameters: ['execution_id: uuid'],
        response: '[{ "id": "uuid", "level": "string", "message": "string", "timestamp": "datetime" }]'
      }
    ]
  },
  {
    name: 'Communication Hub API',
    baseUrl: 'http://localhost:8003',
    version: '0.1.0',
    description: 'Multi-channel communication orchestration service',
    endpoints: [
      {
        method: 'POST',
        path: '/api/v1/communications/send',
        description: 'Send communication message',
        requestBody: '{ "channel": "string", "recipient": "string", "message": "string", "template_id"?: "string" }',
        response: '{ "communication_id": "uuid", "status": "string", "sent_at": "datetime" }'
      },
      {
        method: 'GET',
        path: '/api/v1/communications/status/{communication_id}',
        description: 'Get communication delivery status',
        parameters: ['communication_id: uuid'],
        response: '{ "id": "uuid", "status": "string", "delivered_at"?: "datetime", "error"?: "string" }'
      },
      {
        method: 'GET',
        path: '/api/v1/communications/history/{recipient}',
        description: 'Get communication history for recipient',
        parameters: ['recipient: string', 'limit?: number'],
        response: '[{ "id": "uuid", "channel": "string", "message": "string", "sent_at": "datetime", "status": "string" }]'
      },
      {
        method: 'GET',
        path: '/api/v1/messages/',
        description: 'List messages with filtering',
        parameters: ['channel?: string', 'status?: string', 'limit?: number', 'offset?: number'],
        response: '[{ "id": "uuid", "channel": "string", "recipient": "string", "content": "string", "status": "string" }]'
      },
      {
        method: 'GET',
        path: '/api/v1/messages/{message_id}',
        description: 'Get message by ID',
        parameters: ['message_id: uuid'],
        response: '{ "id": "uuid", "channel": "string", "recipient": "string", "content": "string", "status": "string", "sent_at": "datetime" }'
      },
      {
        method: 'GET',
        path: '/api/v1/messages/templates/',
        description: 'List message templates',
        parameters: ['channel?: string'],
        response: '[{ "id": "uuid", "name": "string", "channel": "string", "template": "string", "variables": [string] }]'
      },
      {
        method: 'POST',
        path: '/api/v1/messages/templates/{template_id}/render',
        description: 'Render message template with data',
        parameters: ['template_id: uuid'],
        requestBody: '{ "variables": { [key: string]: any } }',
        response: '{ "rendered_content": "string" }'
      },
      {
        method: 'GET',
        path: '/api/v1/channels/',
        description: 'List available communication channels',
        response: '[{ "name": "string", "type": "string", "description": "string", "status": "string", "config": object }]'
      },
      {
        method: 'GET',
        path: '/api/v1/channels/{channel_name}',
        description: 'Get channel configuration',
        parameters: ['channel_name: string'],
        response: '{ "name": "string", "type": "string", "description": "string", "status": "string", "config": object }'
      },
      {
        method: 'POST',
        path: '/api/v1/channels/{channel_name}/test',
        description: 'Test communication channel',
        parameters: ['channel_name: string'],
        requestBody: '{ "test_recipient": "string", "test_message": "string" }',
        response: '{ "success": boolean, "message": "string", "response_time": number }'
      }
    ]
  },
  {
    name: 'Analytics Service API',
    baseUrl: 'http://localhost:8004',
    version: '1.0.0',
    description: 'Analytics and metrics collection service',
    endpoints: [
      {
        method: 'POST',
        path: '/api/v1/analytics/events',
        description: 'Create analytics event',
        requestBody: '{ "event_type": "string", "properties": object, "user_id"?: "string", "session_id"?: "string" }',
        response: '{ "event_id": "uuid", "event_type": "string", "timestamp": "datetime", "processed": boolean }'
      },
      {
        method: 'POST',
        path: '/api/v1/analytics/events/bulk',
        description: 'Create multiple analytics events',
        requestBody: '[{ "event_type": "string", "properties": object, "user_id"?: "string" }]',
        response: '[{ "event_id": "uuid", "event_type": "string", "timestamp": "datetime", "processed": boolean }]'
      },
      {
        method: 'POST',
        path: '/api/v1/analytics/messages/analytics',
        description: 'Process message analytics',
        requestBody: '{ "message_id": "uuid", "channel": "string", "metrics": object }',
        response: '{ "analytics_id": "uuid", "message_id": "uuid", "processed_at": "datetime", "metrics": object }'
      },
      {
        method: 'GET',
        path: '/api/v1/analytics/conversations/{conversation_id}/analytics',
        description: 'Get conversation analytics',
        parameters: ['conversation_id: uuid'],
        response: '{ "conversation_id": "uuid", "message_count": number, "response_time_avg": number, "engagement_score": number }'
      },
      {
        method: 'GET',
        path: '/api/v1/analytics/channels/{channel_id}/analytics',
        description: 'Get channel analytics',
        parameters: ['channel_id: uuid', 'time_range?: string'],
        response: '{ "channel_id": "uuid", "total_messages": number, "success_rate": number, "avg_response_time": number }'
      },
      {
        method: 'GET',
        path: '/api/v1/analytics/dashboard',
        description: 'Get dashboard metrics',
        parameters: ['time_range?: string'],
        response: '{ "total_events": number, "active_users": number, "conversion_rate": number, "top_events": [object] }'
      }
    ]
  },
  {
    name: 'AI Orchestration API',
    baseUrl: 'http://localhost:8005',
    version: '0.1.0',
    description: 'AI/ML workflows, insights, and agent orchestration',
    endpoints: [
      {
        method: 'POST',
        path: '/api/v1/insights/generate',
        description: 'Generate AI insights from data',
        requestBody: '{ "data_source": "string", "analysis_type": "string", "parameters": object }',
        response: '{ "insight_id": "uuid", "insights": [object], "confidence": number, "generated_at": "datetime" }'
      },
      {
        method: 'GET',
        path: '/api/v1/insights/contact/{contact_id}',
        description: 'Get insights for specific contact',
        parameters: ['contact_id: uuid', 'limit?: number'],
        response: '{ "contact_id": "uuid", "insights": [object], "last_updated": "datetime" }'
      },
      {
        method: 'GET',
        path: '/api/v1/insights/recommendations/{contact_id}',
        description: 'Get AI recommendations for contact',
        parameters: ['contact_id: uuid'],
        response: '{ "contact_id": "uuid", "recommendations": [object], "priority_score": number }'
      },
      {
        method: 'POST',
        path: '/api/v1/workflows/execute',
        description: 'Execute AI workflow',
        requestBody: '{ "workflow_type": "string", "input_data": object, "config"?: object }',
        response: '{ "execution_id": "uuid", "status": "string", "started_at": "datetime", "estimated_completion": "datetime" }'
      },
      {
        method: 'GET',
        path: '/api/v1/workflows/types',
        description: 'Get available AI workflow types',
        response: '[{ "name": "string", "description": "string", "input_schema": object, "output_schema": object }]'
      },
      {
        method: 'GET',
        path: '/api/v1/workflows/execution/{execution_id}',
        description: 'Get workflow execution status',
        parameters: ['execution_id: uuid'],
        response: '{ "execution_id": "uuid", "status": "string", "progress": number, "result"?: object, "error"?: "string" }'
      },
      {
        method: 'POST',
        path: '/api/v1/agents/execute',
        description: 'Execute AI agent',
        requestBody: '{ "agent_type": "string", "task": "string", "context": object }',
        response: '{ "agent_id": "uuid", "status": "string", "started_at": "datetime" }'
      },
      {
        method: 'GET',
        path: '/api/v1/agents/types',
        description: 'Get available AI agent types',
        response: '[{ "type": "string", "description": "string", "capabilities": [string], "supported_tasks": [string] }]'
      },
      {
        method: 'GET',
        path: '/api/v1/agents/{agent_id}/status',
        description: 'Get AI agent execution status',
        parameters: ['agent_id: uuid'],
        response: '{ "agent_id": "uuid", "status": "string", "current_task": "string", "progress": number, "result"?: object }'
      }
    ]
  }
]

const getMethodColor = (method: string) => {
  switch (method) {
    case 'GET': return 'bg-green-100 text-green-800 border-green-200'
    case 'POST': return 'bg-blue-100 text-blue-800 border-blue-200'
    case 'PUT': return 'bg-orange-100 text-orange-800 border-orange-200'
    case 'PATCH': return 'bg-yellow-100 text-yellow-800 border-yellow-200'
    case 'DELETE': return 'bg-red-100 text-red-800 border-red-200'
    default: return 'bg-gray-100 text-gray-800 border-gray-200'
  }
}

export default function APIDocsPage() {
  const [selectedService, setSelectedService] = useState<string | null>(null)
  const [searchTerm, setSearchTerm] = useState('')

  const filteredServices = API_SERVICES.map(service => ({
    ...service,
    endpoints: service.endpoints.filter(endpoint =>
      endpoint.path.toLowerCase().includes(searchTerm.toLowerCase()) ||
      endpoint.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
      endpoint.method.toLowerCase().includes(searchTerm.toLowerCase())
    )
  })).filter(service => 
    selectedService ? service.name === selectedService : true
  )

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">API Documentation</h1>
          <p className="text-lg text-gray-600">
            Comprehensive API documentation for all CRM microservices
          </p>
        </div>

        {/* Controls */}
        <div className="mb-8 flex flex-col md:flex-row gap-4">
          <div className="flex-1">
            <input
              type="text"
              placeholder="Search endpoints..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
          </div>
          <div className="md:w-64">
            <select
              value={selectedService || ''}
              onChange={(e) => setSelectedService(e.target.value || null)}
              className="w-full px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="">All Services</option>
              {API_SERVICES.map(service => (
                <option key={service.name} value={service.name}>
                  {service.name}
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Services Grid */}
        <div className="space-y-8">
          {filteredServices.map(service => (
            <div key={service.name} className="bg-white rounded-lg shadow-sm border border-gray-200">
              {/* Service Header */}
              <div className="px-6 py-4 border-b border-gray-200">
                <div className="flex justify-between items-start">
                  <div>
                    <h2 className="text-2xl font-semibold text-gray-900">{service.name}</h2>
                    <p className="text-gray-600 mt-1">{service.description}</p>
                    <div className="flex items-center gap-4 mt-2 text-sm">
                      <span className="px-2 py-1 bg-gray-100 rounded text-gray-700">
                        Base URL: {service.baseUrl}
                      </span>
                      <span className="px-2 py-1 bg-blue-100 rounded text-blue-700">
                        v{service.version}
                      </span>
                    </div>
                  </div>
                  <div className="text-right">
                    <a
                      href={`${service.baseUrl}/api/v1/docs`}
                      target="_blank"
                      rel="noopener noreferrer"
                      className="inline-flex items-center px-3 py-2 border border-gray-300 rounded-md text-sm font-medium text-gray-700 bg-white hover:bg-gray-50"
                    >
                      View Swagger Docs
                      <svg className="ml-2 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M10 6H6a2 2 0 00-2 2v10a2 2 0 002 2h10a2 2 0 002-2v-4M14 4h6m0 0v6m0-6L10 14" />
                      </svg>
                    </a>
                  </div>
                </div>
              </div>

              {/* Endpoints */}
              <div className="p-6">
                <h3 className="text-lg font-medium text-gray-900 mb-4">
                  Endpoints ({service.endpoints.length})
                </h3>
                <div className="space-y-4">
                  {service.endpoints.map((endpoint, index) => (
                    <div key={index} className="border border-gray-200 rounded-lg overflow-hidden">
                      <div className="px-4 py-3 bg-gray-50 border-b border-gray-200">
                        <div className="flex items-center justify-between">
                          <div className="flex items-center gap-3">
                            <span className={`px-2 py-1 rounded text-xs font-medium border ${getMethodColor(endpoint.method)}`}>
                              {endpoint.method}
                            </span>
                            <code className="text-sm font-mono text-gray-900">{endpoint.path}</code>
                          </div>
                        </div>
                        <p className="text-sm text-gray-600 mt-2">{endpoint.description}</p>
                      </div>

                      <div className="px-4 py-3 space-y-3">
                        {endpoint.parameters && endpoint.parameters.length > 0 && (
                          <div>
                            <h4 className="text-sm font-medium text-gray-700 mb-2">Parameters</h4>
                            <div className="space-y-1">
                              {endpoint.parameters.map((param, paramIndex) => (
                                <code key={paramIndex} className="block text-xs bg-gray-100 px-2 py-1 rounded text-gray-800">
                                  {param}
                                </code>
                              ))}
                            </div>
                          </div>
                        )}

                        {endpoint.requestBody && (
                          <div>
                            <h4 className="text-sm font-medium text-gray-700 mb-2">Request Body</h4>
                            <pre className="text-xs bg-gray-100 p-3 rounded overflow-x-auto">
                              <code className="text-gray-800">{endpoint.requestBody}</code>
                            </pre>
                          </div>
                        )}

                        {endpoint.response && (
                          <div>
                            <h4 className="text-sm font-medium text-gray-700 mb-2">Response</h4>
                            <pre className="text-xs bg-gray-100 p-3 rounded overflow-x-auto">
                              <code className="text-gray-800">{endpoint.response}</code>
                            </pre>
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Summary */}
        <div className="mt-12 bg-blue-50 border border-blue-200 rounded-lg p-6">
          <h3 className="text-lg font-semibold text-blue-900 mb-2">API Overview</h3>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
            <div>
              <span className="font-medium text-blue-800">Total Services:</span>
              <span className="text-blue-700 ml-2">{API_SERVICES.length}</span>
            </div>
            <div>
              <span className="font-medium text-blue-800">Total Endpoints:</span>
              <span className="text-blue-700 ml-2">
                {API_SERVICES.reduce((sum, service) => sum + service.endpoints.length, 0)}
              </span>
            </div>
            <div>
              <span className="font-medium text-blue-800">API Standards:</span>
              <span className="text-blue-700 ml-2">REST, OpenAPI 3.0</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
