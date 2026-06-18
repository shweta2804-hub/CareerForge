import { useState, useEffect } from 'react'
import { BarChart3, TrendingUp, Users, Building2, FileText } from 'lucide-react'

interface Analytics {
  overview: {
    total_students: number
    total_companies: number
    total_applications: number
    placement_rate: number
    highest_package: number | null
    average_package: number | null
  }
  top_hiring_companies: Array<{
    company_name: string
    total_hired: number
  }>
  branch_wise_stats: Array<{
    branch: string
    total_students: number
    placed_students: number
    placement_percentage: number
  }>
}

export default function Analytics() {
  const [analytics, setAnalytics] = useState<Analytics | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    try {
      const response = await fetch('/api/v1/analytics/full-report')
      if (!response.ok) throw new Error('Failed to fetch analytics')
      const data = await response.json()
      setAnalytics(data.data)
    } catch (error) {
      console.error('Failed to load analytics')
    } finally {
      setLoading(false)
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!analytics) {
    return (
      <div className="card text-center py-12">
        <BarChart3 className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">No analytics data available</h3>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Analytics Dashboard</h1>
        <p className="mt-1 text-sm text-gray-600">Placement statistics and insights</p>
      </div>

      {/* Overview Stats */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        <StatCard
          title="Total Students"
          value={analytics.overview.total_students}
          icon={Users}
          color="blue"
        />
        <StatCard
          title="Total Companies"
          value={analytics.overview.total_companies}
          icon={Building2}
          color="green"
        />
        <StatCard
          title="Total Applications"
          value={analytics.overview.total_applications}
          icon={FileText}
          color="purple"
        />
        <StatCard
          title="Placement Rate"
          value={`${analytics.overview.placement_rate}%`}
          icon={TrendingUp}
          color="orange"
        />
      </div>

      {/* Package Stats */}
      {(analytics.overview.highest_package || analytics.overview.average_package) && (
        <div className="card">
          <h2 className="text-lg font-semibold text-gray-900 mb-4">Package Statistics</h2>
          <div className="grid grid-cols-2 gap-4">
            {analytics.overview.highest_package && (
              <div>
                <p className="text-sm text-gray-600">Highest Package</p>
                <p className="text-2xl font-bold text-gray-900">₹{analytics.overview.highest_package} LPA</p>
              </div>
            )}
            {analytics.overview.average_package && (
              <div>
                <p className="text-sm text-gray-600">Average Package</p>
                <p className="text-2xl font-bold text-gray-900">₹{analytics.overview.average_package} LPA</p>
              </div>
            )}
          </div>
        </div>
      )}

      {/* Top Hiring Companies */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Top Hiring Companies</h2>
        <div className="space-y-3">
          {analytics.top_hiring_companies.map((company, index) => (
            <div key={index} className="flex items-center justify-between">
              <div className="flex items-center">
                <span className="text-sm font-medium text-gray-900">{company.company_name}</span>
              </div>
              <span className="text-sm text-gray-600">{company.total_hired} hired</span>
            </div>
          ))}
        </div>
      </div>

      {/* Branch-wise Stats */}
      <div className="card">
        <h2 className="text-lg font-semibold text-gray-900 mb-4">Branch-wise Placement</h2>
        <div className="space-y-3">
          {analytics.branch_wise_stats.map((stat, index) => (
            <div key={index}>
              <div className="flex items-center justify-between mb-1">
                <span className="text-sm font-medium text-gray-900">{stat.branch}</span>
                <span className="text-sm text-gray-600">{stat.placement_percentage}%</span>
              </div>
              <div className="w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-primary-600 h-2 rounded-full"
                  style={{ width: `${stat.placement_percentage}%` }}
                />
              </div>
            </div>
          ))}
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
    <div className="card">
      <div className="flex items-center">
        <div className={`p-3 rounded-lg ${colorClasses[color]}`}>
          <Icon className="h-6 w-6 text-white" />
        </div>
        <div className="ml-4">
          <p className="text-sm font-medium text-gray-600">{title}</p>
          <p className="text-2xl font-semibold text-gray-900">{value}</p>
        </div>
      </div>
    </div>
  )
}