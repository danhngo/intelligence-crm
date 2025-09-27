'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import {
  CpuChipIcon,
  PlusIcon,
  PlayIcon,
  TrashIcon,
  EyeIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline'

interface AIModel {
  id: string
  name: string
  description: string
  type: string
  framework: string
  version: string
  status: string
  accuracy?: number
  created_at: string
  prediction_count?: number
}

export default function ModelsPage() {
  const [models, setModels] = useState<AIModel[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchModels()
  }, [])

  const fetchModels = async () => {
    try {
      const response = await fetch('/api/ai/models')
      if (!response.ok) {
        throw new Error('Failed to fetch models')
      }
      const data = await response.json()
      setModels(data)
    } catch (err) {
      setError('Failed to load models')
      console.error('Error fetching models:', err)
    } finally {
      setLoading(false)
    }
  }

  const deleteModel = async (modelId: string) => {
    if (!confirm('Are you sure you want to delete this model?')) {
      return
    }

    try {
      const response = await fetch(`/api/ai/models/${modelId}`, {
        method: 'DELETE'
      })
      
      if (!response.ok) {
        throw new Error('Failed to delete model')
      }
      
      // Remove model from list
      setModels(models.filter(model => model.id !== modelId))
    } catch (err) {
      console.error('Error deleting model:', err)
      alert('Failed to delete model')
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'deployed':
        return 'bg-green-100 text-green-800'
      case 'training':
        return 'bg-yellow-100 text-yellow-800'
      case 'draft':
        return 'bg-gray-100 text-gray-800'
      case 'failed':
        return 'bg-red-100 text-red-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-200 rounded w-1/4 mb-4"></div>
            <div className="space-y-4">
              {[1, 2, 3].map(i => (
                <div key={i} className="bg-white h-24 rounded-lg"></div>
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
            <h1 className="text-3xl font-bold text-gray-900">AI Models</h1>
            <p className="mt-2 text-gray-600">
              Manage and deploy machine learning models
            </p>
          </div>
          <Link
            href="/ai/models/new"
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center space-x-2"
          >
            <PlusIcon className="h-5 w-5" />
            <span>Deploy Model</span>
          </Link>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
            <p className="text-red-600">{error}</p>
            <button
              onClick={fetchModels}
              className="mt-2 text-red-600 underline hover:text-red-800"
            >
              Retry
            </button>
          </div>
        )}

        {/* Models Grid */}
        {models.length === 0 ? (
          <div className="text-center py-12">
            <CpuChipIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No models</h3>
            <p className="mt-1 text-sm text-gray-500">
              Get started by deploying your first AI model.
            </p>
            <div className="mt-6">
              <Link
                href="/ai/models/new"
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
              >
                Deploy Model
              </Link>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6">
            {models.map((model) => (
              <div key={model.id} className="bg-white rounded-lg shadow hover:shadow-md transition-shadow">
                <div className="p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-3">
                      <div className="bg-blue-100 p-2 rounded-lg">
                        <CpuChipIcon className="h-6 w-6 text-blue-600" />
                      </div>
                      <div>
                        <h3 className="text-lg font-semibold text-gray-900">{model.name}</h3>
                        <p className="text-sm text-gray-500">{model.framework} • {model.version}</p>
                      </div>
                    </div>
                    <span className={`px-2 py-1 rounded-full text-xs font-medium ${getStatusColor(model.status)}`}>
                      {model.status}
                    </span>
                  </div>

                  <p className="text-gray-600 text-sm mb-4 line-clamp-2">
                    {model.description || 'No description available'}
                  </p>

                  <div className="grid grid-cols-2 gap-4 mb-4">
                    <div>
                      <p className="text-xs text-gray-500 uppercase tracking-wide">Type</p>
                      <p className="font-medium text-gray-900">{model.type}</p>
                    </div>
                    {model.accuracy && (
                      <div>
                        <p className="text-xs text-gray-500 uppercase tracking-wide">Accuracy</p>
                        <p className="font-medium text-gray-900">{(model.accuracy * 100).toFixed(1)}%</p>
                      </div>
                    )}
                  </div>

                  {model.prediction_count && (
                    <div className="mb-4">
                      <p className="text-xs text-gray-500 uppercase tracking-wide">Predictions</p>
                      <p className="font-medium text-gray-900">{model.prediction_count.toLocaleString()}</p>
                    </div>
                  )}

                  <div className="flex space-x-2">
                    <Link
                      href={`/ai/models/${model.id}`}
                      className="flex-1 bg-blue-50 text-blue-600 px-3 py-2 rounded-md text-sm font-medium hover:bg-blue-100 flex items-center justify-center space-x-1"
                    >
                      <EyeIcon className="h-4 w-4" />
                      <span>View</span>
                    </Link>
                    
                    {model.status === 'deployed' && (
                      <Link
                        href={`/ai/predictions/new?model=${model.id}`}
                        className="flex-1 bg-green-50 text-green-600 px-3 py-2 rounded-md text-sm font-medium hover:bg-green-100 flex items-center justify-center space-x-1"
                      >
                        <PlayIcon className="h-4 w-4" />
                        <span>Predict</span>
                      </Link>
                    )}
                    
                    <Link
                      href={`/ai/models/${model.id}/metrics`}
                      className="bg-gray-50 text-gray-600 px-3 py-2 rounded-md text-sm font-medium hover:bg-gray-100 flex items-center justify-center"
                    >
                      <ChartBarIcon className="h-4 w-4" />
                    </Link>
                    
                    <button
                      onClick={() => deleteModel(model.id)}
                      className="bg-red-50 text-red-600 px-3 py-2 rounded-md text-sm font-medium hover:bg-red-100 flex items-center justify-center"
                    >
                      <TrashIcon className="h-4 w-4" />
                    </button>
                  </div>
                </div>

                <div className="bg-gray-50 px-6 py-3 rounded-b-lg">
                  <p className="text-xs text-gray-500">
                    Created {new Date(model.created_at).toLocaleDateString()}
                  </p>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}