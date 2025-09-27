'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import {
  Cog6ToothIcon,
  PlusIcon,
  EyeIcon,
  PlayIcon,
  PauseIcon,
  StopIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
  ClockIcon
} from '@heroicons/react/24/outline'

interface Workflow {
  id: string
  name: string
  description: string
  status: 'active' | 'inactive' | 'running' | 'paused' | 'error'
  type: string
  steps: number
  last_run?: string
  next_run?: string
  success_rate?: number
  created_at: string
  updated_at: string
}

export default function WorkflowsPage() {
  const [workflows, setWorkflows] = useState<Workflow[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchWorkflows()
  }, [])

  const fetchWorkflows = async () => {
    try {
      const response = await fetch('/api/ai/workflows')
      if (!response.ok) {
        throw new Error('Failed to fetch workflows')
      }
      const data = await response.json()
      setWorkflows(data)
    } catch (err) {
      setError('Failed to load workflows')
      console.error('Error fetching workflows:', err)
    } finally {
      setLoading(false)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'active':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />
      case 'running':
        return <PlayIcon className="h-5 w-5 text-blue-500 animate-pulse" />
      case 'paused':
        return <PauseIcon className="h-5 w-5 text-yellow-500" />
      case 'error':
        return <ExclamationCircleIcon className="h-5 w-5 text-red-500" />
      case 'inactive':
        return <StopIcon className="h-5 w-5 text-gray-500" />
      default:
        return <ClockIcon className="h-5 w-5 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'running':
        return 'bg-blue-100 text-blue-800'
      case 'paused':
        return 'bg-yellow-100 text-yellow-800'
      case 'error':
        return 'bg-red-100 text-red-800'
      case 'inactive':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  const handleWorkflowAction = async (workflowId: string, action: 'start' | 'stop' | 'pause') => {
    try {
      const response = await fetch(`/api/ai/workflows/${workflowId}/${action}`, {
        method: 'POST'
      })
      
      if (!response.ok) {
        throw new Error(`Failed to ${action} workflow`)
      }
      
      // Refresh workflows list
      fetchWorkflows()
    } catch (err) {
      console.error(`Error ${action}ing workflow:`, err)
      setError(`Failed to ${action} workflow`)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {[1, 2, 3, 4, 5, 6].map(i => (
                <div key={i} className="bg-white h-48 rounded-lg"></div>
              ))}
            </div>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">AI Workflows</h1>
            <p className="mt-2 text-gray-600">
              Automate AI processes with custom workflows
            </p>
          </div>
          <Link
            href="/ai/workflows/new"
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center space-x-2"
          >
            <PlusIcon className="h-5 w-5" />
            <span>Create Workflow</span>
          </Link>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
            <p className="text-red-600">{error}</p>
            <button
              onClick={fetchWorkflows}
              className="mt-2 text-red-600 underline hover:text-red-800"
            >
              Retry
            </button>
          </div>
        )}

        {/* Workflows Grid */}
        {workflows.length === 0 ? (
          <div className="text-center py-12">
            <Cog6ToothIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No workflows</h3>
            <p className="mt-1 text-sm text-gray-500">
              Get started by creating your first AI workflow.
            </p>
            <div className="mt-6">
              <Link
                href="/ai/workflows/new"
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
              >
                Create Workflow
              </Link>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {workflows.map((workflow) => (
              <div key={workflow.id} className="bg-white rounded-lg shadow hover:shadow-md transition-shadow">
                <div className="p-6">
                  {/* Header */}
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      {getStatusIcon(workflow.status)}
                      <h3 className="text-lg font-medium text-gray-900 truncate">
                        {workflow.name}
                      </h3>
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(workflow.status)}`}>
                      {workflow.status}
                    </span>
                  </div>

                  {/* Description */}
                  <p className="text-sm text-gray-600 mb-4 line-clamp-2">
                    {workflow.description}
                  </p>

                  {/* Metadata */}
                  <div className="space-y-2 mb-4">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Type:</span>
                      <span className="text-gray-900 font-medium">{workflow.type}</span>
                    </div>
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-500">Steps:</span>
                      <span className="text-gray-900">{workflow.steps}</span>
                    </div>
                    {workflow.success_rate !== undefined && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Success Rate:</span>
                        <span className="text-gray-900">{(workflow.success_rate * 100).toFixed(1)}%</span>
                      </div>
                    )}
                    {workflow.last_run && (
                      <div className="flex justify-between text-sm">
                        <span className="text-gray-500">Last Run:</span>
                        <span className="text-gray-900">
                          {new Date(workflow.last_run).toLocaleDateString()}
                        </span>
                      </div>
                    )}
                  </div>

                  {/* Actions */}
                  <div className="flex space-x-2">
                    <Link
                      href={`/ai/workflows/${workflow.id}`}
                      className="flex-1 bg-gray-50 text-gray-700 px-3 py-2 rounded-md text-sm hover:bg-gray-100 flex items-center justify-center space-x-1"
                    >
                      <EyeIcon className="h-4 w-4" />
                      <span>View</span>
                    </Link>

                    {workflow.status === 'active' && (
                      <button
                        onClick={() => handleWorkflowAction(workflow.id, 'start')}
                        className="bg-blue-50 text-blue-600 px-3 py-2 rounded-md text-sm hover:bg-blue-100 flex items-center space-x-1"
                      >
                        <PlayIcon className="h-4 w-4" />
                        <span>Run</span>
                      </button>
                    )}

                    {workflow.status === 'running' && (
                      <button
                        onClick={() => handleWorkflowAction(workflow.id, 'pause')}
                        className="bg-yellow-50 text-yellow-600 px-3 py-2 rounded-md text-sm hover:bg-yellow-100 flex items-center space-x-1"
                      >
                        <PauseIcon className="h-4 w-4" />
                        <span>Pause</span>
                      </button>
                    )}

                    {(workflow.status === 'running' || workflow.status === 'paused') && (
                      <button
                        onClick={() => handleWorkflowAction(workflow.id, 'stop')}
                        className="bg-red-50 text-red-600 px-3 py-2 rounded-md text-sm hover:bg-red-100 flex items-center space-x-1"
                      >
                        <StopIcon className="h-4 w-4" />
                        <span>Stop</span>
                      </button>
                    )}
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}