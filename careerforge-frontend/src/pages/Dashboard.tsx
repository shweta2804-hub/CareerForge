import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { useAuth } from '../contexts/AuthContext'
import { Building2, Calendar, FileText, Users, TrendingUp, ArrowRight } from 'lucide-react'

interface Stats {
  totalStudents?: number
  totalCompanies?: number
  totalDrives?: number
  totalApplications?: number
  placementRate?: number
}

export default function Dashboard() {
  const { user } = useAuth()
  const [stats, setStats] = useState<Stats>({})

  useEffect(() => {
    // TODO: Fetch stats from API
    setStats({
      totalStudents: 150,
      totalCompanies: 25,
      totalDrives: 12,
      totalApplications: 450,
      placementRate: 75,
    })
  }, [])

  const isAdmin = user?.role === 'admin'

  return (
    <div className="space-y-8">
      {/* Welcome Section */}
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="mt-2 text-lg text-gray-600">
          Welcome back, <span className="font-semibold text-gray-900">{user?.full_name}</span>!
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {isAdmin && (
          <>
            <StatCard
              title="Total Students"
              value={stats.totalStudents || 0}
              icon={Users}
              color="blue"
            />
            <StatCard
              title="Total Companies"
              value={stats.totalCompanies || 0}
              icon={Building2}
              color="green"
            />
            <StatCard
              title="Active Drives"
              value={stats.totalDrives || 0}
              icon={Calendar}
              color="purple"
            />
            <StatCard
              title="Total Applications"
              value={stats.totalApplications || 0}
              icon={FileText}
              color="orange"
            />
          </>
        )}
        {!isAdmin && (
          <>
            <StatCard
              title="My Applications"
              value={stats.totalApplications || 0}
              icon={FileText}
              color="blue"
            />
            <StatCard
              title="Placement Rate"
              value={`${stats.placementRate || 0}%`}
              icon={TrendingUp}
              color="green"
            />
          </>
        )}
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-6">Quick Actions</h2>
        <div className="grid grid-cols-1 gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {isAdmin ? (
            <>
              <QuickAction
                title="Create Company"
                description="Add a new company to the portal"
                href="/companies"
                icon={Building2}
              />
              <QuickAction
                title="Create Drive"
                description="Post a new placement drive"
                href="/drives"
                icon={Calendar}
              />
              <QuickAction
                title="View Analytics"
                description="Check placement statistics and insights"
                href="/analytics"
                icon={TrendingUp}
              />
            </>
          ) : (
            <>
              <QuickAction
                title="Browse Drives"
                description="View available placement drives"
                href="/drives"
                icon={Calendar}
              />
              <QuickAction
                title="My Applications"
                description="Track your application status"
                href="/applications"
                icon={FileText}
              />
              <QuickAction
                title="Update Profile"
                description="Edit your student profile and resume"
                href="/profile"
                icon={Users}
              />
            </>
          )}
        </div>
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h2 className="text-xl font-semibold text-gray-900 mb-4">Recent Activity</h2>
        <div className="space-y-3">
          <p className="text-gray-500 italic">No recent activity to show</p>
        </div>
      </div>
    </div>
  )
}

interface StatCardProps {
  title: string
  value: number | string
  icon: React.ElementType
  color: 'blue' | 'green' | 'purple' | 'orange'
}

function StatCard({ title, value, icon: Icon, color }: StatCardProps) {
  const colorClasses = {
    blue: 'bg-blue-500',
    green: 'bg-green-500',
    purple: 'bg-purple-500',
    orange: 'bg-orange-500',
  }

  return (
    <div className="card group hover:scale-105 transition-transform duration-200">
      <div className="flex items-center">
        <div className={`p-3 rounded-xl ${colorClasses[color]} shadow-sm`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
        <div className="ml-4 flex-1">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-3xl font-bold text-gray-900 mt-1">{value}</p>
        </div>
      </div>
    </div>
  )
}

interface QuickActionProps {
  title: string
  description: string
  href: string
  icon: React.ElementType
}

function QuickAction({ title, description, href, icon: Icon }: QuickActionProps) {
  return (
    <Link
      to={href}
      className="group flex items-start p-4 border-2 border-gray-200 rounded-xl hover:border-primary-500 hover:bg-primary-50 transition-all duration-200"
    >
      <div className="p-2 bg-primary-100 rounded-lg group-hover:bg-primary-200 transition-colors">
        <Icon className="h-5 w-5 text-primary-600" />
      </div>
      <div className="ml-3 flex-1">
        <h3 className="text-sm font-semibold text-gray-900 group-hover:text-primary-700">{title}</h3>
        <p className="text-xs text-gray-500 mt-1">{description}</p>
      </div>
      <ArrowRight className="h-4 w-4 text-gray-400 group-hover:text-primary-600 group-hover:translate-x-1 transition-all" />
    </Link>
  )
}