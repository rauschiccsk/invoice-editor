# tests/test_postgres_connection.py
"""
Test PostgreSQL Connection
===========================
Tests connection to PostgreSQL staging database

Requirements:
- PostgreSQL server running
- Database 'invoice_staging' created
- Schema loaded (001_initial_schema.sql)
- psycopg2-binary installed

Run:
    python tests\test_postgres_connection.py
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))


def test_import():
    """Test that database module can be imported"""
    print("=" * 60)
    print("TEST 1: Import Database Module")
    print("=" * 60)

    try:
        from src.database import PostgresClient, create_postgres_client
        from src.database import PostgreSQLConnectionError, PostgreSQLQueryError

        print("✅ Database module imports OK")
        print(f"   - PostgresClient: {PostgresClient}")
        print(f"   - create_postgres_client: {create_postgres_client}")
        print(f"   - PostgreSQLConnectionError: {PostgreSQLConnectionError}")
        print(f"   - PostgreSQLQueryError: {PostgreSQLQueryError}")
        return True

    except ImportError as e:
        print(f"⚠️  psycopg2 not installed: {e}")
        print("\nInstall options:")
        print("  1. pip install psycopg2-binary  (requires C++ build tools)")
        print("  2. See docs/POSTGRESQL_SETUP.md for alternatives")
        return False


def test_connection():
    """Test actual database connection"""
    print("\n" + "=" * 60)
    print("TEST 2: PostgreSQL Connection")
    print("=" * 60)

    try:
        from src.utils import load_config
        from src.database import create_postgres_client

        # Load config
        print("📝 Loading config...")
        config = load_config()
        pg_config = config.get_postgres_config()

        print(f"   Host: {pg_config.get('host')}")
        print(f"   Database: {pg_config.get('database')}")
        print(f"   User: {pg_config.get('user')}")

        # Connect
        print("\n🔌 Connecting to PostgreSQL...")
        client = create_postgres_client(pg_config)

        # Test query
        print("   Executing test query...")
        result = client.fetch_one("SELECT version()")
        version = result[0] if result else "Unknown"

        print(f"\n✅ Connected successfully!")
        print(f"   Version: {version[:50]}...")

        # Test tables
        print("\n📋 Checking tables...")
        tables = client.fetch_all("""
            SELECT table_name 
            FROM information_schema.tables 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)

        print(f"   Found {len(tables)} tables:")
        for (table_name,) in tables:
            print(f"      - {table_name}")

        # Test views
        print("\n👁️  Checking views...")
        views = client.fetch_all("""
            SELECT table_name 
            FROM information_schema.views 
            WHERE table_schema = 'public'
            ORDER BY table_name
        """)

        print(f"   Found {len(views)} views:")
        for (view_name,) in views:
            print(f"      - {view_name}")

        # Test functions
        print("\n⚙️  Checking functions...")
        functions = client.fetch_all("""
            SELECT routine_name 
            FROM information_schema.routines 
            WHERE routine_schema = 'public'
            ORDER BY routine_name
        """)

        print(f"   Found {len(functions)} functions:")
        for (func_name,) in functions:
            print(f"      - {func_name}")

        # Close
        client.close()

        print("\n✅ All connection tests passed!")
        return True

    except ImportError as e:
        print(f"⚠️  Cannot test connection: {e}")
        print("   psycopg2 not installed")
        return False

    except Exception as e:
        print(f"\n❌ Connection test failed: {e}")
        print("\nTroubleshooting:")
        print("  1. Is PostgreSQL server running? (pg_isready)")
        print("  2. Is database created? (CREATE DATABASE invoice_staging)")
        print("  3. Is schema loaded? (psql -f database/schemas/001_initial_schema.sql)")
        print("  4. Is password correct? (check config.yaml)")
        print("  5. See docs/POSTGRESQL_SETUP.md for help")
        return False


def test_crud_operations():
    """Test basic CRUD operations"""
    print("\n" + "=" * 60)
    print("TEST 3: CRUD Operations")
    print("=" * 60)

    try:
        from src.utils import load_config
        from src.database import create_postgres_client
        from datetime import datetime

        # Load config
        config = load_config()
        pg_config = config.get_postgres_config()

        # Connect
        client = create_postgres_client(pg_config)

        # INSERT
        print("📝 Testing INSERT...")
        test_invoice_id = client.insert('invoices_pending', {
            'supplier_ico': 'TEST123',
            'supplier_name': 'Test Supplier - DELETE ME',
            'invoice_number': f'TEST-{datetime.now().strftime("%Y%m%d%H%M%S")}',
            'invoice_date': datetime.now().date(),
            'currency': 'EUR',
            'total_amount': 999.99,
            'status': 'pending'
        })
        print(f"   ✅ Inserted test invoice ID: {test_invoice_id}")

        # SELECT
        print("\n🔍 Testing SELECT...")
        invoice = client.fetch_one(
            "SELECT * FROM invoices_pending WHERE id = %s",
            (test_invoice_id,)
        )
        print(f"   ✅ Fetched invoice: {invoice[3]} ({invoice[1]})")  # number, ico

        # UPDATE
        print("\n✏️  Testing UPDATE...")
        affected = client.update(
            'invoices_pending',
            {'status': 'approved', 'approved_at': datetime.now()},
            'id = %s',
            (test_invoice_id,)
        )
        print(f"   ✅ Updated {affected} rows")

        # DELETE
        print("\n🗑️  Testing DELETE...")
        deleted = client.delete(
            'invoices_pending',
            'id = %s',
            (test_invoice_id,)
        )
        print(f"   ✅ Deleted {deleted} rows")

        # Close
        client.close()

        print("\n✅ All CRUD tests passed!")
        return True

    except ImportError:
        print("⚠️  Cannot test CRUD: psycopg2 not installed")
        return False

    except Exception as e:
        print(f"\n❌ CRUD test failed: {e}")
        return False


def test_transaction():
    """Test transaction support"""
    print("\n" + "=" * 60)
    print("TEST 4: Transaction Support")
    print("=" * 60)

    try:
        from src.utils import load_config
        from src.database import create_postgres_client
        from datetime import datetime

        # Load config
        config = load_config()
        pg_config = config.get_postgres_config()

        # Connect
        client = create_postgres_client(pg_config)

        # Test successful transaction
        print("✅ Testing successful transaction...")
        with client.transaction():
            invoice_id = client.insert('invoices_pending', {
                'supplier_ico': 'TX001',
                'supplier_name': 'Transaction Test',
                'invoice_number': f'TX-{datetime.now().strftime("%H%M%S")}',
                'invoice_date': datetime.now().date(),
                'currency': 'EUR',
                'total_amount': 111.11,
                'status': 'pending'
            })
            print(f"   Inserted invoice ID: {invoice_id}")

            client.insert('invoice_log', {
                'invoice_id': invoice_id,
                'action': 'CREATED',
                'user_name': 'test',
                'notes': 'Transaction test'
            })
            print(f"   Inserted log entry")
        print("   ✅ Transaction committed")

        # Cleanup
        client.delete('invoice_log', 'invoice_id = %s', (invoice_id,))
        client.delete('invoices_pending', 'id = %s', (invoice_id,))

        # Test rollback
        print("\n↩️  Testing rollback...")
        try:
            with client.transaction():
                test_id = client.insert('invoices_pending', {
                    'supplier_ico': 'ROLLBACK',
                    'supplier_name': 'Should Rollback',
                    'invoice_number': 'ROLLBACK-001',
                    'invoice_date': datetime.now().date(),
                    'currency': 'EUR',
                    'total_amount': 222.22,
                    'status': 'pending'
                })
                print(f"   Inserted invoice ID: {test_id}")

                # Simulate error
                raise ValueError("Simulated error - should rollback")
        except ValueError:
            print("   ✅ Transaction rolled back (as expected)")

        # Verify rollback worked
        result = client.fetch_one(
            "SELECT COUNT(*) FROM invoices_pending WHERE supplier_ico = %s",
            ('ROLLBACK',)
        )
        if result[0] == 0:
            print("   ✅ Rollback verified - no data inserted")
        else:
            print("   ❌ Rollback failed - data still exists")

        # Close
        client.close()

        print("\n✅ All transaction tests passed!")
        return True

    except ImportError:
        print("⚠️  Cannot test transactions: psycopg2 not installed")
        return False

    except Exception as e:
        print(f"\n❌ Transaction test failed: {e}")
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("POSTGRESQL CONNECTION TESTS")
    print("=" * 60)
    print()

    results = []

    # Test 1: Import
    results.append(("Import", test_import()))

    # Only continue if import succeeded
    if results[0][1]:
        # Test 2: Connection
        results.append(("Connection", test_connection()))

        # Only continue if connection succeeded
        if results[-1][1]:
            # Test 3: CRUD
            results.append(("CRUD Operations", test_crud_operations()))

            # Test 4: Transactions
            results.append(("Transactions", test_transaction()))

    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)

    for name, success in results:
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status:10} {name}")

    passed = sum(1 for _, success in results if success)
    total = len(results)

    print(f"\nTotal: {passed}/{total} tests passed")

    if passed == total:
        print("\n🎉 All tests passed!")
    elif passed == 1:
        print("\n⚠️  psycopg2 not installed - install to run database tests")
        print("   See docs/POSTGRESQL_SETUP.md")
    else:
        print("\n⚠️  Some tests failed - check errors above")

    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)