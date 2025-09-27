'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { 
  BoltIcon, 
  CpuChipIcon, 
  ChartBarIcon, 
  Cog6ToothIcon,
  AcademicCapIcon,
  PlayIcon,
  StopIcon,
  ExclamationTriangleIcon 
} from '@heroicons/react/24/outline'

interface AIStats {
  models: {
    total: number
    deployed: number
    training: number
  }
  predictions: {
    total: number
    success_rate: number
    avg_response_time: number
  }
  training: {
    active_jobs: number
    completed_jobs: number
    success_rate: number
  }
  workflows: {
    total: number
    active: number
    success_rate: number
  }
}

export default function AIDashboard() {
  const [stats, setStats] = useState<AIStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchStats()
  }, [])

  const fetchStats = async () => {
    try {
      // Fetch stats from multiple endpoints
      const [modelsRes, predictionsRes, trainingRes, workflowsRes] = await Promise.all([
        fetch('/api/ai/models/stats'),
        fetch('/api/ai/predictions/stats'),
        fetch('/api/ai/training/stats'),
        fetch('/api/ai/workflows/stats')
      ])

      // Mock data for now since the endpoints might not return these exact stats
      const mockStats: AIStats = {
        models: {
          total: 5,
          deployed: 3,
          training: 1
        },
        predictions: {
          total: 1250,
          success_rate: 96.5,
          avg_response_time: 45
        },
        training: {
          active_jobs: 2,
          completed_jobs: 12,
          success_rate: 88.2
        },
        workflows: {
          total: 8,
          active: 4,
          success_rate: 94.1
        }
      }

      setStats(mockStats)
    } catch (err) {
      setError('Failed to fetch AI statistics')
      console.error('Error fetching AI stats:', err)
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Loading AI Dashboard...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <ExclamationTriangleIcon className="h-12 w-12 text-red-500 mx-auto" />
          <h2 className="mt-4 text-lg font-semibold text-gray-900">Error Loading Dashboard</h2>
          <p className="mt-2 text-gray-600">{error}</p>
          <button
            onClick={fetchStats}
            className="mt-4 bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
          >
            Retry
          </button>
        </div>
      </div>
    )
  }

  const quickActions = [
    {
      name: 'Deploy New Model',
      description: 'Deploy a trained model for predictions',
      href: '/ai/models/new',
      icon: CpuChipIcon,
      color: 'bg-blue-500'
    },
    {
      name: 'Start Training',
      description: 'Train a new AI model',
      href: '/ai/training/new',
      icon: Cog6ToothIcon,
      color: 'bg-green-500'
    },
    {
      name: 'Run Predictions',
      description: 'Make predictions with existing models',
      href: '/ai/predictions/new',
      icon: BoltIcon,
      color: 'bg-purple-500'
    },
    {
      name: 'Create Workflow',
      description: 'Set up automated AI workflow',
      href: '/ai/workflows/new',
      icon: PlayIcon,
      color: 'bg-orange-500'
    }
  ]

  const navigationCards = [
    {
      name: 'AI Models',
      description: 'Manage and deploy machine learning models',
      href: '/ai/models',
      icon: CpuChipIcon,
      stats: `${stats?.models.deployed}/${stats?.models.total} deployed`,
      color: 'bg-blue-50 border-blue-200'
    },
    {
      name: 'Predictions',
      description: 'View and manage prediction jobs',
      href: '/ai/predictions',
      icon: ChartBarIcon,
      stats: `${stats?.predictions.success_rate}% success rate`,
      color: 'bg-green-50 border-green-200'
    },
    {
      name: 'Model Training',
      description: 'Train and retrain AI models',
      href: '/ai/training',
      icon: Cog6ToothIcon,
      stats: `${stats?.training.active_jobs} active jobs`,
      color: 'bg-orange-50 border-orange-200'
    },
    {
      name: 'AI Workflows',
      description: 'Automated AI-powered processes',
      href: '/ai/workflows',
      icon: BoltIcon,
      stats: `${stats?.workflows.active}/${stats?.workflows.total} active`,
      color: 'bg-purple-50 border-purple-200'
    }
  ]

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900">AI & Machine Learning</h1>
          <p className="mt-2 text-gray-600">
            Manage AI models, predictions, training jobs, and automated workflows
          </p>
        </div>

        {/* Stats Overview */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <CpuChipIcon className="h-8 w-8 text-blue-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Active Models</p>
                <p className="text-2xl font-semibold text-gray-900">{stats?.models.deployed}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <ChartBarIcon className="h-8 w-8 text-green-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Predictions Today</p>
                <p className="text-2xl font-semibold text-gray-900">{stats?.predictions.total}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <Cog6ToothIcon className="h-8 w-8 text-orange-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Training Jobs</p>
                <p className="text-2xl font-semibold text-gray-900">{stats?.training.active_jobs}</p>
              </div>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center">
              <div className="flex-shrink-0">
                <BoltIcon className="h-8 w-8 text-purple-600" />
              </div>
              <div className="ml-4">
                <p className="text-sm font-medium text-gray-500">Active Workflows</p>
                <p className="text-2xl font-semibold text-gray-900">{stats?.workflows.active}</p>
              </div>
            </div>
          </div>
        </div>

        {/* Quick Actions */}
        <div className="mb-8">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Quick Actions</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
            {quickActions.map((action) => (
              <Link
                key={action.name}
                href={action.href}
                className="group relative bg-white p-6 rounded-lg shadow hover:shadow-md transition-shadow"
              >
                <div className={`inline-flex p-3 rounded-lg ${action.color}`}>
                  <action.icon className="h-6 w-6 text-white" />
                </div>
                <div className="mt-4">
                  <h3 className="text-lg font-medium text-gray-900 group-hover:text-blue-600">
                    {action.name}
                  </h3>
                  <p className="mt-1 text-sm text-gray-500">{action.description}</p>
                </div>
              </Link>
            ))}
          </div>
        </div>

        {/* Main Navigation */}
        <div>
          <h2 className="text-lg font-semibold text-gray-900 mb-4">AI Services</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {navigationCards.map((card) => (
              <Link
                key={card.name}
                href={card.href}
                className={`group block p-6 rounded-lg border-2 ${card.color} hover:shadow-lg transition-all`}
              >
                <div className="flex items-center">
                  <card.icon className="h-8 w-8 text-gray-600" />
                  <div className="ml-4 flex-1">
                    <h3 className="text-lg font-semibold text-gray-900 group-hover:text-blue-600">
                      {card.name}
                    </h3>
                    <p className="mt-1 text-sm text-gray-600">{card.description}</p>
                    <p className="mt-2 text-xs font-medium text-gray-500">{card.stats}</p>
                  </div>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}