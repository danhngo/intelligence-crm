'use client'

import { useState } from 'react'
import { useRouter } from 'next/navigation'
import { useCreateCampaign, useContactSegments, useEmailTemplates } from '@/hooks/campaigns'
import Sidebar from '@/components/layout/sidebar'
import { CampaignCreate, CampaignType } from '@/types/api'
import { 
  ArrowLeftIcon,
  InformationCircleIcon
} from '@heroicons/react/24/outline'
import Link from 'next/link'

export default function NewCampaignPage() {
  const router = useRouter()
  const [formData, setFormData] = useState<CampaignCreate>({
    name: '',
    description: '',
    type: 'email',
    subject_line: '',
    sender_name: '',
    sender_email: '',
    target_segments: [],
    contact_list_ids: [],
    template_id: undefined,
    tracking_enabled: true,
    click_tracking_enabled: true,
    open_tracking_enabled: true,
    unsubscribe_enabled: true,
  })
  
  const createCampaign = useCreateCampaign()
  const { data: segments = [] } = useContactSegments()
  const { data: templates = [] } = useEmailTemplates({ is_active: true })

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      const campaign = await createCampaign.mutateAsync(formData)
      router.push(`/campaigns/${campaign.id}`)
    } catch (error) {
      console.error('Failed to create campaign:', error)
    }
  }

  const handleInputChange = (field: keyof CampaignCreate, value: any) => {
    setFormData(prev => ({ ...prev, [field]: value }))
  }

  const handleSegmentChange = (segmentId: string, checked: boolean) => {
    setFormData(prev => ({
      ...prev,
      target_segments: checked 
        ? [...prev.target_segments || [], segmentId]
        : (prev.target_segments || []).filter(id => id !== segmentId)
    }))
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Sidebar />
      
      <div className="md:pl-64">
        <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Header */}
          <div className="mb-8">
            <Link
              href="/campaigns"
              className="inline-flex items-center text-sm text-gray-500 hover:text-gray-700 mb-4"
            >
              <ArrowLeftIcon className="h-4 w-4 mr-1" />
              Back to Campaigns
            </Link>
            <h1 className="text-2xl font-bold text-gray-900">Create New Campaign</h1>
            <p className="text-gray-600">Set up your email marketing campaign</p>
          </div>

          {/* Form */}
          <form onSubmit={handleSubmit} className="space-y-8">
            {/* Basic Information */}
            <div className="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
              <div className="md:grid md:grid-cols-3 md:gap-6">
                <div className="md:col-span-1">
                  <h3 className="text-lg font-medium leading-6 text-gray-900">Basic Information</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    General details about your campaign.
                  </p>
                </div>
                <div className="mt-5 md:mt-0 md:col-span-2">
                  <div className="grid grid-cols-1 gap-6">
                    <div>
                      <label htmlFor="name" className="block text-sm font-medium text-gray-700">
                        Campaign Name *
                      </label>
                      <input
                        type="text"
                        name="name"
                        id="name"
                        required
                        className="mt-1 focus:ring-primary-500 focus:border-primary-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                        value={formData.name}
                        onChange={(e) => handleInputChange('name', e.target.value)}
                        placeholder="Enter campaign name"
                      />
                    </div>

                    <div>
                      <label htmlFor="description" className="block text-sm font-medium text-gray-700">
                        Description
                      </label>
                      <textarea
                        id="description"
                        name="description"
                        rows={3}
                        className="mt-1 focus:ring-primary-500 focus:border-primary-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                        value={formData.description}
                        onChange={(e) => handleInputChange('description', e.target.value)}
                        placeholder="Describe your campaign"
                      />
                    </div>

                    <div>
                      <label htmlFor="type" className="block text-sm font-medium text-gray-700">
                        Campaign Type *
                      </label>
                      <select
                        id="type"
                        name="type"
                        className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                        value={formData.type}
                        onChange={(e) => handleInputChange('type', e.target.value as CampaignType)}
                      >
                        <option value="email">Email</option>
                        <option value="sms">SMS</option>
                        <option value="whatsapp">WhatsApp</option>
                        <option value="multi_channel">Multi-Channel</option>
                      </select>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Email Settings (only show for email campaigns) */}
            {formData.type === 'email' && (
              <div className="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
                <div className="md:grid md:grid-cols-3 md:gap-6">
                  <div className="md:col-span-1">
                    <h3 className="text-lg font-medium leading-6 text-gray-900">Email Settings</h3>
                    <p className="mt-1 text-sm text-gray-500">
                      Configure your email content and sender details.
                    </p>
                  </div>
                  <div className="mt-5 md:mt-0 md:col-span-2">
                    <div className="grid grid-cols-1 gap-6">
                      <div>
                        <label htmlFor="subject_line" className="block text-sm font-medium text-gray-700">
                          Subject Line *
                        </label>
                        <input
                          type="text"
                          name="subject_line"
                          id="subject_line"
                          required
                          className="mt-1 focus:ring-primary-500 focus:border-primary-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                          value={formData.subject_line}
                          onChange={(e) => handleInputChange('subject_line', e.target.value)}
                          placeholder="Enter email subject line"
                        />
                      </div>

                      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
                        <div>
                          <label htmlFor="sender_name" className="block text-sm font-medium text-gray-700">
                            Sender Name
                          </label>
                          <input
                            type="text"
                            name="sender_name"
                            id="sender_name"
                            className="mt-1 focus:ring-primary-500 focus:border-primary-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                            value={formData.sender_name}
                            onChange={(e) => handleInputChange('sender_name', e.target.value)}
                            placeholder="Your Name"
                          />
                        </div>

                        <div>
                          <label htmlFor="sender_email" className="block text-sm font-medium text-gray-700">
                            Sender Email
                          </label>
                          <input
                            type="email"
                            name="sender_email"
                            id="sender_email"
                            className="mt-1 focus:ring-primary-500 focus:border-primary-500 block w-full shadow-sm sm:text-sm border-gray-300 rounded-md"
                            value={formData.sender_email}
                            onChange={(e) => handleInputChange('sender_email', e.target.value)}
                            placeholder="your@example.com"
                          />
                        </div>
                      </div>

                      <div>
                        <label htmlFor="template_id" className="block text-sm font-medium text-gray-700">
                          Email Template
                        </label>
                        <select
                          id="template_id"
                          name="template_id"
                          className="mt-1 block w-full py-2 px-3 border border-gray-300 bg-white rounded-md shadow-sm focus:outline-none focus:ring-primary-500 focus:border-primary-500 sm:text-sm"
                          value={formData.template_id || ''}
                          onChange={(e) => handleInputChange('template_id', e.target.value || undefined)}
                        >
                          <option value="">Select a template (optional)</option>
                          {templates.map((template) => (
                            <option key={template.id} value={template.id}>
                              {template.name}
                            </option>
                          ))}
                        </select>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            )}

            {/* Audience */}
            <div className="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
              <div className="md:grid md:grid-cols-3 md:gap-6">
                <div className="md:col-span-1">
                  <h3 className="text-lg font-medium leading-6 text-gray-900">Audience</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    Choose who will receive your campaign.
                  </p>
                </div>
                <div className="mt-5 md:mt-0 md:col-span-2">
                  <div>
                    <label className="text-base font-medium text-gray-900">Target Segments</label>
                    <p className="text-sm leading-5 text-gray-500">Select contact segments to target</p>
                    <fieldset className="mt-4">
                      <legend className="sr-only">Contact Segments</legend>
                      <div className="space-y-4">
                        {segments.map((segment) => (
                          <div key={segment.id} className="flex items-center">
                            <input
                              id={`segment-${segment.id}`}
                              name="target_segments"
                              type="checkbox"
                              className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                              checked={formData.target_segments?.includes(segment.id) || false}
                              onChange={(e) => handleSegmentChange(segment.id, e.target.checked)}
                            />
                            <div className="ml-3">
                              <label htmlFor={`segment-${segment.id}`} className="font-medium text-gray-700">
                                {segment.name}
                              </label>
                              <p className="text-gray-500 text-sm">
                                {segment.description} ({segment.contact_count} contacts)
                              </p>
                            </div>
                          </div>
                        ))}
                      </div>
                    </fieldset>
                  </div>
                </div>
              </div>
            </div>

            {/* Tracking Settings */}
            <div className="bg-white shadow px-4 py-5 sm:rounded-lg sm:p-6">
              <div className="md:grid md:grid-cols-3 md:gap-6">
                <div className="md:col-span-1">
                  <h3 className="text-lg font-medium leading-6 text-gray-900">Tracking Settings</h3>
                  <p className="mt-1 text-sm text-gray-500">
                    Configure email tracking and analytics.
                  </p>
                </div>
                <div className="mt-5 md:mt-0 md:col-span-2">
                  <div className="space-y-4">
                    <div className="flex items-start">
                      <div className="flex items-center h-5">
                        <input
                          id="tracking_enabled"
                          name="tracking_enabled"
                          type="checkbox"
                          className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                          checked={formData.tracking_enabled}
                          onChange={(e) => handleInputChange('tracking_enabled', e.target.checked)}
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label htmlFor="tracking_enabled" className="font-medium text-gray-700">
                          Enable tracking
                        </label>
                        <p className="text-gray-500">Track overall campaign performance and engagement.</p>
                      </div>
                    </div>

                    <div className="flex items-start">
                      <div className="flex items-center h-5">
                        <input
                          id="open_tracking_enabled"
                          name="open_tracking_enabled"
                          type="checkbox"
                          className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                          checked={formData.open_tracking_enabled}
                          onChange={(e) => handleInputChange('open_tracking_enabled', e.target.checked)}
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label htmlFor="open_tracking_enabled" className="font-medium text-gray-700">
                          Track email opens
                        </label>
                        <p className="text-gray-500">Track when recipients open your emails.</p>
                      </div>
                    </div>

                    <div className="flex items-start">
                      <div className="flex items-center h-5">
                        <input
                          id="click_tracking_enabled"
                          name="click_tracking_enabled"
                          type="checkbox"
                          className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                          checked={formData.click_tracking_enabled}
                          onChange={(e) => handleInputChange('click_tracking_enabled', e.target.checked)}
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label htmlFor="click_tracking_enabled" className="font-medium text-gray-700">
                          Track link clicks
                        </label>
                        <p className="text-gray-500">Track when recipients click links in your emails.</p>
                      </div>
                    </div>

                    <div className="flex items-start">
                      <div className="flex items-center h-5">
                        <input
                          id="unsubscribe_enabled"
                          name="unsubscribe_enabled"
                          type="checkbox"
                          className="focus:ring-primary-500 h-4 w-4 text-primary-600 border-gray-300 rounded"
                          checked={formData.unsubscribe_enabled}
                          onChange={(e) => handleInputChange('unsubscribe_enabled', e.target.checked)}
                        />
                      </div>
                      <div className="ml-3 text-sm">
                        <label htmlFor="unsubscribe_enabled" className="font-medium text-gray-700">
                          Include unsubscribe link
                        </label>
                        <p className="text-gray-500">Add an unsubscribe link to comply with email regulations.</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>

            {/* Form Actions */}
            <div className="flex justify-end space-x-3">
              <Link
                href="/campaigns"
                className="bg-white py-2 px-4 border border-gray-300 rounded-md shadow-sm text-sm font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500"
              >
                Cancel
              </Link>
              <button
                type="submit"
                disabled={createCampaign.isLoading}
                className="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-primary-600 hover:bg-primary-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-primary-500 disabled:opacity-50"
              >
                {createCampaign.isLoading ? 'Creating...' : 'Create Campaign'}
              </button>
            </div>
          </form>
        </div>
      </div>
    </div>
  )
}
