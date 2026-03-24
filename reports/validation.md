# Preprocessed Data & Graph Validation Report

## 1. Local Schema Validation Step
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

## 2. Graph Integrity & Flow Validation
Running Cypher queries to detect orphaned nodes, missing relationships, and broken business flows. Problematic nodes are flagged in the graph with the `Flagged` label and a `flagReason` property.

| Check Description | Entity | Broken Count | Queryable Metadata |
| :--- | :--- | :--- | :--- |
| Orphaned Nodes (No Edges) | Plant, CompanyCode | 40 ⚠️ | `MATCH (n:Flagged {flagReason: 'Orphaned Node'})` |
| Missing Product Reference in Sales Orders | - | 0 ✅ | - |
| Missing Delivery Reference in Billing | - | 0 ✅ | - |
| Broken Flow: Sales Orders with No Delivery | SalesOrder | 14 ⚠️ | `MATCH (n:Flagged {flagReason: 'O2C Leak: No Delivery Found'})` |
| Broken Flow: Deliveries with No Billing | DeliveryDocument | 86 ⚠️ | `MATCH (n:Flagged {flagReason: 'O2C Leak: No Billing Found'})` |
| Broken Flow: Billing with No Accounting | BillingDocument | 40 ⚠️ | `MATCH (n:Flagged {flagReason: 'O2C Leak: No Accounting Document Found'})` |

## 3. Edge Cardinalities
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

**Status: Review and Graph Integrity checks completed.**
