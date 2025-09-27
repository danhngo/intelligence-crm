import { NextRequest, NextResponse } from 'next/server'

const AI_ORCHESTRATION_URL = process.env.AI_ORCHESTRATION_URL || 'http://localhost:8005'

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const skip = searchParams.get('skip') || '0'
  const limit = searchParams.get('limit') || '20'
  
  try {
    const response = await fetch(
      `${AI_ORCHESTRATION_URL}/api/v1/training/?skip=${skip}&limit=${limit}`
    )
    
    if (!response.ok) {
      throw new Error(`AI service error: ${response.status}`)
    }
    
    const trainingJobs = await response.json()
    return NextResponse.json(trainingJobs)
  } catch (error) {
    console.error('Error fetching training jobs:', error)
    return NextResponse.json(
      { error: 'Failed to fetch training jobs' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${AI_ORCHESTRATION_URL}/api/v1/training/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(body)
    })
    
    if (!response.ok) {
      const errorData = await response.json()
      return NextResponse.json(errorData, { status: response.status })
    }
    
    const trainingJob = await response.json()
    return NextResponse.json(trainingJob, { status: 202 })
  } catch (error) {
    console.error('Error creating training job:', error)
    return NextResponse.json(
      { error: 'Failed to create training job' },
      { status: 500 }
    )
  }
}