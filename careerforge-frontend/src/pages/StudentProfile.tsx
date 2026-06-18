import { useState, useEffect } from 'react'
import { User, Mail, Phone, MapPin, GraduationCap, FileText, Upload } from 'lucide-react'
import toast from 'react-hot-toast'

interface StudentProfile {
  id: number
  user_id: number
  branch: string
  cgpa: number
  graduation_year: number
  skills: string
  projects: string
  resume_url: string | null
}

export default function StudentProfile() {
  const [profile, setProfile] = useState<StudentProfile | null>(null)
  const [loading, setLoading] = useState(true)
  const [editing, setEditing] = useState(false)
  const [formData, setFormData] = useState({
    branch: '',
    cgpa: 0,
    graduation_year: new Date().getFullYear(),
    skills: '',
    projects: '',
  })

  useEffect(() => {
    fetchProfile()
  }, [])

  const fetchProfile = async () => {
    try {
      const response = await fetch('/api/v1/students/profile')
      if (!response.ok) throw new Error('Failed to fetch profile')
      const data = await response.json()
      setProfile(data.data)
      setFormData({
        branch: data.data.branch,
        cgpa: data.data.cgpa,
        graduation_year: data.data.graduation_year,
        skills: data.data.skills || '',
        projects: data.data.projects || '',
      })
    } catch (error) {
      console.error('Failed to load profile')
    } finally {
      setLoading(false)
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      const response = await fetch('/api/v1/students/profile', {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(formData),
      })
      if (!response.ok) throw new Error('Failed to update profile')
      toast.success('Profile updated successfully')
      setEditing(false)
      fetchProfile()
    } catch (error) {
      toast.error('Failed to update profile')
    }
  }

  const handleResumeUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (!file) return

    if (file.type !== 'application/pdf') {
      toast.error('Only PDF files are allowed')
      return
    }

    if (file.size > 5 * 1024 * 1024) {
      toast.error('File size must be less than 5MB')
      return
    }

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/api/v1/students/resume', {
        method: 'POST',
        body: formData,
      })
      if (!response.ok) throw new Error('Failed to upload resume')
      toast.success('Resume uploaded successfully')
      fetchProfile()
    } catch (error) {
      toast.error('Failed to upload resume')
    }
  }

  if (loading) {
    return (
      <div className="flex items-center justify-center h-64">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    )
  }

  if (!profile) {
    return (
      <div className="card text-center py-12">
        <User className="mx-auto h-12 w-12 text-gray-400" />
        <h3 className="mt-2 text-sm font-medium text-gray-900">No profile found</h3>
        <p className="mt-1 text-sm text-gray-500">Create your student profile to get started.</p>
      </div>
    )
  }

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Student Profile</h1>
          <p className="mt-1 text-sm text-gray-600">Manage your profile information</p>
        </div>
        {!editing && (
          <button onClick={() => setEditing(true)} className="btn btn-primary">
            Edit Profile
          </button>
        )}
      </div>

      {editing ? (
        <form onSubmit={handleSubmit} className="card space-y-6">
          <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
            <div>
              <label className="label">Branch</label>
              <input
                type="text"
                value={formData.branch}
                onChange={(e) => setFormData({ ...formData, branch: e.target.value })}
                className="input"
                required
              />
            </div>
            <div>
              <label className="label">CGPA</label>
              <input
                type="number"
                step="0.01"
                min="0"
                max="10"
                value={formData.cgpa}
                onChange={(e) => setFormData({ ...formData, cgpa: parseFloat(e.target.value) })}
                className="input"
                required
              />
            </div>
            <div>
              <label className="label">Graduation Year</label>
              <input
                type="number"
                min="2020"
                max="2030"
                value={formData.graduation_year}
                onChange={(e) => setFormData({ ...formData, graduation_year: parseInt(e.target.value) })}
                className="input"
                required
              />
            </div>
            <div>
              <label className="label">Skills (comma-separated)</label>
              <input
                type="text"
                value={formData.skills}
                onChange={(e) => setFormData({ ...formData, skills: e.target.value })}
                className="input"
                placeholder="Python, React, SQL"
              />
            </div>
            <div className="sm:col-span-2">
              <label className="label">Projects (JSON array)</label>
              <textarea
                value={formData.projects}
                onChange={(e) => setFormData({ ...formData, projects: e.target.value })}
                className="input"
                rows={4}
                placeholder='[{"name": "Project 1", "description": "..."}]'
              />
            </div>
          </div>

          <div className="flex justify-end space-x-3">
            <button type="button" onClick={() => setEditing(false)} className="btn btn-secondary">
              Cancel
            </button>
            <button type="submit" className="btn btn-primary">
              Save Changes
            </button>
          </div>
        </form>
      ) : (
        <div className="space-y-6">
          {/* Personal Information */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Personal Information</h2>
            <div className="space-y-4">
              <div className="flex items-center">
                <User className="h-5 w-5 text-gray-400 mr-3" />
                <div>
                  <p className="text-sm text-gray-600">Name</p>
                  <p className="font-medium">Student User</p>
                </div>
              </div>
              <div className="flex items-center">
                <Mail className="h-5 w-5 text-gray-400 mr-3" />
                <div>
                  <p className="text-sm text-gray-600">Email</p>
                  <p className="font-medium">student@example.com</p>
                </div>
              </div>
            </div>
          </div>

          {/* Academic Information */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Academic Information</h2>
            <div className="grid grid-cols-1 gap-6 sm:grid-cols-2">
              <div className="flex items-center">
                <GraduationCap className="h-5 w-5 text-gray-400 mr-3" />
                <div>
                  <p className="text-sm text-gray-600">Branch</p>
                  <p className="font-medium">{profile.branch}</p>
                </div>
              </div>
              <div className="flex items-center">
                <GraduationCap className="h-5 w-5 text-gray-400 mr-3" />
                <div>
                  <p className="text-sm text-gray-600">CGPA</p>
                  <p className="font-medium">{profile.cgpa}</p>
                </div>
              </div>
              <div className="flex items-center">
                <GraduationCap className="h-5 w-5 text-gray-400 mr-3" />
                <div>
                  <p className="text-sm text-gray-600">Graduation Year</p>
                  <p className="font-medium">{profile.graduation_year}</p>
                </div>
              </div>
            </div>
          </div>

          {/* Skills & Projects */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Skills & Projects</h2>
            <div className="space-y-4">
              <div>
                <p className="text-sm text-gray-600 mb-2">Skills</p>
                <div className="flex flex-wrap gap-2">
                  {profile.skills ? JSON.parse(profile.skills).map((skill: string, index: number) => (
                    <span key={index} className="px-3 py-1 bg-primary-50 text-primary-700 rounded-full text-sm">
                      {skill}
                    </span>
                  )) : (
                    <p className="text-sm text-gray-500">No skills added</p>
                  )}
                </div>
              </div>
              <div>
                <p className="text-sm text-gray-600 mb-2">Projects</p>
                {profile.projects ? (
                  <div className="space-y-2">
                    {JSON.parse(profile.projects).map((project: any, index: number) => (
                      <div key={index} className="border-l-2 border-primary-500 pl-3">
                        <p className="font-medium text-sm">{project.name}</p>
                        <p className="text-xs text-gray-600">{project.description}</p>
                      </div>
                    ))}
                  </div>
                ) : (
                  <p className="text-sm text-gray-500">No projects added</p>
                )}
              </div>
            </div>
          </div>

          {/* Resume */}
          <div className="card">
            <h2 className="text-lg font-semibold text-gray-900 mb-4">Resume</h2>
            {profile.resume_url ? (
              <div className="flex items-center justify-between">
                <div className="flex items-center">
                  <FileText className="h-5 w-5 text-primary-600 mr-2" />
                  <a href={profile.resume_url} target="_blank" rel="noopener noreferrer" className="text-primary-600 hover:underline">
                    View Resume
                  </a>
                </div>
                <label className="btn btn-secondary inline-flex items-center cursor-pointer">
                  <Upload className="mr-2 h-4 w-4" />
                  Update
                  <input type="file" accept=".pdf" className="hidden" onChange={handleResumeUpload} />
                </label>
              </div>
            ) : (
              <label className="btn btn-primary inline-flex items-center cursor-pointer">
                <Upload className="mr-2 h-4 w-4" />
                Upload Resume
                <input type="file" accept=".pdf" className="hidden" onChange={handleResumeUpload} />
              </label>
            )}
            <p className="text-xs text-gray-500 mt-2">PDF format only, max 5MB</p>
          </div>
        </div>
      )}
    </div>
  )
}