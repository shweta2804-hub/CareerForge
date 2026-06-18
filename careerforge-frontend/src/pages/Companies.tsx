import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { Plus, Search, Building2, Edit, Trash2 } from 'lucide-react'
import toast from 'react-hot-toast'

interface Company {
  id: number
  name: string
  location: string
  package_offered: number | null
  minimum_cgpa: number
  is_active: boolean
}

export default function Companies() {
  const [companies, setCompanies] = useState<Company[]>([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')

  useEffect(() => {
    fetchCompanies()
  }, [])

  const fetchCompanies = async () => {
    try {
      const response = await fetch('/api/v1/companies')
      if (!response.ok) throw new Error('Failed to fetch companies')
      const data = await response.json()
      setCompanies(data.data || [])
    } catch (error) {
      toast.error('Failed to load companies')
    } finally {
      setLoading(false)
    }
  }

  const handleDelete = async (id: number) => {
    if (!confirm('Are you sure you want to delete this company?')) return
    try {
      const response = await fetch(`/api/v1/companies/${id}`, {
        method: 'DELETE',
      })
      if (!response.ok) throw new Error('Failed to delete')
      setCompanies(companies.filter(c => c.id !== id))
      toast.success('Company deleted successfully')
    } catch (error) {
      toast.error('Failed to delete company')
    }
  }

  const filteredCompanies = companies.filter(c =>
    c.name.toLowerCase().includes(search.toLowerCase())
  )

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
          <h1 className="text-2xl font-bold text-gray-900">Companies</h1>
          <p className="mt-1 text-sm text-gray-600">Manage company profiles</p>
        </div>
        <Link to="/companies/create" className="btn btn-primary inline-flex items-center">
          <Plus className="mr-2 h-5 w-5" />
          Add Company
        </Link>
      </div>

      {/* Search */}
      <div className="card">
        <div className="relative">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 h-5 w-5 text-gray-400" />
          <input
            type="text"
            placeholder="Search companies..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="input pl-10"
          />
        </div>
      </div>

      {/* Companies List */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3">
        {filteredCompanies.map((company) => (
          <div key={company.id} className="card hover:shadow-md transition-shadow">
            <div className="flex items-start justify-between">
              <div className="flex items-center">
                <div className="p-2 bg-primary-50 rounded-lg">
                  <Building2 className="h-6 w-6 text-primary-600" />
                </div>
                <div className="ml-3">
                  <h3 className="text-sm font-medium text-gray-900">{company.name}</h3>
                  <p className="text-xs text-gray-500">{company.location}</p>
                </div>
              </div>
              <span className={`px-2 py-1 text-xs font-medium rounded-full ${
                company.is_active ? 'bg-green-100 text-green-800' : 'bg-gray-100 text-gray-800'
              }`}>
                {company.is_active ? 'Active' : 'Inactive'}
              </span>
            </div>

            <div className="mt-4 space-y-2">
              <div className="flex justify-between text-sm">
                <span className="text-gray-600">Min CGPA:</span>
                <span className="font-medium">{company.minimum_cgpa}</span>
              </div>
              {company.package_offered && (
                <div className="flex justify-between text-sm">
                  <span className="text-gray-600">Package:</span>
                  <span className="font-medium">₹{company.package_offered} LPA</span>
                </div>
              )}
            </div>

            <div className="mt-4 flex space-x-2">
              <Link
                to={`/companies/${company.id}`}
                className="btn btn-secondary flex-1 text-sm"
              >
                View
              </Link>
              <button
                onClick={() => handleDelete(company.id)}
                className="btn btn-danger text-sm"
              >
                <Trash2 className="h-4 w-4" />
              </button>
            </div>
          </div>
        ))}
      </div>

      {filteredCompanies.length === 0 && (
        <div className="card text-center py-12">
          <Building2 className="mx-auto h-12 w-12 text-gray-400" />
          <h3 className="mt-2 text-sm font-medium text-gray-900">No companies found</h3>
          <p className="mt-1 text-sm text-gray-500">Get started by creating a new company.</p>
        </div>
      )}
    </div>
  )
}