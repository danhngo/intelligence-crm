# Communication Hub Service Design

## Architecture Overview

The Communication Hub Service is designed as a scalable, real-time communication platform that integrates multiple channels and provides AI-powered features for message handling and routing.

### High-Level Architecture

```mermaid
graph TB
    subgraph "API Layer"
        REST[REST API]
        WS[WebSocket Server]
        Webhooks[Webhook Handler]
    end

    subgraph "Channel Adapters"
        Email[Email Adapter]
        SMS[SMS Adapter]
        Chat[Chat Adapter]
        Social[Social Media Adapter]
        Voice[Voice Adapter]
    end

    subgraph "Core Services"
        Router[Message Router]
        Queue[Message Queue]
        Processor[Message Processor]
        StateManager[State Manager]
    end

    subgraph "AI Components"
        NLP[NLP Engine]
        Generator[Response Generator]
        Classifier[Intent Classifier]
    end

    subgraph "Storage Layer"
        SQL[(PostgreSQL)]
        Redis[(Redis Cache)]
        S3[File Storage]
    end

    subgraph "External Services"
        ESP[Email Providers]
        SMSP[SMS Providers]
        SocialAPIs[Social APIs]
        VoiceP[Voice Providers]
    end

    REST --> Router
    WS --> Router
    Webhooks --> Router

    Router --> Queue
    Queue --> Processor
    Processor --> StateManager

    Email --> ESP
    SMS --> SMSP
    Social --> SocialAPIs
    Voice --> VoiceP

    Processor --> NLP
    Processor --> Generator
    Processor --> Classifier

    StateManager --> SQL
    StateManager --> Redis
    Processor --> S3
```

## Component Details

### 1. API Layer
- **REST API**
  - Message CRUD operations
  - Channel management
  - Configuration endpoints
  - Analytics queries
- **WebSocket Server**
  - Real-time message delivery
  - Presence management
  - Typing indicators
  - Status updates
- **Webhook Handler**
  - Incoming webhooks
  - Event notifications
  - Integration callbacks

### 2. Channel Adapters
- **Email Adapter**
  - SMTP/IMAP handling
  - Email parsing
  - Attachment processing
  - Threading management
- **SMS Adapter**
  - Provider integration
  - Number pooling
  - Status tracking
  - Rate limiting
- **Chat Adapter**
  - WebSocket management
  - Session handling
  - Presence tracking
  - Typing indicators
- **Social Media Adapter**
  - Platform-specific APIs
  - Rate limit management
  - Media handling
  - Account management
- **Voice Adapter**
  - Call handling
  - Transcription
  - Recording management
  - Quality monitoring

### 3. Core Services
- **Message Router**
  - Channel selection
  - Load balancing
  - Priority routing
  - Rule evaluation
- **Message Queue**
  - Priority queues
  - Dead letter handling
  - Retry mechanisms
  - Rate limiting
- **Message Processor**
  - Content processing
  - Format conversion
  - Attachment handling
  - Metadata enrichment
- **State Manager**
  - Session management
  - Conversation tracking
  - User state
  - Channel state

### 4. AI Components
- **NLP Engine**
  - Language detection
  - Sentiment analysis
  - Entity extraction
  - Topic modeling
- **Response Generator**
  - Template matching
  - Context-aware responses
  - Personalization
  - Multi-language support
- **Intent Classifier**
  - Intent detection
  - Priority assessment
  - Category assignment
  - Routing suggestions

## Data Models

### Campaign Model
```typescript
interface Campaign {
    id: string;                     // UUID
    name: string;                   // Campaign name
    description?: string;           // Campaign description
    type: CampaignType;            // EMAIL | SMS | WHATSAPP | MULTI_CHANNEL
    status: CampaignStatus;        // DRAFT | SCHEDULED | RUNNING | PAUSED | COMPLETED | CANCELLED
    
    // Email-specific fields
    subject_line?: string;          // Email subject
    sender_name?: string;           // Sender display name
    sender_email?: string;          // Sender email address
    
    // Targeting
    target_segments: string[];      // Contact segment IDs
    contact_list_ids: string[];     // Contact list IDs
    
    // Content
    template_id?: string;           // Email template ID
    content?: string;               // Campaign content
    
    // Tracking settings
    tracking_enabled: boolean;      // Overall tracking
    open_tracking_enabled: boolean; // Email open tracking
    click_tracking_enabled: boolean; // Link click tracking
    unsubscribe_enabled: boolean;   // Unsubscribe links
    
    // Scheduling
    scheduled_at?: Date;            // Scheduled send time
    started_at?: Date;              // Actual start time
    completed_at?: Date;            // Completion time
    
    // Metadata
    tenant_id: string;              // Tenant isolation
    created_by: string;             // Creator user ID
    metadata: any;                  // Additional data
    created_at: Date;
    updated_at: Date;
}

interface CampaignMessage {
    id: string;                     // UUID
    campaign_id: string;            // Campaign reference
    contact_id: string;             // Target contact
    channel_type: ChannelType;      // Delivery channel
    
    // Message content
    subject?: string;               // Email subject (personalized)
    content: string;                // Message content
    html_content?: string;          // HTML version
    
    // Delivery tracking
    status: MessageStatus;          // PENDING | SENT | DELIVERED | FAILED | BOUNCED
    sent_at?: Date;                 // Send timestamp
    delivered_at?: Date;            // Delivery confirmation
    failed_at?: Date;               // Failure timestamp
    failure_reason?: string;        // Error details
    
    // External references
    external_message_id?: string;   // Provider message ID
    
    metadata: any;
    created_at: Date;
    updated_at: Date;
}

interface EmailTrackingEvent {
    id: string;                     // UUID
    campaign_id: string;            // Campaign reference
    message_id: string;             // Message reference
    recipient_email: string;        // Recipient identifier
    
    event_type: TrackingEventType;  // OPEN | CLICK | BOUNCE | UNSUBSCRIBE | COMPLAINT
    
    // Event details
    ip_address?: string;            // Client IP
    user_agent?: string;            // Client user agent
    url?: string;                   // Clicked URL (for CLICK events)
    
    metadata: any;                  // Additional event data
    created_at: Date;               // Event timestamp
}

interface EmailTemplate {
    id: string;                     // UUID
    name: string;                   // Template name
    description?: string;           // Template description
    subject: string;                // Email subject template
    
    // Content
    html_content: string;           // HTML email content
    text_content?: string;          // Plain text version
    variables: string[];            // Available variables
    
    // Organization
    category?: string;              // Template category
    is_active: boolean;             // Template status
    
    // Metadata
    tenant_id: string;
    created_by: string;
    metadata: any;
    created_at: Date;
    updated_at: Date;
}

### Message Model
```typescript
interface Message {
    id: string;                 // UUID
    conversationId: string;     // Thread/conversation ID
    channelId: string;          // Channel identifier
    type: MessageType;          // Message classification
    direction: Direction;       // INBOUND | OUTBOUND
    content: {
        text: string;           // Message text
        html?: string;          // HTML content
        attachments: Attachment[]; // Files/media
        metadata: any;          // Channel-specific data
    };
    sender: {
        id: string;            // Sender identifier
        type: SenderType;      // USER | SYSTEM | BOT
        metadata: any;         // Sender information
    };
    recipient: {
        id: string;           // Recipient identifier
        type: RecipientType;  // USER | GROUP | CHANNEL
        metadata: any;        // Recipient information
    };
    status: MessageStatus;    // Delivery status
    priority: Priority;       // Message priority
    tags: string[];          // Classification tags
    sentiment?: {
        score: number;       // -1 to 1
        confidence: number;  // 0 to 1
        labels: string[];   // Emotion labels
    };
    intent?: {
        name: string;       // Classified intent
        confidence: number; // Confidence score
        entities: Entity[]; // Extracted entities
    };
    createdAt: Date;       // Creation timestamp
    updatedAt: Date;       // Last update
    metadata: any;         // Additional data
}

interface Conversation {
    id: string;           // Conversation ID
    channelId: string;    // Primary channel
    participants: string[]; // Participant IDs
    status: ConversationStatus; // Active/Closed
    lastMessage: Message;  // Latest message
    metadata: {
        subject?: string;  // Topic/subject
        category?: string; // Classification
        priority: Priority; // Conversation priority
        tags: string[];    // Organization tags
        customFields: any; // Additional fields
    };
    metrics: {
        messageCount: number; // Total messages
        responseTime: number; // Avg response time
        resolution?: {
            status: ResolutionStatus;
            time: number;    // Time to resolve
        };
    };
    createdAt: Date;
    updatedAt: Date;
}
```

### Channel Model
```typescript
interface Channel {
    id: string;           // Channel identifier
    type: ChannelType;    // Channel type
    provider: string;     // Service provider
    config: {
        credentials: {    // Auth credentials
            encrypted: string;
        };
        settings: {      // Channel settings
            rateLimit: number;
            features: string[];
            templates: Template[];
        };
        routing: {       // Routing rules
            rules: Rule[];
            default: string;
        };
    };
    status: {
        isActive: boolean;
        health: HealthStatus;
        lastCheck: Date;
        metrics: {
            messageCount: number;
            errorRate: number;
            responseTime: number;
        };
    };
    metadata: any;
}
```

## API Specifications

### REST Endpoints
```yaml
# Campaign Management
/api/v1/campaigns:
  post:
    summary: Create campaign
    request:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CampaignCreate'
    response:
      201:
        $ref: '#/components/schemas/Campaign'

  get:
    summary: List campaigns
    parameters:
      - name: status
        in: query
        type: string
      - name: campaign_type
        in: query
        type: string
      - name: search
        in: query
        type: string
    response:
      200:
        type: object
        properties:
          items:
            type: array
            items:
              $ref: '#/components/schemas/Campaign'

/api/v1/campaigns/{id}:
  get:
    summary: Get campaign details
  put:
    summary: Update campaign
  delete:
    summary: Delete campaign

/api/v1/campaigns/{id}/start:
  post:
    summary: Start campaign execution

/api/v1/campaigns/{id}/pause:
  post:
    summary: Pause running campaign

/api/v1/campaigns/{id}/stop:
  post:
    summary: Stop campaign

/api/v1/campaigns/{id}/stats:
  get:
    summary: Get campaign statistics
    response:
      200:
        $ref: '#/components/schemas/CampaignStats'

/api/v1/campaigns/{id}/events:
  get:
    summary: Get campaign tracking events
    parameters:
      - name: event_type
        in: query
        type: string
    response:
      200:
        type: array
        items:
          $ref: '#/components/schemas/EmailTrackingEvent'

# Email Template Management
/api/v1/templates:
  post:
    summary: Create email template
  get:
    summary: List email templates
    parameters:
      - name: category
        in: query
        type: string
      - name: is_active
        in: query
        type: boolean

/api/v1/templates/{id}:
  get:
    summary: Get template details
  put:
    summary: Update template
  delete:
    summary: Delete template

# Email Tracking Endpoints
/api/v1/tracking/open:
  get:
    summary: Track email open (pixel endpoint)
    parameters:
      - name: message_id
        in: query
        type: string
        required: true

/api/v1/tracking/click:
  get:
    summary: Track link click and redirect
    parameters:
      - name: message_id
        in: query
        type: string
        required: true
      - name: url
        in: query
        type: string
        required: true

# Contact Segments
/api/v1/segments:
  get:
    summary: List contact segments
    response:
      200:
        type: array
        items:
          $ref: '#/components/schemas/ContactSegment'

# Legacy Message Endpoints
/api/v1/messages:
  post:
    summary: Send message
    request:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/SendMessageRequest'
    response:
      201:
        $ref: '#/components/schemas/Message'

  get:
    summary: List messages
    parameters:
      - name: conversationId
        in: query
        type: string
      - name: channelId
        in: query
        type: string
    response:
      200:
        type: array
        items:
          $ref: '#/components/schemas/Message'

/api/v1/conversations:
  post:
    summary: Create conversation
    request:
      content:
        application/json:
          schema:
            $ref: '#/components/schemas/CreateConversationRequest'
    response:
      201:
        $ref: '#/components/schemas/Conversation'

/api/v1/channels:
  get:
    summary: List channels
    response:
      200:
        type: array
        items:
          $ref: '#/components/schemas/Channel'
```

### WebSocket Events
```typescript
interface WebSocketEvents {
    // Client -> Server
    'message.send': {
        content: string;
        conversationId: string;
    };
    'typing.start': {
        conversationId: string;
    };
    'typing.stop': {
        conversationId: string;
    };
    'presence.update': {
        status: PresenceStatus;
    };

    // Server -> Client
    'message.received': Message;
    'message.updated': Message;
    'conversation.updated': Conversation;
    'typing.indicator': {
        conversationId: string;
        userId: string;
        isTyping: boolean;
    };
    'presence.changed': {
        userId: string;
        status: PresenceStatus;
    };
}
```

## Integration Patterns

### 1. Campaign Execution Flow
```mermaid
sequenceDiagram
    participant U as User
    participant API as Campaign API
    participant CS as Campaign Service
    participant ES as Email Service
    participant DB as Database
    participant EP as Email Provider
    participant R as Recipient

    U->>API: Start Campaign
    API->>CS: Execute Campaign
    CS->>DB: Get Target Contacts
    DB-->>CS: Contact List
    
    loop For Each Contact
        CS->>ES: Send Email
        ES->>EP: Deliver Message
        EP->>R: Email Delivery
        EP-->>ES: Delivery Status
        ES->>DB: Store Message Record
        
        R->>API: Open Email (Pixel)
        API->>DB: Record Open Event
        
        R->>API: Click Link
        API->>DB: Record Click Event
        API-->>R: Redirect to URL
    end
    
    CS->>DB: Update Campaign Status
    CS-->>API: Campaign Complete
```

### 2. Real-time Email Tracking
```mermaid
sequenceDiagram
    participant R as Recipient
    participant CDN as CDN/Proxy
    participant API as Tracking API
    participant DB as Database
    participant WS as WebSocket
    participant U as User Dashboard

    R->>CDN: Load Email (with tracking pixel)
    CDN->>API: GET /tracking/open?message_id=xxx
    API->>DB: Record Open Event
    API->>WS: Broadcast Event
    WS->>U: Real-time Update
    API-->>CDN: Return 1x1 Pixel
    CDN-->>R: Serve Pixel

    R->>CDN: Click Tracked Link
    CDN->>API: GET /tracking/click?message_id=xxx&url=yyy
    API->>DB: Record Click Event
    API->>WS: Broadcast Event
    WS->>U: Real-time Update
    API-->>CDN: 302 Redirect
    CDN-->>R: Redirect to Target URL
```

### 3. Message Flow (Legacy)
```mermaid
sequenceDiagram
    participant C as Client
    participant API as API Gateway
    participant R as Router
    participant Q as Queue
    participant P as Processor
    participant DB as Database
    participant AI as AI Service

    C->>API: Send Message
    API->>R: Route Message
    R->>Q: Queue Message
    Q->>P: Process Message
    P->>AI: Analyze Content
    AI-->>P: Analysis Results
    P->>DB: Store Message
    P-->>C: Delivery Status
```

### 2. Channel Integration
```mermaid
sequenceDiagram
    participant E as External Service
    participant A as Channel Adapter
    participant R as Router
    participant P as Processor
    participant S as State Manager

    E->>A: Incoming Message
    A->>R: Normalized Message
    R->>P: Route Message
    P->>S: Update State
    S-->>P: Current State
    P-->>A: Processing Result
    A-->>E: Channel Response
```

## Security Considerations

### 1. Authentication & Authorization
- OAuth2/OIDC integration
- JWT token validation
- Role-based access control
- API key management
- Channel credentials encryption

### 2. Data Protection
- End-to-end encryption
- Data encryption at rest
- PII handling
- Data retention policies
- Secure file storage

### 3. Network Security
- TLS/SSL enforcement
- Rate limiting
- DDoS protection
- IP whitelisting
- WebSocket security

## Monitoring & Observability

### 1. Metrics
- Message volume
- Response times
- Error rates
- Channel health
- Queue depth
- Cache hit rates
- AI performance

### 2. Logging
- Request logging
- Error logging
- Audit logging
- Performance logging
- Security events
- Integration status

### 3. Alerts
- Service health
- Error thresholds
- Performance degradation
- Security incidents
- Integration failures
- Resource utilization

## Deployment Strategy

### 1. Infrastructure
- Kubernetes deployment
- Auto-scaling configuration
- Load balancer setup
- Database clustering
- Cache distribution
- Storage configuration

### 2. High Availability
- Multi-zone deployment
- Service redundancy
- Database replication
- Queue mirroring
- Failover handling
- Disaster recovery

### 3. Performance
- CDN integration
- Cache strategies
- Connection pooling
- Query optimization
- Resource allocation
- Batch processing
