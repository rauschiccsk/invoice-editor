# INIT PROMPT - Session 3
# Invoice Editor - UI Foundation

**Project:** invoice-editor  
**Developer:** Zoltán (ICC Komárno)  
**Session Focus:** Phase 3 - UI Foundation (Qt5 Main Window & Invoice List)  
**Date:** 2025-11-12+

---

## 📋 PROJECT STATUS

**Current State:** 20% complete (Phase 2 Complete - Database Layer Ready)  
**Last Session:** Session 2 - Database Layer Implementation ✅ COMPLETE  
**Active Phase:** Phase 3 - UI Foundation  
**Next Goal:** Main window + Invoice list widget

---

## ✅ SESSION 2 ACHIEVEMENTS

**Phase 2: Database Layer - 100% Complete**

1. ✅ **PostgreSQL Schema Design**
   - Complete schema: 6 tables, 2 triggers, 2 views
   - Tested in pgAdmin4
   - File: `database/schemas/001_initial_schema.sql`

2. ✅ **Btrieve Components**
   - Client copied and working
   - Models: GSCAT, Barcode, PAB, MGLST
   - All imports functional

3. ✅ **PostgreSQL Connection Module**
   - Interface: `src/database/postgres_client.py`
   - Connection pooling, CRUD, transactions
   - Note: psycopg2 install pending (requires C++ tools)

4. ✅ **Type Mappings Documentation**
   - Complete guide: `docs/database/TYPE_MAPPINGS.md`
   - Btrieve ↔ PostgreSQL conversions
   - Encoding, dates, decimals

---

## 🎯 SESSION 3 OBJECTIVES

### PRIORITY 1: Main Window Design (HIGH)

**Goal:** Create Qt5 main application window

**Tasks:**
1. Create `main.py` - Application entry point
2. Create `src/ui/main_window.py` - Main window class
3. Design layout:
   - Menu bar (File, Edit, View, Help)
   - Toolbar (common actions)
   - Status bar
   - Central widget placeholder
4. Window settings:
   - Title: "Invoice Editor"
   - Size: 1400x900
   - Icon
   - Keyboard shortcuts

**Deliverable:**
- Working main window that displays
- Menu structure defined
- Toolbar with placeholder actions
- Proper window initialization

---

### PRIORITY 2: Invoice List Widget (HIGH)

**Goal:** Display list of pending invoices

**Tasks:**
1. Create `src/ui/widgets/invoice_list_widget.py`
2. Use QTableView with model
3. Columns:
   - ID
   - Invoice Number
   - Date
   - Supplier Name
   - Amount
   - Currency
   - Status
4. Features:
   - Sortable columns
   - Selection handling
   - Double-click to open detail
   - Context menu (right-click)

**Deliverable:**
- Invoice list displays in main window
- Data loads from PostgreSQL (or stub if psycopg2 not installed)
- Selection works
- Basic navigation

---

### PRIORITY 3: Data Loading (MEDIUM)

**Goal:** Connect UI to PostgreSQL staging database

**Tasks:**
1. Create `src/business/invoice_service.py`
2. Methods:
   - `get_pending_invoices()` → List of invoices
   - `get_invoice_by_id(id)` → Single invoice with items
   - `get_invoice_items(invoice_id)` → Line items
3. Handle psycopg2 not installed:
   - Return stub data if DB not available
   - Show warning in status bar

**Deliverable:**
- Service layer separates UI from database
- Works with or without psycopg2
- Stub data for testing UI

---

### PRIORITY 4: Basic Navigation (MEDIUM)

**Goal:** Keyboard shortcuts and navigation

**Tasks:**
1. Keyboard shortcuts:
   - F5: Refresh list
   - Ctrl+F: Search/filter
   - Ctrl+N: Next invoice
   - Ctrl+P: Previous invoice
   - Escape: Close dialogs
2. Navigation:
   - Arrow keys in list
   - Enter to open detail
   - Tab navigation

**Deliverable:**
- All shortcuts working
- Navigation feels natural
- Status bar shows shortcut hints

---

## 📊 CURRENT PROJECT STATE

### What's Working ✅
- **Btrieve:** Client loads, models parse/serialize
- **PostgreSQL Schema:** Complete, tested in pgAdmin4
- **Config:** YAML loader working
- **Documentation:** All database docs complete

### What's Pending ⏳
- **psycopg2:** Not installed (needs C++ build tools)
- **UI:** Not created yet (this session!)
- **Business Logic:** Not started
- **NEX Integration:** Not started

### What's Available 📦
- Python 3.13 32-bit ✅
- PyQt5 installed ✅
- PyYAML installed ✅
- Project structure ready ✅
- All models working ✅

---

## 🏗️ UI ARCHITECTURE

### Technology Stack
- **Framework:** PyQt5
- **Design:** Designer UI files (optional) or pure Python
- **Pattern:** Model-View pattern
- **Layout:** QMainWindow + dock widgets

### Window Structure
```
MainWindow (QMainWindow)
├── MenuBar
│   ├── File (Exit)
│   ├── Edit (Preferences)
│   ├── View (Refresh)
│   └── Help (About)
├── ToolBar
│   ├── Refresh
│   ├── Search
│   ├── Approve
│   └── Reject
├── Central Widget
│   └── InvoiceListWidget (QTableView)
├── Status Bar
│   ├── Connection status
│   ├── Record count
│   └── Hints
└── Dock Widgets (future)
    ├── Filter panel
    └── Detail panel
```

### Widget Hierarchy
```
src/ui/
├── __init__.py
├── main_window.py          (QMainWindow)
├── widgets/
│   ├── __init__.py
│   ├── invoice_list_widget.py    (QTableView + Model)
│   └── invoice_detail_widget.py  (future)
└── dialogs/
    ├── __init__.py
    └── about_dialog.py      (future)
```

---

## 📁 FILES TO CREATE THIS SESSION

### 1. Application Entry Point
**File:** `main.py`
- Application initialization
- Config loading
- Window creation
- Event loop

### 2. Main Window
**File:** `src/ui/main_window.py`
- QMainWindow subclass
- Menu bar setup
- Toolbar setup
- Status bar setup
- Central widget management

### 3. Invoice List Widget
**File:** `src/ui/widgets/invoice_list_widget.py`
- QTableView subclass
- Custom model (QAbstractTableModel)
- Data loading
- Selection handling
- Context menu

### 4. Invoice Service
**File:** `src/business/invoice_service.py`
- Data access layer
- get_pending_invoices()
- get_invoice_by_id()
- Stub data support

### 5. UI Package Inits
**Files:**
- `src/ui/__init__.py`
- `src/ui/widgets/__init__.py`
- `src/ui/dialogs/__init__.py`
- `src/business/__init__.py`

---

## 🎨 UI DESIGN GUIDELINES

### Visual Style
- **Theme:** System native (Windows)
- **Font:** Segoe UI, 10pt
- **Grid:** Alternating row colors
- **Icons:** Standard Qt icons (for now)

### Layout Principles
1. **Clarity:** Clear visual hierarchy
2. **Efficiency:** Quick access to common actions
3. **Feedback:** Status bar shows current state
4. **Consistency:** Follow Qt conventions

### Keyboard-First Design
- All actions accessible via keyboard
- Shortcuts visible in menus
- Tab order logical
- Focus indicators clear

---

## 🔧 DEVELOPMENT WORKFLOW - SESSION 3

### Step 1: Create Main Window Shell
```bash
# Create UI structure
mkdir src/ui
mkdir src/ui/widgets
mkdir src/ui/dialogs

# Create main.py
# Create src/ui/main_window.py
```

### Step 2: Test Main Window
```bash
python main.py
# Should display empty window with menu/toolbar
```

### Step 3: Add Invoice List Widget
```bash
# Create src/ui/widgets/invoice_list_widget.py
# Integrate into main window
```

### Step 4: Add Stub Data
```bash
# Create src/business/invoice_service.py with stub data
# Connect to invoice list widget
```

### Step 5: Test Navigation
```bash
# Test keyboard shortcuts
# Test selection
# Test refresh
```

---

## 🎯 SUCCESS CRITERIA - SESSION 3

### Must Achieve ✅
- ✅ Main window displays correctly
- ✅ Menu bar functional
- ✅ Invoice list shows data (stub or real)
- ✅ Can select invoices
- ✅ Basic keyboard shortcuts work
- ✅ Status bar shows info

### Quality Gates 🎨
1. Window looks professional
2. Navigation feels natural
3. Code is clean and organized
4. No errors or warnings
5. Proper resource cleanup

---

## 🚨 CRITICAL REMINDERS

### Qt5 Best Practices
1. **Signals/Slots:** Use for communication between widgets
2. **Model/View:** Separate data from presentation
3. **Resource Management:** Parent widgets manage children
4. **Event Loop:** Only one QApplication instance
5. **Threading:** Don't block UI thread

### Development Principles (from Session 2)
1. **One task at a time** - Wait for confirmation
2. **Test immediately** - Run after each component
3. **Update SESSION_NOTES.md** - After each milestone
4. **Commit working code** - Frequent small commits
5. **All code in artifacts** - Never inline

### psycopg2 Handling
- UI must work WITHOUT psycopg2 installed
- Show warning if database unavailable
- Use stub data for development
- Install psycopg2 later when needed

---

## 📚 REFERENCE DOCUMENTS

### Load These First
1. `docs/SESSION_NOTES.md` - Current project status
2. `project_file_access.json` - File manifest
3. This file - Session 3 objectives

### For UI Development
- PyQt5 Documentation: https://doc.qt.io/qtforpython/
- Qt Designer (optional): For visual layout
- `config/config.yaml` - Application settings

### For Database Integration
- `src/database/postgres_client.py` - Database interface
- `docs/POSTGRESQL_SETUP.md` - Database setup guide
- `database/schemas/001_initial_schema.sql` - Schema reference

---

## 🎓 NEXT SESSION PREVIEW

**Session 4: Invoice Detail & Editing**
- Invoice detail window
- Edit invoice items
- Price/rabat calculation
- Form validation

**Estimated Duration:** 4-6 hours

---

## 📝 STUB DATA EXAMPLE

For testing UI without database:

```python
STUB_INVOICES = [
    {
        'id': 1,
        'invoice_number': 'FAV-2025-001',
        'invoice_date': '2025-11-12',
        'supplier_name': 'Test Dodávateľ s.r.o.',
        'supplier_ico': '12345678',
        'total_amount': 1200.00,
        'currency': 'EUR',
        'status': 'pending'
    },
    {
        'id': 2,
        'invoice_number': 'FAV-2025-002',
        'invoice_date': '2025-11-11',
        'supplier_name': 'Iný Dodávateľ a.s.',
        'supplier_ico': '87654321',
        'total_amount': 850.50,
        'currency': 'EUR',
        'status': 'pending'
    }
]
```

---

## 🔗 KEY FILES FROM SESSION 2

### Database
- ✅ `database/schemas/001_initial_schema.sql` - Complete schema
- ✅ `src/database/postgres_client.py` - Database client (stub)

### Btrieve
- ✅ `src/btrieve/btrieve_client.py` - Btrieve client (working)
- ✅ `src/models/gscat.py` - Product model
- ✅ `src/models/barcode.py` - Barcode model

### Configuration
- ✅ `config/config.yaml` - Application config
- ✅ `src/utils/config.py` - Config loader

---

**END OF INIT PROMPT - SESSION 3**

**Status:** Ready to start UI development  
**Priority:** Create main window and invoice list  
**Goal:** Functional UI displaying invoice list  
**Duration:** 4-6 hours estimated