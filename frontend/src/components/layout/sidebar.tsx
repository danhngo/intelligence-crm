import Link from 'next/link'
import { useAuth } from '@/components/auth/auth-provider'
import { useRouter } from 'next/navigation'
import { 
  HomeIcon, 
  UsersIcon, 
  ChartBarIcon, 
  Cog6ToothIcon,
  ChatBubbleLeftRightIcon,
  ArrowRightOnRectangleIcon,
  UserCircleIcon,
  HeartIcon,
  DocumentTextIcon,
  MegaphoneIcon,
  EnvelopeIcon,
  CpuChipIcon,
  BuildingOfficeIcon,
  UserPlusIcon,
  CurrencyDollarIcon
} from '@heroicons/react/24/outline'

const navigationSections = [
  {
    name: 'Overview',
    items: [
      { name: 'Dashboard', href: '/dashboard', icon: HomeIcon },
    ]
  },
  {
    name: 'CRM',
    items: [
      { name: 'Contacts', href: '/contacts', icon: UsersIcon },
      { name: 'Companies', href: '/companies', icon: BuildingOfficeIcon },
      { name: 'Leads', href: '/leads', icon: UserPlusIcon },
      { name: 'Deals', href: '/deals', icon: CurrencyDollarIcon },
    ]
  },
  {
    name: 'Marketing',
    items: [
      { name: 'Campaigns', href: '/campaigns', icon: MegaphoneIcon },
      { name: 'Templates', href: '/templates', icon: EnvelopeIcon },
      { name: 'Messages', href: '/messages', icon: ChatBubbleLeftRightIcon },
    ]
  },
  {
    name: 'Intelligence',
    items: [
      { name: 'AI & ML', href: '/ai', icon: CpuChipIcon },
      { name: 'Analytics', href: '/analytics', icon: ChartBarIcon },
    ]
  },
  {
    name: 'System',
    items: [
      { name: 'Workflows', href: '/workflows', icon: Cog6ToothIcon },
      { name: 'Health', href: '/health', icon: HeartIcon },
      { name: 'API Docs', href: '/api-docs', icon: DocumentTextIcon },
    ]
  }
]

export default function Sidebar() {
  const { user, logout } = useAuth()
  const router = useRouter()

  const handleLogout = () => {
    logout()
    router.push('/login')
  }

  return (
    <div className="hidden md:flex md:w-64 md:flex-col md:fixed md:inset-y-0">
      <div className="flex flex-col flex-grow pt-5 bg-white border-r border-gray-200 overflow-y-auto">
        <div className="flex items-center flex-shrink-0 px-4">
          <h1 className="text-xl font-bold text-gray-900">Intelligence CRM</h1>
        </div>
        
        <div className="mt-5 flex-grow flex flex-col">
          <nav className="flex-1 px-2 pb-4 space-y-4">
            {navigationSections.map((section) => (
              <div key={section.name}>
                <h3 className="px-3 text-xs font-semibold text-gray-500 uppercase tracking-wider">
                  {section.name}
                </h3>
                <div className="mt-1 space-y-1">
                  {section.items.map((item) => (
                    <Link
                      key={item.name}
                      href={item.href}
                      className="group flex items-center px-2 py-2 text-sm font-medium rounded-md text-gray-600 hover:bg-gray-50 hover:text-gray-900"
                    >
                      <item.icon className="mr-3 flex-shrink-0 h-6 w-6" aria-hidden="true" />
                      {item.name}
                    </Link>
                  ))}
                </div>
              </div>
            ))}
          </nav>
        </div>
        
        {user && (
          <div className="flex-shrink-0 flex border-t border-gray-200 p-4">
            <div className="flex items-center">
              <UserCircleIcon className="h-8 w-8 text-gray-400" />
              <div className="ml-3">
                <p className="text-sm font-medium text-gray-700">{user.first_name} {user.last_name}</p>
                <p className="text-xs text-gray-500">{user.email}</p>
              </div>
            </div>
            <button
              onClick={handleLogout}
              className="ml-auto p-2 text-gray-400 hover:text-gray-600"
              title="Logout"
            >
              <ArrowRightOnRectangleIcon className="h-5 w-5" />
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
