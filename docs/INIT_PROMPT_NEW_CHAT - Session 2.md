# INIT PROMPT - Session 2
# Invoice Editor - Database Layer Implementation
**Date:** 2025-11-12 (continuation)  
**Developer:** Zoltán (ICC Komárno)  
**Session Focus:** PostgreSQL schema + Btrieve integration

---

## 📋 PROJECT STATUS

**Current State:** ~5% complete (Project structure ready)  
**Last Session:** Session 1 - Project setup and planning complete  
**Active Phase:** Phase 2 - Database Layer

---

## ✅ SESSION 1 ACHIEVEMENTS

### Completed:
1. ✅ **Architecture Decision:** Qt5 desktop app with direct Btrieve access
2. ✅ **Technology Stack:** Python 3.11 (32-bit) + PyQt5 + PostgreSQL + Btrieve
3. ✅ **Project Structure:** Complete directory layout created
4. ✅ **Documentation Framework:** SESSION_NOTES.md + INIT_PROMPT template
5. ✅ **Reusable Components Identified:** Btrieve client + Models from nex-genesis-server

### Key Decisions:
- ✅ Standalone Qt5 app (not web-based)
- ✅ Direct Btrieve access (no FastAPI layer)
- ✅ PostgreSQL staging for approval workflow
- ✅ Single operator (no complex locking)
- ✅ Copy proven code from nex-genesis-server

---

## 🎯 SESSION 2 OBJECTIVES

### PRIORITY 1: PostgreSQL Schema Design (HIGH)

**Goal:** Design complete staging database schema

**Tasks:**
1. Create `database/schemas/001_initial_schema.sql`
2. Map Btrieve tables to PostgreSQL:
   - GSCAT → products_staging
   - BARCODE → barcodes_staging
   - PAB → suppliers_staging (reference only)
   - TSH/TSI → (not needed in staging)
3. Design invoice tables:
   - invoices_pending
   - invoice_items_pending
   - invoice_log
4. Add indexes and constraints
5. Document data type mappings (Btrieve → PostgreSQL)

**Deliverable:**
- Complete SQL schema file
- Data dictionary document

---

### PRIORITY 2: Copy Btrieve Components (HIGH)

**Source:** nex-genesis-server project

**Components to Copy:**
```
nex-genesis-server/src/btrieve/
  → invoice-editor/src/btrieve/
  
nex-genesis-server/src/models/
  → invoice-editor/src/models/
  (gscat.py, barcode.py, pab.py, tsh.py, tsi.py, mglst.py)
  
nex-genesis-server/src/utils/config.py
  → invoice-editor/src/utils/config.py
```

**Tasks:**
1. Copy src/btrieve/ directory
2. Copy all model files
3. Copy config.py utility
4. Adapt imports for new project structure
5. Create config/config.yaml template
6. Test Btrieve connectivity

**Testing Checklist:**
- [ ] Import BtrieveClient works
- [ ] Open GSCAT.BTR successful
- [ ] Read first record works
- [ ] Close file works
- [ ] All models import correctly

---

### PRIORITY 3: PostgreSQL Connection Module (MEDIUM)

**Goal:** Create database access layer for staging DB

**Tasks:**
1. Create `src/database/postgres_client.py`
2. Connection pool management
3. Basic CRUD operations
4. Transaction support
5. Error handling

**Key Methods:**
```python
class PostgresClient:
    def __init__(config)
    def connect()
    def execute_query(sql, params)
    def fetch_one(sql, params)
    def fetch_all(sql, params)
    def begin_transaction()
    def commit()
    def rollback()
    def close()
```

---

### PRIORITY 4: Data Type Mapping Documentation (MEDIUM)

**Goal:** Document Btrieve ↔ PostgreSQL conversions

**Create:** `docs/database/TYPE_MAPPINGS.md`

**Content:**
```
Btrieve (Delphi) → PostgreSQL

longint (4 bytes)     → INTEGER
string (fixed)        → VARCHAR(n)
double (8 bytes)      → NUMERIC(12,2) [for money]
boolean (1 byte)      → BOOLEAN
TDateTime (date)      → DATE
TDateTime (time)      → TIMESTAMP

Encoding:
CP852/Windows-1250    → UTF-8
```

---

## 📊 POSTGRESQL SCHEMA OVERVIEW

### Table: invoices_pending

**Purpose:** Store ISDOC invoices awaiting approval

**Columns:**
```sql
id                  SERIAL PRIMARY KEY
supplier_ico        VARCHAR(20) NOT NULL
supplier_name       VARCHAR(200)
invoice_number      VARCHAR(50) NOT NULL
invoice_date        DATE NOT NULL
currency            VARCHAR(3) DEFAULT 'EUR'
total_amount        NUMERIC(12,2) NOT NULL
isdoc_xml           TEXT

-- Workflow
status              VARCHAR(20) NOT NULL DEFAULT 'pending'
                    -- pending, approved, rejected, imported
created_at          TIMESTAMP DEFAULT NOW()
approved_by         VARCHAR(50)
approved_at         TIMESTAMP
imported_at         TIMESTAMP

-- NEX Genesis reference (after import)
nex_doc_number      VARCHAR(50)
nex_pab_code        INTEGER

-- Constraints
UNIQUE(supplier_ico, invoice_number)
```

### Table: invoice_items_pending

**Purpose:** Line items of pending invoices

**Columns:**
```sql
id                      SERIAL PRIMARY KEY
invoice_id              INTEGER NOT NULL REFERENCES invoices_pending(id)
line_number             INTEGER NOT NULL

-- Original data from ISDOC
original_name           VARCHAR(200) NOT NULL
original_quantity       NUMERIC(12,3) NOT NULL
original_price          NUMERIC(12,2) NOT NULL
original_ean            VARCHAR(50)

-- Operator edits
edited_name             VARCHAR(200)
edited_category_code    INTEGER       -- FK to MGLST
edited_price_buy        NUMERIC(12,2)
edited_price_sell       NUMERIC(12,2)
edited_discount_percent NUMERIC(5,2)  -- Rabat %

-- Flags
was_edited              BOOLEAN DEFAULT FALSE

-- NEX Genesis reference (after import)
nex_gs_code             INTEGER       -- Created GsCode

-- Constraints
UNIQUE(invoice_id, line_number)
```

### Table: invoice_log

**Purpose:** Audit trail

**Columns:**
```sql
id              SERIAL PRIMARY KEY
invoice_id      INTEGER NOT NULL REFERENCES invoices_pending(id)
action          VARCHAR(50) NOT NULL
                -- CREATED, EDITED, APPROVED, REJECTED, IMPORTED
user_name       VARCHAR(50)
timestamp       TIMESTAMP DEFAULT NOW()
changes         JSONB
notes           TEXT
```

---

## 🔧 BTRIEVE TABLES MAPPING

### GSCAT (Product Catalog) → products_staging

**Purpose:** Cache for product suggestions/validation

**Minimal columns needed:**
```sql
gs_code         INTEGER PRIMARY KEY
gs_name         VARCHAR(200)
mglst_code      INTEGER
price_buy       NUMERIC(12,2)
price_sell      NUMERIC(12,2)
active          BOOLEAN
last_sync       TIMESTAMP
```

### BARCODE → barcodes_staging

**Purpose:** EAN lookup cache

```sql
gs_code         INTEGER
bar_code        VARCHAR(50) PRIMARY KEY
last_sync       TIMESTAMP
```

### MGLST (Categories) → categories_cache

**Purpose:** Category dropdown

```sql
mglst_code      INTEGER PRIMARY KEY
mglst_name      VARCHAR(200)
parent_code     INTEGER
last_sync       TIMESTAMP
```

**Note:** These are READ-ONLY caches, periodically synced from NEX Genesis.

---

## 🚀 DEVELOPMENT WORKFLOW - SESSION 2

### Step 1: Create PostgreSQL Schema
```bash
cd invoice-editor
# Create database/schemas/001_initial_schema.sql
# with complete schema
```

### Step 2: Copy Btrieve Components
```bash
# From nex-genesis-server to invoice-editor:
cp -r ../nex-genesis-server/src/btrieve/ ./src/btrieve/
cp ../nex-genesis-server/src/models/*.py ./src/models/
cp ../nex-genesis-server/src/utils/config.py ./src/utils/
```

### Step 3: Create Configuration
```bash
# Create config/config.yaml
# Copy from nex-genesis-server and adapt
```

### Step 4: Test Btrieve Connection
```python
# Create tests/test_btrieve_connection.py
from src.btrieve.btrieve_client import BtrieveClient

client = BtrieveClient()
pos_block = client.open_file("C:\\NEX\\YEARACT\\STORES\\GSCAT.BTR")
status, data = client.get_first(pos_block)
client.close_file(pos_block)

print(f"✅ Btrieve working! Status: {status}")
```

### Step 5: Create PostgreSQL Client
```bash
# Create src/database/postgres_client.py
# with connection pool and basic CRUD
```

### Step 6: Test PostgreSQL Connection
```python
# Create tests/test_postgres_connection.py
from src.database.postgres_client import PostgresClient

client = PostgresClient()
client.connect()
result = client.execute_query("SELECT version()")
print(f"✅ PostgreSQL working! Version: {result}")
```

---

## 📁 FILES TO CREATE THIS SESSION

1. **database/schemas/001_initial_schema.sql**
   - Complete PostgreSQL schema
   - All tables, indexes, constraints

2. **src/btrieve/** (copied from nex-genesis-server)
   - btrieve_client.py
   - constants.py
   - __init__.py

3. **src/models/** (copied from nex-genesis-server)
   - gscat.py
   - barcode.py
   - pab.py
   - tsh.py
   - tsi.py
   - mglst.py
   - __init__.py

4. **src/database/postgres_client.py**
   - Connection management
   - CRUD operations
   - Transaction support

5. **src/utils/config.py** (adapted from nex-genesis-server)
   - YAML configuration loading
   - Path validation

6. **config/config.yaml**
   - Database connections
   - Application settings

7. **tests/test_btrieve_connection.py**
   - Btrieve connectivity test

8. **tests/test_postgres_connection.py**
   - PostgreSQL connectivity test

9. **docs/database/TYPE_MAPPINGS.md**
   - Data type conversion reference

---

## 🎯 SUCCESS CRITERIA - SESSION 2

**Must Achieve:**
- ✅ Complete PostgreSQL schema designed
- ✅ Btrieve components copied and working
- ✅ PostgreSQL connection module created
- ✅ Both databases accessible from code
- ✅ Basic tests passing

**Quality Gates:**
1. Can connect to NEX Genesis (Btrieve)
2. Can connect to PostgreSQL
3. Can read from GSCAT.BTR
4. Can query invoices_pending table
5. All imports work without errors

---

## 🔒 CRITICAL REMINDERS

### Btrieve Rules (from nex-genesis-server)
1. **32-bit Python REQUIRED** - NEX Genesis uses 32-bit DLL
2. **dataLen = 4 bytes** (c_uint32, not c_uint16)
3. **Filename in key_buffer** for open operation
4. **Always close files** in finally block
5. **CP852/Windows-1250** encoding for Czech/Slovak text

### Development Principles
1. **One task at a time** - Wait for confirmation
2. **Test immediately** - Don't accumulate untested code
3. **Update SESSION_NOTES.md** - After each task
4. **Commit working code** - Frequent small commits
5. **No code generation** without explicit request

### PostgreSQL Best Practices
1. Use NUMERIC for money (not FLOAT)
2. Add proper indexes (foreign keys, search columns)
3. Use constraints (NOT NULL, UNIQUE, CHECK)
4. Document column purposes
5. Plan for future growth

---

## 📚 REFERENCE DOCUMENTS

**Load these first:**
1. `project_file_access.json` - File manifest
2. `SESSION_NOTES.md` - Current progress
3. `nex-genesis-server/docs/context/btrieve_rules.md` - Critical Btrieve patterns

**For Btrieve integration:**
- nex-genesis-server/src/btrieve/btrieve_client.py
- nex-genesis-server/docs/NEX_DATABASE_STRUCTURE.md
- nex-genesis-server/database-schema/*.bdf files

---

## 🎓 NEXT SESSION PREVIEW

**Session 3: UI Foundation**
- Main window design
- Invoice list widget
- Basic navigation
- Keyboard shortcuts

**Estimated Duration:** 4-6 hours

---

**END OF INIT PROMPT - SESSION 2**

**Status:** Ready for database layer implementation  
**Priority:** Create PostgreSQL schema + copy Btrieve components  
**Goal:** Both databases accessible and tested