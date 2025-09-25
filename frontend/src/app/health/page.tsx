'use client'

import { useState, useEffect } from 'react'
import { useAuth } from '@/components/auth/auth-provider'
import Sidebar from '@/components/layout/sidebar'
import { 
  CheckCircleIcon, 
  XCircleIcon, 
  ExclamationTriangleIcon,
  ArrowPathIcon,
  ServerIcon,
  CircleStackIcon,
  CpuChipIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

interface ServiceStatus {
  name: string
  type: 'api' | 'database' | 'cache'
  url: string
  status: 'healthy' | 'unhealthy' | 'degraded' | 'checking'
  responseTime?: number
  lastCheck: Date
  error?: string
  details?: {
    version?: string
    uptime?: string
    connections?: number
  }
}

const SERVICES: Omit<ServiceStatus, 'status' | 'lastCheck' | 'responseTime'>[] = [
  {
    name: 'User Management API',
    type: 'api',
    url: 'http://localhost:8002/health'
  },
  {
    name: 'Communication Hub API',
    type: 'api',
    url: 'http://localhost:8003/health'
  },
  {
    name: 'Analytics Service API',
    type: 'api', 
    url: 'http://localhost:8004/health'
  },
  {
    name: 'AI Orchestration API',
    type: 'api',
    url: 'http://localhost:8005/health'
  },
  {
    name: 'CRM Core API',
    type: 'api',
    url: 'http://localhost:8000/health'
  },
  {
    name: 'Workflow Engine API',
    type: 'api',
    url: 'http://localhost:8001/health'
  }
]

function ServiceCard({ service }: { service: ServiceStatus }) {
  const getStatusIcon = () => {
    switch (service.status) {
      case 'healthy':
        return <CheckCircleIcon className="h-6 w-6 text-green-500" />
      case 'unhealthy':
        return <XCircleIcon className="h-6 w-6 text-red-500" />
      case 'degraded':
        return <ExclamationTriangleIcon className="h-6 w-6 text-yellow-500" />
      case 'checking':
        return <ArrowPathIcon className="h-6 w-6 text-blue-500 animate-spin" />
    }
  }

  const getTypeIcon = () => {
    switch (service.type) {
      case 'api':
        return <ServerIcon className="h-5 w-5 text-gray-400" />
      case 'database':
        return <CircleStackIcon className="h-5 w-5 text-gray-400" />
      case 'cache':
        return <CpuChipIcon className="h-5 w-5 text-gray-400" />
    }
  }

  const getStatusColor = () => {
    switch (service.status) {
      case 'healthy':
        return 'border-green-200 bg-green-50'
      case 'unhealthy':
        return 'border-red-200 bg-red-50'
      case 'degraded':
        return 'border-yellow-200 bg-yellow-50'
      case 'checking':
        return 'border-blue-200 bg-blue-50'
    }
  }

  return (
    <div className={`rounded-lg border p-6 ${getStatusColor()}`}>
      <div className="flex items-start justify-between">
        <div className="flex items-start space-x-3">
          <div className="flex-shrink-0 mt-1">
            {getTypeIcon()}
          </div>
          <div className="min-w-0 flex-1">
            <h3 className="text-lg font-medium text-gray-900">{service.name}</h3>
            <p className="text-sm text-gray-500 capitalize">{service.type}</p>
            <p className="text-xs text-gray-400 mt-1">{service.url}</p>
          </div>
        </div>
        <div className="flex-shrink-0">
          {getStatusIcon()}
        </div>
      </div>

      <div className="mt-4 space-y-2">
        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-500">Status:</span>
          <span className={`font-medium capitalize ${
            service.status === 'healthy' ? 'text-green-700' :
            service.status === 'unhealthy' ? 'text-red-700' :
            service.status === 'degraded' ? 'text-yellow-700' :
            'text-blue-700'
          }`}>
            {service.status}
          </span>
        </div>

        {service.responseTime && (
          <div className="flex items-center justify-between text-sm">
            <span className="text-gray-500">Response Time:</span>
            <span className="text-gray-900">{service.responseTime}ms</span>
          </div>
        )}

        <div className="flex items-center justify-between text-sm">
          <span className="text-gray-500">Last Check:</span>
          <span className="text-gray-900 flex items-center">
            <ClockIcon className="h-4 w-4 mr-1" />
            {service.lastCheck.toLocaleTimeString()}
          </span>
        </div>

        {service.error && (
          <div className="mt-2 p-2 bg-red-100 border border-red-200 rounded text-sm text-red-700">
            {service.error}
          </div>
        )}

        {service.details && (
          <div className="mt-2 space-y-1 text-xs text-gray-600">
            {service.details.version && (
              <div>Version: {service.details.version}</div>
            )}
            {service.details.uptime && (
              <div>Uptime: {service.details.uptime}</div>
            )}
            {service.details.connections !== undefined && (
              <div>Connections: {service.details.connections}</div>
            )}
          </div>
        )}
      </div>
    </div>
  )
}

function OverallHealthSummary({ services }: { services: ServiceStatus[] }) {
  const healthyCount = services.filter(s => s.status === 'healthy').length
  const unhealthyCount = services.filter(s => s.status === 'unhealthy').length
  const degradedCount = services.filter(s => s.status === 'degraded').length
  const checkingCount = services.filter(s => s.status === 'checking').length

  const overallStatus = unhealthyCount > 0 ? 'critical' : 
                       degradedCount > 0 ? 'warning' : 
                       checkingCount > 0 ? 'checking' : 'healthy'

  return (
    <div className="bg-white shadow rounded-lg p-6 mb-8">
      <h2 className="text-xl font-semibold text-gray-900 mb-4">System Health Overview</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="text-center">
          <div className="text-2xl font-bold text-green-600">{healthyCount}</div>
          <div className="text-sm text-gray-500">Healthy</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-yellow-600">{degradedCount}</div>
          <div className="text-sm text-gray-500">Degraded</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-red-600">{unhealthyCount}</div>
          <div className="text-sm text-gray-500">Unhealthy</div>
        </div>
        <div className="text-center">
          <div className="text-2xl font-bold text-blue-600">{checkingCount}</div>
          <div className="text-sm text-gray-500">Checking</div>
        </div>
      </div>

      <div className="mt-4 flex items-center justify-center">
        <div className={`px-3 py-1 rounded-full text-sm font-medium ${
          overallStatus === 'healthy' ? 'bg-green-100 text-green-800' :
          overallStatus === 'warning' ? 'bg-yellow-100 text-yellow-800' :
          overallStatus === 'critical' ? 'bg-red-100 text-red-800' :
          'bg-blue-100 text-blue-800'
        }`}>
          Overall Status: {overallStatus.charAt(0).toUpperCase() + overallStatus.slice(1)}
        </div>
      </div>
    </div>
  )
}

export default function HealthDashboard() {
  const { isAuthenticated, isLoading } = useAuth()
  const [services, setServices] = useState<ServiceStatus[]>([])
  const [isRefreshing, setIsRefreshing] = useState(false)
  const [autoRefresh, setAutoRefresh] = useState(true)

  const refreshAllServices = async () => {
    setIsRefreshing(true)
    
    // Set all services to checking status first
    setServices(prev => prev.length > 0 ? prev.map(s => ({ ...s, status: 'checking' as const })) : 
      SERVICES.map(s => ({ 
        ...s, 
        type: 'api' as const,
        status: 'checking' as const, 
        lastCheck: new Date() 
      }))
    )

    try {
      const response = await fetch('/api/health')
      if (response.ok) {
        const healthData = await response.json()
        const formattedServices: ServiceStatus[] = healthData.services.map((service: any) => ({
          name: service.name,
          type: 'api' as const,
          url: SERVICES.find(s => s.name === service.name)?.url || '',
          status: service.status,
          responseTime: service.responseTime,
          lastCheck: new Date(service.lastCheck),
          error: service.error,
          details: service.details
        }))
        setServices(formattedServices)
      } else {
        throw new Error('Failed to fetch health data')
      }
    } catch (error) {
      console.error('Error checking services:', error)
      // Fallback to unhealthy status for all services
      const errorServices: ServiceStatus[] = SERVICES.map(service => ({
        ...service,
        type: 'api' as const,
        status: 'unhealthy' as const,
        lastCheck: new Date(),
        error: 'Failed to fetch health data'
      }))
      setServices(errorServices)
    } finally {
      setIsRefreshing(false)
    }
  }

  useEffect(() => {
    refreshAllServices()
  }, [])

  useEffect(() => {
    if (autoRefresh) {
      const interval = setInterval(refreshAllServices, 30000) // Refresh every 30 seconds
      return () => clearInterval(interval)
    }
  }, [autoRefresh])

  if (isLoading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!isAuthenticated) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-50">
        <div className="max-w-md w-full">
          <div className="text-center">
            <h2 className="text-3xl font-bold text-gray-900">Access Denied</h2>
            <p className="mt-2 text-gray-600">Please log in to view system health</p>
            <a
              href="/login"
              className="mt-4 inline-flex items-center px-4 py-2 border border-transparent text-base font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
            >
              Sign In
            </a>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      
      <div className="md:pl-64">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="flex justify-between items-center mb-8">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">System Health Dashboard</h1>
              <p className="text-gray-600">Monitor the status of all CRM services and infrastructure</p>
            </div>
            
            <div className="flex items-center space-x-4">
              <div className="flex items-center">
                <input
                  type="checkbox"
                  id="autoRefresh"
                  checked={autoRefresh}
                  onChange={(e) => setAutoRefresh(e.target.checked)}
                  className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                />
                <label htmlFor="autoRefresh" className="ml-2 text-sm text-gray-700">
                  Auto-refresh (30s)
                </label>
              </div>
              
              <button
                onClick={refreshAllServices}
                disabled={isRefreshing}
                className="inline-flex items-center px-4 py-2 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
              >
                <ArrowPathIcon className={`h-4 w-4 mr-2 ${isRefreshing ? 'animate-spin' : ''}`} />
                Refresh All
              </button>
            </div>
          </div>

          {/* Overall Health Summary */}
          {services.length > 0 && <OverallHealthSummary services={services} />}

          {/* Services Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {services.map((service, index) => (
              <ServiceCard key={`${service.name}-${index}`} service={service} />
            ))}
          </div>

          {/* Last Updated Info */}
          <div className="mt-8 text-center text-sm text-gray-500">
            Last updated: {services.length > 0 ? services[0].lastCheck.toLocaleString() : 'Never'}
          </div>
        </div>
      </div>
    </div>
  )
}
