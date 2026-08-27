# GPJ Core Architecture

## Purpose

GPJ Core is the foundational institutional module of the GPJ Campus Management Platform.

It provides the shared institutional data model, institutional relationships, memberships, and security foundations required by later GPJ modules.

## Models

### gpj.institution

Represents an institution.

Core responsibilities:
- Institution identity
- Unique institution code
- Institutional relationships
- Active/archive state

Related entities include:
- Campuses
- Departments
- Organizational Units
- Designations
- Institutional Roles
- Memberships

### gpj.campus

Represents a campus belonging to an institution.

Campus codes are institution-scoped.

### gpj.department

Represents a department.

A department belongs to an institution and may optionally belong to a campus.

Campus/institution consistency is enforced.

### gpj.organizational.unit

Represents an organizational hierarchy.

Supports:
- Parent/child hierarchy
- parent_path
- Recursive hierarchy prevention
- Institution-scoped codes

### gpj.designation

Represents an institutional designation.

Codes are institution-scoped.

### gpj.institutional.role

Represents an institutional role.

Codes are institution-scoped.

### gpj.institution.membership

Represents a user's membership in an institution.

Membership functionality includes:
- Institution relationship
- User relationship
- Active state
- Default membership behavior
- Institution-scoped uniqueness

### res.users extension

Users are extended with GPJ institutional membership information and institution-aware context.

## Business Rules

The existing test suite establishes the following behavior:

- Institution codes are globally unique.
- Campus codes are unique within an institution.
- Department codes are unique within an institution.
- Organizational Unit codes are unique within an institution.
- Designation codes are unique within an institution.
- Institutional Role codes are unique within an institution.
- Department/campus/institution relationships must remain consistent.
- Organizational Unit recursion is prevented.
- Institutions use archival rather than destructive deletion.
- Referential deletion is restricted where required.
- Users are isolated by institution through record rules.
- Multi-institution users may access their permitted institutions.
- Default institution context is respected.
- Administrators manage memberships only within permitted institutions.
- Read-only users cannot modify protected records.
- Memberships are unique per user/institution.
- Only one default membership is permitted per user.
- Membership computed fields remain consistent.
- Superusers bypass normal record-rule restrictions.
- Established-year validation is enforced.

## Security

Security is implemented through:

- Odoo access control CSV
- GPJ security groups
- Record rules
- Institution-aware access restrictions

UI restrictions must never replace backend security.

## Current UI Scope

GPJ Core UI should expose the existing foundation through:

- GPJ Core application
- Dashboard
- Institution management
- Campus management
- Department management
- Organizational Unit management
- Designation management
- Institutional Role management
- Membership management
- Institution-aware user information

## Out of Scope

The following belong to later GPJ modules unless explicitly moved into Core:

- Academic Programs
- Student management
- Faculty management
- Academic workflows
- Full access administration UI

## UI Principle

The UI should present the existing backend functionality using the GPJ Stitch design system.

Do not introduce new business entities simply to satisfy a screen design.
