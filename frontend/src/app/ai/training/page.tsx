'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import {
  AcademicCapIcon,
  PlusIcon,
  EyeIcon,
  ClockIcon,
  CheckCircleIcon,
  ExclamationCircleIcon,
  ChartBarIcon
} from '@heroicons/react/24/outline'

interface TrainingJob {
  job_id: string
  status: string
  model_id: string
  model_type: string
  progress: number
  current_epoch?: number
  total_epochs?: number
  metrics?: {
    accuracy?: number
    loss?: number
    validation_accuracy?: number
    validation_loss?: number
  }
  created_at: string
  completed_at?: string
  estimated_completion?: string
}

export default function TrainingPage() {
  const [jobs, setJobs] = useState<TrainingJob[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    fetchTrainingJobs()
    // Poll for updates every 5 seconds for running jobs
    const interval = setInterval(() => {
      if (jobs.some(job => job.status === 'running')) {
        fetchTrainingJobs()
      }
    }, 5000)

    return () => clearInterval(interval)
  }, [jobs])

  const fetchTrainingJobs = async () => {
    try {
      const response = await fetch('/api/ai/training')
      if (!response.ok) {
        throw new Error('Failed to fetch training jobs')
      }
      const data = await response.json()
      setJobs(data)
    } catch (err) {
      setError('Failed to load training jobs')
      console.error('Error fetching training jobs:', err)
    } finally {
      setLoading(false)
    }
  }

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'completed':
        return <CheckCircleIcon className="h-5 w-5 text-green-500" />
      case 'running':
        return <ClockIcon className="h-5 w-5 text-blue-500 animate-pulse" />
      case 'failed':
        return <ExclamationCircleIcon className="h-5 w-5 text-red-500" />
      default:
        return <ClockIcon className="h-5 w-5 text-gray-500" />
    }
  }

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'bg-green-100 text-green-800'
      case 'running':
        return 'bg-blue-100 text-blue-800'
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
                <div key={i} className="bg-white h-32 rounded-lg"></div>
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
            <h1 className="text-3xl font-bold text-gray-900">AI Training</h1>
            <p className="mt-2 text-gray-600">
              Manage model training jobs and monitor progress
            </p>
          </div>
          <Link
            href="/ai/training/new"
            className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center space-x-2"
          >
            <PlusIcon className="h-5 w-5" />
            <span>Start Training</span>
          </Link>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
            <p className="text-red-600">{error}</p>
            <button
              onClick={fetchTrainingJobs}
              className="mt-2 text-red-600 underline hover:text-red-800"
            >
              Retry
            </button>
          </div>
        )}

        {/* Training Jobs List */}
        {jobs.length === 0 ? (
          <div className="text-center py-12">
            <AcademicCapIcon className="mx-auto h-12 w-12 text-gray-400" />
            <h3 className="mt-2 text-sm font-medium text-gray-900">No training jobs</h3>
            <p className="mt-1 text-sm text-gray-500">
              Get started by training your first AI model.
            </p>
            <div className="mt-6">
              <Link
                href="/ai/training/new"
                className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
              >
                Start Training
              </Link>
            </div>
          </div>
        ) : (
          <div className="space-y-6">
            {jobs.map((job) => (
              <div key={job.job_id} className="bg-white shadow rounded-lg overflow-hidden">
                <div className="px-6 py-4">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center space-x-4">
                      {getStatusIcon(job.status)}
                      <div>
                        <h3 className="text-lg font-medium text-gray-900">
                          {job.model_type} Model Training
                        </h3>
                        <p className="text-sm text-gray-500">
                          Job {job.job_id.slice(0, 8)}... • Model {job.model_id.slice(0, 8)}...
                        </p>
                      </div>
                    </div>
                    
                    <div className="flex items-center space-x-4">
                      <span className={`px-3 py-1 rounded-full text-sm font-medium ${getStatusColor(job.status)}`}>
                        {job.status}
                      </span>
                      <Link
                        href={`/ai/training/${job.job_id}`}
                        className="bg-blue-50 text-blue-600 px-3 py-2 rounded-md text-sm hover:bg-blue-100 flex items-center space-x-1"
                      >
                        <EyeIcon className="h-4 w-4" />
                        <span>View Details</span>
                      </Link>
                    </div>
                  </div>

                  {/* Progress Section */}
                  <div className="mb-4">
                    <div className="flex justify-between text-sm text-gray-600 mb-1">
                      <span>Training Progress</span>
                      <span>{job.progress.toFixed(1)}%</span>
                    </div>
                    <div className="bg-gray-200 rounded-full h-2">
                      <div 
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${job.progress}%` }}
                      ></div>
                    </div>
                    {job.current_epoch && job.total_epochs && (
                      <div className="flex justify-between text-xs text-gray-500 mt-1">
                        <span>Epoch {job.current_epoch} of {job.total_epochs}</span>
                        {job.estimated_completion && (
                          <span>Est. completion: {new Date(job.estimated_completion).toLocaleTimeString()}</span>
                        )}
                      </div>
                    )}
                  </div>

                  {/* Metrics */}
                  {job.metrics && (
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                      {job.metrics.accuracy && (
                        <div className="bg-gray-50 rounded-lg p-3">
                          <div className="text-xs text-gray-500">Accuracy</div>
                          <div className="text-lg font-semibold text-gray-900">
                            {(job.metrics.accuracy * 100).toFixed(1)}%
                          </div>
                        </div>
                      )}
                      {job.metrics.loss && (
                        <div className="bg-gray-50 rounded-lg p-3">
                          <div className="text-xs text-gray-500">Loss</div>
                          <div className="text-lg font-semibold text-gray-900">
                            {job.metrics.loss.toFixed(4)}
                          </div>
                        </div>
                      )}
                      {job.metrics.validation_accuracy && (
                        <div className="bg-gray-50 rounded-lg p-3">
                          <div className="text-xs text-gray-500">Val Accuracy</div>
                          <div className="text-lg font-semibold text-gray-900">
                            {(job.metrics.validation_accuracy * 100).toFixed(1)}%
                          </div>
                        </div>
                      )}
                      {job.metrics.validation_loss && (
                        <div className="bg-gray-50 rounded-lg p-3">
                          <div className="text-xs text-gray-500">Val Loss</div>
                          <div className="text-lg font-semibold text-gray-900">
                            {job.metrics.validation_loss.toFixed(4)}
                          </div>
                        </div>
                      )}
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}