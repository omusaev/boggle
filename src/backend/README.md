# Alembic
Generate a new migration
```bash
alembic -c alembic/alembic.ini revision --autogenerate -m '<MESSAGE>'
```

Apply all new migrations
```bash
alembic -c alembic/alembic.ini upgrade head
```