# Intelligence CRM Frontend

A modern TypeScript React frontend for the Intelligence CRM Platform built with Next.js 14, TypeScript, and Tailwind CSS.

## Features

🚀 **Modern Tech Stack**
- Next.js 14 with App Router
- TypeScript for type safety
- Tailwind CSS for styling
- React Query for data fetching
- Framer Motion for animations

📊 **CRM Functionality**
- Interactive dashboard with real-time metrics
- Contact management with CRUD operations
- Analytics and reporting
- Workflow automation interface
- Real-time messaging system
- User authentication and authorization

🎨 **UI/UX**
- Responsive design for all devices
- Modern, clean interface
- Loading states and error handling
- Toast notifications
- Dark mode support (coming soon)

## Getting Started

### Prerequisites

- Node.js 18+ and npm
- Backend services running (Analytics, CRM, User Management, etc.)

### Installation

```bash
# Install dependencies
npm install

# Copy environment variables
cp .env.example .env.local

# Update environment variables in .env.local
```

### Environment Variables

Create a `.env.local` file with the following variables:

```env
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000
NEXT_PUBLIC_CRM_API_URL=http://localhost:8001
NEXT_PUBLIC_USER_API_URL=http://localhost:8002
NEXT_PUBLIC_WORKFLOW_API_URL=http://localhost:8003
NEXT_PUBLIC_AI_API_URL=http://localhost:8004
```

### Development

```bash
# Start development server
npm run dev

# Open http://localhost:3000
```

### Production Build

```bash
# Build for production
npm run build

# Start production server
npm start
```

### Docker Deployment

```bash
# Build Docker image
docker build -t intelligence-crm-frontend .

# Run with Docker Compose
docker-compose up -d
```

## Project Structure

```
src/
├── app/                  # Next.js 14 App Router
│   ├── dashboard/        # Dashboard pages
│   ├── contacts/         # Contact management
│   ├── analytics/        # Analytics pages
│   ├── workflows/        # Workflow pages
│   ├── login/           # Authentication
│   └── layout.tsx       # Root layout
├── components/          # Reusable components
│   ├── auth/           # Authentication components
│   ├── layout/         # Layout components
│   ├── ui/             # UI components
│   └── forms/          # Form components
├── hooks/              # Custom React hooks
│   └── api.ts          # API hooks with React Query
├── lib/                # Utility libraries
│   └── api-client.ts   # API client configuration
├── types/              # TypeScript type definitions
│   └── api.ts          # API types
└── styles/             # Global styles
    └── globals.css     # Tailwind CSS imports
```

## API Integration

The frontend communicates with multiple backend services:

- **Analytics Service** (Port 8000): Dashboard metrics and analytics
- **CRM Core Service** (Port 8001): Contact and deal management
- **User Management Service** (Port 8002): Authentication and user data
- **Workflow Engine** (Port 8003): Automation and workflows
- **AI Orchestration Service** (Port 8004): AI-powered features

## Key Features

### Dashboard
- Real-time metrics display
- Quick action buttons
- Performance indicators
- System health monitoring

### Contact Management
- CRUD operations for contacts
- Advanced search and filtering
- Bulk operations
- Contact details and history

### Analytics
- Interactive charts and graphs
- Custom date ranges
- Export functionality
- Real-time data updates

### Workflows
- Visual workflow builder
- Automated process management
- Execution monitoring
- Template library

### Messaging
- Multi-channel communication
- Real-time message updates
- Message analytics
- Response automation

## Authentication

The application uses JWT-based authentication:

1. Users log in with email/password
2. JWT token stored in localStorage
3. Token included in API requests
4. Automatic token refresh (planned)

Default demo credentials:
- Email: `admin@example.com`
- Password: `password`

## Development

### Code Style
- ESLint and Prettier configured
- TypeScript strict mode enabled
- Consistent component patterns
- Proper error handling

### State Management
- React Query for server state
- React Context for auth state
- Local state with useState/useReducer

### Styling
- Tailwind CSS utility classes
- Component-specific styles
- Responsive design patterns
- Consistent color scheme

## Deployment

### Production Environment
- Optimized build with Next.js
- Static file optimization
- Image optimization
- Performance monitoring

### Docker
- Multi-stage Docker build
- Minimal production image
- Health checks included
- Container orchestration ready

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Contact the development team
