# GPJ Architecture

This directory is the architectural source of truth for the Campus Management Platform.

## Documents

- 00_system_architecture.md — overall platform architecture
- 01_gpj_core.md — GPJ Core backend and UI scope
- 02_gpj_profiles.md — GPJ Profiles architecture
- 03_gpj_academics.md — GPJ Academics architecture
- 04_gpj_access.md — GPJ Access architecture
- 05_ui_design_system.md — shared Stitch-derived UI system

## Design Source

The original Stitch design package is preserved under:

design/stitch/

The Stitch package is the visual reference.

The architecture documents translate that design into implementation constraints.

## Implementation Rule

Backend behavior is governed by Odoo models, security rules, and automated tests.

Visual behavior is governed by the Stitch-derived UI design system.

When the two conflict, do not silently change business behavior. Document the conflict and resolve it deliberately.
