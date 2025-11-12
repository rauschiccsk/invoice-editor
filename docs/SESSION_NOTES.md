# SESSION NOTES - Invoice Editor
**Last Updated:** 2025-11-12  
**Developer:** Zoltán (ICC Komárno)  
**Current Session:** Session 1 - Project Setup & Planning

---

## 📊 PROJECT STATUS

**Overall Progress:** 0% (Project Setup Phase)  
**Current Phase:** Planning & Architecture Design  
**Active Session:** Session 1

---

## 🎯 PROJECT OVERVIEW

### Project Name
**Invoice Editor** - ISDOC Approval & NEX Genesis Integration

### Purpose
Qt5 desktop aplikácia pre schvaľovanie dodávateľských faktúr pred ich zaevidovaním do NEX Genesis ERP systému.

### Workflow
```
supplier_invoice_loader
    ↓ (generuje ISDOC XML)
PostgreSQL Staging DB
    ↓ (operátor schvaľuje/edituje)
Invoice Editor (Qt5)
    ↓ (schválené faktúry)
NEX Genesis (Btrieve)
```

### Key Requirements
1. **Zobrazenie pending faktúr** z PostgreSQL staging DB
2. **Editácia položek:**
   - Názov položky
   - Tovarová skupina
   - Predajná cena
   - Rabat % (prepočet ceny)
3. **Schválenie** → import do NEX Genesis:
   - Create/update products (GSCAT)
   - Create/update barcodes (BARCODE)
   - Create delivery notes (TSH/TSI)
   - Validate suppliers (PAB)

---

## 🏗️ ARCHITECTURE DECISIONS

### Technology Stack
- **UI Framework:** Qt5 (PyQt5)
- **Language:** Python 3.11+ (32-bit required for Btrieve)
- **Staging Database:** PostgreSQL
- **Target Database:** NEX Genesis (Btrieve)
- **Deployment:** PyInstaller single executable

### Key Design Decisions
1. ✅ **Standalone Qt5 application** (not web-based)
2. ✅ **Direct Btrieve access** (no FastAPI middleware)
3. ✅ **PostgreSQL staging** for approval workflow
4. ✅ **Single operator** (no multi-user locking needed)
5. ✅ **Copy Btrieve client** from nex-genesis-server project

### Rationale
- **Qt5 chosen over Web UI:**
  - Native performance (instant response)
  - Customer familiar with NEX Genesis (Delphi desktop app)
  - Keyboard shortcuts support
  - Grid editing capabilities
  - Developer expertise in Qt5

- **Direct Btrieve access:**
  - Faster (no API layer)
  - Simpler architecture
  - Single operator = no conflicts
  - Copy proven code from nex-genesis-server

---

## 📁 PROJECT STRUCTURE

```
invoice-editor/
├── docs/
│   ├── architecture/       # Architecture documents
│   ├── sessions/          # Session notes history
│   ├── database/          # Database schemas
│   └── screenshots/       # UI screenshots
│
├── src/
│   ├── ui/                # Qt5 UI components
│   │   ├── dialogs/
│   │   └── widgets/
│   ├── btrieve/           # Btrieve client (from nex-genesis-server)
│   ├── models/            # Data models (from nex-genesis-server)
│   ├── database/          # PostgreSQL access
│   ├── business/          # Business logic
│   └── utils/             # Utilities
│
├── database/
│   ├── schemas/           # PostgreSQL table definitions
│   └── migrations/        # Database migrations
│
├── config/
│   └── config.yaml        # Configuration file
│
├── scripts/               # Utility scripts
├── tests/                 # Test suite
├── resources/             # Icons, images, UI files
│
├── main.py               # Entry point
└── requirements.txt      # Dependencies
```

---

## 🗄️ DATABASE ARCHITECTURE

### PostgreSQL Staging Database

**Purpose:** Store pending invoices for operator approval

**Key Tables:**
```sql
invoices_pending (
    id, supplier_ico, invoice_number, invoice_date,
    total_amount, isdoc_xml,
    status, created_at, approved_at, imported_at,
    nex_doc_number
)

invoice_items_pending (
    id, invoice_id, line_number,
    original_name, original_quantity, original_price, original_ean,
    edited_name, edited_category_code, 
    edited_price_buy, edited_price_sell, edited_discount_percent,
    was_edited, nex_gs_code
)

invoice_log (
    id, invoice_id, action, timestamp, user_name, notes
)
```

### NEX Genesis (Btrieve)

**Target:** Production ERP database

**Key Tables:**
- **GSCAT.BTR** - Product catalog (705 bytes)
- **BARCODE.BTR** - Barcodes (~50 bytes)
- **PAB00000.BTR** - Business partners (1269 bytes)
- **TSHA-001.BTR** - Delivery notes header
- **TSIA-001.BTR** - Delivery notes items
- **MGLST.BTR** - Product categories

**Note:** PostgreSQL tables will mirror Btrieve structures but with proper naming (no abbreviations).

---

## 📋 DEVELOPMENT PLAN

### PHASE 1: Setup & Foundation (Session 1)
**Status:** 🔄 In Progress

**Tasks:**
- [ ] Create project structure
- [ ] Setup Git repository
- [ ] Create SESSION_NOTES.md
- [ ] Create INIT_PROMPT template
- [ ] Create generate_project_access.py script
- [ ] Design PostgreSQL schema
- [ ] Map Btrieve → PostgreSQL structure
- [ ] Document architecture decisions

**Deliverables:**
- Project structure ready
- Documentation framework
- Database schema design

---

### PHASE 2: Database Layer (Session 2-3)
**Status:** ⏳ Planned

**Tasks:**
- [ ] Create PostgreSQL schemas
- [ ] Copy Btrieve client from nex-genesis-server
- [ ] Copy Models from nex-genesis-server
- [ ] Test Btrieve connectivity
- [ ] Create PostgreSQL connection module
- [ ] Implement data access layer

---

### PHASE 3: UI Foundation (Session 4-5)
**Status:** ⏳ Planned

**Tasks:**
- [ ] Main window design
- [ ] Invoice list widget
- [ ] Invoice detail/edit window
- [ ] Grid editing widget
- [ ] Navigation & shortcuts

---

### PHASE 4: Business Logic (Session 6-8)
**Status:** ⏳ Planned

**Tasks:**
- [ ] ISDOC import from PostgreSQL
- [ ] Invoice validation
- [ ] Product matching/creation logic
- [ ] Price calculation & rabat
- [ ] Delivery note generation

---

### PHASE 5: NEX Genesis Integration (Session 9-11)
**Status:** ⏳ Planned

**Tasks:**
- [ ] GSCAT operations (create/update products)
- [ ] BARCODE operations
- [ ] PAB validation
- [ ] TSH/TSI creation
- [ ] PLU reservation mechanism
- [ ] Transaction handling

---

### PHASE 6: Testing & Polish (Session 12-13)
**Status:** ⏳ Planned

**Tasks:**
- [ ] Unit tests
- [ ] Integration tests
- [ ] User acceptance testing
- [ ] Bug fixes
- [ ] Documentation
- [ ] Build & deployment

---

## 🎯 CURRENT SESSION: Session 1

### Session Goal
Setup project structure and planning documentation

### Completed Tasks
- ✅ Architecture analysis (Qt5 vs Web)
- ✅ Technology stack decision
- ✅ Project structure design
- ⏳ Documentation framework (in progress)

### In Progress
- 🔄 Create project structure script
- 🔄 SESSION_NOTES.md
- 🔄 INIT_PROMPT template
- 🔄 generate_project_access.py

### Next Steps
1. Run create_project_structure.py
2. Initialize Git repository
3. Design detailed PostgreSQL schema
4. Map all Btrieve tables to PostgreSQL
5. Document data type conversions

---

## 💡 KEY INSIGHTS

### From nex-genesis-server Experience
1. **Btrieve Client Works:** 
   - Proven code ready to copy
   - All models tested (GSCAT, PAB, BARCODE, TSH, TSI)
   - Repository pattern available

2. **Critical Btrieve Rules:**
   - dataLen = 4 bytes (c_uint32)
   - Filename in key_buffer for open
   - Always close files in finally block
   - CP852/Windows-1250 encoding for text

3. **PLU Reservation Pattern:**
   - Create record with user ID
   - Read back and verify
   - Retry if conflict
   - Already working in NEX Genesis

### Qt5 Advantages
- Customer comfortable (similar to NEX Genesis)
- Keyboard shortcuts natural
- Grid editing proven
- Local cache possible
- Deployment via network share

---

## 🔧 CONFIGURATION STRATEGY

### config.yaml Structure
```yaml
database:
  postgres:
    host: localhost
    port: 5432
    database: invoice_staging
    user: invoices
    password: ${ENV:POSTGRES_PASSWORD}
  
  nex_genesis:
    root_path: C:\NEX
    stores_path: C:\NEX\YEARACT\STORES
    dials_path: C:\NEX\YEARACT\DIALS
    dll_path: C:\Program Files (x86)\Pervasive Software\PSQL\bin

application:
  window_title: Invoice Editor
  default_book: "001"
  book_type: "A"
  
  ui:
    theme: light
    font_size: 10
    grid_row_height: 25

logging:
  level: INFO
  file: logs/invoice_editor.log
  max_size: 10485760  # 10MB
  backup_count: 5
```

---

## 📊 SUCCESS METRICS

### Phase 1 (Setup)
- ✅ Project structure created
- ✅ Documentation framework ready
- ✅ Database schema designed
- ✅ Git initialized

### Phase 2 (Database)
- 🎯 Btrieve connection working
- 🎯 PostgreSQL connection working
- 🎯 Read from both databases
- 🎯 Data models functional

### Phase 3 (UI)
- 🎯 Main window displays
- 🎯 Invoice list loads
- 🎯 Detail window editable
- 🎯 Keyboard shortcuts work

### Phase 4 (Business)
- 🎯 Load invoices from staging
- 🎯 Edit all required fields
- 🎯 Calculate rabat correctly
- 🎯 Validation working

### Phase 5 (Integration)
- 🎯 Create products in GSCAT
- 🎯 Create delivery notes (TSH/TSI)
- 🎯 Handle all Btrieve operations
- 🎯 No data corruption

### Phase 6 (Production)
- 🎯 All tests pass
- 🎯 Executable builds
- 🎯 Customer acceptance
- 🎯 Deployed to production

---

## 🚨 CRITICAL REMINDERS

1. **32-bit Python Required**
   - NEX Genesis uses 32-bit Btrieve DLL
   - Use Python 3.11 32-bit
   - All dependencies must be 32-bit compatible

2. **Btrieve File Locking**
   - Always use try-finally
   - Close files even on error
   - File-level locks (not row-level)

3. **Single Operator Design**
   - No need for complex locking
   - PostgreSQL staging = master
   - Btrieve only on final approval

4. **Data Integrity**
   - Validate before Btrieve write
   - Use transactions where possible
   - Log all operations

5. **Development Workflow**
   - One task at a time
   - Test before proceeding
   - Update SESSION_NOTES.md
   - Commit working code

---

## 📝 SESSION LOG

### 2025-11-12 - Session 1 Start
- **Topic:** Project setup and architecture planning
- **Duration:** In progress
- **Key Decision:** Qt5 with direct Btrieve access
- **Next Session:** Database schema design and Btrieve integration

---

## 🔗 RELATED PROJECTS

### nex-genesis-server
- **URL:** https://github.com/rauschiccsk/nex-genesis-server
- **Status:** Phase 2.1 complete (FastAPI + Repositories)
- **Reusable Components:**
  - src/btrieve/ - Btrieve client ✅
  - src/models/ - All table models ✅
  - src/repositories/ - CRUD operations ✅
  - tests/ - Test patterns ✅

### supplier_invoice_loader
- **Status:** Production (generates ISDOC XML)
- **Integration:** Will write to PostgreSQL staging DB
- **Interface:** Direct PostgreSQL insert

---

## 📈 TOKEN USAGE TRACKING

**Current Chat:**
- Used: ~92,000 tokens
- Planning & architecture discussion
- No code generation yet (documentation only)

**Efficiency Strategy:**
- Use artifacts for all documents
- Minimal inline text
- Reference existing code
- Clear, structured sessions

---

**END OF SESSION NOTES**

**Status:** Session 1 in progress - Project setup  
**Next:** Finalize structure, create schemas, start Session 2  
**Ready for:** Database layer implementation