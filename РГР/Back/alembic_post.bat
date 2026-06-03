@echo off
alembic revision --autogenerate -m "Unmanual migration"
alembic upgrade head