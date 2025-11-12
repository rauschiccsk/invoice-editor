# INIT PROMPT - New Chat Session
# Invoice Editor - ISDOC Invoice Approval & NEX Genesis Integration

**Project:** invoice-editor  
**Developer:** Zoltán (ICC Komárno)  
**Repository:** https://github.com/rauschiccsk/invoice-editor

---

## 🚀 QUICK START FOR NEW SESSION

### CRITICAL: Load Context First!

**Always load these 2 files at the start of EVERY new chat:**

1. **SESSION_NOTES.md** - Current project status and progress
2. **project_file_access.json** - Manifest of all project files

**GitHub URLs (with cache busting):**
```
https://raw.githubusercontent.com/rauschiccsk/invoice-editor/main/SESSION_NOTES.md?v=TIMESTAMP
https://raw.githubusercontent.com/rauschiccsk/invoice-editor/main/docs/project_file_access.json?v=TIMESTAMP
```

**Note:** Replace TIMESTAMP with actual cache version from generate_project_access.py output.

---

## 📋 PROJECT OVERVIEW

### What is Invoice Editor?

Qt5 desktop aplikácia pre schvaľovanie a editáciu dodávateľských faktúr pred zaevidovaním do NEX Genesis ERP.

### Complete Workflow
```
supplier_invoice_loader
    ↓ (Email PDF → ISDOC XML)
PostgreSQL Staging DB
    ↓ (Store pending invoices)
Invoice Editor (Qt5) ← THIS APPLICATION
    ↓ (Operator approves/edits)
NEX Genesis (Btrieve)
    ↓ (Create delivery notes, products, barcodes)
```

### Key Features
- 📋 Display pending invoices from PostgreSQL
- ✏️ Edit item names, categories, prices, rabat %
- 💰 Automatic price recalculation on rabat change
- ✅ Approve → create delivery notes in NEX Genesis
- 🔄 Direct Btrieve access (no API middleware)

---

## 🏗️ ARCHITECTURE

### Technology Stack
- **UI:** Qt5 (PyQt5)
- **Language:** Python 3.11+ (32-bit REQUIRED!)
- **Staging DB:** PostgreSQL
- **Production DB:** NEX Genesis (Btrieve)
- **Deployment:** PyInstaller single executable

### Key Decisions
1. ✅ Qt5 desktop app (not web-based)
2. ✅ Direct Btrieve access (proven from nex-genesis-server)
3. ✅ PostgreSQL staging for approval workflow
4. ✅ Single operator (no multi-user locking)

---

## 📁 PROJECT STRUCTURE

```
invoice-editor/
├── docs/               # Documentation
├── src/
│   ├── ui/            # Qt5 UI components
│   ├── btrieve/       # Btrieve client (from nex-genesis-server)
│   ├── models/        # Data models
│   ├── database/      # PostgreSQL access
│   ├── business/      # Business logic
│   └── utils/         # Utilities
├── database/          # PostgreSQL schemas
├── config/            # Configuration
├── scripts/           # Utility scripts
├── tests/             # Test suite
├── resources/         # Icons, UI files
├── main.py           # Entry point
└── requirements.txt
```

---

## 🗄️ DATABASES

### PostgreSQL Staging
- **invoices_pending** - Headers
- **invoice_items_pending** - Line items (editable)
- **invoice_log** - Audit trail
- **Cache tables** - GSCAT, BARCODE, MGLST (synced from NEX)

### NEX Genesis (Btrieve)
- **GSCAT.BTR** - Product catalog
- **BARCODE.BTR** - Barcodes
- **PAB00000.BTR** - Business partners
- **TSHA-001.BTR** - Delivery notes header
- **TSIA-001.BTR** - Delivery notes items
- **MGLST.BTR** - Categories

---

## 🎯 DEVELOPMENT WORKFLOW

### Session Pattern
1. **Load context** - SESSION_NOTES.md + project_file_access.json
2. **Check current status** - What's completed? What's next?
3. **Work on one task** - Complete before moving to next
4. **Test immediately** - Verify before proceeding
5. **Update SESSION_NOTES.md** - Document progress
6. **Commit changes** - Frequent small commits

### Task Execution
- ✅ One step at a time
- ✅ Wait for confirmation before next step
- ✅ All code in artifacts (never inline)
- ✅ Test after each change
- ✅ Update documentation

---

## 📚 KEY REFERENCE DOCUMENTS

**Always check SESSION_NOTES.md for:**
- Current phase and progress
- Active tasks
- Last session achievements
- Next steps
- Known issues

**Architecture & Design:**
- `docs/architecture/` - Architecture decisions
- `docs/database/` - Database schemas and mappings
- `docs/sessions/` - Historical session notes

**From nex-genesis-server:**
- Btrieve client implementation
- Data models (GSCAT, PAB, BARCODE, TSH, TSI)
- Critical Btrieve rules (dataLen=4 bytes, encoding, etc.)

---

## 🔒 CRITICAL RULES

### Btrieve Requirements
1. **32-bit Python MANDATORY** - NEX Genesis uses 32-bit DLL
2. **Proven components available** - from nex-genesis-server
3. **File-level locking** - Btrieve locks entire file
4. **Single operator design** - No concurrent conflicts

### Development Principles
1. **One task at a time** - Complete before next
2. **Test immediately** - Don't accumulate untested code
3. **Update SESSION_NOTES.md** - After each task
4. **Commit frequently** - Small, working commits
5. **All code in artifacts** - Never inline
6. **No alternatives** - Single recommended solution only

### Communication
- **Language:** Slovak (technical terms in English)
- **Format:** Clear, structured, actionable
- **Code:** Always in artifacts
- **Confirmation:** Wait before proceeding to next step

---

## 🎓 REMINDERS FOR CLAUDE

1. **Load context FIRST:**
   - SESSION_NOTES.md (current progress)
   - project_file_access.json (file manifest)

2. **Check current phase:**
   - Where are we in development?
   - What's the active task?
   - What was completed last session?

3. **One step at a time:**
   - Present single task
   - Wait for confirmation
   - Test before next step

4. **Update SESSION_NOTES.md:**
   - After completing tasks
   - Document decisions
   - Track progress

5. **Use proven components:**
   - Copy from nex-genesis-server
   - Don't reinvent Btrieve client
   - Use tested patterns

---

## 📊 DEVELOPMENT PHASES

1. **Setup** (5%) - Project structure, Git
2. **Database Layer** (15%) - PostgreSQL + Btrieve
3. **UI Foundation** (25%) - Main window, invoice list
4. **Business Logic** (30%) - Edit, validate, approve
5. **NEX Integration** (20%) - Create delivery notes, products
6. **Testing & Production** (5%) - Tests, build, deploy

**Check SESSION_NOTES.md for current phase and detailed tasks!**

---

## 🔗 RELATED RESOURCES

- **nex-genesis-server:** https://github.com/rauschiccsk/nex-genesis-server
- **supplier_invoice_loader:** Production (generates ISDOC)
- **NEX Genesis ERP:** Target system (Delphi 6 + Btrieve)

---

## ⚡ START NEW SESSION

**Steps:**
1. ✅ Load SESSION_NOTES.md
2. ✅ Load project_file_access.json
3. ✅ Review current phase and progress
4. ✅ Identify next task from SESSION_NOTES.md
5. ✅ Present task to user
6. ✅ Wait for confirmation
7. ✅ Execute task step-by-step
8. ✅ Test and verify
9. ✅ Update SESSION_NOTES.md
10. ✅ Commit changes

---

**REMEMBER:**
- 🔴 Always load context first (SESSION_NOTES.md)
- 🔴 One task at a time
- 🔴 Test immediately
- 🔴 Update documentation
- 🔴 Slovak language (technical terms in English)

---

**END OF INIT PROMPT**

**Ready to start?** Load SESSION_NOTES.md and let's continue! 🚀