# TalentMatch AI - Frontend

Next.js frontend for the TalentMatch AI application.

## Features

- 📄 **Drag & Drop CV Upload**: Easy PDF upload with react-dropzone
- ✏️ **Manual Text Input**: Alternative paste option for CV text
- 📊 **Interactive Results**: Visual score display with tabs for detailed analysis
- 📱 **Responsive Design**: Works on desktop, tablet, and mobile
- 🎨 **Modern UI**: Built with Tailwind CSS and shadcn/ui

## Tech Stack

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Components**: shadcn/ui
- **State**: Zustand
- **Charts**: Recharts
- **Icons**: Lucide React

## Getting Started

### Prerequisites

- Node.js 18+
- Backend API running (see `apps/api`)

### Development

```bash
# Install dependencies
npm install

# Run development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
app/
├── layout.tsx        # Root layout with providers
├── page.tsx          # Landing page
├── analyze/
│   └── page.tsx      # Main analysis flow
├── globals.css       # Global styles
components/
├── ui/               # shadcn/ui components
├── layout/           # Layout components (Navbar, Footer)
├── cv-upload/        # CV upload components
├── job-input/        # Job description input
└── results/          # Results display
lib/
├── api/              # API client
├── store/            # Zustand stores
└── utils.ts          # Utilities
types/
└── index.ts          # TypeScript types
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `NEXT_PUBLIC_API_URL` | Backend API URL | `http://localhost:8000/api/v1` |

## Key Components

### CVUploadZone
Handles PDF file uploads with drag & drop support.

### JobInputForm
Form for entering job descriptions with automatic skill detection.

### ScoreDisplay
Visual display of the match score with progress bars for each section.

### AnalysisDetails
Tabbed interface showing skills comparison, strengths, gaps, and recommendations.
