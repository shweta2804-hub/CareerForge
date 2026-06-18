# Frontend Implementation Plan - CareerForge

## Backend API
- **Base URL**: https://careerforge-tw8t.onrender.com
- **Documentation**: https://careerforge-tw8t.onrender.com/docs
- **Authentication**: JWT Bearer tokens
- **API Version**: v1

---

## 1. Technology Stack

### Core Technologies
- **React 18** - UI library
- **TypeScript 5** - Type safety
- **Vite 5** - Build tool and dev server
- **React Router 6** - Client-side routing
- **Axios** - HTTP client
- **Tailwind CSS 3** - Styling framework

### Form & Validation
- **React Hook Form 7** - Form state management
- **Zod 3** - Schema validation
- **@hookform/resolvers** - Zod integration

### Additional Libraries
- **React Query (TanStack Query)** - Server state management
- **React Hot Toast** - Notifications
- **Lucide React** - Icons
- **date-fns** - Date formatting

---

## 2. Project Structure

```
careerforge-frontend/
├── public/
│   ├── favicon.ico
│   └── images/
│       ├── logo.png
│       └── placeholder-avatar.png
├── src/
│   ├── components/
│   │   ├── ui/
│   │   │   ├── Button.tsx
│   │   │   ├── Input.tsx
│   │   │   ├── Card.tsx
│   │   │   ├── Modal.tsx
│   │   │   ├── Table.tsx
│   │   │   ├── Badge.tsx
│   │   │   ├── Spinner.tsx
│   │   │   └── Alert.tsx
│   │   ├── layout/
│   │   │   ├── Header.tsx
│   │   │   ├── Sidebar.tsx
│   │   │   ├── Footer.tsx
│   │   │   └── Layout.tsx
│   │   └── auth/
│   │       ├── ProtectedRoute.tsx
│   │       └── RoleGuard.tsx
│   ├── pages/
│   │   ├── Login.tsx
│   │   ├── Register.tsx
│   │   ├── Dashboard.tsx
│   │   ├── StudentProfile.tsx
│   │   ├── Companies.tsx
│   │   ├── PlacementDrives.tsx
│   │   ├── Applications.tsx
│   │   ├── Assessments.tsx
│   │   ├── Analytics.tsx
│   │   └── NotFound.tsx
│   ├── services/
│   │   ├── api.ts
│   │   ├── auth.service.ts
│   │   ├── student.service.ts
│   │   ├── company.service.ts
│   │   ├── drive.service.ts
│   │   ├── application.service.ts
│   │   ├── assessment.service.ts
│   │   └── analytics.service.ts
│   ├── contexts/
│   │   └── AuthContext.tsx
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useApi.ts
│   │   └── useForm.ts
│   ├── types/
│   │   ├── auth.ts
│   │   ├── student.ts
│   │   ├── company.ts
│   │   ├── drive.ts
│   │   ├── application.ts
│   │   ├── assessment.ts
│   │   └── analytics.ts
│   ├── utils/
│   │   ├── constants.ts
│   │   ├── helpers.ts
│   │   └── validators.ts
│   ├── App.tsx
│   ├── main.tsx
│   └── index.css
├── .env.example
├── .gitignore
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
├── tailwind.config.js
├── postcss.config.js
└── README.md
```

---

## 3. Configuration Files

### 3.1 package.json
**Key Dependencies**:
- react, react-dom, react-router-dom
- axios, @tanstack/react-query
- react-hook-form, zod, @hookform/resolvers
- tailwindcss, postcss, autoprefixer
- react-hot-toast, lucide-react, date-fns

**Scripts**:
- dev: Vite dev server
- build: Production build
- preview: Preview production build
- lint: ESLint
- type-check: TypeScript compiler check

### 3.2 vite.config.ts
- React plugin
- Proxy configuration for API calls
- Environment variable loading
- Build optimization

### 3.3 tsconfig.json
- Strict mode enabled
- Path aliases (@/components, @/pages, @/services, etc.)
- ES2020 target
- React JSX settings

### 3.4 tailwind.config.js
- Content paths for purging
- Custom color scheme (primary, secondary, accent)
- Responsive breakpoints
- Dark mode support (optional)

### 3.5 .env.example
```
VITE_API_URL=https://careerforge-tw8t.onrender.com
VITE_APP_NAME=CareerForge
```

---

## 4. API Client Configuration

### 4.1 Axios Instance (src/services/api.ts)

**Features**:
- Base URL from environment variable
- Request interceptor:
  - Attach JWT token from localStorage
  - Handle token refresh on 401
- Response interceptor:
  - Handle 401/403 errors
  - Global error handling
  - Toast notifications

**Implementation**:
```typescript
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor
api.interceptors.response.use(
  (response) => response,
  async (error) => {
    if (error.response?.status === 401) {
      // Handle token refresh or logout
    }
    return Promise.reject(error);
  }
);
```

### 4.2 Service Modules

**Structure**: Each service module handles one domain

**auth.service.ts**:
- login(email, password)
- register(data)
- refreshToken(token)
- getCurrentUser()
- logout()

**student.service.ts**:
- getProfile()
- updateProfile(data)
- uploadResume(file)
- getAllStudents(params)
- getStudentById(id)

**company.service.ts**:
- getAllCompanies(params)
- getCompanyById(id)
- createCompany(data)
- updateCompany(id, data)
- deleteCompany(id)
- searchCompanies(name)

**drive.service.ts**:
- getAllDrives(params)
- getPublishedDrives(params)
- getDriveById(id)
- createDrive(data)
- updateDrive(id, data)
- publishDrive(id)
- closeDrive(id)
- deleteDrive(id)

**application.service.ts**:
- applyToDrive(driveId)
- getMyApplications()
- getDriveApplications(driveId)
- getApplicationById(id)
- updateApplicationStatus(id, status, reason)
- getAllApplications(params)

**assessment.service.ts**:
- getAllAssessments(params)
- getAssessmentById(id)
- createAssessment(data)
- updateAssessment(id, data)
- deleteAssessment(id)
- submitScore(assessmentId, score)
- getMyScores()
- getAssessmentScores(assessmentId)

**analytics.service.ts**:
- getOverview()
- getTopCompanies(limit)
- getBranchStats()
- getFullReport()

---

## 5. Authentication Context

### 5.1 AuthContext (src/contexts/AuthContext.tsx)

**State**:
- user: User | null
- token: string | null
- loading: boolean
- isAuthenticated: boolean

**Methods**:
- login(email, password)
- register(data)
- logout()
- refreshToken()
- updateUser(user)

**Implementation**:
- Context API for global state
- localStorage for persistence
- Auto-refresh token before expiry
- Redirect to login on 401

### 5.2 Custom Hooks

**useAuth.ts**:
```typescript
const { user, login, register, logout, loading } = useAuth();
```

**useApi.ts**:
```typescript
const { data, isLoading, error, refetch } = useApi(queryKey, queryFn);
```

---

## 6. Routing Configuration

### 6.1 Route Structure (src/App.tsx)

**Public Routes**:
- `/login` - Login page
- `/register` - Registration page

**Protected Routes** (require authentication):
- `/dashboard` - Dashboard
- `/profile` - Student profile
- `/companies` - Companies list
- `/drives` - Placement drives
- `/applications` - My applications
- `/assessments` - Assessments
- `/analytics` - Analytics dashboard

**Admin-Only Routes**:
- `/companies/create` - Create company
- `/drives/create` - Create drive
- `/assessments/create` - Create assessment
- `/analytics` - View analytics

**Catch-All**:
- `*` - 404 Not Found

### 6.2 Route Protection

**ProtectedRoute Component**:
- Check authentication status
- Redirect to login if not authenticated
- Show loading spinner while checking
- Render children if authenticated

**RoleGuard Component**:
- Check user role (admin/student)
- Redirect to dashboard if unauthorized
- Render children if authorized

---

## 7. Page Implementations

### 7.1 Login Page (src/pages/Login.tsx)

**Features**:
- Email and password form
- Form validation (Zod schema)
- Remember me checkbox
- Forgot password link (placeholder)
- Link to registration
- Error message display
- Loading state

**Form Schema (Zod)**:
```typescript
const loginSchema = z.object({
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
});
```

**API Integration**:
- POST /api/v1/auth/login
- Store token in localStorage
- Redirect to dashboard

**UI Components**:
- Centered card layout
- Logo and branding
- Input fields with icons
- Submit button with loading state
- Error alert

### 7.2 Register Page (src/pages/Register.tsx)

**Features**:
- Full name, email, password, confirm password
- Role selection (Student/Admin)
- Form validation
- Link to login
- Error message display

**Form Schema (Zod)**:
```typescript
const registerSchema = z.object({
  full_name: z.string().min(2, 'Name too short'),
  email: z.string().email('Invalid email'),
  password: z.string().min(8, 'Password must be at least 8 characters'),
  confirmPassword: z.string(),
  role: z.enum(['student', 'admin']),
}).refine(data => data.password === data.confirmPassword, {
  message: "Passwords don't match",
  path: ['confirmPassword'],
});
```

**API Integration**:
- POST /api/v1/auth/register
- Auto-login after registration
- Redirect to dashboard

### 7.3 Dashboard Page (src/pages/Dashboard.tsx)

**Features**:
- Welcome message with user name
- Quick stats cards (total applications, drives, etc.)
- Recent activity list
- Upcoming drives
- Quick action buttons

**Data Display**:
- Student: Show profile completion, recent applications
- Admin: Show total users, companies, drives, applications

**Components**:
- StatsCard component
- RecentActivityList component
- QuickActions component

### 7.4 Student Profile Page (src/pages/StudentProfile.tsx)

**Features**:
- View profile information
- Edit profile form
- Resume upload section
- Skills management
- Projects management

**Sections**:
1. Personal Information (read-only)
2. Academic Information (editable)
   - Branch
   - CGPA
   - Graduation Year
3. Skills (editable, comma-separated)
4. Projects (editable, JSON array)
5. Resume Upload
   - Upload button
   - Current resume link
   - File validation (PDF, 5MB)

**Forms**:
- StudentUpdate schema (Zod)
- File upload with progress

**API Integration**:
- GET /api/v1/students/profile
- PUT /api/v1/students/profile
- POST /api/v1/students/resume

### 7.5 Companies Page (src/pages/Companies.tsx)

**Features**:
- List all companies with pagination
- Search companies by name
- View company details
- Create company (admin only)
- Edit company (admin only)
- Delete company (admin only)

**Components**:
- CompanyList - Table with pagination
- CompanyCard - Card view (optional)
- CompanyForm - Create/Edit modal
- CompanySearch - Search bar
- CompanyDetails - Detail view modal

**Data Display**:
- Company name
- Location
- Package offered
- Minimum CGPA
- Required skills
- Active status

**Actions**:
- Admin: Create, Edit, Delete
- Student/User: View, Search

**API Integration**:
- GET /api/v1/companies
- GET /api/v1/companies/{id}
- POST /api/v1/companies
- PUT /api/v1/companies/{id}
- DELETE /api/v1/companies/{id}
- GET /api/v1/companies/search/{name}

### 7.6 Placement Drives Page (src/pages/PlacementDrives.tsx)

**Features**:
- List all drives with filters
- View published drives (student view)
- Create drive (admin only)
- Publish/Close drive (admin only)
- View drive details
- Apply to drive (student)

**Components**:
- DriveList - List with filters
- DriveCard - Card component
- DriveForm - Create/Edit modal
- DriveDetails - Detail view
- StatusBadge - Draft/Published/Closed

**Filters**:
- Status (All, Draft, Published, Closed)
- Company
- Date range

**Student View**:
- See only published drives
- Apply button
- View application status

**Admin View**:
- See all drives
- Create/Edit/Delete actions
- Publish/Close actions

**API Integration**:
- GET /api/v1/drives
- GET /api/v1/drives/published
- GET /api/v1/drives/{id}
- POST /api/v1/drives
- PUT /api/v1/drives/{id}
- POST /api/v1/drives/{id}/publish
- POST /api/v1/drives/{id}/close
- DELETE /api/v1/drives/{id}

### 7.7 Applications Page (src/pages/Applications.tsx)

**Features**:
- View my applications (student)
- View all applications (admin)
- Filter by status
- View application details
- Update application status (admin)

**Components**:
- ApplicationList - List with filters
- ApplicationCard - Card component
- ApplicationDetails - Detail modal
- StatusUpdateForm - Update status form

**Status Types**:
- Applied
- Shortlisted
- Interview Scheduled
- Selected
- Rejected

**Student View**:
- See own applications
- View status and details
- See company and drive info

**Admin View**:
- See all applications
- Filter by drive
- Update status
- Add rejection reason

**API Integration**:
- GET /api/v1/applications/my-applications
- GET /api/v1/applications/drive/{id}
- GET /api/v1/applications/{id}
- POST /api/v1/applications
- PUT /api/v1/applications/{id}/status
- GET /api/v1/applications

### 7.8 Assessments Page (src/pages/Assessments.tsx)

**Features**:
- List all assessments
- View assessment details
- Take assessment (student)
- Submit assessment
- View scores (student)
- View all scores (admin)
- Create/Edit/Delete assessment (admin)

**Components**:
- AssessmentList - List view
- AssessmentCard - Card component
- AssessmentForm - Create/Edit form
- AssessmentTaker - Take assessment interface
- ScoreDisplay - Show results

**Student Features**:
- View available assessments
- Take assessment (input score)
- View submitted scores
- See pass/fail status

**Admin Features**:
- Create assessment (title, description, total marks, passing marks)
- Edit assessment
- Delete assessment
- View all student scores

**API Integration**:
- GET /api/v1/assessments
- GET /api/v1/assessments/{id}
- POST /api/v1/assessments
- PUT /api/v1/assessments/{id}
- DELETE /api/v1/assessments/{id}
- POST /api/v1/assessments/{id}/submit
- GET /api/v1/assessments/my-scores
- GET /api/v1/assessments/{id}/scores

### 7.9 Analytics Page (src/pages/Analytics.tsx)

**Features**:
- Overview statistics
- Top hiring companies chart
- Branch-wise placement stats
- Full report view

**Components**:
- StatsCard - Display metrics
- ChartCard - Chart container
- DataTable - Tabular data
- ExportButton - Export functionality (optional)

**Metrics Displayed**:
- Total students
- Total companies
- Total applications
- Placement rate (%)
- Highest package
- Average package

**Charts** (using Recharts or Chart.js):
- Bar chart: Top hiring companies
- Pie chart: Branch distribution
- Line chart: Placement trends (optional)

**Tables**:
- Branch-wise statistics
- Top companies list

**API Integration**:
- GET /api/v1/analytics/overview
- GET /api/v1/analytics/top-companies
- GET /api/v1/analytics/branch-stats
- GET /api/v1/analytics/full-report

**Access**: Admin only

### 7.10 Not Found Page (src/pages/NotFound.tsx)

**Features**:
- 404 error message
- Return to home button
- Suggested links

---

## 8. UI/UX Design System

### 8.1 Color Palette

**Primary Colors**:
- Primary Blue: #3B82F6 (buttons, links, highlights)
- Primary Dark: #1E40AF (hover states)
- Success Green: #10B981 (success messages)
- Warning Yellow: #F59E0B (warnings)
- Error Red: #EF4444 (errors)
- Gray Scale: #6B7280, #9CA3AF, #D1D5DB, #E5E7EB, #F3F4F6, #F9FAFB

**Background**:
- Main: #FFFFFF
- Secondary: #F9FAFB
- Dark: #111827

**Text**:
- Primary: #111827
- Secondary: #6B7280
- Muted: #9CA3AF

### 8.2 Typography

**Font Family**: Inter (Google Fonts)

**Font Sizes**:
- xs: 0.75rem (12px)
- sm: 0.875rem (14px)
- base: 1rem (16px)
- lg: 1.125rem (18px)
- xl: 1.25rem (20px)
- 2xl: 1.5rem (24px)
- 3xl: 1.875rem (30px)
- 4xl: 2.25rem (36px)

**Font Weights**:
- Normal: 400
- Medium: 500
- Semibold: 600
- Bold: 700

### 8.3 Spacing

**Base Unit**: 4px

**Spacing Scale**:
- 1: 4px
- 2: 8px
- 3: 12px
- 4: 16px
- 5: 20px
- 6: 24px
- 8: 32px
- 10: 40px
- 12: 48px
- 16: 64px

### 8.4 Components

**Button Variants**:
- Primary (blue)
- Secondary (gray)
- Success (green)
- Danger (red)
- Outline
- Ghost

**Button Sizes**:
- Small (sm)
- Medium (md)
- Large (lg)

**Form Inputs**:
- Text input
- Email input
- Password input
- Select dropdown
- Textarea
- File upload
- Checkbox
- Radio

**Cards**:
- Default card
- Elevated card (shadow)
- Bordered card

**Tables**:
- Striped rows
- Hover effect
- Sortable headers
- Pagination

---

## 9. State Management

### 9.1 Server State (React Query)

**Usage**:
- API data fetching
- Caching
- Background refetching
- Optimistic updates

**Example**:
```typescript
const { data: companies, isLoading } = useQuery({
  queryKey: ['companies'],
  queryFn: () => companyService.getAll(),
});
```

### 9.2 Client State (Context API)

**Usage**:
- Authentication state
- User information
- UI state (sidebar, theme)

**Contexts**:
- AuthContext - User authentication
- ThemeContext - Dark/light mode (optional)

---

## 10. Implementation Phases

### Phase 1: Project Setup (Day 1)
1. Initialize Vite + React + TypeScript project
2. Install dependencies
3. Configure Tailwind CSS
4. Set up folder structure
5. Configure routing
6. Create base layout components
7. Set up API client with Axios
8. Create authentication context

**Deliverables**:
- Working dev server
- Routing configured
- API client ready
- Auth context functional

### Phase 2: Authentication Pages (Day 2)
1. Create Login page with form
2. Create Register page with form
3. Implement form validation (Zod)
4. Connect to auth API
5. Implement protected routes
6. Add loading states and error handling

**Deliverables**:
- Working login/register
- Token management
- Protected route wrapper

### Phase 3: Layout & Navigation (Day 3)
1. Create Header component
2. Create Sidebar component
3. Create Footer component
4. Implement responsive layout
5. Add navigation links
6. Implement logout functionality
7. Add user menu dropdown

**Deliverables**:
- Complete layout system
- Responsive navigation
- User menu

### Phase 4: Dashboard (Day 4)
1. Create Dashboard page
2. Add statistics cards
3. Add recent activity section
4. Implement role-based content
5. Add quick action buttons

**Deliverables**:
- Functional dashboard
- Stats display
- Role-based UI

### Phase 5: Student Profile (Day 5)
1. Create Student Profile page
2. Add profile view section
3. Add edit profile form
4. Implement resume upload
5. Add skills/projects management
6. Connect to API

**Deliverables**:
- Complete profile management
- Resume upload functionality

### Phase 6: Companies Module (Day 6-7)
1. Create Companies list page
2. Add search functionality
3. Create company detail view
4. Create company form (admin)
5. Implement CRUD operations
6. Add pagination

**Deliverables**:
- Full companies module
- Search and filter
- Admin CRUD

### Phase 7: Placement Drives Module (Day 8-9)
1. Create Drives list page
2. Add filters (status, company)
3. Create drive detail view
4. Create drive form (admin)
5. Implement publish/close actions
6. Add apply functionality (student)

**Deliverables**:
- Complete drives module
- Status management
- Application integration

### Phase 8: Applications Module (Day 10)
1. Create Applications list page
2. Add status filters
3. Create application detail view
4. Implement status update (admin)
5. Add rejection reason field
6. Show company/drive info

**Deliverables**:
- Full applications module
- Status tracking
- Admin management

### Phase 9: Assessments Module (Day 11-12)
1. Create Assessments list page
2. Create assessment form (admin)
3. Implement assessment taker (student)
4. Add score submission
5. Create scores view
6. Add pass/fail indicators

**Deliverables**:
- Complete assessments module
- Score calculation
- Admin/student views

### Phase 10: Analytics Module (Day 13)
1. Create Analytics page
2. Add overview statistics
3. Create charts (top companies, branch stats)
4. Implement data tables
5. Add loading states
6. Format data display

**Deliverables**:
- Analytics dashboard
- Charts and tables
- Admin-only access

### Phase 11: Polish & Testing (Day 14)
1. Add loading spinners
2. Add error boundaries
3. Implement error handling
4. Add toast notifications
5. Test all flows
6. Fix bugs
7. Optimize performance

**Deliverables**:
- Polished UI
- Error handling
- Performance optimized

### Phase 12: Deployment Prep (Day 15)
1. Build production bundle
2. Test production build
3. Create environment configs
4. Write deployment README
5. Optimize assets
6. Add meta tags

**Deliverables**:
- Production-ready build
- Deployment documentation

---

## 11. Component Library

### 11.1 UI Components (src/components/ui/)

**Button**:
- Variants: primary, secondary, success, danger, outline, ghost
- Sizes: sm, md, lg
- Loading state
- Icon support
- Disabled state

**Input**:
- Text, email, password types
- Label and error message
- Icon support
- Required indicator

**Card**:
- Title and description
- Content slot
- Footer slot
- Variants: default, elevated, bordered

**Modal**:
- Title and content
- Close button
- Backdrop click to close
- Size variants: sm, md, lg, xl

**Table**:
- Striped rows
- Hover effect
- Sortable columns
- Pagination
- Empty state

**Badge**:
- Variants: primary, secondary, success, warning, danger
- Sizes: sm, md, lg

**Spinner**:
- Sizes: sm, md, lg
- Colors: primary, white

**Alert**:
- Variants: info, success, warning, error
- Dismissible
- Icon support

### 11.2 Layout Components (src/components/layout/)

**Header**:
- Logo
- Navigation links
- User menu
- Mobile menu toggle

**Sidebar**:
- Navigation menu
- Active link indicator
- Collapsible sections
- Mobile responsive

**Footer**:
- Copyright
- Links
- Version info

**Layout**:
- Wraps pages
- Includes Header, Sidebar, Footer
- Responsive behavior

### 11.3 Auth Components (src/components/auth/)

**ProtectedRoute**:
- Checks authentication
- Shows loading
- Redirects to login

**RoleGuard**:
- Checks user role
- Redirects if unauthorized
- Renders children if authorized

---

## 12. API Integration Details

### 12.1 Authentication Flow

**Login**:
1. User enters credentials
2. POST /api/v1/auth/login
3. Store token in localStorage
4. Store user data in context
5. Redirect to dashboard

**Register**:
1. User fills registration form
2. POST /api/v1/auth/register
3. Auto-login with credentials
4. Store token and user data
5. Redirect to dashboard

**Token Refresh**:
1. Interceptor detects 401
2. POST /api/v1/auth/refresh
3. Update token in localStorage
4. Retry original request

**Logout**:
1. Clear localStorage
2. Clear context state
3. Redirect to login

### 12.2 Error Handling

**Global Error Handling**:
- 401: Redirect to login
- 403: Show forbidden message
- 404: Show not found
- 500: Show error message
- Network errors: Show retry button

**Toast Notifications**:
- Success: Green toast
- Error: Red toast
- Warning: Yellow toast
- Info: Blue toast

---

## 13. Responsive Design

### 13.1 Breakpoints

**Tailwind Breakpoints**:
- sm: 640px (mobile landscape)
- md: 768px (tablet)
- lg: 1024px (laptop)
- xl: 1280px (desktop)
- 2xl: 1536px (large desktop)

### 13.2 Responsive Behavior

**Mobile (< 768px)**:
- Hamburger menu
- Full-width cards
- Stacked layouts
- Bottom navigation (optional)

**Tablet (768px - 1024px)**:
- Collapsible sidebar
- 2-column grids
- Adjusted spacing

**Desktop (> 1024px)**:
- Full sidebar
- Multi-column layouts
- Maximum width container (1280px)

---

## 14. Performance Optimization

### 14.1 Code Splitting
- Route-based code splitting
- Lazy load pages
- Dynamic imports for heavy components

### 14.2 Asset Optimization
- Image optimization
- Font subsetting
- Tree shaking
- Minification

### 14.3 Caching Strategy
- React Query caching
- LocalStorage for auth
- Service worker (optional)

---

## 15. Security Considerations

### 15.1 Authentication
- Store tokens in localStorage
- Send tokens in Authorization header
- Auto-refresh before expiry
- Clear tokens on logout

### 15.2 Authorization
- Check roles before rendering
- Hide admin routes from students
- Validate on backend (already implemented)

### 15.3 XSS Prevention
- React's built-in XSS protection
- Sanitize user inputs
- Avoid innerHTML

### 15.4 CSRF Protection
- CORS configured on backend
- Same-origin policy

---

## 16. Testing Strategy

### 16.1 Unit Tests
- Test utility functions
- Test custom hooks
- Test components in isolation

### 16.2 Integration Tests
- Test API service functions
- Test authentication flow
- Test form submissions

### 16.3 E2E Tests (Optional)
- Test critical user flows
- Login → Dashboard → Actions
- Use Playwright or Cypress

---

## 17. Deployment

### 17.1 Build Process
```bash
npm run build
```
- Output: `dist/` folder
- Optimized assets
- Minified code

### 17.2 Deployment Options
1. **Vercel** (Recommended)
   - Connect GitHub repo
   - Auto-deploy on push
   - Preview deployments

2. **Netlify**
   - Connect GitHub repo
   - Auto-deploy
   - Form handling

3. **Render**
   - Static site hosting
   - Connect to same backend

### 17.3 Environment Variables
- Production API URL
- App name
- Feature flags (optional)

---

## 18. Development Workflow

### 18.1 Git Workflow
```
main (production)
  └── develop (staging)
       └── feature/* (new features)
       └── bugfix/* (bug fixes)
```

### 18.2 Commit Convention
- feat: New feature
- fix: Bug fix
- docs: Documentation
- style: Formatting
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance

---

## 19. Timeline Summary

| Phase | Duration | Deliverable |
|-------|----------|-------------|
| 1. Project Setup | 1 day | Working dev environment |
| 2. Authentication | 1 day | Login/Register pages |
| 3. Layout & Navigation | 1 day | Complete layout system |
| 4. Dashboard | 1 day | Dashboard page |
| 5. Student Profile | 1 day | Profile management |
| 6. Companies Module | 2 days | Companies CRUD |
| 7. Placement Drives | 2 days | Drives management |
| 8. Applications | 1 day | Applications module |
| 9. Assessments | 2 days | Assessments module |
| 10. Analytics | 1 day | Analytics dashboard |
| 11. Polish & Testing | 1 day | Bug fixes and polish |
| 12. Deployment Prep | 1 day | Production build |

**Total Estimated Time**: 14 days

---

## 20. Success Criteria

### 20.1 Functional Requirements
- ✅ All 10 pages implemented
- ✅ Authentication flow working
- ✅ All CRUD operations functional
- ✅ Responsive design
- ✅ Role-based access control

### 20.2 Technical Requirements
- ✅ TypeScript strict mode
- ✅ No console errors
- ✅ Loading states for all async operations
- ✅ Error handling for all API calls
- ✅ Form validation with Zod

### 20.3 UI/UX Requirements
- ✅ Professional design
- ✅ Consistent styling
- ✅ Intuitive navigation
- ✅ Fast loading (< 2s initial load)
- ✅ Mobile responsive

---

## 21. Next Steps

1. **Review this plan** with stakeholders
2. **Set up development environment**
3. **Initialize Vite project**
4. **Install dependencies**
5. **Begin Phase 1 implementation**
6. **Follow TDD approach** (optional)
7. **Regular code reviews**
8. **Continuous testing**

---

## 22. Notes

- Backend API is already deployed and functional
- All API endpoints are documented at /docs
- JWT authentication is required for most endpoints
- Role-based access (admin/student) is implemented
- File upload (resume) requires Cloudinary credentials
- Email notifications are optional

**Backend Documentation**: https://careerforge-tw8t.onrender.com/docs