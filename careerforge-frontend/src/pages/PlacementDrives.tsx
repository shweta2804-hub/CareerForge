import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Plus, Calendar, Search, ExternalLink } from 'lucide-react'
import toast from 'react-hot-toast'

interface Drive {
  id: number
  company_id: number
  company_name: string
  drive_date: string
  application_deadline: string
  open_positions: number
  status: string
  description: string
}

export default function PlacementDrives() {
  const [drives, setDrives] = useState<Drive[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState('all')

  useEffect(() => {
    fetchDrives()
  }, [])

  const fetchDrives = async () => {
    try {
      const response = await fetch('/api/v1/drives')
      if (!response.ok) throw new Error('Failed to fetch drives')
      const data = await response.json()
      setDrives(data.data || [])
    } catch (error) {
      toast.error('Failed to load placement drives')
    } finally {
      setLoading(false)
    }
  }

  const filteredDrives = drives.filter(drive => {
    if (filter === 'all') return true
    return drive.status.toLowerCase() === filter
  })

  const getStatusColor = (status: string) => {
    switch (status.toLowerCase()) {
      case 'published':
        return 'bg-green-100 text-green-800'
      case 'draft':
        return 'bg-yellow-100 text-yellow-800'
      case 'closed':
        return 'bg-gray-100 text-gray-800'
      default:
        return 'bg-gray-100 text-gray-800'
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Placement Drives</h1>
          <p className="mt-1 text-sm text-gray-600">Browse and manage placement drives</p>
        </div>
        <Link to="/drives/create" className="btn btn-primary inline-flex items-center">
          <Plus className="mr-2 h-5 w-5" />
          Create Drive
        </Link>
      </div>

      {/* Filters */}
      <div className="card">
        <div className="flex flex-col sm:flex-row gap-4">
          <div className="flex-1 relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
            <input
              type="text"
              placeholder="Search drives..."
              className="input pl-10"
            />
          </div>
          <select
            value={filter}
            onChange={(e) => setFilter(e.target.value)}
            className="input w-full sm:w-48"
          >
            <option value="all">All Status</option>
            <option value="published">Published</option>
            <option value="draft">Draft</option>
            <option value="closed">Closed</option>
          </select>
        </div>
      </div>

      {/* Drives List */}
      <div className="grid grid-cols-1 gap-6">
        {filteredDrives.map((drive) => (
          <div key={drive.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between">
              <div className="flex items-start">
                <div className="p-2 bg-primary-50 rounded-lg">
                  <Calendar className="h-6 w-6 text-primary-600" />
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-gray-900">{drive.company_name}</h3>
                  <p className="text-xs text-gray-500 mt-1">{drive.description || 'No description'}</p>
                </div>
              </div>
              <span className={`px-2 py-1 text-xs font-medium rounded-full ${getStatusColor(drive.status)}`}>
                {drive.status}
              </span>
            </div>

            <div className="mt-4 grid grid-cols-2 gap-4 text-sm">
              <div>
                <p className="text-gray-600">Drive Date</p>
                <p className="font-medium">{new Date(drive.drive_date).toLocaleDateString()}</p>
              </div>
              <div>
                <p className="text-gray-600">Deadline</p>
                <p className="font-medium">{new Date(drive.application_deadline).toLocaleDateString()}</p>
              </div>
              <div>
                <p className="text-gray-600">Open Positions</p>
                <p className="font-medium">{drive.open_positions}</p>
              </div>
            </div>

            <div className="mt-4 flex space-x-2">
              <Link
                to={`/drives/${drive.id}`}
                className="btn btn-secondary flex-1 text-sm inline-flex items-center justify-center"
              >
                <ExternalLink className="mr-2 h-4 w-4" />
                View Details
              </Link>
            </div>
          </div>
        ))}
      </div>

      {filteredDrives.length === 0 && (
        <div className="card text-center py-12">
          <Calendar className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No drives found</h3>
          <p className="mt-1 text-sm text-gray-500">No placement drives available at the moment.</p>
        </div>
      )}
    </div>
  )
}