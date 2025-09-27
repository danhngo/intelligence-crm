'use client'

import { useState } from 'react'
import Sidebar from '@/components/layout/sidebar'
import { 
  PlusIcon, 
  MagnifyingGlassIcon,
  PencilIcon,
  TrashIcon,
  EyeIcon,
  UserIcon,
  ArrowRightIcon 
} from '@heroicons/react/24/outline'

// Mock data - replace with actual API calls
const mockLeads = [
  {
    id: '1',
    first_name: 'John',
    last_name: 'Smith',
    email: 'john.smith@example.com',
    phone: '+1-555-123-4567',
    company: 'Tech Solutions Inc',
    title: 'CTO',
    status: 'qualified',
    source: 'website',
    lead_score: 85,
    interest_level: 'hot',
    expected_close_date: '2024-12-15T00:00:00Z',
    created_at: '2024-09-15T10:00:00Z'
  },
  {
    id: '2',
    first_name: 'Sarah',
    last_name: 'Johnson',
    email: 'sarah.j@startup.co',
    phone: '+1-555-987-6543',
    company: 'Innovation Startup',
    title: 'Founder',
    status: 'new',
    source: 'referral',
    lead_score: 92,
    interest_level: 'warm',
    expected_close_date: '2024-11-30T00:00:00Z',
    created_at: '2024-09-20T14:30:00Z'
  },
  {
    id: '3',
    first_name: 'Michael',
    last_name: 'Brown',
    email: 'mbrown@enterprise.com',
    phone: '+1-555-456-7890',
    company: 'Enterprise Corp',
    title: 'VP Sales',
    status: 'nurturing',
    source: 'campaign',
    lead_score: 67,
    interest_level: 'cold',
    expected_close_date: '2025-01-15T00:00:00Z',
    created_at: '2024-09-10T09:15:00Z'
  }
]

const statusColors = {
  new: 'bg-blue-100 text-blue-800',
  qualified: 'bg-green-100 text-green-800',
  nurturing: 'bg-yellow-100 text-yellow-800',
  converted: 'bg-emerald-100 text-emerald-800',
  lost: 'bg-red-100 text-red-800'
}

const interestColors = {
  hot: 'bg-red-100 text-red-800',
  warm: 'bg-orange-100 text-orange-800',
  cold: 'bg-blue-100 text-blue-800'
}

export default function LeadsPage() {
  const [search, setSearch] = useState('')
  const [statusFilter, setStatusFilter] = useState('')
  const [selectedLeads, setSelectedLeads] = useState<string[]>([])
  const [leads] = useState(mockLeads)
  const [isLoading] = useState(false)

  const filteredLeads = leads.filter(lead => {
    const matchesSearch = 
      lead.first_name.toLowerCase().includes(search.toLowerCase()) ||
      lead.last_name.toLowerCase().includes(search.toLowerCase()) ||
      lead.email.toLowerCase().includes(search.toLowerCase()) ||
      lead.company.toLowerCase().includes(search.toLowerCase())
    
    const matchesStatus = !statusFilter || lead.status === statusFilter
    
    return matchesSearch && matchesStatus
  })

  const handleDelete = async (leadId: string) => {
    if (confirm('Are you sure you want to delete this lead?')) {
      // TODO: Implement delete API call
      console.log('Deleting lead:', leadId)
    }
  }

  const handleConvert = async (leadId: string) => {
    if (confirm('Convert this lead to a contact?')) {
      // TODO: Implement convert API call
      console.log('Converting lead:', leadId)
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString()
  }

  const getScoreColor = (score: number) => {
    if (score >= 80) return 'text-green-600'
    if (score >= 60) return 'text-yellow-600'
    return 'text-red-600'
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      
      <div className="md:pl-64">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="sm:flex sm:items-center sm:justify-between mb-8">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Leads</h1>
              <p className="text-gray-600">Manage and track your sales leads</p>
            </div>
            <div className="mt-4 sm:mt-0">
              <button
                type="button"
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <PlusIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
                Add Lead
              </button>
            </div>
          </div>

          {/* Search and Filters */}
          <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="relative col-span-2">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search leads..."
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <select 
              className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500"
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value)}
            >
              <option value="">All Statuses</option>
              <option value="new">New</option>
              <option value="qualified">Qualified</option>
              <option value="nurturing">Nurturing</option>
              <option value="converted">Converted</option>
              <option value="lost">Lost</option>
            </select>
          </div>

          {/* Leads Table */}
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            {isLoading ? (
              <div className="p-8 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
                <p className="mt-4 text-gray-500">Loading leads...</p>
              </div>
            ) : filteredLeads.length === 0 ? (
              <div className="p-8 text-center">
                <UserIcon className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">No leads</h3>
                <p className="mt-1 text-sm text-gray-500">
                  {search || statusFilter ? 'No leads match your filters.' : 'Get started by creating a new lead.'}
                </p>
              </div>
            ) : (
              <ul className="divide-y divide-gray-200">
                {filteredLeads.map((lead) => (
                  <li key={lead.id}>
                    <div className="px-4 py-4 sm:px-6">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <input
                            type="checkbox"
                            className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                            checked={selectedLeads.includes(lead.id)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setSelectedLeads([...selectedLeads, lead.id])
                              } else {
                                setSelectedLeads(selectedLeads.filter(id => id !== lead.id))
                              }
                            }}
                          />
                          <div className="ml-4 flex-1 min-w-0">
                            <div className="flex items-center">
                              <h3 className="text-lg font-medium text-gray-900">
                                {lead.first_name} {lead.last_name}
                              </h3>
                              <span className={`ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${statusColors[lead.status as keyof typeof statusColors]}`}>
                                {lead.status}
                              </span>
                              <span className={`ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${interestColors[lead.interest_level as keyof typeof interestColors]}`}>
                                {lead.interest_level}
                              </span>
                            </div>
                            <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-4">
                              <div>
                                <p className="text-xs text-gray-500">Company & Title</p>
                                <p className="text-sm text-gray-900">{lead.company}</p>
                                <p className="text-sm text-gray-600">{lead.title}</p>
                              </div>
                              <div>
                                <p className="text-xs text-gray-500">Contact Info</p>
                                <p className="text-sm text-gray-900">{lead.email}</p>
                                <p className="text-sm text-gray-600">{lead.phone}</p>
                              </div>
                              <div>
                                <p className="text-xs text-gray-500">Lead Score</p>
                                <p className={`text-lg font-bold ${getScoreColor(lead.lead_score)}`}>
                                  {lead.lead_score}/100
                                </p>
                              </div>
                              <div>
                                <p className="text-xs text-gray-500">Expected Close</p>
                                <p className="text-sm text-gray-900">{formatDate(lead.expected_close_date)}</p>
                                <p className="text-xs text-gray-500">Source: {lead.source}</p>
                              </div>
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2 ml-4">
                          <button
                            type="button"
                            onClick={() => handleConvert(lead.id)}
                            className="inline-flex items-center p-2 border border-green-300 rounded-md text-green-600 hover:text-green-700 hover:border-green-400"
                            title="Convert to contact"
                          >
                            <ArrowRightIcon className="h-4 w-4" />
                          </button>
                          <button
                            type="button"
                            className="inline-flex items-center p-2 border border-gray-300 rounded-md text-gray-400 hover:text-gray-500 hover:border-gray-400"
                            title="View lead"
                          >
                            <EyeIcon className="h-4 w-4" />
                          </button>
                          <button
                            type="button"
                            className="inline-flex items-center p-2 border border-gray-300 rounded-md text-gray-400 hover:text-gray-500 hover:border-gray-400"
                            title="Edit lead"
                          >
                            <PencilIcon className="h-4 w-4" />
                          </button>
                          <button
                            type="button"
                            onClick={() => handleDelete(lead.id)}
                            className="inline-flex items-center p-2 border border-gray-300 rounded-md text-red-400 hover:text-red-500 hover:border-red-400"
                            title="Delete lead"
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
          {selectedLeads.length > 0 && (
            <div className="mt-4 bg-white rounded-lg shadow p-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">
                  {selectedLeads.length} lead{selectedLeads.length !== 1 ? 's' : ''} selected
                </span>
                <div className="space-x-2">
                  <button
                    type="button"
                    className="inline-flex items-center px-3 py-2 border border-green-300 shadow-sm text-sm leading-4 font-medium rounded-md text-green-700 bg-white hover:bg-green-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-green-500"
                  >
                    Convert Selected
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

          {/* Quick Stats */}
          <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-5">
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <UserIcon className="h-6 w-6 text-gray-400" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Total Leads</dt>
                      <dd className="text-lg font-medium text-gray-900">{leads.length}</dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
            
            {Object.entries(statusColors).map(([status, colorClass]) => {
              const count = leads.filter(lead => lead.status === status).length
              return (
                <div key={status} className="bg-white overflow-hidden shadow rounded-lg">
                  <div className="p-5">
                    <div className="flex items-center">
                      <div className="flex-shrink-0">
                        <div className={`w-6 h-6 rounded-full flex items-center justify-center ${colorClass.replace('text-', 'bg-').replace('-800', '-100')}`}>
                          <div className={`w-2 h-2 rounded-full ${colorClass.replace('text-', 'bg-')}`}></div>
                        </div>
                      </div>
                      <div className="ml-5 w-0 flex-1">
                        <dl>
                          <dt className="text-sm font-medium text-gray-500 truncate capitalize">{status}</dt>
                          <dd className="text-lg font-medium text-gray-900">{count}</dd>
                        </dl>
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
  )
}