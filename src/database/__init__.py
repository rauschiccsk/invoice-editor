# src/database/__init__.py
"""
Database Access Layer
=====================
PostgreSQL staging database client and utilities

Modules:
- postgres_client: PostgreSQL connection pool and CRUD operations

Usage:
    from src.database import PostgresClient, create_postgres_client

    # Using context manager
    with PostgresClient(config) as client:
        invoices = client.fetch_all("SELECT * FROM invoices WHERE status = %s", ("pending",))

    # Manual connection management
    client = create_postgres_client(config)
    try:
        result = client.insert('invoices', {'number': 'INV-001', 'date': '2025-11-12'})
    finally:
        client.close()
"""

from src.database.postgres_client import (
    PostgresClient,
    create_postgres_client,
    PostgreSQLConnectionError,
    PostgreSQLQueryError,
)

__all__ = [
    'PostgresClient',
    'create_postgres_client',
    'PostgreSQLConnectionError',
    'PostgreSQLQueryError',
]

__version__ = '1.0.0'
