# INIT PROMPT - Session 1
# Invoice Editor - Project Setup & Planning
**Date:** 2025-11-12  
**Developer:** Zoltán (ICC Komárno)  
**Session Focus:** Initialize project structure and architecture planning

---

## 📋 PROJECT OVERVIEW

### Project Name
**Invoice Editor** - ISDOC Invoice Approval & NEX Genesis Integration

### Business Purpose
Qt5 desktop aplikácia pre schvaľovanie a editáciu dodávateľských faktúr pred ich zaevidovaním do NEX Genesis ERP systému.

### Complete Workflow
```
1. supplier_invoice_loader (Python/FastAPI)
   ↓ Spracuje PDF faktúry z emailu
   ↓ Vytvorí ISDOC XML
   
2. PostgreSQL Staging Database
   ↓ Uloží pending faktúry
   
3. Invoice Editor (Qt5 Desktop App) ← THIS PROJECT
   ↓ Operátor schvaľuje/edituje
   ↓ Upraví názvy, ceny, rabat, skupiny
   
4. NEX Genesis ERP (Btrieve)
   ↓ Vytvorí dodacie listy (TSH/TSI)
   ↓ Aktualizuje produkty (GSCAT)
   ↓ Aktualizuje čiarové kódy (BARCODE)
```

### Key Requirements from Customer

**Operátor musí mať možnosť upraviť:**
1. ✏️ **Názov tovarovej položky** - prispôsobiť pre NEX Genesis
2. 📁 **Tovarovú skupinu** - zmeniť kategóriu (MGLST)
3. 💰 **Predajnú cenu** - upraviť selling price
4. 📊 **Rabat %** - percentuálna zľava medzi nákupnou a predajnou cenou
   - Automatický prepočet predajnej ceny po zmene rabatu

**Po schválení:**
- Vytvorí dodací list v NEX Genesis (TSH/TSI)
- Vytvorí produkty ak neexistujú (GSCAT)
- Vytvorí čiarové kódy (BARCODE)
- Validuje dodávateľa (PAB)

---

## 🏗️ ARCHITECTURE DECISION

### Technology Stack Selected

**UI Framework:** Qt5 (PyQt5)
- Native desktop performance
- Customer familiar with desktop apps (NEX Genesis je Delphi)
- Keyboard shortcuts support
- Professional grid editing
- Developer expertise

**Language:** Python 3.11+ (32-bit REQUIRED!)
- NEX Genesis uses 32-bit Btrieve DLL
- Must use 32-bit Python for compatibility

**Databases:**
- **PostgreSQL** - Staging database (invoices_pending)
- **Btrieve** - NEX Genesis production database (direct access)

**Key Design Decision:**
✅ **Direct Btrieve Access** (no FastAPI middleware)
- Faster (no API layer)
- Simpler architecture
- Single operator = no multi-user conflicts
- Copy proven Btrieve client from nex-genesis-server

### Why Qt5 over Web UI?

**Customer Requirements:**
- ⚡ High performance (instant response like NEX Genesis)
- 🎯 Keyboard shortcuts (F9=approve, F5=refresh, etc.)
- 📊 Grid editing (inline cell editing)
- 💻 Desktop comfort (familiar workflow)

**Qt5 Advantages:**
- Native performance (no network latency)
- Keyboard shortcuts work naturally
- QTableWidget = professional editable grids
- Looks and feels like NEX Genesis (Delphi app)
- Developer has Qt5 experience

**Web UI Disadvantages:**
- 50-200ms latency (network)
- Keyboard shortcuts limited
- Grid editing needs libraries
- Requires server infrastructure
- Customer prefers desktop apps

---

## 🎯 SESSION 1 OBJECTIVES

### Goal
Create complete project structure and planning documentation

### Tasks for This Session

1. ✅ **Run create_project_structure.py**
   - Create all directories
   - Setup Python packages
   - Create placeholder files

2. ✅ **Initialize Git Repository**
   ```bash
   cd invoice-editor
   git init
   git add .
   git commit -m "Initial project structure"
   ```

3. ✅ **Create Documentation Framework**
   - SESSION_NOTES.md (current progress)
   - INIT_PROMPT templates (for future sessions)
   - generate_project_access.py (manifest generator)

4. 📋 **Plan Database Architecture**
   - Design PostgreSQL staging schema
   - Map Btrieve tables to PostgreSQL
   - Document data type conversions

5. 📋 **Identify Reusable Components**
   - From nex-genesis-server project:
     - src/btrieve/ (Btrieve client ✅)
     - src/models/ (all table models ✅)
     - src/repositories/ (CRUD patterns)
     - tests/ (testing patterns)

---

## 📁 PROJECT STRUCTURE

```
invoice-editor/
├── docs/                   # Documentation
│   ├── architecture/       # Architecture docs
│   ├── sessions/          # Session history
│   ├── database/          # DB schemas & mappings
│   └── screenshots/       # UI mockups
│
├── src/                   # Source code
│   ├── ui/                # Qt5 UI components
│   │   ├── main_window.py
│   │   ├── invoice_list.py
│   │   ├── invoice_detail.py
│   │   ├── dialogs/
│   │   └── widgets/
│   │
│   ├── btrieve/           # Btrieve client (from nex-server)
│   │   ├── btrieve_client.py
│   │   └── constants.py
│   │
│   ├── models/            # Data models (from nex-server)
│   │   ├── gscat.py       # Product catalog
│   │   ├── barcode.py     # Barcodes
│   │   ├── pab.py         # Partners
│   │   ├── tsh.py         # Delivery notes header
│   │   ├── tsi.py         # Delivery notes items
│   │   └── mglst.py       # Categories
│   │
│   ├── database/          # Database access
│   │   ├── postgres_client.py
│   │   └── models.py      # PostgreSQL models
│   │
│   ├── business/          # Business logic
│   │   ├── invoice_processor.py
│   │   ├── product_manager.py
│   │   └── validators.py
│   │
│   └── utils/             # Utilities
│       ├── config.py
│       └── isdoc_parser.py
│
├── database/              # Database files
│   ├── schemas/          # PostgreSQL schemas
│   │   └── 001_initial_schema.sql
│   └── migrations/       # DB migrations
│
├── config/               # Configuration
│   ├── config.yaml       # Main config
│   └── config_template.yaml
│
├── scripts/              # Utility scripts
│   ├── create_project_structure.py
│   └── generate_project_access.py
│
├── tests/                # Tests
│   ├── unit/
│   ├── integration/
│   └── fixtures/
│
├── resources/            # Resources
│   ├── icons/
│   ├── images/
│   └── ui/              # Qt Designer files
│
├── main.py              # Entry point
├── requirements.txt     # Dependencies
├── .gitignore
└── README.md
```

---

## 🗄️ DATABASE ARCHITECTURE OVERVIEW

### PostgreSQL Staging Database

**Purpose:** Store ISDOC invoices for operator approval/editing

**Core Tables:**
1. **invoices_pending** - Invoice headers
2. **invoice_items_pending** - Invoice line items (editable)
3. **invoice_log** - Audit trail

**Cache Tables (read-only, synced from NEX):**
1. **products_cache** - GSCAT data for suggestions
2. **barcodes_cache** - Barcode lookup
3. **categories_cache** - MGLST for dropdowns
4. **suppliers_cache** - PAB for validation

### NEX Genesis (Btrieve)

**Target:** Production ERP database (direct access)

**Tables Used:**
- **GSCAT.BTR** - Product catalog (create/update)
- **BARCODE.BTR** - Barcodes (create)
- **PAB00000.BTR** - Business partners (validate)
- **TSHA-001.BTR** - Delivery notes header (create)
- **TSIA-001.BTR** - Delivery notes items (create)
- **MGLST.BTR** - Product categories (read-only)

**Important Notes:**
- Btrieve uses file-level locking (not row-level)
- Single operator = no locking conflicts
- PostgreSQL staging = master during approval
- Btrieve write only on final approval

---

## 🔄 DATA FLOW

### 1. Invoice Import (supplier_invoice_loader)
```
Email PDF → Parse → ISDOC XML → PostgreSQL staging
Status: 'pending'
```

### 2. Operator Approval (this app)
```
Load from PostgreSQL
↓
Display in Qt5 grid
↓
Operator edits:
  - Change name
  - Change category
  - Change price
  - Change rabat % → recalculate price
↓
Save changes to PostgreSQL (draft)
↓
Operator clicks Approve (F9)
```

### 3. NEX Genesis Import
```
Validate all fields
↓
Begin transaction
↓
Check/Create supplier (PAB)
↓
For each item:
  - Check product exists (GSCAT)
  - Create if missing (with PLU reservation)
  - Check/create barcode (BARCODE)
↓
Create delivery note header (TSH)
Create delivery note items (TSI)
↓
Update PostgreSQL:
  - status = 'imported'
  - nex_doc_number = 'DL-2025-0001'
↓
Commit transaction
↓
Show success message
```

---

## 📋 DEVELOPMENT PHASES

### Phase 1: Setup (Session 1) - THIS SESSION
- [x] Architecture decision (Qt5 selected)
- [x] Technology stack confirmed
- [ ] Project structure created
- [ ] Git initialized
- [ ] Documentation framework ready

### Phase 2: Database Layer (Session 2-3)
- [ ] PostgreSQL schema design
- [ ] Copy Btrieve components
- [ ] PostgreSQL connection module
- [ ] Test both database connections

### Phase 3: UI Foundation (Session 4-5)
- [ ] Main window
- [ ] Invoice list widget
- [ ] Invoice detail/edit window
- [ ] Navigation & shortcuts

### Phase 4: Business Logic (Session 6-8)
- [ ] Load invoices from staging
- [ ] Edit operations & validation
- [ ] Rabat calculation
- [ ] Approval workflow

### Phase 5: NEX Integration (Session 9-11)
- [ ] GSCAT operations
- [ ] BARCODE operations
- [ ] TSH/TSI creation
- [ ] PLU reservation
- [ ] Transaction handling

### Phase 6: Testing & Production (Session 12-13)
- [ ] Unit tests
- [ ] Integration tests
- [ ] Build executable
- [ ] User acceptance
- [ ] Production deployment

---

## 🔗 RELATED PROJECTS

### nex-genesis-server
- **URL:** https://github.com/rauschiccsk/nex-genesis-server
- **Status:** Phase 2.1 complete (FastAPI + Repositories)
- **Reusable:** 
  - Btrieve client (proven, working)
  - All models (GSCAT, PAB, BARCODE, TSH, TSI, MGLST)
  - Repository patterns
  - Test patterns

### supplier_invoice_loader
- **Status:** Production
- **Function:** Email PDF → ISDOC XML
- **Integration:** Writes to PostgreSQL staging

---

## 🚀 QUICK START - FIRST STEPS

### 1. Create Project Structure
```bash
python scripts/create_project_structure.py
```

### 2. Initialize Git
```bash
cd invoice-editor
git init
git add .
git commit -m "Initial project structure"
```

### 3. Setup Python Environment
```bash
# IMPORTANT: Use 32-bit Python!
python -m venv venv32
venv32\Scripts\activate
pip install -r requirements.txt
```

### 4. Next Session Preparation
- Design PostgreSQL schema
- Copy Btrieve components
- Create configuration files

---

## 🎓 CRITICAL REMINDERS

### Btrieve Requirements
1. **32-bit Python MANDATORY** - NEX Genesis uses 32-bit DLL
2. **Proven Btrieve client available** - from nex-genesis-server
3. **Critical rules documented** - dataLen=4 bytes, encoding, etc.
4. **All models tested** - GSCAT, PAB, BARCODE working

### Development Workflow
1. **One task at a time** - wait for confirmation
2. **Test immediately** - don't accumulate untested code
3. **Update SESSION_NOTES.md** - after each task
4. **Commit frequently** - small, working commits
5. **All code in artifacts** - never inline

### Qt5 Development
1. Use Qt Designer for complex forms
2. Keyboard shortcuts from start
3. Grid editing = QTableWidget
4. Test on Windows (target platform)

---

## 📊 SUCCESS CRITERIA - SESSION 1

**Must Complete:**
- ✅ Project structure created
- ✅ Git repository initialized
- ✅ Documentation framework ready
- ✅ Architecture decisions documented
- ✅ Reusable components identified

**Ready for Session 2:**
- PostgreSQL schema design
- Btrieve component integration
- Database connectivity testing

---

**END OF INIT PROMPT - SESSION 1**

**Status:** Project initialization  
**Priority:** Create structure, setup Git, document architecture  
**Next Session:** Database layer implementation  
**Estimated Duration:** 2-3 hours