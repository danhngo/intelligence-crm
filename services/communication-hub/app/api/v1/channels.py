"""Channels API endpoints."""

from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from app.core.database import get_db
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()


class Channel(BaseModel):
    """Channel model."""
    name: str
    type: str  # email, sms, slack, webhook, etc.
    enabled: bool
    config: Dict[str, Any]
    description: str = ""


@router.get("/", response_model=List[Channel])
async def list_channels(
    db: AsyncSession = Depends(get_db)
) -> List[Channel]:
    """List all available communication channels."""
    # Mock implementation
    return [
        Channel(
            name="email",
            type="email",
            enabled=True,
            config={"provider": "sendgrid", "from_email": "noreply@crm.com"},
            description="Email communication channel"
        ),
        Channel(
            name="sms",
            type="sms",
            enabled=True,
            config={"provider": "twilio", "from_number": "+1234567890"},
            description="SMS communication channel"
        ),
        Channel(
            name="slack",
            type="slack",
            enabled=False,
            config={"webhook_url": "", "channel": "#notifications"},
            description="Slack communication channel"
        ),
        Channel(
            name="webhook",
            type="webhook",
            enabled=True,
            config={"url": "", "headers": {}},
            description="Webhook communication channel"
        )
    ]


@router.get("/{channel_name}")
async def get_channel(
    channel_name: str,
    db: AsyncSession = Depends(get_db)
) -> Channel:
    """Get specific channel configuration."""
    # Mock implementation
    channels = {
        "email": Channel(
            name="email",
            type="email",
            enabled=True,
            config={"provider": "sendgrid", "from_email": "noreply@crm.com"},
            description="Email communication channel"
        ),
        "sms": Channel(
            name="sms",
            type="sms",
            enabled=True,
            config={"provider": "twilio", "from_number": "+1234567890"},
            description="SMS communication channel"
        )
    }
    
    if channel_name not in channels:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Channel not found")
    
    return channels[channel_name]


@router.post("/{channel_name}/test")
async def test_channel(
    channel_name: str,
    test_config: Dict[str, Any],
    db: AsyncSession = Depends(get_db)
) -> Dict[str, Any]:
    """Test a communication channel."""
    # Mock implementation
    return {
        "channel": channel_name,
        "status": "success",
        "message": f"Test message sent successfully via {channel_name}",
        "test_id": f"test-{channel_name}-123"
    }
