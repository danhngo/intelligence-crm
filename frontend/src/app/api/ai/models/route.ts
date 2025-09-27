import { NextRequest, NextResponse } from 'next/server'

const AI_ORCHESTRATION_URL = process.env.AI_ORCHESTRATION_URL || 'http://localhost:8005'

export async function GET() {
  try {
    const response = await fetch(`${AI_ORCHESTRATION_URL}/api/v1/models/`)
    
    if (!response.ok) {
      throw new Error(`AI service error: ${response.status}`)
    }
    
    const models = await response.json()
    return NextResponse.json(models)
  } catch (error) {
    console.error('Error fetching models:', error)
    return NextResponse.json(
      { error: 'Failed to fetch models' },
      { status: 500 }
    )
  }
}

export async function POST(request: NextRequest) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${AI_ORCHESTRATION_URL}/api/v1/models/`, {
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
    
    const model = await response.json()
    return NextResponse.json(model, { status: 201 })
  } catch (error) {
    console.error('Error creating model:', error)
    return NextResponse.json(
      { error: 'Failed to create model' },
      { status: 500 }
    )
  }
}