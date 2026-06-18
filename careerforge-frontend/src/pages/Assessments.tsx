import { useState, useEffect } from 'react'
import { ClipboardList, CheckCircle, XCircle } from 'lucide-react'

interface Assessment {
  id: number
  title: string
  description: string
  total_marks: number
  passing_marks: number
  is_active: boolean
}

export default function Assessments() {
  const [assessments, setAssessments] = useState<Assessment[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetchAssessments()
  }, [])

  const fetchAssessments = async () => {
    try {
      const response = await fetch('/api/v1/assessments')
      if (!response.ok) throw new Error('Failed to fetch assessments')
      const data = await response.json()
      setAssessments(data.data || [])
    } catch (error) {
      console.error('Failed to load assessments')
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

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-2xl font-bold text-gray-900">Assessments</h1>
        <p className="mt-1 text-sm text-gray-600">View and take assessments</p>
      </div>

      {assessments.length === 0 ? (
        <div className="card text-center py-12">
          <ClipboardList className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No assessments available</h3>
          <p className="mt-1 text-sm text-gray-500">Check back later for new assessments.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
          {assessments.map((assessment) => (
            <div key={assessment.id} className="card hover:shadow-md transition-shadow">
              <div className="flex items-start">
                <div className="p-2 bg-primary-50 rounded-lg">
                  <ClipboardList className="h-6 w-6 text-primary-600" />
                </div>
                <div className="ml-3 flex-1">
                  <h3 className="text-sm font-medium text-gray-900">{assessment.title}</h3>
                  <p className="text-xs text-gray-500 mt-1">{assessment.description || 'No description'}</p>
                </div>
              </div>

              <div className="mt-4 space-y-2 text-sm">
                <div className="flex justify-between">
                  <span className="text-gray-600">Total Marks:</span>
                  <span className="font-medium">{assessment.total_marks}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-600">Passing Marks:</span>
                  <span className="font-medium">{assessment.passing_marks}</span>
                </div>
              </div>

              <div className="mt-4">
                <button className="btn btn-primary w-full text-sm">
                  Take Assessment
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}