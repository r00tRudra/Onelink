# FRONTEND STRUCTURE

This document outlines the enhanced frontend architecture with separated concerns, reusable components, and modular styling.

## 📁 Directory Structure

```
FRONTEND/
├── auth/                      # Authentication pages
│   └── sign-in.html          # OAuth login page (formerly login.html)
│
├── pages/                      # Main application pages
│   ├── landing.html           # Public landing page (formerly landing_before_login.html)
│   └── dashboard.html         # User dashboard (formerly landing_after_login.html)
│
├── shared/                     # Shared resources
│   ├── tokens.css            # CSS design tokens & variables
│   ├── reset.css             # CSS reset & base styles
│   ├── components.css        # Reusable component styles
│   ├── utilities.css         # Layout & utility classes
│   ├── responsive.css        # Responsive breakpoints
│   └── utils.js              # Shared JavaScript utilities
│
├── components/               # Reusable component templates
│   └── (future: isolated components)
│
├── assets/                   # Static assets
│   └── (images, icons, etc.)
│
└── [old files]              # Original files (can be removed after migration)
    ├── login.html
    ├── landing_before_login.html
    └── landing_after_login.html
```

## 🎨 Styling Architecture

### Design Tokens (`shared/tokens.css`)
Centralized CSS variables for:
- **Colors**: Primary, semantic (success, error, warning), neutral palette
- **Spacing**: Scale from `--space-xs` to `--space-12xl`
- **Border Radius**: From `--radius-sm` to `--radius-pill`
- **Typography**: Font families and sizes
- **Layout**: Sidebar width, max-width, container padding

### Layer System

1. **reset.css**: Browser resets, normalization, base animations
2. **components.css**: Reusable UI patterns
   - Buttons (primary, outline, ghost, danger, sizes)
   - Badges and pills
   - Cards and modals
   - Forms
   - Progress bars
   - Spinners
   - Toasts

3. **utilities.css**: Tailwind-like utility classes
   - Display & layout (flex, grid)
   - Spacing (margin, padding)
   - Typography (font sizes, weights, colors)
   - Sizing (width, height, max-width)
   - Positioning (fixed, absolute, sticky, z-index)
   - Effects (shadows, blur, opacity)
   - Animations (reveal, slide, fade)
  
     

4. **responsive.css**: Mobile-first breakpoints
   - `max-width: 1100px` (large tablets)
   - `max-width: 900px` (tablets)
   - `max-width: 700px` (mobile landscape)
   - `max-width: 540px` (mobile portrait)
   - `max-width: 420px` (small phones)

### Page-Specific Styles

Each HTML file includes inline `<style>` tags for page-specific styling:
- **auth/sign-in.html**: Authentication card, gradient backgrounds
- **pages/landing.html**: Hero section, features grid, CTA cards
- **pages/dashboard.html**: Sidebar layout, top bar, content grid

## 🔧 JavaScript Architecture (`shared/utils.js`)

Modular utility objects:

### `Auth`
```javascript
Auth.getToken()              // Get JWT token
Auth.getUser()               // Get user object
Auth.isAuthenticated()       // Check auth state
Auth.setToken(token)         // Store token
Auth.setUser(user)           // Store user data
Auth.clear()                 // Clear auth storage
Auth.logout()                // Logout (clears + navigates)
```

### `UI`
```javascript
UI.showToast(message)        // Show notification
UI.showLoading(element)      // Add loading state
UI.hideLoading(element)      // Remove loading state
UI.openModal(id)             // Show modal
UI.closeModal(id)            // Hide modal
UI.toggleModal(id)           // Toggle modal
```

### `DOM`
```javascript
DOM.qs(selector)             // querySelector
DOM.qsa(selector)            // querySelectorAll
DOM.byId(id)                 // getElementById
DOM.show/hide/toggle(elem)   // Show/hide elements
DOM.addClass/removeClass(elem, class)    // Class management
DOM.setText/setHTML(elem, value)         // Content manipulation
DOM.on/off(elem, event, handler)         // Event listeners
```

### `URL`
```javascript
URL.getParam(key)            // Get URL parameter
URL.getParams()              // Get all parameters object
URL.setParam(key, value)     // Update URL parameter
```

### `Storage`
```javascript
Storage.set(key, value)      // Store value (auto-serializes objects)
Storage.get(key)             // Retrieve value (auto-deserializes)
Storage.remove(key)          // Delete key
Storage.clear()              // Clear all storage
```

### `Observer`
```javascript
Observer.initReveal(threshold)  // Initialize reveal animations
```

### `Timing`
```javascript
Timing.debounce(func, delay)    // Debounced function
Timing.throttle(func, limit)    // Throttled function
```

### `API`
```javascript
API.get(endpoint)            // GET request
API.post(endpoint, data)     // POST request
API.put(endpoint, data)      // PUT request
API.delete(endpoint)         // DELETE request
```

## 📄 Pages

### Authentication Flow (`auth/sign-in.html`)

**Route**: `/auth/sign-in.html`

**Purpose**: OAuth authentication with GitHub/Google

**Sections**:
- Login view with OAuth buttons
- Callback handler (receives token from backend)
- Loading state with spinner
- Error state with recovery options

**State Management**: Uses `Auth` utility for token/user storage

---

### Landing Page (`pages/landing.html`)

**Route**: `/landing.html` or `/` (public)

**Purpose**: Public-facing marketing site

**Sections**:
1. **Hero**: Value proposition + CTA
2. **Preview**: Portfolio mockup demonstrating product
3. **Features**: Grid of key features
4. **CTA Section**: Final call to action
5. **Footer**: Links and branding

**Navigation**:
- Responsive hamburger menu on mobile
- Auth state detection (shows login/dashboard links)

**Features**:
- Scroll reveal animations
- Responsive grid layouts
- Mobile drawer navigation

---

### Dashboard (`pages/dashboard.html`)

**Route**: `/pages/dashboard.html` (protected)

**Purpose**: Authenticated user control center

**Layout**:
- Fixed sidebar navigation (240px)
- Sticky top bar with breadcrumbs
- Responsive content area

**Sections** (each toggleable via sidebar):
1. **Dashboard**: Overview with stats and recent repos
2. **Repositories**: Full repo list (placeholder)
3. **Portfolio**: Preview page (placeholder)
4. **Resume**: PDF import (placeholder)
5. **Experience**: Work history management (placeholder)
6. **Skills**: Technical skills (placeholder)
7. **Education**: Academic background (placeholder)
8. **Settings**: Account settings (placeholder)

**Responsive Behavior**:
- Sidebar collapses to drawer at 700px
- Stats grid 4→2→1 columns
- Mobile hamburger menu

## 🎯 Component Buttons

### Sizes & Variants

```html
<!-- Sizes -->
<button class="btn btn-primary">Default</button>
<button class="btn btn-primary btn-sm">Small</button>
<button class="btn btn-primary btn-lg">Large</button>
<button class="btn btn-primary btn-icon">Icon</button>

<!-- Variants -->
<button class="btn btn-primary">Primary (accent color)</button>
<button class="btn btn-outline">Outline (border)</button>
<button class="btn btn-ghost">Ghost (minimal)</button>
<button class="btn btn-danger">Danger (red)</button>
```

## 🎭 Common Patterns

### Card Component
```html
<div class="card">
  <div class="card-header">
    <span class="card-title">Title</span>
    <button class="btn btn-ghost btn-sm">Action</button>
  </div>
  <div class="card-body">
    Content here...
  </div>
</div>
```

### Badge / Pill
```html
<div class="badge">
  <span class="badge-dot"></span>
  Beta
</div>

<span class="pill pill-accent">Accent</span>
<span class="pill pill-green">Success</span>
<span class="pill pill-blue">Info</span>
```

### Grid Layouts
```html
<!-- 2-column grid with responsive collapse -->
<div class="grid-2">
  <div>Column 1</div>
  <div>Column 2</div>
</div>

<!-- Similar for grid-3, grid-4 -->
```

### Toast Notifications
```javascript
UI.showToast('Success message!');
UI.showToast('Error happened', 3000); // 3 second duration
```

## 🔄 Migration Notes

### Old → New Mapping
- `login.html` → `auth/sign-in.html`
- `landing_before_login.html` → `pages/landing.html`
- `landing_after_login.html` → `pages/dashboard.html`

### All Styles Now Imported From `shared/`
Every HTML imports:
```html
<link rel="stylesheet" href="../shared/tokens.css" />
<link rel="stylesheet" href="../shared/reset.css" />
<link rel="stylesheet" href="../shared/components.css" />
<link rel="stylesheet" href="../shared/utilities.css" />
<link rel="stylesheet" href="../shared/responsive.css" />
```

### All JavaScript Utilities From `shared/utils.js`
```html
<script src="../shared/utils.js"></script>
```

Then access via: `Auth.getToken()`, `UI.showToast()`, etc.

## 📱 Responsive Breakpoints

| Breakpoint | Width | Device | Changes |
|-----------|-------|--------|---------|
| Desktop   | 1100+ | Desktop | Full layout, 4-col grids |
| Tablet    | 900-1100 | Large tablet | 3→2 col grids |
| Mobile L  | 700-900 | Mobile landscape | 2-col grids, sidebar drawer |
| Mobile    | 540-700 | Mobile portrait | 1-col grids, compact UI |
| Small    | <420 | Small phone | Single column, minimal spacing |

## 🎨 Color System

All colors are CSS variables:

```css
--accent: #c8f04d          /* Primary brand color (lime green) */
--bg: #0c0c0e               /* Background */
--surface: #131316          /* Card background */
--text: #f0ede8             /* Text color */
--muted: #7a7880            /* Disabled/secondary text */

/* Status colors */
--red: #f87171              /* Error */
--green: #4ade80            /* Success */
--blue: #6c8eff             /* Info */
--orange: #fb923c           /* Warning */
```

## 🚀 Next Steps

1. **Remove old files** once migration is complete:
   - Delete `login.html`
   - Delete `landing_before_login.html`
   - Delete `landing_after_login.html`

2. **Create component library** in `components/` folder:
   - Extract repeating patterns
   - Create isolated component files
   - Document component APIs

3. **Add TypeScript** (optional):
   - Convert `shared/utils.js` to `shared/utils.ts`
   - Add type definitions
   - Improve IDE autocomplete

4. **Build system** (optional):
   - Minify CSS/JS
   - Bundle for production
   - Add source maps

## 📚 Additional Resources

- **CSS Variables**: `shared/tokens.css` (line 1-60)
- **Button Styles**: `shared/components.css` (line 12-180)
- **Layout Utilities**: `shared/utilities.css` (line 1-80)
- **Mobile Breakpoints**: `shared/responsive.css` (line 1-100)
