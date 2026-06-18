# CareerForge Frontend

Modern React + TypeScript frontend for CareerForge placement portal.

## Tech Stack

- **React 18** - UI library
- **TypeScript 5** - Type safety
- **Vite 5** - Build tool
- **React Router 6** - Routing
- **Tailwind CSS 3** - Styling
- **React Hook Form + Zod** - Form validation
- **Axios** - HTTP client
- **React Query** - Server state management
- **React Hot Toast** - Notifications
- **Lucide React** - Icons

## Getting Started

### Prerequisites

- Node.js 18+
- npm or yarn

### Installation

1. **Navigate to frontend directory**
   ```bash
   cd careerforge-frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Update `.env` with your backend URL if needed.

4. **Start development server**
   ```bash
   npm run dev
   ```

5. **Open browser**
   ```
   http://localhost:3000
   ```

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build
- `npm run lint` - Run ESLint
- `npm run type-check` - Run TypeScript compiler

## Project Structure

```
careerforge-frontend/
├── src/
│   ├── components/       # Reusable components
│   │   ├── auth/        # Authentication components
│   │   ├── layout/      # Layout components
│   │   └── ui/          # UI components
│   ├── contexts/        # React contexts
│   ├── hooks/           # Custom hooks
│   ├── pages/           # Page components
│   ├── services/        # API services
│   ├── types/           # TypeScript types
│   ├── utils/           # Utility functions
│   ├── App.tsx          # Main app component
│   └── main.tsx         # Entry point
├── public/              # Static assets
└── package.json
```

## Features

- ✅ JWT Authentication
- ✅ Role-based access (Admin/Student)
- ✅ Responsive design
- ✅ Form validation with Zod
- ✅ Loading states
- ✅ Error handling
- ✅ Toast notifications
- ✅ Protected routes

## Pages

1. **Login** - User authentication
2. **Register** - New user registration
3. **Dashboard** - Overview and quick actions
4. **Student Profile** - Profile management
5. **Companies** - Company listings
6. **Placement Drives** - Drive management
7. **Applications** - Application tracking
8. **Assessments** - Assessment management
9. **Analytics** - Statistics and insights
10. **404** - Not found page

## Backend API

- **URL**: https://careerforge-tw8t.onrender.com
- **Docs**: https://careerforge-tw8t.onrender.com/docs

## Building for Production

```bash
npm run build
```

The build output will be in the `dist/` directory.

## Deployment

### Vercel

1. Push code to GitHub
2. Import project in Vercel
3. Add environment variable `VITE_API_URL`
4. Deploy

### Netlify

1. Build the project: `npm run build`
2. Deploy the `dist/` folder
3. Configure redirects for SPA routing

### Render

1. Connect GitHub repository
2. Set build command: `npm run build`
3. Set publish directory: `dist`
4. Add environment variables

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_URL` | Backend API URL | Yes |
| `VITE_APP_NAME` | Application name | No |

## License

MIT