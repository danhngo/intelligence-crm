'use client'

import { useState } from 'react'
import { useCampaign, useCampaignStats, useCampaignEvents } from '@/hooks/campaigns'
import Sidebar from '@/components/layout/sidebar'
import { 
  ArrowLeftIcon,
  EnvelopeIcon,
  CursorArrowRippleIcon,
  EyeIcon,
  ExclamationTriangleIcon,
  CalendarDaysIcon,
  ClockIcon
} from '@heroicons/react/24/outline'
import Link from 'next/link'
import { format } from 'date-fns'

interface CampaignAnalyticsProps {
  params: {
    id: string
  }
}

export default function CampaignAnalyticsPage({ params }: CampaignAnalyticsProps) {
  const { id } = params
  const [eventTypeFilter, setEventTypeFilter] = useState<string>('')
  
  const { data: campaign, isLoading: campaignLoading } = useCampaign(id)
  const { data: stats, isLoading: statsLoading } = useCampaignStats(id)
  const { data: events = [], isLoading: eventsLoading } = useCampaignEvents(id, {
    limit: 100,
    event_type: eventTypeFilter || undefined
  })

  if (campaignLoading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Sidebar />
        <div className="md:pl-64">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="animate-pulse">
              <div className="h-8 bg-gray-200 rounded w-1/3 mb-4"></div>
              <div className="h-4 bg-gray-200 rounded w-1/2"></div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  if (!campaign) {
    return (
      <div className="min-h-screen bg-gray-50">
        <Sidebar />
        <div className="md:pl-64">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
            <div className="text-center">
              <ExclamationTriangleIcon className="mx-auto h-12 w-12 text-gray-400" />
              <h3 className="mt-2 text-sm font-medium text-gray-900">Campaign not found</h3>
              <p className="mt-1 text-sm text-gray-500">The campaign you're looking for doesn't exist.</p>
              <div className="mt-6">
                <Link
                  href="/campaigns"
                  className="inline-flex items-center px-4 py-2 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700"
                >
                  Back to Campaigns
                </Link>
              </div>
            </div>
          </div>
        </div>
      </div>
    )
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ACTIVE': return 'bg-green-100 text-green-800'
      case 'PAUSED': return 'bg-yellow-100 text-yellow-800'
      case 'COMPLETED': return 'bg-blue-100 text-blue-800'
      case 'FAILED': return 'bg-red-100 text-red-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const getEventTypeColor = (eventType: string) => {
    switch (eventType) {
      case 'OPEN': return 'bg-blue-100 text-blue-800'
      case 'CLICK': return 'bg-green-100 text-green-800'
      case 'BOUNCE': return 'bg-red-100 text-red-800'
      case 'UNSUBSCRIBE': return 'bg-yellow-100 text-yellow-800'
      default: return 'bg-gray-100 text-gray-800'
    }
  }

  const calculateOpenRate = () => {
    if (!stats || stats.sent_count === 0) return '0'
    return ((stats.unique_opens_count / stats.sent_count) * 100).toFixed(1)
  }

  const calculateClickRate = () => {
    if (!stats || stats.sent_count === 0) return '0'
    return ((stats.unique_clicks_count / stats.sent_count) * 100).toFixed(1)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      
      <div className="md:pl-64">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="mb-8">
            <Link
              href="/campaigns"
              className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-4"
            >
              <ArrowLeftIcon className="h-4 w-4 mr-1" />
              Back to Campaigns
            </Link>
            <div className="flex items-center justify-between">
              <div>
                <h1 className="text-2xl font-bold text-gray-900">{campaign.name}</h1>
                <div className="mt-2 flex items-center space-x-4">
                  <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getStatusColor(campaign.status)}`}>
                    {campaign.status}
                  </span>
                  <span className="text-sm text-gray-500">
                    Created {format(new Date(campaign.created_at), 'MMM d, yyyy')}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Stats Overview */}
          <div className="grid grid-cols-1 gap-5 sm:grid-cols-2 lg:grid-cols-4 mb-8">
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <EnvelopeIcon className="h-6 w-6 text-gray-400" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Messages Sent</dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {statsLoading ? '-' : stats?.sent_count.toLocaleString() || '0'}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <EyeIcon className="h-6 w-6 text-blue-400" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Open Rate</dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {statsLoading ? '-' : `${calculateOpenRate()}%`}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <CursorArrowRippleIcon className="h-6 w-6 text-green-400" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Click Rate</dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {statsLoading ? '-' : `${calculateClickRate()}%`}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <ExclamationTriangleIcon className="h-6 w-6 text-red-400" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Bounces</dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {statsLoading ? '-' : stats?.bounce_count.toLocaleString() || '0'}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Detailed Stats */}
          {stats && (
            <div className="bg-white shadow overflow-hidden sm:rounded-md mb-8">
              <div className="px-4 py-5 sm:px-6">
                <h3 className="text-lg leading-6 font-medium text-gray-900">Detailed Analytics</h3>
                <p className="mt-1 max-w-2xl text-sm text-gray-500">
                  Comprehensive campaign performance metrics
                </p>
              </div>
              <div className="border-t border-gray-200">
                <dl>
                  <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Total Opens</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                      {stats.total_opens_count.toLocaleString()} ({stats.unique_opens_count.toLocaleString()} unique)
                    </dd>
                  </div>
                  <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Total Clicks</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                      {stats.total_clicks_count.toLocaleString()} ({stats.unique_clicks_count.toLocaleString()} unique)
                    </dd>
                  </div>
                  <div className="bg-gray-50 px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Unsubscribes</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                      {stats.unsubscribe_count.toLocaleString()}
                    </dd>
                  </div>
                  <div className="bg-white px-4 py-5 sm:grid sm:grid-cols-3 sm:gap-4 sm:px-6">
                    <dt className="text-sm font-medium text-gray-500">Complaints</dt>
                    <dd className="mt-1 text-sm text-gray-900 sm:mt-0 sm:col-span-2">
                      {stats.complaint_count.toLocaleString()}
                    </dd>
                  </div>
                </dl>
              </div>
            </div>
          )}

          {/* Recent Events */}
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            <div className="px-4 py-5 sm:px-6">
              <div className="flex items-center justify-between">
                <div>
                  <h3 className="text-lg leading-6 font-medium text-gray-900">Recent Events</h3>
                  <p className="mt-1 max-w-2xl text-sm text-gray-500">
                    Real-time tracking events for this campaign
                  </p>
                </div>
                <div className="flex items-center space-x-3">
                  <select
                    value={eventTypeFilter}
                    onChange={(e) => setEventTypeFilter(e.target.value)}
                    className="block w-32 py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                  >
                    <option value="">All Events</option>
                    <option value="OPEN">Opens</option>
                    <option value="CLICK">Clicks</option>
                    <option value="BOUNCE">Bounces</option>
                    <option value="UNSUBSCRIBE">Unsubscribes</option>
                  </select>
                </div>
              </div>
            </div>
            <div className="border-t border-gray-200">
              {eventsLoading ? (
                <div className="px-4 py-5">
                  <div className="animate-pulse space-y-4">
                    {[...Array(5)].map((_, i) => (
                      <div key={i} className="flex items-center space-x-3">
                        <div className="h-4 bg-gray-200 rounded w-20"></div>
                        <div className="h-4 bg-gray-200 rounded flex-1"></div>
                        <div className="h-4 bg-gray-200 rounded w-32"></div>
                      </div>
                    ))}
                  </div>
                </div>
              ) : events.length === 0 ? (
                <div className="px-4 py-5 text-center">
                  <CalendarDaysIcon className="mx-auto h-12 w-12 text-gray-400" />
                  <h3 className="mt-2 text-sm font-medium text-gray-900">No events yet</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    Events will appear here as recipients interact with your campaign.
                  </p>
                </div>
              ) : (
                <ul className="divide-y divide-gray-200">
                  {events.map((event) => (
                    <li key={event.id} className="px-4 py-4">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center space-x-3">
                          <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getEventTypeColor(event.event_type)}`}>
                            {event.event_type}
                          </span>
                          <div>
                            <p className="text-sm font-medium text-gray-900">
                              {event.recipient_email}
                            </p>
                            {event.url && (
                              <p className="text-sm text-gray-500 truncate max-w-md">
                                {event.url}
                              </p>
                            )}
                            {event.user_agent && (
                              <p className="text-xs text-gray-400 truncate max-w-md">
                                {event.user_agent}
                              </p>
                            )}
                          </div>
                        </div>
                        <div className="flex items-center text-sm text-gray-500">
                          <ClockIcon className="h-4 w-4 mr-1" />
                          {format(new Date(event.created_at), 'MMM d, h:mm a')}
                        </div>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
