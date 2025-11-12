# INIT PROMPT - Session 5
# Invoice Editor - NEX Genesis Integration

**Project:** invoice-editor  
**Developer:** Zoltán (ICC Komárno)  
**Session Focus:** Phase 5 - NEX Genesis Integration  
**Date:** 2025-11-12+

---

## 📋 PROJECT STATUS

**Current State:** 70% complete (Phase 4 Complete - Database Integration Working)  
**Last Session:** Session 4B - PostgreSQL Integration & Schema Adaptation ✅ COMPLETE  
**Active Phase:** Phase 5 - NEX Genesis Integration  
**Next Goal:** Approval workflow + Delivery note creation

---

## ✅ SESSION 4B ACHIEVEMENTS

### PostgreSQL Integration - 100% Complete

1. ✅ **PostgreSQL Driver Switch**
   - Resolved 32-bit compatibility (psycopg3 → pg8000)
   - Pure Python driver (no libpq.dll dependency)
   - Working connection with environment variables

2. ✅ **Production Schema Adaptation**
   - Schema mapping layer in invoice_service.py
   - Production columns (edited_name, edited_mglst_code, etc.)
   - Mapped to UI columns (item_name, category_code, etc.)
   - Transparent to UI layer

3. ✅ **Full Database Integration**
   - Invoice list loads from PostgreSQL
   - Invoice items load from invoice_items_pending
   - Edit functionality with real-time calculation
   - Save updates database (edited columns)
   - Transaction handling with rollback

4. ✅ **Working Workflow**
   - Load invoices → Select → Open detail
   - Load items → Edit values → Auto-calculate
   - Save (Ctrl+S) → Update database → Refresh

---

## 🎯 SESSION 5 OBJECTIVES

### PRIORITY 1: Approval Workflow (HIGH)

**Goal:** Implement invoice approval process

**Tasks:**
1. Add "Schváliť" (Approve) button to detail window
2. Update invoice status: pending → approved
3. Set approved_by, approved_at timestamp
4. Trigger NEX Genesis operations
5. Close window and refresh list

**Deliverable:**
- Working approval button
- Status update in database
- Audit trail (invoice_log)

---

### PRIORITY 2: GSCAT Product Creation (HIGH)

**Goal:** Create/update products in NEX Genesis GSCAT

**Tasks:**
1. Check if product exists (by EAN or name)
2. Reserve PLU code if new product
3. Create GSCAT record
4. Set product attributes (name, prices, category)
5. Handle errors and rollback

**Key Fields:**
- GSCAT.NAME (from edited_name)
- GSCAT.MGLST (from edited_mglst_code)
- GSCAT.NAKUPC (from edited_price_buy)
- GSCAT.PREDAJC (from edited_price_sell)

**Deliverable:**
- Product creation in GSCAT.BTR
- PLU reservation mechanism
- Error handling

---

### PRIORITY 3: BARCODE Creation (MEDIUM)

**Goal:** Create barcode records in BARCODE.BTR

**Tasks:**
1. Create BARCODE record for each item
2. Link to GSCAT (PLU code)
3. Set EAN/barcode value
4. Handle duplicates

**Key Fields:**
- BARCODE.CARKOD (EAN from original_ean)
- BARCODE.GS (PLU from GSCAT)

**Deliverable:**
- Barcode records in BARCODE.BTR
- Link products to barcodes

---

### PRIORITY 4: Delivery Note Creation (MEDIUM)

**Goal:** Create delivery note (prijemka) in TSH/TSI

**Tasks:**
1. Create TSH header record
2. Create TSI item records for each line
3. Set document number, date, supplier
4. Link items to GSCAT products
5. Set quantities and prices

**Key Files:**
- TSHA-001.BTR (header)
- TSIA-001.BTR (items)

**Deliverable:**
- Delivery note in NEX Genesis
- Proper document numbering
- Linked to supplier (PAB)

---

## 📊 CURRENT PROJECT STATE

### What's Working ✅

1. **PostgreSQL Integration**
   - pg8000 Pure Python driver
   - Schema mapping layer
   - Load/save operations
   - Transaction handling

2. **UI Components**
   - Main window with invoice list
   - Detail window with editable grid
   - Real-time calculation
   - Keyboard shortcuts

3. **Edit Functionality**
   - In-place cell editing
   - Auto-calculate: rabat → price → total
   - Save to database
   - Validation

4. **Btrieve Components**
   - Client loaded and working
   - Models: GSCAT, BARCODE, PAB, MGLST
   - Read operations tested
   - Ready for write operations

### What's Pending ⏳

1. **Approval Workflow**
   - Approve button not implemented
   - Status change not working
   - No NEX Genesis trigger

2. **NEX Genesis Write**
   - No GSCAT create/update
   - No BARCODE creation
   - No TSH/TSI creation
   - No PLU reservation

3. **Advanced Features**
   - No item add/delete
   - No product lookup
   - No category dropdown
   - No batch operations

---

## 🏗️ NEX GENESIS ARCHITECTURE

### Database Files (Btrieve)

**GSCAT.BTR** - Product Catalog
- Key: PLU code (integer)
- Fields: NAME, MGLST, NAKUPC, PREDAJC, etc.
- Action: Create/Update products

**BARCODE.BTR** - Barcodes
- Key: CARKOD (EAN string)
- Fields: GS (PLU), CARKOD
- Action: Create barcode links

**PAB00000.BTR** - Business Partners
- Key: PAB_KOD (integer)
- Action: Validate supplier exists

**MGLST.BTR** - Categories
- Key: MGLST_KOD (integer)
- Action: Read only (validate category)

**TSHA-001.BTR** - Delivery Note Header
- Key: Document number
- Action: Create new document

**TSIA-001.BTR** - Delivery Note Items
- Key: Document number + line
- Action: Create line items

### Critical Btrieve Rules

1. **File Locking:** Btrieve locks entire file during write
2. **Transaction:** No built-in transactions, must handle manually
3. **Encoding:** CP852/Windows-1250 for strings
4. **Dates:** Delphi TDateTime format (base 1899-12-30)
5. **dataLen:** Always 4 bytes (c_uint32)

---

## 📁 KEY FILES FOR SESSION 5

### Files to Create

1. **src/business/nex_genesis_service.py** (NEW)
   - NEX Genesis operations
   - GSCAT create/update
   - BARCODE create
   - TSH/TSI create
   - PLU reservation

2. **src/business/approval_workflow.py** (NEW)
   - Approval process orchestration
   - Status updates
   - NEX Genesis trigger
   - Error handling

### Files to Update

3. **src/ui/invoice_detail_window.py**
   - Add "Schváliť" button
   - Connect to approval workflow
   - Show progress/errors

4. **src/business/invoice_service.py**
   - Add approval methods
   - Update invoice status
   - Log approval

---

## 🔧 DEVELOPMENT WORKFLOW - SESSION 5

### Step 1: Approval Button
```python
# In invoice_detail_window.py
approve_button = QPushButton("Schváliť faktúru")
approve_button.clicked.connect(self._on_approve)
```

### Step 2: NEX Genesis Service
```python
# src/business/nex_genesis_service.py
class NexGenesisService:
    def create_product(self, item_data):
        # Reserve PLU
        # Create GSCAT record
        # Create BARCODE record
        pass
```

### Step 3: Approval Workflow
```python
# src/business/approval_workflow.py
class ApprovalWorkflow:
    def approve_invoice(self, invoice_id):
        # For each item:
        #   - Create/update GSCAT
        #   - Create BARCODE
        # Create TSH/TSI
        # Update invoice status
        pass
```

---

## 🎯 SUCCESS CRITERIA - SESSION 5

### Must Achieve ✅

- ✅ Approve button works
- ✅ Invoice status changes to 'approved'
- ✅ Products created in GSCAT.BTR
- ✅ Barcodes created in BARCODE.BTR
- ✅ Delivery note created in TSH/TSI
- ✅ Error handling with rollback

### Quality Gates 🎨

1. All NEX Genesis writes successful
2. Data integrity maintained
3. Proper error messages
4. Audit trail complete
5. Transaction safety

---

## 🚨 CRITICAL REMINDERS

### NEX Genesis Rules

1. **PLU Reservation:** Must be unique, sequential
2. **File Locking:** Handle Btrieve file locks
3. **Encoding:** CP852 for all strings
4. **Dates:** Delphi TDateTime format
5. **Error Handling:** Manual rollback needed

### Development Principles

1. **One task at a time** - Wait for confirmation
2. **Test immediately** - After each component
3. **Update SESSION_NOTES.md** - After milestones
4. **All code in artifacts** - Never inline
5. **Transaction safety** - Rollback on error

---

## 📚 REFERENCE DOCUMENTS

### Load These First

1. **SESSION_NOTES.md** - Current project status (CRITICAL)
2. **project_file_access.json** - File manifest
3. This file - Session 5 objectives

### For NEX Genesis Integration

- **src/btrieve/btrieve_client.py** - Btrieve operations
- **src/models/gscat.py** - Product model
- **src/models/barcode.py** - Barcode model
- **src/models/pab.py** - Supplier model
- **docs/database/TYPE_MAPPINGS.md** - Type conversions

### For Workflow

- **src/business/invoice_service.py** - Current service layer
- **src/ui/invoice_detail_window.py** - Detail window UI

---

## 🎓 NEXT SESSION PREVIEW

**Session 6:** Testing & Production
- Unit tests
- Integration tests
- PyInstaller build
- Deployment
- Documentation

**Estimated Duration:** 4-6 hours

---

## 🔗 KEY ACHIEVEMENTS SO FAR

### Technical Stack ✅
- Qt5 UI working
- PostgreSQL integrated (pg8000)
- Btrieve client ready
- Schema mapping working
- Edit + Save functional

### User Workflow ✅
- Load invoices from database
- Open detail window
- Edit items with auto-calculation
- Save changes to PostgreSQL
- Ready for approval → NEX Genesis

---

**END OF INIT PROMPT - SESSION 5**

**Status:** Ready to implement NEX Genesis integration  
**Priority:** Approval workflow + Product creation  
**Goal:** Complete approval → delivery note creation  
**Duration:** 6-8 hours estimated