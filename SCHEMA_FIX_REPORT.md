# SCHEMA FIX REPORT

## Issue

**`sqlalchemy.exc.ProgrammingError: column users.is_superuser does not exist`**

## Root Cause

The `User` SQLAlchemy model (`app/models/user.py:22`) defines `is_superuser` as a mapped column:

```python
is_superuser = Column(Boolean, default=False)
```

However, the initial Alembic migration (`001_initial_migration.py`) that creates the `users` table never included this column. The model and database schema drifted apart.

## Schema Drift Comparison

| Artifact | Has `is_superuser`? |
|----------|---------------------|
| `app/models/user.py` (SQLAlchemy) | ✅ Yes |
| `app/schemas/user.py` (Pydantic) | ✅ Yes |
| `alembic/versions/001_initial_migration.py` | ❌ No |
| Production `users` table | ❌ No |
| `alembic/versions/002_add_is_superuser.py` (fix) | ✅ Yes |

## Affected Files

| File | Change |
|------|--------|
| `alembic/versions/002_add_is_superuser.py` | **NEW** — adds `is_superuser BOOLEAN NOT NULL DEFAULT false` to `users` table |
| `app/models/user.py:22` | No change needed (already correct) |
| `app/schemas/user.py:30` | No change needed (already correct) |

## Fix Applied

**Migration:** `002_add_is_superuser.py`

- **Revision:** `002`
- **Parent:** `001`
- **Operation:** `ALTER TABLE users ADD COLUMN is_superuser BOOLEAN NOT NULL DEFAULT false`
- **Default:** `false` (existing rows get `false`)
- **Nullable:** No (matches model's `default=False`)

```python
def upgrade() -> None:
    op.add_column(
        'users',
        sa.Column('is_superuser', sa.Boolean(), nullable=False, server_default=sa.text('false'))
    )
```

## How Migrations Are Applied

The application auto-applies migrations on startup via `app/main.py:29-41`:

```python
@app.on_event("startup")
async def startup_event():
    from alembic import command
    from alembic.config import Config as AlembicConfig
    alembic_cfg = AlembicConfig(alembic_ini_path)
    command.upgrade(alembic_cfg, "head")
```

On **Render**, simply:
1. Deploy or restart the service
2. The startup event calls `alembic upgrade head`
3. Migration `002` runs, adding `is_superuser` to `users`
4. The error is resolved

## Verification Checklist

- [x] `002_add_is_superuser.py` exists and chains to `001`
- [x] Migration committed to `main` at `f07edbc`
- [x] Migration pushed to `origin/main`
- [ ] Render redeployed (migration auto-applies on startup)
- [ ] `POST /auth/register` returns 201
- [ ] `POST /auth/login` returns tokens
- [ ] `GET /auth/me` returns user info