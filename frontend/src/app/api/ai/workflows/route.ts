import { NextRequest, NextResponse } from 'next/server'

const AI_ORCHESTRATION_URL = process.env.AI_ORCHESTRATION_URL || 'http://localhost:8005'

export async function GET(request: NextRequest) {
  const { searchParams } = new URL(request.url)
  const skip = searchParams.get('skip') || '0'
  const limit = searchParams.get('limit') || '20'
  
  try {
    const response = await fetch(
      `${AI_ORCHESTRATION_URL}/api/v1/workflows/?skip=${skip}&limit=${limit}`
    )
    
    if (!response.ok) {
      throw new Error(`AI service error: ${response.status}`)
    }
    
    const workflows = await response.json()
    return NextResponse.json(workflows)
  } catch (error) {
    console.error('Error fetching workflows:', error)
    return NextResponse.json(
      { error: 'Failed to fetch workflows' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${AI_ORCHESTRATION_URL}/api/v1/workflows/`, {
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
    
    const workflow = await response.json()
    return NextResponse.json(workflow, { status: 201 })
  } catch (error) {
    console.error('Error creating workflow:', error)
    return NextResponse.json(
      { error: 'Failed to create workflow' },
      { status: 500 }
    )
  }
}