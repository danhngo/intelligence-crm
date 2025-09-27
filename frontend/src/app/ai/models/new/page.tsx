'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import Link from 'next/link'
import { ArrowLeftIcon } from '@heroicons/react/24/outline'

interface ModelFormData {
  name: string
  description: string
  type: string
  framework: string
  version: string
  algorithm: string
  hyperparameters: Record<string, any>
  features: string[]
}

export default function NewModelPage() {
  const router = useRouter()
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  
  const [formData, setFormData] = useState<ModelFormData>({
    name: '',
    description: '',
    type: 'classification',
    framework: 'scikit-learn',
    version: '1.0.0',
    algorithm: 'random_forest',
    hyperparameters: {},
    features: []
  })

  const [hyperparameterInputs, setHyperparameterInputs] = useState<Array<{key: string, value: string, type: string}>>([
    { key: 'n_estimators', value: '100', type: 'number' },
    { key: 'max_depth', value: '10', type: 'number' },
    { key: 'random_state', value: '42', type: 'number' }
  ])

  const [featuresInput, setFeaturesInput] = useState('')

  const modelTypes = [
    { value: 'classification', label: 'Classification' },
    { value: 'regression', label: 'Regression' },
    { value: 'clustering', label: 'Clustering' },
    { value: 'recommendation', label: 'Recommendation' },
    { value: 'natural_language', label: 'Natural Language' }
  ]

  const frameworks = [
    { value: 'scikit-learn', label: 'Scikit-Learn' },
    { value: 'tensorflow', label: 'TensorFlow' },
    { value: 'pytorch', label: 'PyTorch' },
    { value: 'xgboost', label: 'XGBoost' },
    { value: 'lightgbm', label: 'LightGBM' }
  ]

  const algorithms = {
    'scikit-learn': [
      { value: 'random_forest', label: 'Random Forest' },
      { value: 'logistic_regression', label: 'Logistic Regression' },
      { value: 'svm', label: 'Support Vector Machine' },
      { value: 'neural_network', label: 'Neural Network' }
    ],
    'xgboost': [
      { value: 'xgboost_classifier', label: 'XGBoost Classifier' },
      { value: 'xgboost_regressor', label: 'XGBoost Regressor' }
    ],
    'tensorflow': [
      { value: 'deep_neural_network', label: 'Deep Neural Network' },
      { value: 'cnn', label: 'Convolutional Neural Network' },
      { value: 'rnn', label: 'Recurrent Neural Network' }
    ]
  }

  const addHyperparameter = () => {
    setHyperparameterInputs([...hyperparameterInputs, { key: '', value: '', type: 'string' }])
  }

  const updateHyperparameter = (index: number, field: string, value: string) => {
    const updated = hyperparameterInputs.map((param, i) => 
      i === index ? { ...param, [field]: value } : param
    )
    setHyperparameterInputs(updated)
  }

  const removeHyperparameter = (index: number) => {
    setHyperparameterInputs(hyperparameterInputs.filter((_, i) => i !== index))
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    setError(null)

    try {
      // Process hyperparameters
      const hyperparameters: Record<string, any> = {}
      hyperparameterInputs.forEach(param => {
        if (param.key && param.value) {
          if (param.type === 'number') {
            hyperparameters[param.key] = parseFloat(param.value)
          } else if (param.type === 'boolean') {
            hyperparameters[param.key] = param.value.toLowerCase() === 'true'
          } else {
            hyperparameters[param.key] = param.value
          }
        }
      })

      // Process features
      const features = featuresInput
        .split(',')
        .map(f => f.trim())
        .filter(f => f.length > 0)

      const modelData = {
        name: formData.name,
        description: formData.description,
        type: formData.type,
        framework: formData.framework,
        version: formData.version,
        model_configuration: {
          algorithm: formData.algorithm,
          hyperparameters,
          features: features.length > 0 ? features : undefined
        },
        input_schema: {
          type: 'object',
          properties: features.reduce((acc, feature) => {
            acc[feature] = { type: 'number' }
            return acc
          }, {} as Record<string, any>),
          required: features
        }
      }

      const response = await fetch('/api/ai/models', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify(modelData)
      })

      if (!response.ok) {
        const errorData = await response.json()
        throw new Error(errorData.message || 'Failed to create model')
      }

      const createdModel = await response.json()
      router.push(`/ai/models/${createdModel.id}`)
    } catch (err: any) {
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="mb-8">
          <div className="flex items-center space-x-4 mb-4">
            <Link
              href="/ai/models"
              className="p-2 rounded-lg border border-gray-300 hover:bg-gray-50"
            >
              <ArrowLeftIcon className="h-5 w-5 text-gray-600" />
            </Link>
            <div>
              <h1 className="text-3xl font-bold text-gray-900">Deploy New Model</h1>
              <p className="mt-2 text-gray-600">Configure and deploy a machine learning model</p>
            </div>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 rounded-md p-4 mb-6">
            <p className="text-red-600">{error}</p>
          </div>
        )}

        {/* Form */}
        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Basic Information</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Model Name *
                </label>
                <input
                  type="text"
                  required
                  value={formData.name}
                  onChange={(e) => setFormData({...formData, name: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="e.g., lead_scoring_model_v1"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Version *
                </label>
                <input
                  type="text"
                  required
                  value={formData.version}
                  onChange={(e) => setFormData({...formData, version: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                  placeholder="1.0.0"
                />
              </div>
            </div>

            <div className="mt-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Description
              </label>
              <textarea
                rows={3}
                value={formData.description}
                onChange={(e) => setFormData({...formData, description: e.target.value})}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="Describe what this model does..."
              />
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Model Configuration</h2>
            
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Type *
                </label>
                <select
                  required
                  value={formData.type}
                  onChange={(e) => setFormData({...formData, type: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {modelTypes.map(type => (
                    <option key={type.value} value={type.value}>{type.label}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Framework *
                </label>
                <select
                  required
                  value={formData.framework}
                  onChange={(e) => setFormData({...formData, framework: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {frameworks.map(framework => (
                    <option key={framework.value} value={framework.value}>{framework.label}</option>
                  ))}
                </select>
              </div>

              <div>
                <label className="block text-sm font-medium text-gray-700 mb-2">
                  Algorithm *
                </label>
                <select
                  required
                  value={formData.algorithm}
                  onChange={(e) => setFormData({...formData, algorithm: e.target.value})}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                >
                  {(algorithms[formData.framework as keyof typeof algorithms] || []).map(algorithm => (
                    <option key={algorithm.value} value={algorithm.value}>{algorithm.label}</option>
                  ))}
                </select>
              </div>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Features (comma-separated)
              </label>
              <input
                type="text"
                value={featuresInput}
                onChange={(e) => setFeaturesInput(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                placeholder="engagement_score, profile_score, interaction_frequency"
              />
              <p className="text-sm text-gray-500 mt-1">
                List the input features this model expects
              </p>
            </div>
          </div>

          <div className="bg-white rounded-lg shadow p-6">
            <div className="flex items-center justify-between mb-4">
              <h2 className="text-lg font-semibold text-gray-900">Hyperparameters</h2>
              <button
                type="button"
                onClick={addHyperparameter}
                className="bg-blue-600 text-white px-3 py-1 rounded-md text-sm hover:bg-blue-700"
              >
                Add Parameter
              </button>
            </div>

            <div className="space-y-3">
              {hyperparameterInputs.map((param, index) => (
                <div key={index} className="grid grid-cols-12 gap-3 items-end">
                  <div className="col-span-4">
                    <input
                      type="text"
                      value={param.key}
                      onChange={(e) => updateHyperparameter(index, 'key', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Parameter name"
                    />
                  </div>
                  <div className="col-span-4">
                    <input
                      type="text"
                      value={param.value}
                      onChange={(e) => updateHyperparameter(index, 'value', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                      placeholder="Value"
                    />
                  </div>
                  <div className="col-span-3">
                    <select
                      value={param.type}
                      onChange={(e) => updateHyperparameter(index, 'type', e.target.value)}
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500"
                    >
                      <option value="string">String</option>
                      <option value="number">Number</option>
                      <option value="boolean">Boolean</option>
                    </select>
                  </div>
                  <div className="col-span-1">
                    <button
                      type="button"
                      onClick={() => removeHyperparameter(index)}
                      className="w-full bg-red-100 text-red-600 px-2 py-2 rounded-md hover:bg-red-200"
                    >
                      ×
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Submit */}
          <div className="flex justify-end space-x-4">
            <Link
              href="/ai/models"
              className="px-4 py-2 border border-gray-300 rounded-md text-gray-700 hover:bg-gray-50"
            >
              Cancel
            </Link>
            <button
              type="submit"
              disabled={loading}
              className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 disabled:opacity-50"
            >
              {loading ? 'Deploying...' : 'Deploy Model'}
            </button>
          </div>
        </form>
      </div>
    </div>
  )
}