---
name: Institutional Core ERP
colors:
  surface: '#f8f9fa'
  surface-dim: '#d9dadb'
  surface-bright: '#f8f9fa'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f3f4f5'
  surface-container: '#edeeef'
  surface-container-high: '#e7e8e9'
  surface-container-highest: '#e1e3e4'
  on-surface: '#191c1d'
  on-surface-variant: '#44474e'
  inverse-surface: '#2e3132'
  inverse-on-surface: '#f0f1f2'
  outline: '#75777f'
  outline-variant: '#c5c6cf'
  surface-tint: '#4e5e81'
  primary: '#031635'
  on-primary: '#ffffff'
  primary-container: '#1a2b4b'
  on-primary-container: '#8293b8'
  inverse-primary: '#b6c6ef'
  secondary: '#4355b9'
  on-secondary: '#ffffff'
  secondary-container: '#8596ff'
  on-secondary-container: '#11278e'
  tertiary: '#21004d'
  on-tertiary: '#ffffff'
  tertiary-container: '#3a047c'
  on-tertiary-container: '#a57eec'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#b6c6ef'
  on-primary-fixed: '#081b3a'
  on-primary-fixed-variant: '#364768'
  secondary-fixed: '#dee0ff'
  secondary-fixed-dim: '#bac3ff'
  on-secondary-fixed: '#00105c'
  on-secondary-fixed-variant: '#293ca0'
  tertiary-fixed: '#ebdcff'
  tertiary-fixed-dim: '#d4bbff'
  on-tertiary-fixed: '#260058'
  on-tertiary-fixed-variant: '#572e99'
  background: '#f8f9fa'
  on-background: '#191c1d'
  surface-variant: '#e1e3e4'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  headline-md:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: Inter
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  label-md:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  sidebar-width: 260px
  sidebar-collapsed: 72px
  topbar-height: 64px
  gutter: 16px
  margin-page: 24px
  table-cell-padding: 12px 16px
---

## Brand & Style

This design system is engineered for the **Government Polytechnic, Jalgaon (GPJ)**. The brand personality is rooted in **Professionalism, Authority, and Efficiency**. As a mission-critical ERP for academic administration, the UI must prioritize information density and functional clarity over decorative trends.

The visual style is **Corporate Modern** with a focus on data integrity. It utilizes a structured Odoo-inspired ERP shell that provides a sense of permanence and reliability. The aesthetic is clean and high-contrast, ensuring that administrators can navigate complex datasets—such as student records, infrastructure logs, and faculty roles—without cognitive fatigue. 

The emotional response should be one of **trust and control**. By using a structured grid and a disciplined color palette, the interface communicates that the data is secure, organized, and authoritative.

## Colors

The color strategy uses a hierarchy of blues to distinguish between structural navigation and functional interaction.

- **Primary (#1a2b4b):** Deep Navy is reserved for the global navigation sidebar, providing a grounded, institutional anchor for the application.
- **Secondary (#3f51b5):** Indigo is used for primary actions (buttons, active states, and selection), offering high visibility and professional energy.
- **Tertiary (#7e57c2):** A subtle Purple used sparingly for accents, specialized badges, or identifying specific academic modules to break the monotony of the blue-heavy interface.
- **Background (#f8f9fa):** A cool Light-Gray workspace reduces glare during long periods of data entry, while pure white is used for card surfaces to create separation.
- **Semantic Colors:** Standardized green, amber, and red are utilized for status badges (e.g., "Active," "Pending," "Inactive") within data tables.

## Typography

The design system uses **Inter** exclusively to ensure maximum legibility across high-density data tables and complex forms. 

- **Hierarchy:** Dramatic scale is avoided in favor of subtle weight shifts. Headlines use Semi-Bold (600) to stand out against the functional body text.
- **Data Density:** The base body size is set to **14px** for standard content, with a **13px** variant used specifically for dense data tables to maximize the number of visible rows.
- **Labels:** Small, all-caps labels with slight letter spacing are used for table headers and form section titles to differentiate "metadata" from "user data."

## Layout & Spacing

This design system follows a **Desktop-First (1440px)** philosophy, reflecting the primary usage environment of administrative staff.

- **Shell Architecture:** A fixed, collapsible left sidebar manages the primary navigation. The top bar is reserved for contextual tools: breadcrumbs (Left), Global Search (Center), and Academic Year/User Settings (Right).
- **The Workspace:** Content resides in a white "card" or "canvas" area with a 24px margin from the screen edges. 
- **Grid:** For forms, use a **12-column grid**. Standard form fields should span 6 columns (two-column layout) to optimize vertical space while remaining readable.
- **Table Density:** Professional CRUD tables use a compact 12px vertical padding for cells, allowing users to view more records without scrolling.

## Elevation & Depth

To maintain a clean, institutional look, the system uses **Tonal Layers** and **Low-Contrast Outlines** rather than heavy shadows.

- **Surface Levels:** 
  - Level 0: Light Gray (#f8f9fa) - The background canvas.
  - Level 1: White (#ffffff) - Cards, data tables, and input containers.
- **Borders:** Subtle 1px borders (#e0e4e8) are used to define card boundaries and table rows, providing structure without visual noise.
- **Shadows:** A single "Soft Elevation" style is used for floating elements like dropdown menus or active modals: `0px 4px 12px rgba(0, 0, 0, 0.08)`. This keeps the UI feeling light and modern.

## Shapes

The shape language is disciplined and geometric. 

- **Standard Radius:** A consistent **8px (roundedness 2)** is applied to main cards and content containers.
- **Interactive Elements:** Buttons and input fields use a slightly tighter **6px** radius to feel precise and professional.
- **Badges:** Status badges use a **pill-shape (fully rounded)** to distinguish them from clickable buttons and data fields.

## Components

- **Fixed Sidebar:** Categories should be separated by subtle dividers. The "Active" state uses a Primary Indigo background with a white icon.
- **CRUD Tables:**
  - **Headers:** Light gray background (#f1f3f5) with sticky positioning.
  - **Rows:** Alternating "Zebra" striping is optional, but 1px bottom borders are mandatory.
  - **Action Icons:** Use subtle gray icons that turn primary indigo on hover.
- **Status Badges:** Compact labels with light background tints and high-contrast text (e.g., Light Green background with Dark Green text).
- **Form Groups:** Use "Section Headers" with a bold underline or light-gray background bar to group related fields (e.g., "Personal Information" vs. "Academic Details").
- **Search Bar:** A prominent global search in the top bar with a keyboard shortcut hint (e.g., `/` or `Ctrl+K`).
- **Permission Matrix:** A specialized grid component using checkboxes and toggle switches, essential for the Security & Access module.