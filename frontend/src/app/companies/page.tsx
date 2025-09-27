'use client'

import { useState } from 'react'
import Sidebar from '@/components/layout/sidebar'
import { 
  PlusIcon, 
  MagnifyingGlassIcon,
  PencilIcon,
  TrashIcon,
  EyeIcon,
  BuildingOfficeIcon 
} from '@heroicons/react/24/outline'

// Mock data - replace with actual API calls
const mockCompanies = [
  {
    id: '1',
    name: 'Acme Corporation',
    industry: 'Technology',
    employee_count: 150,
    annual_revenue: 5000000,
    status: 'active',
    website: 'https://acme.com',
    email: 'info@acme.com',
    phone: '+1-555-123-4567',
    city: 'San Francisco',
    country: 'USA',
    created_at: '2024-01-15T10:00:00Z'
  },
  {
    id: '2',
    name: 'TechStart Solutions',
    industry: 'Software',
    employee_count: 50,
    annual_revenue: 1200000,
    status: 'prospect',
    website: 'https://techstart.io',
    email: 'hello@techstart.io',
    phone: '+1-555-987-6543',
    city: 'New York',
    country: 'USA',
    created_at: '2024-02-20T14:30:00Z'
  }
]

export default function CompaniesPage() {
  const [search, setSearch] = useState('')
  const [selectedCompanies, setSelectedCompanies] = useState<string[]>([])
  const [companies] = useState(mockCompanies)
  const [isLoading] = useState(false)

  const filteredCompanies = companies.filter(company =>
    company.name.toLowerCase().includes(search.toLowerCase()) ||
    company.industry.toLowerCase().includes(search.toLowerCase()) ||
    company.email.toLowerCase().includes(search.toLowerCase())
  )

  const handleDelete = async (companyId: string) => {
    if (confirm('Are you sure you want to delete this company?')) {
      // TODO: Implement delete API call
      console.log('Deleting company:', companyId)
    }
  }

  const formatRevenue = (revenue: number) => {
    return new Intl.NumberFormat('en-US', {
      style: 'currency',
      currency: 'USD',
      minimumFractionDigits: 0,
      maximumFractionDigits: 0,
    }).format(revenue)
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      
      <div className="md:pl-64">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="sm:flex sm:items-center sm:justify-between mb-8">
            <div>
              <h1 className="text-2xl font-bold text-gray-900">Companies</h1>
              <p className="text-gray-600">Manage your business accounts and organizations</p>
            </div>
            <div className="mt-4 sm:mt-0">
              <button
                type="button"
                className="inline-flex items-center px-4 py-2 border border-transparent rounded-md shadow-sm text-sm font-medium text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                <PlusIcon className="-ml-1 mr-2 h-5 w-5" aria-hidden="true" />
                Add Company
              </button>
            </div>
          </div>

          {/* Search and Filters */}
          <div className="mb-6 grid grid-cols-1 gap-4 sm:grid-cols-3">
            <div className="relative col-span-2">
              <MagnifyingGlassIcon className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search companies..."
                className="block w-full pl-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-primary-500 focus:border-primary-500"
                value={search}
                onChange={(e) => setSearch(e.target.value)}
              />
            </div>
            <select className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500">
              <option value="">All Industries</option>
              <option value="technology">Technology</option>
              <option value="software">Software</option>
              <option value="finance">Finance</option>
              <option value="healthcare">Healthcare</option>
            </select>
          </div>

          {/* Companies Grid */}
          <div className="bg-white shadow overflow-hidden sm:rounded-md">
            {isLoading ? (
              <div className="p-8 text-center">
                <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600 mx-auto"></div>
                <p className="mt-4 text-gray-500">Loading companies...</p>
              </div>
            ) : filteredCompanies.length === 0 ? (
              <div className="p-8 text-center">
                <BuildingOfficeIcon className="mx-auto h-12 w-12 text-gray-400" />
                <h3 className="mt-2 text-sm font-medium text-gray-900">No companies</h3>
                <p className="mt-1 text-sm text-gray-500">
                  {search ? 'No companies match your search.' : 'Get started by creating a new company.'}
                </p>
              </div>
            ) : (
              <ul className="divide-y divide-gray-200">
                {filteredCompanies.map((company) => (
                  <li key={company.id}>
                    <div className="px-4 py-4 sm:px-6">
                      <div className="flex items-center justify-between">
                        <div className="flex items-center">
                          <input
                            type="checkbox"
                            className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-gray-300 rounded"
                            checked={selectedCompanies.includes(company.id)}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setSelectedCompanies([...selectedCompanies, company.id])
                              } else {
                                setSelectedCompanies(selectedCompanies.filter(id => id !== company.id))
                              }
                            }}
                          />
                          <div className="ml-4 flex-1 min-w-0">
                            <div className="flex items-center">
                              <h3 className="text-lg font-medium text-gray-900 truncate">
                                {company.name}
                              </h3>
                              <span className={`ml-2 inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${
                                company.status === 'active' ? 'bg-green-100 text-green-800' :
                                company.status === 'prospect' ? 'bg-blue-100 text-blue-800' :
                                'bg-gray-100 text-gray-800'
                              }`}>
                                {company.status}
                              </span>
                            </div>
                            <div className="mt-2 grid grid-cols-1 gap-2 sm:grid-cols-4">
                              <div>
                                <p className="text-xs text-gray-500">Industry</p>
                                <p className="text-sm text-gray-900">{company.industry}</p>
                              </div>
                              <div>
                                <p className="text-xs text-gray-500">Employees</p>
                                <p className="text-sm text-gray-900">{company.employee_count}</p>
                              </div>
                              <div>
                                <p className="text-xs text-gray-500">Revenue</p>
                                <p className="text-sm text-gray-900">{formatRevenue(company.annual_revenue)}</p>
                              </div>
                              <div>
                                <p className="text-xs text-gray-500">Location</p>
                                <p className="text-sm text-gray-900">{company.city}, {company.country}</p>
                              </div>
                            </div>
                            <div className="mt-2">
                              <p className="text-sm text-gray-600">{company.email}</p>
                              <p className="text-sm text-gray-500">{company.phone}</p>
                            </div>
                          </div>
                        </div>
                        <div className="flex items-center space-x-2 ml-4">
                          <button
                            type="button"
                            className="inline-flex items-center p-2 border border-gray-300 rounded-md text-gray-400 hover:text-gray-500 hover:border-gray-400"
                            title="View company"
                          >
                            <EyeIcon className="h-4 w-4" />
                          </button>
                          <button
                            type="button"
                            className="inline-flex items-center p-2 border border-gray-300 rounded-md text-gray-400 hover:text-gray-500 hover:border-gray-400"
                            title="Edit company"
                          >
                            <PencilIcon className="h-4 w-4" />
                          </button>
                          <button
                            type="button"
                            onClick={() => handleDelete(company.id)}
                            className="inline-flex items-center p-2 border border-gray-300 rounded-md text-red-400 hover:text-red-500 hover:border-red-400"
                            title="Delete company"
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
          {selectedCompanies.length > 0 && (
            <div className="mt-4 bg-white rounded-lg shadow p-4">
              <div className="flex items-center justify-between">
                <span className="text-sm text-gray-600">
                  {selectedCompanies.length} compan{selectedCompanies.length !== 1 ? 'ies' : 'y'} selected
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

          {/* Quick Stats */}
          <div className="mt-8 grid grid-cols-1 gap-4 sm:grid-cols-4">
            <div className="bg-white overflow-hidden shadow rounded-lg">
              <div className="p-5">
                <div className="flex items-center">
                  <div className="flex-shrink-0">
                    <BuildingOfficeIcon className="h-6 w-6 text-gray-400" />
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Total Companies</dt>
                      <dd className="text-lg font-medium text-gray-900">{companies.length}</dd>
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
                      <dt className="text-sm font-medium text-gray-500 truncate">Active</dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {companies.filter(c => c.status === 'active').length}
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
                    <div className="w-6 h-6 bg-blue-100 rounded-full flex items-center justify-center">
                      <div className="w-2 h-2 bg-blue-600 rounded-full"></div>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Prospects</dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {companies.filter(c => c.status === 'prospect').length}
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
                    <div className="w-6 h-6 bg-yellow-100 rounded-full flex items-center justify-center">
                      <div className="w-2 h-2 bg-yellow-600 rounded-full"></div>
                    </div>
                  </div>
                  <div className="ml-5 w-0 flex-1">
                    <dl>
                      <dt className="text-sm font-medium text-gray-500 truncate">Avg Revenue</dt>
                      <dd className="text-lg font-medium text-gray-900">
                        {formatRevenue(companies.reduce((acc, c) => acc + c.annual_revenue, 0) / companies.length)}
                      </dd>
                    </dl>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}