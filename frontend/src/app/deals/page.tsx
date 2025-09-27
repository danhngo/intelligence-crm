'use client'

import { useState } from 'react'
import Sidebar from '@/components/layout/sidebar'
import { 
  PlusIcon, 
  MagnifyingGlassIcon,
  PencilIcon,
  TrashIcon,
  EyeIcon,
  CurrencyDollarIcon,
  ChartBarIcon 
} from '@heroicons/react/24/outline'

// Mock data - replace with actual API calls
const mockDeals = [
  {
    id: '1',
    title: 'Enterprise Software License',
    description: 'Annual enterprise software licensing deal for 500 users',
    value: 150000,
    currency: 'USD',
    stage: 'negotiation',
    probability: 75,
    expected_close_date: '2024-11-30T00:00:00Z',
    actual_close_date: null,
    contact_id: '1',
    contact_name: 'John Smith',
    company_name: 'Tech Solutions Inc',
    assigned_user: 'Sarah Wilson',
    created_at: '2024-08-15T10:00:00Z'
  },
  {
    id: '2',
    title: 'Consulting Services Package',
    description: 'Digital transformation consulting for Q1 2025',
    value: 75000,
    currency: 'USD',
    stage: 'proposal',
    probability: 60,
    expected_close_date: '2024-12-15T00:00:00Z',
    actual_close_date: null,
    contact_id: '2',
    contact_name: 'Sarah Johnson',
    company_name: 'Innovation Startup',
    assigned_user: 'Mike Rodriguez',
    created_at: '2024-09-01T14:30:00Z'
  },
  {
    id: '3',
    title: 'Custom Development Project',
    description: 'Build custom CRM integration module',
    value: 85000,
    currency: 'USD',
    stage: 'closed-won',
    probability: 100,
    expected_close_date: '2024-10-15T00:00:00Z',
    actual_close_date: '2024-10-12T00:00:00Z',
    contact_id: '3',
    contact_name: 'Michael Brown',
    company_name: 'Enterprise Corp',
    assigned_user: 'Lisa Chen',
    created_at: '2024-07-20T09:15:00Z'
  },
  {
    id: '4',
    title: 'SaaS Platform Subscription',
    description: 'Annual subscription for premium features',
    value: 24000,
    currency: 'USD',
    stage: 'closed-lost',
    probability: 0,
    expected_close_date: '2024-09-30T00:00:00Z',
    actual_close_date: '2024-09-28T00:00:00Z',
    contact_id: '4',
    contact_name: 'Emily Davis',
    company_name: 'Small Business Co',
    assigned_user: 'John Anderson',
    created_at: '2024-08-05T16:20:00Z'
  }
]

const stageColors = {
  'lead': 'bg-gray-100 text-gray-800',
  'qualified': 'bg-blue-100 text-blue-800',
  'proposal': 'bg-yellow-100 text-yellow-800',
  'negotiation': 'bg-orange-100 text-orange-800',
  'closed-won': 'bg-green-100 text-green-800',
  'closed-lost': 'bg-red-100 text-red-800'
}

const stageOrder = ['lead', 'qualified', 'proposal', 'negotiation', 'closed-won', 'closed-lost']

export default function DealsPage() {
  const [search, setSearch] = useState('')
  const [stageFilter, setStageFilter] = useState('')
  const [selectedDeals, setSelectedDeals] = useState<string[]>([])
  const [deals] = useState(mockDeals)
  const [isLoading] = useState(false)

  const filteredDeals = deals.filter(deal => {
    const matchesSearch = 
      deal.title.toLowerCase().includes(search.toLowerCase()) ||
      deal.company_name.toLowerCase().includes(search.toLowerCase()) ||
      deal.contact_name.toLowerCase().includes(search.toLowerCase()) ||
      deal.assigned_user.toLowerCase().includes(search.toLowerCase())
    
    const matchesStage = !stageFilter || deal.stage === stageFilter
    
    return matchesSearch && matchesStage
  })

  const handleDelete = async (dealId: string) => {
    if (confirm('Are you sure you want to delete this deal?')) {
      // TODO: Implement delete API call
      console.log('Deleting deal:', dealId)
    }
  }

  const formatCurrency = (amount: number, currency: string = 'USD') => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: currency
    }).format(amount)
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const getProbabilityColor = (probability: number) => {
    if (probability >= 80) return 'text-green-600'
    if (probability >= 60) return 'text-yellow-600'
    if (probability >= 40) return 'text-orange-600'
    return 'text-red-600'
  }

  const getTotalValue = () => {
    return deals
      .filter(deal => !['closed-lost'].includes(deal.stage))
      .reduce((sum, deal) => sum + deal.value, 0)
  }

  const getWonValue = () => {
    return deals
      .filter(deal => deal.stage === 'closed-won')
      .reduce((sum, deal) => sum + deal.value, 0)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      
      <div className="md:pl-64">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="sm:flex sm:items-center sm:justify-between mb-8">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Deals</h1>
              <p className="text-gray-600">Manage your sales pipeline and deals</p>
            </div>
            <div className="mt-4 sm:mt-0">
              <button
                type="button"
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <PlusIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
                Add Deal
              </button>
            </div>
          </div>

          {/* Pipeline Stats */}
          <div className="mb-8 grid grid-cols-1 gap-4 sm:grid-cols-4">
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <CurrencyDollarIcon className="h-6 w-6 text-green-400" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Total Pipeline</dt>
                      <dd className="text-lg font-medium text-gray-900">{formatCurrency(getTotalValue())}</dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <ChartBarIcon className="h-6 w-6 text-blue-400" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Won This Month</dt>
                      <dd className="text-lg font-medium text-gray-900">{formatCurrency(getWonValue())}</dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>

            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <div className="w-6 h-6 bg-green-100 rounded-full flex items-center justify-center">
                      <div className="w-2 h-2 bg-green-600 rounded-full"></div>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Won Deals</dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {deals.filter(d => d.stage === 'closed-won').length}
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
                    <div className="w-6 h-6 bg-orange-100 rounded-full flex items-center justify-center">
                      <div className="w-2 h-2 bg-orange-600 rounded-full"></div>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Active Deals</dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {deals.filter(d => !['closed-won', 'closed-lost'].includes(d.stage)).length}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Search and Filters */}
          <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="relative col-span-2">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search deals..."
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <select 
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              value={stageFilter}
              onChange={(e) => setStageFilter(e.target.value)}
            >
              <option value="">All Stages</option>
              {stageOrder.map(stage => (
                <option key={stage} value={stage} className="capitalize">
                  {stage.replace('-', ' ')}
                </option>
              ))}
            </select>
          </div>

          {/* Deals Table */}
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            {isLoading ? (
              <div className="p-8 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
                <p className="mt-4 text-gray-500">Loading deals...</p>
              </div>
            ) : filteredDeals.length === 0 ? (
              <div className="p-8 text-center">
                <CurrencyDollarIcon className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">No deals</h3>
                <p className="mt-1 text-sm text-gray-500">
                  {search || stageFilter ? 'No deals match your filters.' : 'Get started by creating a new deal.'}
                </p>
              </div>
            ) : (
              <ul className="divide-y divide-gray-200">
                {filteredDeals.map((deal) => (
                  <li key={deal.id}>
                    <div className="px-4 py-4 sm:px-6">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <input
                            type="checkbox"
                            className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                            checked={selectedDeals.includes(deal.id)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setSelectedDeals([...selectedDeals, deal.id])
                              } else {
                                setSelectedDeals(selectedDeals.filter(id => id !== deal.id))
                              }
                            }}
                          />
                          <div className="ml-4 flex-1 min-w-0">
                            <div className="flex items-center">
                              <h3 className="text-lg font-medium text-gray-900">
                                {deal.title}
                              </h3>
                              <span className={`ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${stageColors[deal.stage as keyof typeof stageColors]}`}>
                                {deal.stage.replace('-', ' ')}
                              </span>
                            </div>
                            <p className="mt-1 text-sm text-gray-600">{deal.description}</p>
                            
                            <div className="mt-3 grid grid-cols-1 gap-2 sm:grid-cols-4">
                              <div>
                                <p className="text-xs text-gray-500">Value & Probability</p>
                                <p className="text-lg font-bold text-gray-900">{formatCurrency(deal.value)}</p>
                                <p className={`text-sm font-medium ${getProbabilityColor(deal.probability)}`}>
                                  {deal.probability}% probability
                                </p>
                              </div>
                              <div>
                                <p className="text-xs text-gray-500">Contact & Company</p>
                                <p className="text-sm text-gray-900">{deal.contact_name}</p>
                                <p className="text-sm text-gray-600">{deal.company_name}</p>
                              </div>
                              <div>
                                <p className="text-xs text-gray-500">Assigned To</p>
                                <p className="text-sm text-gray-900">{deal.assigned_user}</p>
                              </div>
                              <div>
                                <p className="text-xs text-gray-500">Expected Close</p>
                                <p className="text-sm text-gray-900">{formatDate(deal.expected_close_date)}</p>
                                {deal.actual_close_date && (
                                  <p className="text-xs text-gray-500">
                                    Closed: {formatDate(deal.actual_close_date)}
                                  </p>
                                )}
                              </div>
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2 ml-4">
                          <button
                            type="button"
                            className="inline-flex items-center p-2 border border-gray-300 rounded-md text-gray-400 hover:text-gray-500 hover:border-gray-400"
                            title="View deal"
                          >
                            <EyeIcon className="h-4 w-4" />
                          </button>
                          <button
                            type="button"
                            className="inline-flex items-center p-2 border border-gray-300 rounded-md text-gray-400 hover:text-gray-500 hover:border-gray-400"
                            title="Edit deal"
                          >
                            <PencilIcon className="h-4 w-4" />
                          </button>
                          <button
                            type="button"
                            onClick={() => handleDelete(deal.id)}
                            className="inline-flex items-center p-2 border border-gray-300 rounded-md text-red-400 hover:text-red-500 hover:border-red-400"
                            title="Delete deal"
                          >
                            <TrashIcon className="h-4 w-4" />
                          </button>
                        </div>
                      </div>
                    </div>
                  </li>
                ))}
              </ul>
            )}
          </div>

          {/* Bulk Actions */}
          {selectedDeals.length > 0 && (
            <div className="mt-4 bg-white rounded-lg shadow p-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">
                  {selectedDeals.length} deal{selectedDeals.length !== 1 ? 's' : ''} selected
                </span>
                <div className="space-x-2">
                  <button
                    type="button"
                    className="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
                  >
                    Update Stage
                  </button>
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

          {/* Pipeline Overview */}
          <div className="mt-8">
            <h2 className="text-lg font-medium text-gray-900 mb-4">Pipeline by Stage</h2>
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-6">
              {stageOrder.map((stage) => {
                const stageDeals = deals.filter(deal => deal.stage === stage)
                const stageValue = stageDeals.reduce((sum, deal) => sum + deal.value, 0)
                
                return (
                  <div key={stage} className="bg-white overflow-hidden shadow rounded-lg">
                    <div className="p-5">
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <dt className={`text-sm font-medium capitalize mb-2 px-2 py-1 rounded-full ${stageColors[stage as keyof typeof stageColors]}`}>
                            {stage.replace('-', ' ')}
                          </dt>
                          <dd className="text-lg font-medium text-gray-900">{stageDeals.length}</dd>
                          <dd className="text-sm text-gray-600">{formatCurrency(stageValue)}</dd>
                        </div>
                      </div>
                    </div>
                  </div>
                )
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}