'use client'

import { useAuth } from '@/components/auth/auth-provider'
import { useDashboardMetrics } from '@/hooks/api'
import { useCampaigns } from '@/hooks/campaigns'
import Sidebar from '@/components/layout/sidebar'
import { 
  ChartBarIcon, 
  UsersIcon, 
  ChatBubbleLeftRightIcon, 
  ClockIcon,
  StarIcon,
  ArrowTrendingUpIcon,
  MegaphoneIcon,
  EnvelopeIcon 
} from '@heroicons/react/24/outline'

interface MetricCardProps {
  title: string
  value: string | number
  icon: React.ComponentType<any>
  trend?: string
  color?: string
}

function MetricCard({ title, value, icon: Icon, trend, color = 'blue' }: MetricCardProps) {
  return (
    <div className="bg-white overflow-hidden shadow rounded-lg">
      <div className="p-5">
        <div className="flex items-center">
          <div className="flex-shrink-0">
            <Icon className={`h-6 w-6 text-${color}-600`} aria-hidden="true" />
          </div>
          <div className="ml-5 w-0 flex-1">
            <dl>
              <dt className="text-sm font-medium text-gray-500 truncate">{title}</dt>
              <dd className="text-lg font-medium text-gray-900">{value}</dd>
            </dl>
          </div>
        </div>
        {trend && (
          <div className="mt-4">
            <div className="flex items-center text-sm text-green-600">
              <ArrowTrendingUpIcon className="h-4 w-4 mr-1" />
              {trend}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default function Dashboard() {
  const { isAuthenticated, isLoading } = useAuth()
  const { data: metrics, isLoading: metricsLoading } = useDashboardMetrics()
  const { data: campaigns = [] } = useCampaigns({ limit: 5 })

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
            <h2 className="text-3xl font-bold text-gray-900">Welcome to Intelligence CRM</h2>
            <p className="mt-2 text-gray-600">Please log in to continue</p>
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
          <div className="mb-8">
            <h1 className="text-2xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-600">Welcome to your CRM analytics overview</p>
          </div>

          {/* Metrics Grid */}
          {metricsLoading ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              {[...Array(6)].map((_, i) => (
                <div key={i} className="bg-white p-6 rounded-lg shadow animate-pulse">
                  <div className="h-4 bg-gray-200 rounded w-1/2 mb-2"></div>
                  <div className="h-6 bg-gray-200 rounded w-1/3"></div>
                </div>
              ))}
            </div>
          ) : metrics ? (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
              <MetricCard
                title="Total Contacts"
                value={metrics.total_contacts.toLocaleString()}
                icon={UsersIcon}
                color="blue"
              />
              <MetricCard
                title="Active Users"
                value={metrics.active_users.toLocaleString()}
                icon={UsersIcon}
                color="green"
              />
              <MetricCard
                title="Total Conversations"
                value={metrics.total_conversations.toLocaleString()}
                icon={ChatBubbleLeftRightIcon}
                color="purple"
              />
              <MetricCard
                title="Avg Response Time"
                value={`${metrics.avg_response_time.toFixed(1)}s`}
                icon={ClockIcon}
                color="yellow"
              />
              <MetricCard
                title="Satisfaction Score"
                value={`${(metrics.satisfaction_score * 100).toFixed(1)}%`}
                icon={StarIcon}
                color="pink"
              />
              <MetricCard
                title="Conversion Rate"
                value={`${(metrics.conversion_rate * 100).toFixed(1)}%`}
                icon={ArrowTrendingUpIcon}
                color="indigo"
              />
              <MetricCard
                title="Total Campaigns"
                value={campaigns.length.toLocaleString()}
                icon={MegaphoneIcon}
                color="orange"
              />
              <MetricCard
                title="Active Campaigns"
                value={campaigns.filter(c => c.status === 'RUNNING').length.toLocaleString()}
                icon={MegaphoneIcon}
                color="green"
              />
            </div>
          ) : (
            <div className="text-center py-12">
              <ChartBarIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">No data available</h3>
              <p className="mt-1 text-sm text-gray-500">Start using the platform to see analytics.</p>
            </div>
          )}

          {/* Quick Actions */}
          <div className="bg-white shadow rounded-lg">
            <div className="px-6 py-4 border-b border-gray-200">
              <h3 className="text-lg font-medium text-gray-900">Quick Actions</h3>
            </div>
            <div className="p-6">
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <a
                  href="/contacts/new"
                  className="block p-4 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors"
                >
                  <UsersIcon className="h-8 w-8 text-blue-600 mb-2" />
                  <h4 className="font-medium text-gray-900">Add New Contact</h4>
                  <p className="text-sm text-gray-600">Create a new customer contact</p>
                </a>
                <a
                  href="/campaigns/new"
                  className="block p-4 bg-orange-50 rounded-lg hover:bg-orange-100 transition-colors"
                >
                  <MegaphoneIcon className="h-8 w-8 text-orange-600 mb-2" />
                  <h4 className="font-medium text-gray-900">Create Campaign</h4>
                  <p className="text-sm text-gray-600">Launch a new marketing campaign</p>
                </a>
                <a
                  href="/templates"
                  className="block p-4 bg-green-50 rounded-lg hover:bg-green-100 transition-colors"
                >
                  <EnvelopeIcon className="h-8 w-8 text-green-600 mb-2" />
                  <h4 className="font-medium text-gray-900">Email Templates</h4>
                  <p className="text-sm text-gray-600">Manage email templates</p>
                </a>
                <a
                  href="/analytics"
                  className="block p-4 bg-purple-50 rounded-lg hover:bg-purple-100 transition-colors"
                >
                  <ChartBarIcon className="h-8 w-8 text-purple-600 mb-2" />
                  <h4 className="font-medium text-gray-900">View Analytics</h4>
                  <p className="text-sm text-gray-600">Analyze your performance</p>
                </a>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
