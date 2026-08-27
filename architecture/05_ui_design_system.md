# GPJ UI Design System

## Source of Truth

The visual design is based on the Stitch design package:

design/stitch/extracted/stitch_gpj_core_erp_administration/institutional_core_erp/DESIGN.md

The Stitch design is the visual and interaction reference for the GPJ ERP interface.

## Brand

Government Polytechnic, Jalgaon (GPJ)

Brand personality:
- Professional
- Authoritative
- Efficient
- Trustworthy
- Data-focused

Visual direction:
- Corporate Modern
- Odoo-inspired ERP shell
- High information density
- Functional clarity over decoration
- Strong data integrity cues

## Application Shell

Desktop-first administrative ERP.

### Sidebar

- Fixed left navigation
- Width: 260px
- Collapsed width: 72px
- Primary institutional navigation
- Categories separated by subtle dividers
- Active navigation uses primary/indigo treatment

### Top Bar

Height: 64px.

Contains:
- Breadcrumb/context on left
- Global search in center
- Academic year/user settings on right

### Workspace

- Light gray application background
- White content cards/canvases
- 24px page margin
- 16px general gutter

## Layout

Forms:
- 12-column conceptual grid
- Standard fields generally occupy two-column layouts
- Section grouping should reduce vertical scrolling

Tables:
- Dense administrative CRUD tables
- 12px vertical / 16px horizontal cell padding
- Sticky/light-gray headers
- Bottom borders on rows
- Optional zebra striping
- Search/filter/grouping where appropriate

## Typography

Font family:
- Inter

Key sizes:
- Headline XL: 24px / 700
- Headline LG: 20px / 600
- Headline MD: 16px / 600
- Body LG: 15px / 400
- Body MD: 14px / 400
- Body SM: 13px / 400
- Label MD: 12px / 600
- Label SM: 11px / 500

Dense tables should favor 13px body text.

## Colors

Primary institutional navy:
- #031635
- #1a2b4b

Secondary/interactive indigo:
- #4355b9

Tertiary purple:
- #21004d / #3a047c

Application background:
- #f8f9fa

Primary surface:
- #ffffff

Semantic states:
- Green for active/success
- Amber for pending/warning
- Red for inactive/error

## Shapes

Cards:
- 8px radius

Buttons and inputs:
- Approximately 6px radius

Status badges:
- Fully rounded pill shape

## Elevation

Prefer borders and tonal layers over heavy shadows.

Normal surfaces:
- 1px subtle borders

Floating elements:
- Soft elevation only

## CRUD Components

Each GPJ administrative model should provide an appropriate combination of:

- List view
- Form view
- Search view
- Filters
- Grouping where useful
- Create action
- Edit action
- Archive/unarchive where supported
- Record status indicators
- Contextual actions

## Form Design

Forms should use clear sections.

Example section concepts:
- Basic Information
- Institutional Information
- Administrative Information
- Status
- Relationships

Use compact labels and avoid unnecessary decorative elements.

## Navigation

Navigation must expose actual implemented functionality.

Do not create navigation entries for functionality that does not exist.

GPJ Core navigation should remain focused on its foundational institutional domain.

## Dashboard

The dashboard should follow the Stitch ERP dashboard direction and present:

- Institutional overview
- Key administrative counts
- Membership/institution indicators
- Useful shortcuts
- Recent/relevant administrative information

Dashboard metrics must be backed by real Odoo data.

Do not fabricate statistics.

## Security-Aware UI

The UI must respect existing Odoo security rules.

A user must not receive UI actions that allow them to bypass backend access restrictions.

UI visibility is not a substitute for record rules or access rights.

## Important Implementation Rule

The Stitch design controls visual presentation and interaction patterns.

The existing GPJ Core Python models, security rules, and tests control business behavior.

Do not change business logic merely to reproduce a visual design.

If the visual design requires functionality that does not exist in GPJ Core, document the gap rather than inventing backend behavior.

## Reference Screens

The Stitch package contains:

- erp_dashboard
- institution_profile
- academic_programs
- access_overview

Academic Programs and Access Overview are references for the broader GPJ ERP and should not automatically be implemented inside GPJ Core unless explicitly assigned to this module.
