# GPJ Campus Management Platform — System Architecture

## Platform

The GPJ Campus Management Platform is organized as modular Odoo applications.

Each module owns a specific business domain while sharing the institutional foundation provided by GPJ Core.

## Module Boundaries

### GPJ Core

Foundational institutional infrastructure.

Responsibilities:
- Institutions
- Campuses
- Departments
- Organizational Units
- Designations
- Institutional Roles
- Institutional Memberships
- Institution-aware users
- Shared institutional security foundations

### GPJ Profiles

People/profile domain built on GPJ Core.

Responsibilities will be defined before implementation.

### GPJ Academics

Academic domain built on GPJ Core and related profile functionality.

Expected domain includes academic programs and related academic structures.

Detailed scope will be defined before implementation.

### GPJ Access

Administrative security and access-management domain.

Expected domain includes access administration and permission-oriented interfaces.

Detailed scope will be defined before implementation.

## Dependency Direction

GPJ Core is the foundation.

Future modules may depend on GPJ Core.

GPJ Core must not depend on future domain modules merely to provide their UI.

## Design Authority

The Stitch design package preserved under:

design/stitch/

is the visual reference for the GPJ ERP interface.

The architecture documents translate the design into implementation constraints.

## Implementation Authority

Business behavior is governed by:
- Odoo models
- constraints
- security rules
- automated tests

Visual behavior is governed by:
- Stitch designs
- GPJ UI design system
- module-specific UI architecture

## Module Independence

A module should not introduce business logic belonging to another module.

If a screen references functionality outside the current module, treat it as a dependency or future-module requirement rather than silently implementing it in the current module.

## Development Principle

Build the platform incrementally:

1. Establish and test the backend foundation.
2. Define architecture.
3. Implement UI from the approved design.
4. Validate security and behavior.
5. Perform manual application testing.
6. Commit a stable checkpoint.
7. Proceed to the next module.
