import { NextRequest, NextResponse } from 'next/server'
import http from 'http'

// Disable static generation for this API route
export const dynamic = 'force-dynamic'

const SERVICES = [
  { name: 'User Management API', url: 'http://user-management-api:8000/health' },
  { name: 'CRM Core API', url: 'http://crm-core-api:8000/health' },
  { name: 'Workflow Engine API', url: 'http://workflow-engine-api:8000/health' },
  { name: 'Communication Hub API', url: 'http://communication-hub-api:8000/health' },
  { name: 'Analytics Service API', url: 'http://analytics-service-api:8000/health' },
  { name: 'AI Orchestration API', url: 'http://ai-orchestration-api:8000/health' }
]

function httpGet(url: string): Promise<{ data: any, responseTime: number }> {
  return new Promise((resolve, reject) => {
    const startTime = Date.now()
    const request = http.get(url, (response) => {
      let data = ''
      
      response.on('data', (chunk) => {
        data += chunk
      })
      
      response.on('end', () => {
        const responseTime = Date.now() - startTime
        try {
          const jsonData = JSON.parse(data)
          resolve({ data: jsonData, responseTime })
        } catch {
          resolve({ data: { status: 'healthy' }, responseTime })
        }
      })
    })
    
    request.on('error', (error) => {
      const responseTime = Date.now() - startTime
      reject({ error, responseTime })
    })
    
    request.setTimeout(5000, () => {
      request.destroy()
      reject({ error: new Error('Timeout'), responseTime: 5000 })
    })
  })
}

export async function GET() {
  const healthChecks = await Promise.all(
    SERVICES.map(async (service) => {
      try {
        const { data, responseTime } = await httpGet(service.url)
        
        return {
          name: service.name,
          status: 'healthy' as const,
          responseTime,
          lastCheck: new Date().toISOString(),
          details: data
        }
      } catch ({ error, responseTime }: any) {
        return {
          name: service.name,
          status: 'unhealthy' as const,
          responseTime: responseTime || 0,
          lastCheck: new Date().toISOString(),
          error: error instanceof Error ? error.message : 'Connection failed'
        }
      }
    })
  )

  return NextResponse.json({
    services: healthChecks,
    timestamp: new Date().toISOString(),
    summary: {
      total: healthChecks.length,
      healthy: healthChecks.filter(s => s.status === 'healthy').length,
      unhealthy: healthChecks.filter(s => s.status === 'unhealthy').length
    }
  })
}
