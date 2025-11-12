# src/database/postgres_client.py
"""
PostgreSQL Database Client
==========================
Connection pool management and database operations for invoice staging database

Supports:
- Connection pooling
- CRUD operations
- Transactions
- Context managers
- Error handling

Note: Requires psycopg2-binary package
Install: pip install psycopg2-binary
"""

import logging
from typing import Optional, List, Dict, Any, Tuple
from contextlib import contextmanager
from datetime import datetime

# Lazy import - only fails when actually trying to use PostgreSQL
try:
    import psycopg2
    from psycopg2 import pool, sql, extras

    PSYCOPG2_AVAILABLE = True
except ImportError:
    PSYCOPG2_AVAILABLE = False
    psycopg2 = None
    pool = None
    sql = None
    extras = None

logger = logging.getLogger(__name__)


class PostgreSQLConnectionError(Exception):
    """Raised when connection to PostgreSQL fails"""
    pass


class PostgreSQLQueryError(Exception):
    """Raised when query execution fails"""
    pass


class PostgresClient:
    """
    PostgreSQL database client with connection pooling

    Features:
    - Connection pool management (min/max connections)
    - Automatic connection recycling
    - Transaction support (begin, commit, rollback)
    - Context managers for safe resource handling
    - Query execution with parameter binding
    - Batch operations

    Example:
        # Initialize client
        client = PostgresClient(config)
        client.connect()

        # Execute query
        result = client.execute_query(
            "INSERT INTO invoices (number, date) VALUES (%s, %s)",
            ("INV-001", "2025-11-12")
        )

        # Fetch data
        invoices = client.fetch_all("SELECT * FROM invoices WHERE status = %s", ("pending",))

        # Transaction
        with client.transaction():
            client.execute_query("UPDATE invoices SET status = %s WHERE id = %s", ("approved", 1))
            client.execute_query("INSERT INTO invoice_log (...) VALUES (...)")

        # Close
        client.close()
    """

    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize PostgreSQL client

        Args:
            config: Configuration dict with connection parameters
                   Example: {
                       'host': 'localhost',
                       'port': 5432,
                       'database': 'invoice_staging',
                       'user': 'postgres',
                       'password': 'secret',
                       'pool_size': 5,
                       'max_overflow': 10
                   }
        """
        if not PSYCOPG2_AVAILABLE:
            raise ImportError(
                "psycopg2-binary is not installed. "
                "Install it with: pip install psycopg2-binary"
            )

        self.config = config or {}
        self._pool: Optional[pool.SimpleConnectionPool] = None
        self._connection = None  # Current connection in transaction
        self._transaction_active = False

    def connect(self) -> None:
        """
        Create connection pool

        Raises:
            PostgreSQLConnectionError: If connection fails
        """
        try:
            min_connections = self.config.get('pool_size', 1)
            max_connections = self.config.get('pool_size', 1) + self.config.get('max_overflow', 10)

            self._pool = pool.SimpleConnectionPool(
                min_connections,
                max_connections,
                host=self.config.get('host', 'localhost'),
                port=self.config.get('port', 5432),
                database=self.config.get('database', 'invoice_staging'),
                user=self.config.get('user', 'postgres'),
                password=self.config.get('password', ''),
                connect_timeout=self.config.get('connection_timeout', 10)
            )

            # Test connection
            conn = self._pool.getconn()
            self._pool.putconn(conn)

            logger.info(f"✅ Connected to PostgreSQL: {self.config.get('database')}")

        except Exception as e:
            logger.error(f"❌ Failed to connect to PostgreSQL: {e}")
            raise PostgreSQLConnectionError(f"Connection failed: {e}")

    def close(self) -> None:
        """Close all connections in pool"""
        if self._pool:
            self._pool.closeall()
            logger.info("✅ Closed PostgreSQL connection pool")

    def _get_connection(self):
        """Get connection from pool or current transaction"""
        if self._transaction_active and self._connection:
            return self._connection

        if not self._pool:
            raise PostgreSQLConnectionError("Not connected. Call connect() first.")

        return self._pool.getconn()

    def _release_connection(self, conn) -> None:
        """Release connection back to pool (only if not in transaction)"""
        if not self._transaction_active:
            self._pool.putconn(conn)

    def execute_query(
            self,
            query: str,
            params: Optional[Tuple] = None,
            fetch: bool = False
    ) -> Optional[List[Tuple]]:
        """
        Execute SQL query with parameters

        Args:
            query: SQL query with %s placeholders
            params: Query parameters tuple
            fetch: If True, return fetched rows (for SELECT)

        Returns:
            List of tuples if fetch=True, None otherwise

        Raises:
            PostgreSQLQueryError: If query execution fails

        Example:
            # Insert
            client.execute_query(
                "INSERT INTO invoices (number, date) VALUES (%s, %s)",
                ("INV-001", "2025-11-12")
            )

            # Select
            rows = client.execute_query(
                "SELECT * FROM invoices WHERE status = %s",
                ("pending",),
                fetch=True
            )
        """
        conn = None
        cursor = None

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute(query, params)

            if fetch:
                result = cursor.fetchall()
            else:
                result = None

            if not self._transaction_active:
                conn.commit()

            return result

        except Exception as e:
            if conn and not self._transaction_active:
                conn.rollback()
            logger.error(f"❌ Query failed: {e}\nQuery: {query}")
            raise PostgreSQLQueryError(f"Query execution failed: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                self._release_connection(conn)

    def fetch_one(self, query: str, params: Optional[Tuple] = None) -> Optional[Tuple]:
        """
        Fetch single row

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            Single row tuple or None

        Example:
            invoice = client.fetch_one(
                "SELECT * FROM invoices WHERE id = %s",
                (123,)
            )
        """
        conn = None
        cursor = None

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute(query, params)
            result = cursor.fetchone()

            return result

        except Exception as e:
            logger.error(f"❌ Fetch failed: {e}")
            raise PostgreSQLQueryError(f"Fetch failed: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                self._release_connection(conn)

    def fetch_all(self, query: str, params: Optional[Tuple] = None) -> List[Tuple]:
        """
        Fetch all rows

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            List of row tuples

        Example:
            invoices = client.fetch_all(
                "SELECT * FROM invoices WHERE status = %s",
                ("pending",)
            )
        """
        conn = None
        cursor = None

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute(query, params)
            result = cursor.fetchall()

            return result

        except Exception as e:
            logger.error(f"❌ Fetch failed: {e}")
            raise PostgreSQLQueryError(f"Fetch failed: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                self._release_connection(conn)

    def fetch_dict(self, query: str, params: Optional[Tuple] = None) -> List[Dict[str, Any]]:
        """
        Fetch rows as dictionaries

        Args:
            query: SQL query
            params: Query parameters

        Returns:
            List of dictionaries (column_name: value)

        Example:
            invoices = client.fetch_dict(
                "SELECT id, number, status FROM invoices WHERE status = %s",
                ("pending",)
            )
            # Result: [{'id': 1, 'number': 'INV-001', 'status': 'pending'}, ...]
        """
        conn = None
        cursor = None

        try:
            conn = self._get_connection()
            cursor = conn.cursor(cursor_factory=extras.RealDictCursor)

            cursor.execute(query, params)
            result = cursor.fetchall()

            return [dict(row) for row in result]

        except Exception as e:
            logger.error(f"❌ Fetch failed: {e}")
            raise PostgreSQLQueryError(f"Fetch failed: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                self._release_connection(conn)

    def insert(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        """
        Insert row into table

        Args:
            table: Table name
            data: Dictionary of column: value

        Returns:
            Inserted row ID (if RETURNING id is supported)

        Example:
            invoice_id = client.insert('invoices', {
                'invoice_number': 'INV-001',
                'invoice_date': '2025-11-12',
                'total_amount': 1200.00
            })
        """
        columns = list(data.keys())
        values = list(data.values())

        placeholders = ', '.join(['%s'] * len(values))
        columns_str = ', '.join(columns)

        query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders}) RETURNING id"

        result = self.fetch_one(query, tuple(values))

        if result:
            return result[0]
        return None

    def update(self, table: str, data: Dict[str, Any], where: str, where_params: Tuple) -> int:
        """
        Update rows in table

        Args:
            table: Table name
            data: Dictionary of column: value to update
            where: WHERE clause (without WHERE keyword)
            where_params: Parameters for WHERE clause

        Returns:
            Number of affected rows

        Example:
            affected = client.update(
                'invoices',
                {'status': 'approved', 'approved_at': datetime.now()},
                'id = %s',
                (123,)
            )
        """
        set_clause = ', '.join([f"{col} = %s" for col in data.keys()])
        values = list(data.values()) + list(where_params)

        query = f"UPDATE {table} SET {set_clause} WHERE {where}"

        conn = None
        cursor = None

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute(query, tuple(values))
            affected = cursor.rowcount

            if not self._transaction_active:
                conn.commit()

            return affected

        except Exception as e:
            if conn and not self._transaction_active:
                conn.rollback()
            logger.error(f"❌ Update failed: {e}")
            raise PostgreSQLQueryError(f"Update failed: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                self._release_connection(conn)

    def delete(self, table: str, where: str, where_params: Tuple) -> int:
        """
        Delete rows from table

        Args:
            table: Table name
            where: WHERE clause (without WHERE keyword)
            where_params: Parameters for WHERE clause

        Returns:
            Number of deleted rows

        Example:
            deleted = client.delete('invoices', 'id = %s', (123,))
        """
        query = f"DELETE FROM {table} WHERE {where}"

        conn = None
        cursor = None

        try:
            conn = self._get_connection()
            cursor = conn.cursor()

            cursor.execute(query, where_params)
            affected = cursor.rowcount

            if not self._transaction_active:
                conn.commit()

            return affected

        except Exception as e:
            if conn and not self._transaction_active:
                conn.rollback()
            logger.error(f"❌ Delete failed: {e}")
            raise PostgreSQLQueryError(f"Delete failed: {e}")

        finally:
            if cursor:
                cursor.close()
            if conn:
                self._release_connection(conn)

    @contextmanager
    def transaction(self):
        """
        Transaction context manager

        Automatically commits on success, rolls back on error

        Example:
            with client.transaction():
                client.execute_query("UPDATE invoices SET status = %s WHERE id = %s", ("approved", 1))
                client.execute_query("INSERT INTO invoice_log (...) VALUES (...)")
            # Auto-commit on exit

        Example with error:
            try:
                with client.transaction():
                    client.execute_query("UPDATE ...")
                    raise ValueError("Something went wrong")
            except ValueError:
                pass  # Transaction was auto-rolled back
        """
        if not self._pool:
            raise PostgreSQLConnectionError("Not connected. Call connect() first.")

        self._connection = self._pool.getconn()
        self._transaction_active = True

        try:
            yield self
            self._connection.commit()
            logger.debug("✅ Transaction committed")

        except Exception as e:
            self._connection.rollback()
            logger.error(f"❌ Transaction rolled back: {e}")
            raise

        finally:
            self._pool.putconn(self._connection)
            self._connection = None
            self._transaction_active = False

    def begin_transaction(self) -> None:
        """Begin transaction manually (alternative to context manager)"""
        if self._transaction_active:
            raise PostgreSQLQueryError("Transaction already active")

        self._connection = self._pool.getconn()
        self._transaction_active = True
        logger.debug("🔄 Transaction started")

    def commit(self) -> None:
        """Commit current transaction"""
        if not self._transaction_active:
            raise PostgreSQLQueryError("No active transaction")

        try:
            self._connection.commit()
            logger.debug("✅ Transaction committed")
        finally:
            self._pool.putconn(self._connection)
            self._connection = None
            self._transaction_active = False

    def rollback(self) -> None:
        """Rollback current transaction"""
        if not self._transaction_active:
            raise PostgreSQLQueryError("No active transaction")

        try:
            self._connection.rollback()
            logger.warning("⚠️  Transaction rolled back")
        finally:
            self._pool.putconn(self._connection)
            self._connection = None
            self._transaction_active = False

    def __enter__(self):
        """Context manager entry"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        self.close()
        return False


# Helper function
def create_postgres_client(config: Dict[str, Any]) -> PostgresClient:
    """
    Create and connect PostgreSQL client

    Args:
        config: Configuration dictionary

    Returns:
        Connected PostgresClient instance

    Example:
        config = {
            'host': 'localhost',
            'database': 'invoice_staging',
            'user': 'postgres',
            'password': 'secret'
        }
        client = create_postgres_client(config)
    """
    client = PostgresClient(config)
    client.connect()
    return client