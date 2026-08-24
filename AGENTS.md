# AGENTS.md — Odoo Custom Addons Repository

## Project Structure
```
custom_addons/
├── .github/              # CI workflows
├── addons/               # Custom Odoo modules (one per directory)
│   ├── my_module/
│   │   ├── __manifest__.py
│   │   ├── __init__.py
│   │   ├── models/
│   │   ├── views/
│   │   ├── security/
│   │   └── tests/
├── config/
│   └── odoo.conf         # Odoo server config
├── requirements.txt      # Python dependencies
├── requirements-dev.txt  # Dev dependencies (lint, test)
└── scripts/              # Helper scripts
```

## Developer Commands

### Run Odoo Server
```bash
# With custom addons path
odoo -c config/odoo.conf -d mydb --addons-path=addons,/path/to/odoo/addons

# Or using docker (common)
docker-compose up -d
```

### Install/Update Module
```bash
# CLI (no UI)
odoo -c config/odoo.conf -d mydb -i my_module --stop-after-init
odoo -c config/odoo.conf -d mydb -u my_module --stop-after-init
```

### Run Tests
```bash
# Odoo test runner
odoo -c config/odoo.conf -d mydb --test-enable --test-tags my_module

# Python unittest directly (if structured)
python -m pytest addons/my_module/tests/
```

### Lint & Format
```bash
# Ruff (recommended for speed)
ruff check addons/
ruff format addons/

# Or flake8 + black
flake8 addons/
black addons/
```

### Type Check
```bash
# If using pyright/mypy with Odoo stubs
pyright addons/
```

## Odoo-Specific Conventions

### Module Manifest (`__manifest__.py`)
Required keys: `name`, `version`, `depends`, `data`, `demo`, `installable`, `auto_install`
```python
{
    'name': 'My Module',
    'version': '1.0.0',
    'depends': ['base', 'sale'],
    'data': ['views/my_view.xml'],
    'installable': True,
}
```

### Model Definition
```python
# models/my_model.py
from odoo import models, fields, api

class MyModel(models.Model):
    _name = 'my.model'
    _description = 'My Model'
    
    name = fields.Char(required=True)
    partner_id = fields.Many2one('res.partner')
```

### XML Views
- Place in `views/` directory
- Reference in manifest `data` list
- Use `_inherit` for extending existing views

### Security
- `security/ir.model.access.csv` for model access rights
- `security/<module>.xml` for record rules

## CI / Pre-commit
```yaml
# .github/workflows/ci.yml typical steps:
# 1. ruff check
# 2. ruff format --check
# 3. pyright (if configured)
# 4. odoo --test-enable --test-tags <module>
```

## Common Gotchas
- **Addon path order matters**: custom addons before Odoo core addons
- **Database naming**: use consistent `-d` name across commands
- **Manifest `depends`**: missing deps cause install failures
- **XML IDs**: must be unique across all installed modules
- **Translations**: `.po` files in `i18n/` auto-loaded
- **Migrations**: use `pre-init-hook`/`post-init-hook` in manifest for data migrations

## Useful References
- Odoo developer docs: https://www.odoo.com/documentation/
- OCA (Odoo Community Association) guidelines: https://github.com/OCA
- `odoo-bin --help` for all CLI options