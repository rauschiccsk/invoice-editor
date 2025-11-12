"""
Invoice Service - Business logic for invoice operations
Provides data access layer between UI and database
"""

import logging
from typing import List, Dict, Optional
from decimal import Decimal


class InvoiceService:
    """Service for invoice operations"""

    def __init__(self, config):
        self.config = config
        self.logger = logging.getLogger(__name__)

        # Try to initialize PostgreSQL client
        self.db_client = None
        self._init_database()

    def _init_database(self):
        """Initialize database connection"""
        try:
            from database.postgres_client import PostgresClient
            self.db_client = PostgresClient(self.config)
            self.logger.info("PostgreSQL client initialized")
        except ImportError:
            self.logger.warning(
                "psycopg2 not installed - using stub data. "
                "Install psycopg2-binary to connect to PostgreSQL."
            )
        except Exception as e:
            self.logger.error(f"Failed to initialize database: {e}")
            self.logger.warning("Using stub data")

    def get_pending_invoices(self) -> List[Dict]:
        """
        Get list of pending invoices

        Returns:
            List of invoice dictionaries
        """
        if self.db_client:
            try:
                return self._get_invoices_from_database()
            except Exception as e:
                self.logger.error(f"Database query failed: {e}")
                self.logger.warning("Falling back to stub data")

        return self._get_stub_invoices()

    def _get_invoices_from_database(self) -> List[Dict]:
        """Get invoices from PostgreSQL (not implemented yet)"""
        # TODO: Implement actual database query
        # For now, return stub data
        self.logger.info("Database query not yet implemented, using stub data")
        return self._get_stub_invoices()

    def _get_stub_invoices(self) -> List[Dict]:
        """Get stub invoice data for testing"""
        self.logger.info("Using stub invoice data")

        return [
            {
                'id': 1,
                'invoice_number': 'FAV-2025-001',
                'invoice_date': '2025-11-12',
                'supplier_name': 'Test Dodávateľ s.r.o.',
                'supplier_ico': '12345678',
                'total_amount': Decimal('1200.00'),
                'currency': 'EUR',
                'status': 'pending'
            },
            {
                'id': 2,
                'invoice_number': 'FAV-2025-002',
                'invoice_date': '2025-11-11',
                'supplier_name': 'Iný Dodávateľ a.s.',
                'supplier_ico': '87654321',
                'total_amount': Decimal('850.50'),
                'currency': 'EUR',
                'status': 'pending'
            },
            {
                'id': 3,
                'invoice_number': 'FAV-2025-003',
                'invoice_date': '2025-11-10',
                'supplier_name': 'ABC Trading s.r.o.',
                'supplier_ico': '11223344',
                'total_amount': Decimal('2450.75'),
                'currency': 'EUR',
                'status': 'pending'
            },
            {
                'id': 4,
                'invoice_number': 'FAV-2025-004',
                'invoice_date': '2025-11-09',
                'supplier_name': 'XYZ Company a.s.',
                'supplier_ico': '55667788',
                'total_amount': Decimal('675.25'),
                'currency': 'EUR',
                'status': 'pending'
            },
            {
                'id': 5,
                'invoice_number': 'FAV-2025-005',
                'invoice_date': '2025-11-08',
                'supplier_name': 'Slovak Suppliers s.r.o.',
                'supplier_ico': '99887766',
                'total_amount': Decimal('3125.00'),
                'currency': 'EUR',
                'status': 'pending'
            }
        ]

    def get_invoice_by_id(self, invoice_id: int) -> Optional[Dict]:
        """
        Get single invoice by ID

        Args:
            invoice_id: Invoice ID

        Returns:
            Invoice dictionary or None
        """
        invoices = self.get_pending_invoices()
        for invoice in invoices:
            if invoice['id'] == invoice_id:
                return invoice
        return None

    def get_invoice_items(self, invoice_id: int) -> List[Dict]:
        """
        Get invoice line items

        Args:
            invoice_id: Invoice ID

        Returns:
            List of item dictionaries
        """
        # TODO: Implement actual database query
        self.logger.info(f"Getting items for invoice {invoice_id}")
        return []
