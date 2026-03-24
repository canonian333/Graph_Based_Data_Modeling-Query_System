# Data Preprocessing Report

This report details the transformations applied to the O2C dataset, including foreign key normalisation, stable node IDs, and data quality mitigations based on EDA.

## Dataset: `billing_document_cancellations`
- **Original Shape**: 80 rows, 14 columns
- **Duplicates Removed**: 0
- **Normalised IDs & Assigned Stable Prefixes**: billingDocument, cancelledBillingDocument, companyCode, accountingDocument, soldToParty
- **Final Shape**: 80 rows, 14 columns

## Dataset: `billing_document_headers`
- **Original Shape**: 163 rows, 14 columns
- **Duplicates Removed**: 0
- **Normalised IDs & Assigned Stable Prefixes**: billingDocument, cancelledBillingDocument, companyCode, accountingDocument, soldToParty
- **Final Shape**: 163 rows, 14 columns

## Dataset: `billing_document_items`
- **Original Shape**: 245 rows, 9 columns
- **Duplicates Removed**: 0
- **Normalised IDs & Assigned Stable Prefixes**: billingDocument, material, referenceSdDocument
- **Final Shape**: 245 rows, 9 columns

## Dataset: `business_partner_addresses`
- **Original Shape**: 8 rows, 20 columns
- **Duplicates Removed**: 0
- **Normalised IDs & Assigned Stable Prefixes**: businessPartner
- **Final Shape**: 8 rows, 20 columns

## Dataset: `business_partners`
- **Original Shape**: 8 rows, 19 columns
- **Duplicates Removed**: 0
- **Normalised IDs & Assigned Stable Prefixes**: businessPartner, customer
- **Final Shape**: 8 rows, 19 columns

## Dataset: `customer_company_assignments`
- **Original Shape**: 8 rows, 13 columns
- **Duplicates Removed**: 0
- **Normalised IDs & Assigned Stable Prefixes**: customer, companyCode, reconciliationAccount
- **Final Shape**: 8 rows, 13 columns

## Dataset: `customer_sales_area_assignments`
- **Original Shape**: 28 rows, 19 columns
- **Duplicates Removed**: 0
- **Normalised IDs & Assigned Stable Prefixes**: customer
- **Final Shape**: 28 rows, 19 columns

## Dataset: `journal_entry_items_accounts_receivable`
- **Original Shape**: 123 rows, 22 columns
- **Duplicates Removed**: 0
- **Normalised IDs & Assigned Stable Prefixes**: companyCode, accountingDocument, glAccount, referenceDocument, customer, clearingAccountingDocument
- **Final Shape**: 123 rows, 22 columns

## Dataset: `outbound_delivery_headers`
- **Original Shape**: 86 rows, 13 columns
- **Duplicates Removed**: 0
- **Dropped sparse columns (>90% null)**: actualGoodsMovementDate
- **Normalised IDs & Assigned Stable Prefixes**: deliveryDocument, shippingPoint
- **Final Shape**: 86 rows, 12 columns

## Dataset: `outbound_delivery_items`
- **Original Shape**: 137 rows, 11 columns
- **Duplicates Removed**: 0
- **Dropped sparse columns (>90% null)**: lastChangeDate
- **Normalised IDs & Assigned Stable Prefixes**: deliveryDocument, plant, referenceSdDocument
- **Final Shape**: 137 rows, 10 columns

## Dataset: `payments_accounts_receivable`
- **Original Shape**: 120 rows, 23 columns
- **Duplicates Removed**: 0
- **Dropped sparse columns (>90% null)**: invoiceReference, invoiceReferenceFiscalYear, salesDocument, salesDocumentItem, assignmentReference, costCenter
- **Normalised IDs & Assigned Stable Prefixes**: companyCode, accountingDocument, clearingAccountingDocument, customer, glAccount
- **Final Shape**: 120 rows, 17 columns

## Dataset: `plants`
- **Original Shape**: 44 rows, 14 columns
- **Duplicates Removed**: 0
- **Normalised IDs & Assigned Stable Prefixes**: plant
- **Final Shape**: 44 rows, 14 columns

## Dataset: `product_descriptions`
- **Original Shape**: 69 rows, 3 columns
- **Duplicates Removed**: 0
- **Normalised IDs & Assigned Stable Prefixes**: product
- **Final Shape**: 69 rows, 3 columns

## Dataset: `product_plants`
- **Original Shape**: 3036 rows, 9 columns
- **Duplicates Removed**: 0
- **Normalised IDs & Assigned Stable Prefixes**: product, plant
- **Final Shape**: 3036 rows, 9 columns

## Dataset: `product_storage_locations`
- **Original Shape**: 16723 rows, 5 columns
- **Duplicates Removed**: 0
- **Dropped sparse columns (>90% null)**: dateOfLastPostedCntUnRstrcdStk
- **Normalised IDs & Assigned Stable Prefixes**: product, plant
- **Final Shape**: 16723 rows, 4 columns

## Dataset: `products`
- **Original Shape**: 69 rows, 17 columns
- **Duplicates Removed**: 0
- **Dropped sparse columns (>90% null)**: crossPlantStatusValidityDate
- **Normalised IDs & Assigned Stable Prefixes**: product
- **Final Shape**: 69 rows, 16 columns

## Dataset: `sales_order_headers`
- **Original Shape**: 100 rows, 24 columns
- **Duplicates Removed**: 0
- **Normalised IDs & Assigned Stable Prefixes**: salesOrder, soldToParty
- **Final Shape**: 100 rows, 24 columns

## Dataset: `sales_order_items`
- **Original Shape**: 167 rows, 13 columns
- **Duplicates Removed**: 0
- **Normalised IDs & Assigned Stable Prefixes**: salesOrder, material
- **Final Shape**: 167 rows, 13 columns

## Dataset: `sales_order_schedule_lines`
- **Original Shape**: 179 rows, 6 columns
- **Duplicates Removed**: 0
- **Normalised IDs & Assigned Stable Prefixes**: salesOrder
- **Final Shape**: 179 rows, 6 columns

