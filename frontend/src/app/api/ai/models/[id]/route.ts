import { NextRequest, NextResponse } from 'next/server'

const AI_ORCHESTRATION_URL = process.env.AI_ORCHESTRATION_URL || 'http://localhost:8005'

export async function GET(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const response = await fetch(`${AI_ORCHESTRATION_URL}/api/v1/models/${params.id}`)
    
    if (!response.ok) {
      if (response.status === 404) {
        return NextResponse.json({ error: 'Model not found' }, { status: 404 })
      }
      throw new Error(`AI service error: ${response.status}`)
    }
    
    const model = await response.json()
    return NextResponse.json(model)
  } catch (error) {
    console.error('Error fetching model:', error)
    return NextResponse.json(
      { error: 'Failed to fetch model' },
      { status: 500 }
    )
  }
}

export async function PUT(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const body = await request.json()
    
    const response = await fetch(`${AI_ORCHESTRATION_URL}/api/v1/models/${params.id}`, {
      method: 'PUT',
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
    return NextResponse.json(model)
  } catch (error) {
    console.error('Error updating model:', error)
    return NextResponse.json(
      { error: 'Failed to update model' },
      { status: 500 }
    )
  }
}

export async function DELETE(
  request: NextRequest,
  { params }: { params: { id: string } }
) {
  try {
    const response = await fetch(`${AI_ORCHESTRATION_URL}/api/v1/models/${params.id}`, {
      method: 'DELETE'
    })
    
    if (!response.ok) {
      if (response.status === 404) {
        return NextResponse.json({ error: 'Model not found' }, { status: 404 })
      }
      throw new Error(`AI service error: ${response.status}`)
    }
    
    return NextResponse.json({}, { status: 204 })
  } catch (error) {
    console.error('Error deleting model:', error)
    return NextResponse.json(
      { error: 'Failed to delete model' },
      { status: 500 }
    )
  }
}