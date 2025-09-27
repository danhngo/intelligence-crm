'use client'

import { useState } from 'react'
import { 
  useCampaigns, 
  useDeleteCampaign, 
  useStartCampaign, 
  usePauseCampaign, 
  useStopCampaign 
} from '@/hooks/campaigns'
import Sidebar from '@/components/layout/sidebar'
import { Campaign, CampaignStatus } from '@/types/api'
import { 
  PlusIcon, 
  MagnifyingGlassIcon,
  PencilIcon,
  TrashIcon,
  EyeIcon,
  PlayIcon,
  PauseIcon,
  StopIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline'
import Link from 'next/link'

const statusColors = {
  DRAFT: 'bg-gray-100 text-gray-800',
  SCHEDULED: 'bg-blue-100 text-blue-800',
  RUNNING: 'bg-green-100 text-green-800',
  PAUSED: 'bg-yellow-100 text-yellow-800',
  COMPLETED: 'bg-purple-100 text-purple-800',
  CANCELLED: 'bg-red-100 text-red-800',
}

const typeColors = {
  EMAIL: 'bg-blue-50 text-blue-700',
  SMS: 'bg-green-50 text-green-700',
  WHATSAPP: 'bg-emerald-50 text-emerald-700',
  MULTI_CHANNEL: 'bg-purple-50 text-purple-700',
}

export default function CampaignsPage() {
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState<string>('')
  const [typeFilter, setTypeFilter] = useState<string>('')
  const [selectedCampaigns, setSelectedCampaigns] = useState<string[]>([])
  
  const { data: campaigns = [], isLoading, refetch } = useCampaigns({
    search: search || undefined,
    status: statusFilter || undefined,
    campaign_type: typeFilter || undefined,
  })
  
  const deleteCampaign = useDeleteCampaign()
  const startCampaign = useStartCampaign()
  const pauseCampaign = usePauseCampaign()
  const stopCampaign = useStopCampaign()

  const handleDelete = async (campaignId: string) => {
    if (confirm('Are you sure you want to delete this campaign?')) {
      try {
        await deleteCampaign.mutateAsync(campaignId)
        refetch()
      } catch (error) {
        console.error('Failed to delete campaign:', error)
      }
    }
  }

  const handleStart = async (campaignId: string) => {
    try {
      await startCampaign.mutateAsync(campaignId)
      refetch()
    } catch (error) {
      console.error('Failed to start campaign:', error)
    }
  }

  const handlePause = async (campaignId: string) => {
    try {
      await pauseCampaign.mutateAsync(campaignId)
      refetch()
    } catch (error) {
      console.error('Failed to pause campaign:', error)
    }
  }

  const handleStop = async (campaignId: string) => {
    try {
      await stopCampaign.mutateAsync(campaignId)
      refetch()
    } catch (error) {
      console.error('Failed to stop campaign:', error)
    }
  }

  const filteredCampaigns = campaigns.filter((campaign: Campaign) => {
    const matchesSearch = !search || 
      campaign.name.toLowerCase().includes(search.toLowerCase()) ||
      campaign.description?.toLowerCase().includes(search.toLowerCase())
    
    const matchesStatus = !statusFilter || campaign.status === statusFilter
    const matchesType = !typeFilter || campaign.type === typeFilter
    
    return matchesSearch && matchesStatus && matchesType
  })

  const getActionButton = (campaign: Campaign) => {
    switch (campaign.status) {
      case 'DRAFT':
      case 'PAUSED':
        return (
          <button
            onClick={() => handleStart(campaign.id)}
            className="inline-flex items-center p-2 border border-green-300 rounded-md text-green-600 hover:text-green-700 hover:border-green-400"
            title="Start campaign"
          >
            <PlayIcon className="h-4 w-4" />
          </button>
        )
      case 'RUNNING':
        return (
          <div className="flex space-x-1">
            <button
              onClick={() => handlePause(campaign.id)}
              className="inline-flex items-center p-2 border border-yellow-300 rounded-md text-yellow-600 hover:text-yellow-700 hover:border-yellow-400"
              title="Pause campaign"
            >
              <PauseIcon className="h-4 w-4" />
            </button>
            <button
              onClick={() => handleStop(campaign.id)}
              className="inline-flex items-center p-2 border border-red-300 rounded-md text-red-600 hover:text-red-700 hover:border-red-400"
              title="Stop campaign"
            >
              <StopIcon className="h-4 w-4" />
            </button>
          </div>
        )
      default:
        return null
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      
      <div className="md:pl-64">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="sm:flex sm:items-center sm:justify-between mb-8">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Email Campaigns</h1>
              <p className="text-gray-600">Create and manage your email marketing campaigns</p>
            </div>
            <div className="mt-4 sm:mt-0">
              <Link
                href="/campaigns/new"
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <PlusIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
                New Campaign
              </Link>
            </div>
          </div>

          {/* Filters */}
          <div className="mb-6 grid grid-cols-1 md:grid-cols-3 gap-4">
            {/* Search */}
            <div className="relative">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search campaigns..."
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>

            {/* Status Filter */}
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
              className="block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="">All Statuses</option>
              <option value="DRAFT">Draft</option>
              <option value="SCHEDULED">Scheduled</option>
              <option value="RUNNING">Running</option>
              <option value="PAUSED">Paused</option>
              <option value="COMPLETED">Completed</option>
              <option value="CANCELLED">Cancelled</option>
            </select>

            {/* Type Filter */}
            <select
              value={typeFilter}
              onChange={(e) => setTypeFilter(e.target.value)}
              className="block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
            >
              <option value="">All Types</option>
              <option value="EMAIL">Email</option>
              <option value="SMS">SMS</option>
              <option value="WHATSAPP">WhatsApp</option>
              <option value="MULTI_CHANNEL">Multi-Channel</option>
            </select>
          </div>

          {/* Campaigns Table */}
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            {isLoading ? (
              <div className="p-8 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
                <p className="mt-4 text-gray-500">Loading campaigns...</p>
              </div>
            ) : filteredCampaigns.length === 0 ? (
              <div className="p-8 text-center">
                <p className="text-gray-500">
                  {search || statusFilter || typeFilter ? 'No campaigns match your filters.' : 'No campaigns found.'}
                </p>
              </div>
            ) : (
              <ul className="divide-y divide-gray-200">
                {filteredCampaigns.map((campaign: Campaign) => (
                  <li key={campaign.id}>
                    <div className="px-4 py-4 flex items-center justify-between">
                      <div className="flex items-center">
                        <input
                          type="checkbox"
                          className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                          checked={selectedCampaigns.includes(campaign.id)}
                          onChange={(e) => {
                            if (e.target.checked) {
                              setSelectedCampaigns([...selectedCampaigns, campaign.id])
                            } else {
                              setSelectedCampaigns(selectedCampaigns.filter(id => id !== campaign.id))
                            }
                          }}
                        />
                        <div className="ml-4 flex-1">
                          <div className="flex items-center">
                            <h3 className="text-sm font-medium text-gray-900">
                              {campaign.name}
                            </h3>
                            <span className={`ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusColors[campaign.status]}`}>
                              {campaign.status.toLowerCase()}
                            </span>
                            <span className={`ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${typeColors[campaign.type]}`}>
                              {campaign.type.toLowerCase()}
                            </span>
                          </div>
                          <div className="mt-1">
                            {campaign.description && (
                              <p className="text-sm text-gray-600">{campaign.description}</p>
                            )}
                            <div className="flex items-center text-xs text-gray-500 mt-1">
                              <span>Recipients: {campaign.total_recipients}</span>
                              {campaign.sent_count > 0 && (
                                <>
                                  <span className="mx-2">•</span>
                                  <span>Sent: {campaign.sent_count}</span>
                                </>
                              )}
                              {campaign.opened_count > 0 && (
                                <>
                                  <span className="mx-2">•</span>
                                  <span>Opened: {campaign.opened_count}</span>
                                </>
                              )}
                              {campaign.clicked_count > 0 && (
                                <>
                                  <span className="mx-2">•</span>
                                  <span>Clicked: {campaign.clicked_count}</span>
                                </>
                              )}
                            </div>
                          </div>
                        </div>
                      </div>
                      <div className="flex items-center space-x-2">
                        {getActionButton(campaign)}
                        
                        <Link
                          href={`/campaigns/${campaign.id}/analytics`}
                          className="inline-flex items-center p-2 border border-gray-300 rounded-md text-gray-400 hover:text-gray-500 hover:border-gray-400"
                          title="View analytics"
                        >
                          <ChartBarIcon className="h-4 w-4" />
                        </Link>
                        
                        <Link
                          href={`/campaigns/${campaign.id}`}
                          className="inline-flex items-center p-2 border border-gray-300 rounded-md text-gray-400 hover:text-gray-500 hover:border-gray-400"
                          title="View campaign"
                        >
                          <EyeIcon className="h-4 w-4" />
                        </Link>
                        
                        <Link
                          href={`/campaigns/${campaign.id}/edit`}
                          className="inline-flex items-center p-2 border border-gray-300 rounded-md text-gray-400 hover:text-gray-500 hover:border-gray-400"
                          title="Edit campaign"
                        >
                          <PencilIcon className="h-4 w-4" />
                        </Link>
                        
                        <button
                          type="button"
                          onClick={() => handleDelete(campaign.id)}
                          className="inline-flex items-center p-2 border border-gray-300 rounded-md text-red-400 hover:text-red-500 hover:border-red-400"
                          title="Delete campaign"
                        >
                          <TrashIcon className="h-4 w-4" />
                        </button>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Bulk Actions */}
          {selectedCampaigns.length > 0 && (
            <div className="mt-4 bg-white rounded-lg shadow p-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">
                  {selectedCampaigns.length} campaign{selectedCampaigns.length !== 1 ? 's' : ''} selected
                </span>
                <div className="space-x-2">
                  <button
                    type="button"
                    className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    Export
                  </button>
                  <button
                    type="button"
                    className="inline-flex items-center px-3 py-2 border border-transparent text-sm leading-4 font-medium rounded-md text-white bg-red-600 hover:bg-red-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-red-500"
                  >
                    Delete Selected
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
