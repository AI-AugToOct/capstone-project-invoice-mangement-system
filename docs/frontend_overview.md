# Frontend Architecture Overview

## 🎨 System Architecture

The **Smart Invoice Analyzer** frontend is built using **Next.js 14** with **React 18**, **TypeScript**, **Tailwind CSS**, and **shadcn/ui** components. The interface is fully localized in **Arabic (RTL)** with dark mode support.

### Technology Stack

- **Framework**: Next.js 14.2.3 (App Router)
- **UI Library**: React 18.3.1
- **Language**: TypeScript 5.4.5
- **Styling**: Tailwind CSS 3.4.3
- **Components**: shadcn/ui (Radix UI primitives)
- **Animations**: Framer Motion 11.2.10
- **Charts**: Recharts 2.12.7
- **Theme**: next-themes 0.4.6
- **PDF Generation**: jsPDF 3.0.3
- **State Management**: React Hooks (useState, useEffect)

---

## 📂 Project Structure

```
frontend-nextjs/
├── app/                          # Next.js App Router
│   ├── layout.tsx                # Root layout with Navbar & theme
│   ├── page.tsx                  # Home page (landing)
│   ├── globals.css               # Global styles & animations
│   ├── upload/
│   │   └── page.tsx              # Invoice upload & camera capture
│   ├── invoices/
│   │   └── page.tsx              # Invoice list with filters
│   ├── dashboard/
│   │   └── page.tsx              # Analytics dashboard
│   └── chat/
│       └── page.tsx              # AI chat interface
├── components/                   # Reusable components
│   ├── Navbar.tsx                # Navigation bar with theme toggle
│   ├── InvoiceResultCard.tsx     # Display analyzed invoice
│   ├── CameraCapture.tsx         # Camera input component
│   ├── ImageModal.tsx            # Full-screen image viewer
│   ├── GlobalLoader.tsx          # Loading animation
│   ├── ThemeToggle.tsx           # Dark mode switcher
│   ├── theme-provider.tsx        # Theme context provider
│   └── ui/                       # shadcn/ui primitives
│       ├── button.tsx
│       ├── card.tsx
│       ├── dialog.tsx
│       ├── select.tsx
│       ├── toast.tsx
│       ├── progress.tsx
│       └── scroll-area.tsx
├── lib/                          # Utilities
│   ├── utils.ts                  # Class name helper (cn)
│   └── pdfUtils.ts               # PDF generation functions
├── tailwind.config.ts            # Tailwind configuration
├── next.config.js                # Next.js configuration
└── package.json                  # Dependencies
```

---

## 🎯 Core Pages

### 1. Home Page (`/`)

**Purpose**: Landing page with branding and call-to-action.

**Features**:
- Animated gradient background (`animate-gradient`)
- Hero section with brand name: **مُـفـــــوْتِــــر**
- Tagline: "مُـفـــــوْتِــــر — يحفظ،يدير، يحلل، ويختصر وقتك."
- Feature cards: Upload, Analytics, Chat, Management
- Benefit pills: Speed, Security, Time-saving, Accuracy
- Scroll indicator with smooth animation
- Responsive design (mobile-first)

**Design**:
- Full-width layout (no container constraints)
- Color palette: `#8dbcc7` (teal) + `#d4a574` (gold)
- Framer Motion animations on scroll
- Cairo font family

---

### 2. Upload Page (`/upload`)

**Purpose**: Upload or capture invoice images for AI analysis.

**Features**:
- File upload via drag-and-drop or file picker
- Camera capture using `navigator.mediaDevices.getUserMedia`
- Real-time progress bar during upload & analysis
- Image preview before submission
- Display analyzed results in `InvoiceResultCard`

**User Flow**:
```
1. User selects file or captures from camera
   ↓
2. Frontend sends to POST /upload/
   ↓
3. Receives Supabase image URL
   ↓
4. Frontend sends URL to POST /vlm/analyze
   ↓
5. Displays analyzed data:
   - Business category + Invoice type
   - Invoice details (number, date, vendor, branch, phone)
   - Financial summary (subtotal, tax, discounts, total)
   - AI insight in Arabic
   - Line items table
   ↓
6. User can reset and upload new invoice
```

**Components Used**:
- `Card` for layout structure
- `Button` for actions
- `Progress` for upload status
- `InvoiceResultCard` for results display
- `CameraCapture` for camera input
- `GlobalLoader` during processing

---

### 3. Invoices Page (`/invoices`)

**Purpose**: Browse and manage all uploaded invoices.

**Features**:
- Grid layout of invoice cards
- Filter by category/type (`Select` dropdown)
- Real-time filtering (no page reload)
- Invoice card display:
  - Image thumbnail (clickable for full view)
  - Vendor name + Invoice type badge
  - Date, cashier, branch
  - Total, discount, payment method
  - AI insight text
- PDF download button (downloads original image as PDF)
- Image modal for enlarged view with zoom/pan
- Responsive grid: 1 column (mobile) → 2 (tablet) → 3 (desktop)

**API Integration**:
```typescript
const fetchInvoices = async () => {
  const response = await fetch(`${API_BASE}/invoices/all`);
  const data = await response.json();
  setInvoices(data);
};
```

**Filtering Logic**:
```typescript
useEffect(() => {
  if (categoryFilter === "all") {
    setFilteredInvoices(invoices);
  } else {
    const filtered = invoices.filter((inv) => 
      inv.invoice_type?.trim() === categoryFilter.trim()
    );
    setFilteredInvoices(filtered);
  }
}, [categoryFilter, invoices]);
```

**PDF Generation**:
- Uses `jsPDF` to embed original image
- Full-page PDF (A4 portrait)
- Downloads as: `{vendor}_{invoice_number}.pdf`

---

### 4. Dashboard Page (`/dashboard`)

**Purpose**: Visualize spending analytics and insights.

**Features**:
- **Interactive Filters**:
  - Category filter (مطعم, مقهى, صيدلية, etc.)
  - Month filter (1-12)
  - Payment method filter (Cash, Visa, Mada, etc.)
  - Filters update all data instantly
  
- **Statistics Cards**:
  - Total invoices count
  - Total spending (sum of all invoices)
  - Average spending per invoice
  - Most frequent vendor

- **Charts** (Recharts):
  - **Category Pie Chart**: Spending distribution by business type
    - Donut style with inner/outer radius
    - Separate legend below chart (prevents label overlap)
    - Pastel color palette
  - **Monthly Area Chart**: Spending trend over time
  - **Payment Method Bar Chart**: Spending by payment type
  - **Day of Week Radar Chart**: Spending patterns

- **Smart Insights**:
  - 6 dynamic Arabic insights generated from filtered data
  - Examples:
    - "لديك ١٥ فاتورة مقهى — يبدو أنك من محبي القهوة!"
    - "أكثر طرق الدفع استخدامًا: Visa"

- **Top Vendors Table**:
  - Top 5 vendors by frequency
  - Total spending per vendor

**Design**:
- Fixed animated gradient background
- 2-column responsive grid layout
- Backdrop blur on cards
- Hover animations on all interactive elements
- Loading state with Arabic text

**API Integration**:
```typescript
// Fetch all invoices for filtering
const response = await fetch(`${API_BASE}/invoices/all`);

// Fetch dashboard stats
const statsResponse = await fetch(`${API_BASE}/dashboard/stats`);
```

---

### 5. Chat Page (`/chat`)

**Purpose**: Natural language Q&A about invoices.

**Features**:
- Chat interface (similar to ChatGPT)
- User messages (right-aligned)
- AI messages (left-aligned)
- Message history with scroll area
- Typing animation for AI responses
- Invoice cards inside chat bubbles:
  - Vendor name + invoice type
  - Date + total amount
  - Image thumbnail (clickable)
  - PDF download button
- Handles multiple invoices per response
- Dark mode support

**User Flow**:
```
1. User types question: "أرسل لي فواتير دانكن"
   ↓
2. Frontend sends to POST /chat/ask
   ↓
3. Backend uses hybrid intelligence:
   - SQL mode for aggregations
   - RAG mode for semantic search
   - Retrieval mode for specific vendors
   ↓
4. Returns answer + invoices array
   ↓
5. Frontend displays:
   - Text answer
   - Invoice cards with images
```

**Message Structure**:
```typescript
interface Message {
  role: "user" | "assistant";
  content: string;
  invoices?: Invoice[];
}
```

**Components**:
- `ScrollArea` for message list
- `Card` for invoice preview
- `ImageModal` for full-size view
- `Button` for PDF download
- `GlobalLoader` during AI processing

---

## 🎨 Design System

### Color Palette

**Primary**: `#8dbcc7` (Teal/Cyan)
- Used for: Navbar active links, primary buttons, accents

**Secondary**: `#d4a574` (Gold/Beige)
- Used for: Secondary buttons, gradients, highlights

**Gradients**:
```css
from-[#8dbcc7] to-[#d4a574]  /* Teal to Gold */
from-[#8dbcc7] via-[#a0cad4] to-[#d4a574]  /* Extended gradient */
```

**Background Animations**:
```css
/* Light mode */
.animate-gradient {
  background: linear-gradient(
    -45deg, 
    #e0f7fa,  /* Light teal */
    #fff9e6,  /* Light gold */
    #f0f4f8,  /* Light blue-gray */
    #e8f5f1,  /* Light mint */
    #e0f7fa
  );
  background-size: 400% 400%;
  animation: gradientShift 25s ease infinite;
}

/* Dark mode */
.dark .animate-gradient {
  background: linear-gradient(
    -45deg, 
    #0f172a,  /* Dark slate */
    #1e293b,  /* Dark gray */
    #334155,  /* Medium gray */
    #1e1b4b,  /* Dark purple */
    #0f172a
  );
}
```

### Typography

**Primary Font**: Cairo (Arabic-optimized)
- Weights: 400 (regular), 600 (semibold), 700 (bold), 900 (black)

**Font Sizes**:
- Hero: `text-7xl md:text-8xl lg:text-9xl` (72px → 96px → 128px)
- Page titles: `text-5xl md:text-6xl` (48px → 60px)
- Card titles: `text-xl` (20px)
- Body text: `text-base` (16px)

### Spacing & Layout

- **Container**: `max-w-7xl mx-auto px-6 md:px-16 lg:px-24 xl:px-32`
- **Card padding**: `p-6`
- **Section spacing**: `space-y-8`
- **Grid gaps**: `gap-6`

### Shadows & Effects

```css
/* Card shadows */
shadow-xl hover:shadow-2xl

/* Backdrop blur */
backdrop-blur-md

/* Rounded corners */
rounded-2xl (16px)
rounded-xl (12px)
```

---

## 🔄 State Management

### React Hooks Used

1. **useState**: Component-level state
   ```typescript
   const [invoices, setInvoices] = useState<Invoice[]>([]);
   const [loading, setLoading] = useState(false);
   ```

2. **useEffect**: Data fetching & side effects
   ```typescript
   useEffect(() => {
     fetchInvoices();
   }, []);
   ```

3. **useTheme**: Dark mode management (next-themes)
   ```typescript
   const { theme, setTheme } = useTheme();
   ```

4. **useToast**: Notifications (shadcn/ui)
   ```typescript
   toast({ 
     title: "نجح!", 
     description: "تم رفع الفاتورة" 
   });
   ```

---

## 🌐 API Integration

### Base URL

```typescript
export const API_BASE = 
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://127.0.0.1:8000";
```

### Fetch Examples

**Upload Invoice**:
```typescript
const formData = new FormData();
formData.append("file", file);

const response = await fetch(`${API_BASE}/upload/`, {
  method: "POST",
  body: formData,
});

const data = await response.json();
const imageUrl = data.url;
```

**Analyze Invoice**:
```typescript
const response = await fetch(`${API_BASE}/vlm/analyze`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ image_url: imageUrl }),
});

const result = await response.json();
```

**Get All Invoices**:
```typescript
const response = await fetch(`${API_BASE}/invoices/all`);
const invoices = await response.json();
```

**Chat**:
```typescript
const response = await fetch(`${API_BASE}/chat/ask`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({ question: userInput }),
});

const data = await response.json();
```

---

## 🎭 Animations & Interactions

### Framer Motion Variants

**Page Entry**:
```typescript
<motion.div
  initial={{ opacity: 0, y: 30 }}
  animate={{ opacity: 1, y: 0 }}
  transition={{ duration: 0.8 }}
>
```

**Card Hover**:
```typescript
<motion.div
  whileHover={{ scale: 1.05 }}
  whileTap={{ scale: 0.95 }}
>
```

**Scroll Animations**:
```typescript
<motion.div
  initial={{ opacity: 0, y: 50 }}
  whileInView={{ opacity: 1, y: 0 }}
  viewport={{ once: true, amount: 0.3 }}
>
```

### CSS Transitions

```css
/* Smooth transitions */
transition-all duration-300

/* Hover scale */
hover:scale-105 transition-transform duration-300

/* Shadow transitions */
shadow-xl hover:shadow-2xl transition-all duration-500
```

---

## 📱 Responsive Design

### Breakpoints (Tailwind)

- **sm**: 640px (mobile landscape)
- **md**: 768px (tablet)
- **lg**: 1024px (laptop)
- **xl**: 1280px (desktop)
- **2xl**: 1536px (large desktop)

### Responsive Patterns

**Grid**:
```typescript
<div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
```

**Text**:
```typescript
<h1 className="text-4xl md:text-5xl lg:text-6xl">
```

**Padding**:
```typescript
<div className="px-6 md:px-16 lg:px-24 xl:px-32">
```

**Navigation**:
```typescript
<span className="hidden sm:inline">
```

---

## 🌙 Dark Mode Implementation

### Theme Provider

```typescript
// app/layout.tsx
<ThemeProvider
  attribute="class"
  defaultTheme="system"
  enableSystem
  disableTransitionOnChange
>
  {children}
</ThemeProvider>
```

### Theme Toggle Component

```typescript
<DropdownMenu>
  <DropdownMenuItem onClick={() => setTheme("light")}>
    فاتح
  </DropdownMenuItem>
  <DropdownMenuItem onClick={() => setTheme("dark")}>
    داكن
  </DropdownMenuItem>
  <DropdownMenuItem onClick={() => setTheme("system")}>
    النظام
  </DropdownMenuItem>
</DropdownMenu>
```

### Dark Mode Styles

```css
/* Background */
bg-white dark:bg-gray-900

/* Text */
text-gray-900 dark:text-white

/* Cards */
bg-white/80 dark:bg-gray-900/80
```

---

## 🛠️ Component Library (shadcn/ui)

### Components Used

1. **Button**: Primary/secondary actions
2. **Card**: Content containers
3. **Dialog**: Modals (image viewer)
4. **Select**: Dropdown filters
5. **Toast**: Notifications
6. **Progress**: Upload/analysis progress
7. **ScrollArea**: Chat messages
8. **DropdownMenu**: Theme toggle

### Custom Components

1. **Navbar**: Navigation with theme toggle
2. **InvoiceResultCard**: Display analyzed invoice
3. **CameraCapture**: Camera input
4. **ImageModal**: Full-screen image viewer with zoom
5. **GlobalLoader**: Loading animation
6. **ThemeToggle**: Dark mode switcher

---

## 📊 Frontend Component Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      Next.js App (App Router)                    │
└─────────────────────────────────────────────────────────────────┘
                                 │
                    ┌────────────┼────────────┐
                    │            │            │
         ┌──────────▼───┐  ┌────▼─────┐  ┌──▼──────────┐
         │   Layout     │  │  Navbar  │  │   Theme     │
         │   (Root)     │  │          │  │   Provider  │
         └──────────────┘  └──────────┘  └─────────────┘
                    │
        ┌───────────┼───────────┬───────────┬───────────┐
        │           │           │           │           │
   ┌────▼────┐ ┌───▼─────┐ ┌──▼──────┐ ┌─▼────────┐ ┌▼──────┐
   │  Home   │ │ Upload  │ │ Invoices│ │Dashboard │ │ Chat  │
   │  Page   │ │  Page   │ │  Page   │ │   Page   │ │ Page  │
   └─────────┘ └────┬────┘ └────┬────┘ └────┬─────┘ └───┬───┘
                    │           │           │           │
                    └───────────┼───────────┼───────────┘
                                │           │
                    ┌───────────▼───────────▼───────────┐
                    │       API Layer (fetch)           │
                    └───────────┬───────────────────────┘
                                │
                    ┌───────────▼───────────┐
                    │   FastAPI Backend     │
                    │   (127.0.0.1:8000)    │
                    └───────────────────────┘
```

---

## 🚀 Build & Deployment

### Development Mode

```bash
cd frontend-nextjs
npm install
npm run dev
```

Runs on: `http://localhost:3000`

### Production Build

```bash
npm run build
npm start
```

### Environment Variables

Create `.env.local`:

```env
NEXT_PUBLIC_API_BASE_URL=http://127.0.0.1:8000
NEXT_PUBLIC_SUPABASE_URL=https://[project].supabase.co
NEXT_PUBLIC_SUPABASE_KEY=your_anon_key
```

---

## 🔍 Key Features Summary

1. ✅ **Full Arabic UI (RTL)**: All text and layout in Arabic
2. ✅ **Dark Mode**: System-aware theme switching
3. ✅ **Responsive**: Mobile-first design
4. ✅ **Animations**: Smooth Framer Motion effects
5. ✅ **Real-time Filtering**: Instant updates without reload
6. ✅ **Camera Capture**: Native device camera access
7. ✅ **Image Viewer**: Zoom, pan, download
8. ✅ **PDF Generation**: Download invoices as PDF
9. ✅ **Charts**: Interactive Recharts visualizations
10. ✅ **AI Chat**: Natural language interface

---

## 📝 Code Style & Best Practices

### TypeScript

- Use interfaces for type definitions
- Avoid `any` type (use `unknown` if needed)
- Enable strict mode

### React

- Use functional components with hooks
- Avoid prop drilling (use context when needed)
- Memoize expensive calculations with `useMemo`

### CSS/Tailwind

- Use utility classes over custom CSS
- Follow mobile-first responsive design
- Use `cn()` helper for conditional classes

### Accessibility

- Use semantic HTML tags
- Add ARIA labels for screen readers
- Ensure keyboard navigation
- Maintain color contrast ratios

---

**Last Updated**: October 7, 2025  
**Version**: 1.0.0

