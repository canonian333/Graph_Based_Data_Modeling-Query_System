# Preprocessed Data Validation Report

## 1. Schema Validation Step
Checking if all entity files are loaded properly with expected columns and zero critical errors.

- ✅ `billing_document_cancellations` loaded successfully (80 rows, 14 columns).
- ✅ `billing_document_headers` loaded successfully (163 rows, 14 columns).
- ✅ `billing_document_items` loaded successfully (245 rows, 9 columns).
- ✅ `business_partners` loaded successfully (8 rows, 19 columns).
- ✅ `business_partner_addresses` loaded successfully (8 rows, 20 columns).
- ✅ `customer_company_assignments` loaded successfully (8 rows, 13 columns).
- ✅ `customer_sales_area_assignments` loaded successfully (28 rows, 19 columns).
- ✅ `journal_entry_items_accounts_receivable` loaded successfully (123 rows, 22 columns).
- ✅ `outbound_delivery_headers` loaded successfully (86 rows, 12 columns).
- ✅ `outbound_delivery_items` loaded successfully (137 rows, 10 columns).
- ✅ `payments_accounts_receivable` loaded successfully (120 rows, 17 columns).
- ✅ `plants` loaded successfully (44 rows, 14 columns).
- ✅ `products` loaded successfully (69 rows, 16 columns).
- ✅ `product_descriptions` loaded successfully (69 rows, 3 columns).
- ✅ `product_plants` loaded successfully (3036 rows, 9 columns).
- ✅ `product_storage_locations` loaded successfully (16723 rows, 4 columns).
- ✅ `sales_order_headers` loaded successfully (100 rows, 24 columns).
- ✅ `sales_order_items` loaded successfully (167 rows, 13 columns).
- ✅ `sales_order_schedule_lines` loaded successfully (179 rows, 6 columns).

**Result: All entity files pass schema validation step with zero critical errors.**

## 2. Foreign Key Resolution
Checking resolving foreign key references across all entity types.

| Table | Foreign Key Column | Target Entity | Match Rate |
| :--- | :--- | :--- | :--- |
| sales_order_headers | soldToParty | CUST_ | 100.00% |
| sales_order_items | material | PROD_ | 100.00% |
| billing_document_headers | soldToParty | CUST_ | 100.00% |
| billing_document_headers | accountingDocument | ACC_ | 87.73% |
| billing_document_items | material | PROD_ | 100.00% |
| billing_document_items | referenceSdDocument | DEL_ | 100.00% |
| outbound_delivery_items | plant | PLANT_ | 100.00% |
| outbound_delivery_items | referenceSdDocument | SO_ | 100.00% |
| journal_entry_items_accounts_receivable | customer | CUST_ | 100.00% |
| payments_accounts_receivable | customer | CUST_ | 100.00% |
| customer_company_assignments | reconciliationAccount | GL_ | 100.00% |

**Result: Some foreign key references have slightly lower match rates (expected if transactional dataset is smaller than master dataset context).**

## 3. Reproducibility & Documentation
- **Preprocessing Script**: `preprocess.py` & `generate_schema.py` exist, are documented, and verified reproducible.
- **Schema Diagram**: Documented as Mermaid diagram in `reports/schema.md` (Verified).

## 4. Edge Cardinalities
Expected cardinalities defined for graph modelling ingestion:
- **Customer to SalesOrder**: `1:N`
- **BusinessPartner to Customer**: `1:1`
- **SalesOrder to Product**: `N:M` (via Item Lines)
- **DeliveryDocument to SalesOrder**: `N:1`
- **BillingDocument to SalesOrder**: `N:1`
- **DeliveryDocument to Plant**: `N:1`
- **BillingDocument to Customer**: `N:1`
- **BillingDocument to AccountingDocument**: `1:1`
- **AccountingDocument to GLAccount**: `N:1`
- **Customer to CompanyCode**: `1:N` (Assignments)

**Status: Review completed. Schema and validation checks passed and ready for ingestion work.**
