# Exploratory Data Analysis Report

## Dataset: `billing_document_cancellations`

### 1. Basic Information
- **Rows**: 80
- **Columns**: 14

### 2. Data Types
```markdown
| Column                     | Type    |
|:---------------------------|:--------|
| billingDocument            | int64   |
| billingDocumentType        | object  |
| creationDate               | object  |
| creationTime               | object  |
| lastChangeDateTime         | object  |
| billingDocumentDate        | object  |
| billingDocumentIsCancelled | bool    |
| cancelledBillingDocument   | object  |
| totalNetAmount             | float64 |
| transactionCurrency        | object  |
| companyCode                | object  |
| fiscalYear                 | int64   |
| accountingDocument         | int64   |
| soldToParty                | int64   |
```

### 3. Statistical Description
```markdown
| Statistic   |   billingDocument |   totalNetAmount |   fiscalYear |   accountingDocument |   soldToParty |
|:------------|------------------:|-----------------:|-------------:|---------------------:|--------------:|
| count       |      80           |           80     |           80 |         80           |      80       |
| mean        |       9.05195e+07 |          375.993 |         2025 |          9.40002e+09 |       3.2e+08 |
| std         |   49602.8         |          252.84  |            0 |      48970.4         |       0.6751  |
| min         |       9.05042e+07 |          151.69  |         2025 |          9.4e+09     |       3.2e+08 |
| 25%         |       9.05042e+07 |          221.19  |         2025 |          9.4e+09     |       3.2e+08 |
| 50%         |       9.05043e+07 |          329.66  |         2025 |          9.4e+09     |       3.2e+08 |
| 75%         |       9.05043e+07 |          442.183 |         2025 |          9.4e+09     |       3.2e+08 |
| max         |       9.06787e+07 |         2033.65  |         2025 |          9.40017e+09 |       3.2e+08 |
```

### 4. Missing Values (Nulls)
No missing values found in any columns.

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `billing_document_headers`

### 1. Basic Information
- **Rows**: 163
- **Columns**: 14

### 2. Data Types
```markdown
| Column                     | Type    |
|:---------------------------|:--------|
| billingDocument            | int64   |
| billingDocumentType        | object  |
| creationDate               | object  |
| creationTime               | object  |
| lastChangeDateTime         | object  |
| billingDocumentDate        | object  |
| billingDocumentIsCancelled | bool    |
| cancelledBillingDocument   | object  |
| totalNetAmount             | float64 |
| transactionCurrency        | object  |
| companyCode                | object  |
| fiscalYear                 | int64   |
| accountingDocument         | int64   |
| soldToParty                | int64   |
```

### 3. Statistical Description
```markdown
| Statistic   |   billingDocument |   totalNetAmount |   fiscalYear |   accountingDocument |   soldToParty |
|:------------|------------------:|-----------------:|-------------:|---------------------:|--------------:|
| count       |     163           |          163     |          163 |        163           |     163       |
| mean        |       9.08303e+07 |          373.673 |         2025 |          9.40032e+09 |       3.2e+08 |
| std         |  317149           |          250.308 |            0 |     312104           |       0.6758  |
| min         |       9.05042e+07 |          151.69  |         2025 |          9.4e+09     |       3.2e+08 |
| 25%         |       9.05043e+07 |          221.19  |         2025 |          9.4e+09     |       3.2e+08 |
| 50%         |       9.06787e+07 |          329.66  |         2025 |          9.40017e+09 |       3.2e+08 |
| 75%         |       9.11502e+07 |          439.83  |         2025 |          9.40064e+09 |       3.2e+08 |
| max         |       9.11502e+07 |         2033.65  |         2025 |          9.40064e+09 |       3.2e+08 |
```

### 4. Missing Values (Nulls)
No missing values found in any columns.

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `billing_document_items`

### 1. Basic Information
- **Rows**: 245
- **Columns**: 9

### 2. Data Types
```markdown
| Column                  | Type    |
|:------------------------|:--------|
| billingDocument         | int64   |
| billingDocumentItem     | int64   |
| material                | object  |
| billingQuantity         | int64   |
| billingQuantityUnit     | object  |
| netAmount               | float64 |
| transactionCurrency     | object  |
| referenceSdDocument     | int64   |
| referenceSdDocumentItem | int64   |
```

### 3. Statistical Description
```markdown
| Statistic   |   billingDocument |   billingDocumentItem |   billingQuantity |   netAmount |   referenceSdDocument |   referenceSdDocumentItem |
|:------------|------------------:|----------------------:|------------------:|------------:|----------------------:|--------------------------:|
| count       |     245           |              245      |          245      |     245     |         245           |                  245      |
| mean        |       9.08314e+07 |               20.2857 |            1.049  |     248.607 |           8.07396e+07 |                   20.2857 |
| std         |  317506           |               20.9684 |            0.2163 |     213.39  |        4733.82        |                   20.9684 |
| min         |       9.05042e+07 |               10      |            1      |       0     |           8.07379e+07 |                   10      |
| 25%         |       9.05043e+07 |               10      |            1      |       0     |           8.07381e+07 |                   10      |
| 50%         |       9.06787e+07 |               10      |            1      |     240.72  |           8.07381e+07 |                   10      |
| 75%         |       9.11502e+07 |               20      |            1      |     363.56  |           8.07381e+07 |                   20      |
| max         |       9.11502e+07 |              120      |            2      |    1301.82  |           8.07546e+07 |                  120      |
```

### 4. Missing Values (Nulls)
No missing values found in any columns.

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `business_partner_addresses`

### 1. Basic Information
- **Rows**: 8
- **Columns**: 20

### 2. Data Types
```markdown
| Column                 | Type   |
|:-----------------------|:-------|
| businessPartner        | int64  |
| addressId              | int64  |
| validityStartDate      | object |
| validityEndDate        | object |
| addressUuid            | object |
| addressTimeZone        | object |
| cityName               | object |
| country                | object |
| poBox                  | object |
| poBoxDeviatingCityName | object |
| poBoxDeviatingCountry  | object |
| poBoxDeviatingRegion   | object |
| poBoxIsWithoutNumber   | bool   |
| poBoxLobbyName         | object |
| poBoxPostalCode        | object |
| postalCode             | object |
| region                 | object |
| streetName             | object |
| taxJurisdiction        | object |
| transportZone          | object |
```

### 3. Statistical Description
```markdown
| Statistic   |   businessPartner |   addressId |
|:------------|------------------:|------------:|
| count       |       8           |        8    |
| mean        |       3.175e+08   |     8323.75 |
| std         |       4.62909e+06 |     2294.77 |
| min         |       3.1e+08     |     4605    |
| 25%         |       3.175e+08   |     8296.25 |
| 50%         |       3.2e+08     |     9550    |
| 75%         |       3.2e+08     |     9567.5  |
| max         |       3.2e+08     |     9598    |
```

### 4. Missing Values (Nulls)
No missing values found in any columns.

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `business_partners`

### 1. Basic Information
- **Rows**: 8
- **Columns**: 19

### 2. Data Types
```markdown
| Column                   | Type   |
|:-------------------------|:-------|
| businessPartner          | int64  |
| customer                 | int64  |
| businessPartnerCategory  | int64  |
| businessPartnerFullName  | object |
| businessPartnerGrouping  | object |
| businessPartnerName      | object |
| correspondenceLanguage   | object |
| createdByUser            | object |
| creationDate             | object |
| creationTime             | object |
| firstName                | object |
| formOfAddress            | int64  |
| industry                 | object |
| lastChangeDate           | object |
| lastName                 | object |
| organizationBpName1      | object |
| organizationBpName2      | object |
| businessPartnerIsBlocked | bool   |
| isMarkedForArchiving     | bool   |
```

### 3. Statistical Description
```markdown
| Statistic   |   businessPartner |    customer |   businessPartnerCategory |   formOfAddress |
|:------------|------------------:|------------:|--------------------------:|----------------:|
| count       |       8           | 8           |                         8 |               8 |
| mean        |       3.175e+08   | 3.175e+08   |                         2 |               3 |
| std         |       4.62909e+06 | 4.62909e+06 |                         0 |               0 |
| min         |       3.1e+08     | 3.1e+08     |                         2 |               3 |
| 25%         |       3.175e+08   | 3.175e+08   |                         2 |               3 |
| 50%         |       3.2e+08     | 3.2e+08     |                         2 |               3 |
| 75%         |       3.2e+08     | 3.2e+08     |                         2 |               3 |
| max         |       3.2e+08     | 3.2e+08     |                         2 |               3 |
```

### 4. Missing Values (Nulls)
No missing values found in any columns.

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `customer_company_assignments`

### 1. Basic Information
- **Rows**: 8
- **Columns**: 13

### 2. Data Types
```markdown
| Column                         | Type   |
|:-------------------------------|:-------|
| customer                       | int64  |
| companyCode                    | object |
| accountingClerk                | object |
| accountingClerkFaxNumber       | object |
| accountingClerkInternetAddress | object |
| accountingClerkPhoneNumber     | object |
| alternativePayerAccount        | object |
| paymentBlockingReason          | object |
| paymentMethodsList             | object |
| paymentTerms                   | object |
| reconciliationAccount          | int64  |
| deletionIndicator              | bool   |
| customerAccountGroup           | object |
```

### 3. Statistical Description
```markdown
| Statistic   |    customer |   reconciliationAccount |
|:------------|------------:|------------------------:|
| count       | 8           |                8        |
| mean        | 3.175e+08   |                1.55e+07 |
| std         | 4.62909e+06 |                4.6291   |
| min         | 3.1e+08     |                1.55e+07 |
| 25%         | 3.175e+08   |                1.55e+07 |
| 50%         | 3.2e+08     |                1.55e+07 |
| 75%         | 3.2e+08     |                1.55e+07 |
| max         | 3.2e+08     |                1.55e+07 |
```

### 4. Missing Values (Nulls)
No missing values found in any columns.

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `customer_sales_area_assignments`

### 1. Basic Information
- **Rows**: 28
- **Columns**: 19

### 2. Data Types
```markdown
| Column                      | Type   |
|:----------------------------|:-------|
| customer                    | int64  |
| salesOrganization           | object |
| distributionChannel         | object |
| division                    | int64  |
| billingIsBlockedForCustomer | object |
| completeDeliveryIsDefined   | bool   |
| creditControlArea           | object |
| currency                    | object |
| customerPaymentTerms        | object |
| deliveryPriority            | int64  |
| incotermsClassification     | object |
| incotermsLocation1          | object |
| salesGroup                  | object |
| salesOffice                 | object |
| shippingCondition           | object |
| slsUnlmtdOvrdelivIsAllwd    | bool   |
| supplyingPlant              | object |
| salesDistrict               | object |
| exchangeRateType            | object |
```

### 3. Statistical Description
```markdown
| Statistic   |     customer |   division |   deliveryPriority |
|:------------|-------------:|-----------:|-------------------:|
| count       | 28           |         28 |                 28 |
| mean        |  3.18572e+08 |         99 |                  0 |
| std         |  3.56348e+06 |          0 |                  0 |
| min         |  3.1e+08     |         99 |                  0 |
| 25%         |  3.2e+08     |         99 |                  0 |
| 50%         |  3.2e+08     |         99 |                  0 |
| 75%         |  3.2e+08     |         99 |                  0 |
| max         |  3.2e+08     |         99 |                  0 |
```

### 4. Missing Values (Nulls)
No missing values found in any columns.

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `journal_entry_items_accounts_receivable`

### 1. Basic Information
- **Rows**: 123
- **Columns**: 22

### 2. Data Types
```markdown
| Column                      | Type    |
|:----------------------------|:--------|
| companyCode                 | object  |
| fiscalYear                  | int64   |
| accountingDocument          | int64   |
| glAccount                   | int64   |
| referenceDocument           | int64   |
| costCenter                  | object  |
| profitCenter                | object  |
| transactionCurrency         | object  |
| amountInTransactionCurrency | float64 |
| companyCodeCurrency         | object  |
| amountInCompanyCodeCurrency | float64 |
| postingDate                 | object  |
| documentDate                | object  |
| accountingDocumentType      | object  |
| accountingDocumentItem      | int64   |
| assignmentReference         | object  |
| lastChangeDateTime          | object  |
| customer                    | int64   |
| financialAccountType        | object  |
| clearingDate                | object  |
| clearingAccountingDocument  | object  |
| clearingDocFiscalYear       | int64   |
```

### 3. Statistical Description
```markdown
| Statistic   |   fiscalYear |   accountingDocument |   glAccount |   referenceDocument |   amountInTransactionCurrency |   amountInCompanyCodeCurrency |   accountingDocumentItem |   customer |   clearingDocFiscalYear |
|:------------|-------------:|---------------------:|------------:|--------------------:|------------------------------:|------------------------------:|-------------------------:|-----------:|------------------------:|
| count       |          123 |        123           |  123        |       123           |                      123      |                      123      |                      123 |  123       |                 123     |
| mean        |         2025 |          9.4003e+09  |    1.55e+07 |         9.08103e+07 |                       98.3715 |                       98.3715 |                        1 |    3.2e+08 |                1975.61  |
| std         |            0 |     309775           |    0        |    314786           |                     1619.97   |                     1619.97   |                        0 |    0.3378  |                 313.649 |
| min         |         2025 |          9.4e+09     |    1.55e+07 |         9.05042e+07 |                    -7199.1    |                    -7199.1    |                        1 |    3.2e+08 |                   0     |
| 25%         |         2025 |          9.4e+09     |    1.55e+07 |         9.05042e+07 |                     -991.515  |                     -991.515  |                        1 |    3.2e+08 |                2025     |
| 50%         |         2025 |          9.40017e+09 |    1.55e+07 |         9.06787e+07 |                      638.4    |                      638.4    |                        1 |    3.2e+08 |                2025     |
| 75%         |         2025 |          9.40064e+09 |    1.55e+07 |         9.11502e+07 |                     1167      |                     1167      |                        1 |    3.2e+08 |                2025     |
| max         |         2025 |          9.40064e+09 |    1.55e+07 |         9.11502e+07 |                     7199.1    |                     7199.1    |                        1 |    3.2e+08 |                2025     |
```

### 4. Missing Values (Nulls)
```markdown
| Column       |   Null Count | Percentage   |
|:-------------|-------------:|:-------------|
| clearingDate |            3 | 2.44%        |
```

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `outbound_delivery_headers`

### 1. Basic Information
- **Rows**: 86
- **Columns**: 13

### 2. Data Types
```markdown
| Column                       | Type   |
|:-----------------------------|:-------|
| actualGoodsMovementDate      | object |
| actualGoodsMovementTime      | object |
| creationDate                 | object |
| creationTime                 | object |
| deliveryBlockReason          | object |
| deliveryDocument             | int64  |
| hdrGeneralIncompletionStatus | object |
| headerBillingBlockReason     | object |
| lastChangeDate               | object |
| overallGoodsMovementStatus   | object |
| overallPickingStatus         | object |
| overallProofOfDeliveryStatus | object |
| shippingPoint                | object |
```

### 3. Statistical Description
```markdown
| Statistic   |   deliveryDocument |
|:------------|-------------------:|
| count       |       86           |
| mean        |        8.07398e+07 |
| std         |     5092           |
| min         |        8.07377e+07 |
| 25%         |        8.07381e+07 |
| 50%         |        8.07381e+07 |
| 75%         |        8.07381e+07 |
| max         |        8.07546e+07 |
```

### 4. Missing Values (Nulls)
```markdown
| Column                  |   Null Count | Percentage   |
|:------------------------|-------------:|:-------------|
| actualGoodsMovementDate |           83 | 96.51%       |
| lastChangeDate          |            3 | 3.49%        |
```

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `outbound_delivery_items`

### 1. Basic Information
- **Rows**: 137
- **Columns**: 11

### 2. Data Types
```markdown
| Column                  | Type    |
|:------------------------|:--------|
| actualDeliveryQuantity  | int64   |
| batch                   | object  |
| deliveryDocument        | int64   |
| deliveryDocumentItem    | int64   |
| deliveryQuantityUnit    | object  |
| itemBillingBlockReason  | object  |
| lastChangeDate          | float64 |
| plant                   | object  |
| referenceSdDocument     | int64   |
| referenceSdDocumentItem | int64   |
| storageLocation         | object  |
```

### 3. Statistical Description
```markdown
| Statistic   |   actualDeliveryQuantity |   deliveryDocument |   deliveryDocumentItem |   lastChangeDate |   referenceSdDocument |   referenceSdDocumentItem |
|:------------|-------------------------:|-------------------:|-----------------------:|-----------------:|----------------------:|--------------------------:|
| count       |                 137      |      137           |               137      |                0 |              137      |                  137      |
| mean        |                   2.2263 |        8.07395e+07 |                20.8029 |              nan |           740549      |                   20.8029 |
| std         |                   5.6347 |     4699.57        |                20.3664 |              nan |               26.6614 |                   20.3664 |
| min         |                   1      |        8.07377e+07 |                10      |              nan |           740506      |                   10      |
| 25%         |                   1      |        8.07381e+07 |                10      |              nan |           740528      |                   10      |
| 50%         |                   1      |        8.07381e+07 |                10      |              nan |           740549      |                   10      |
| 75%         |                   1      |        8.07381e+07 |                20      |              nan |           740565      |                   20      |
| max         |                  48      |        8.07546e+07 |               120      |              nan |           740604      |                  120      |
```

### 4. Missing Values (Nulls)
```markdown
| Column         |   Null Count | Percentage   |
|:---------------|-------------:|:-------------|
| lastChangeDate |          137 | 100.0%       |
```

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `payments_accounts_receivable`

### 1. Basic Information
- **Rows**: 120
- **Columns**: 23

### 2. Data Types
```markdown
| Column                      | Type    |
|:----------------------------|:--------|
| companyCode                 | object  |
| fiscalYear                  | int64   |
| accountingDocument          | int64   |
| accountingDocumentItem      | int64   |
| clearingDate                | object  |
| clearingAccountingDocument  | int64   |
| clearingDocFiscalYear       | int64   |
| amountInTransactionCurrency | float64 |
| transactionCurrency         | object  |
| amountInCompanyCodeCurrency | float64 |
| companyCodeCurrency         | object  |
| customer                    | int64   |
| invoiceReference            | float64 |
| invoiceReferenceFiscalYear  | float64 |
| salesDocument               | float64 |
| salesDocumentItem           | float64 |
| postingDate                 | object  |
| documentDate                | object  |
| assignmentReference         | float64 |
| glAccount                   | int64   |
| financialAccountType        | object  |
| profitCenter                | object  |
| costCenter                  | float64 |
```

### 3. Statistical Description
```markdown
| Statistic   |   fiscalYear |   accountingDocument |   accountingDocumentItem |   clearingAccountingDocument |   clearingDocFiscalYear |   amountInTransactionCurrency |   amountInCompanyCodeCurrency |   customer |   invoiceReference |   invoiceReferenceFiscalYear |   salesDocument |   salesDocumentItem |   assignmentReference |   glAccount |   costCenter |
|:------------|-------------:|---------------------:|-------------------------:|-----------------------------:|------------------------:|------------------------------:|------------------------------:|-----------:|-------------------:|-----------------------------:|----------------:|--------------------:|----------------------:|------------:|-------------:|
| count       |          120 |        120           |                      120 |                120           |                     120 |                      120      |                      120      |  120       |                  0 |                            0 |               0 |                   0 |                     0 |  120        |            0 |
| mean        |         2025 |          9.40031e+09 |                        1 |                  9.40064e+09 |                    2025 |                       78.7088 |                       78.7088 |    3.2e+08 |                nan |                          nan |             nan |                 nan |                   nan |    1.55e+07 |          nan |
| std         |            0 |     311537           |                        0 |                 37.9587      |                       0 |                     1635.3    |                     1635.3    |    0.3224  |                nan |                          nan |             nan |                 nan |                   nan |    0        |          nan |
| min         |         2025 |          9.4e+09     |                        1 |                  9.40064e+09 |                    2025 |                    -7199.1    |                    -7199.1    |    3.2e+08 |                nan |                          nan |             nan |                 nan |                   nan |    1.55e+07 |          nan |
| 25%         |         2025 |          9.4e+09     |                        1 |                  9.40064e+09 |                    2025 |                    -1027.39   |                    -1027.39   |    3.2e+08 |                nan |                          nan |             nan |                 nan |                   nan |    1.55e+07 |          nan |
| 50%         |         2025 |          9.40017e+09 |                        1 |                  9.40064e+09 |                    2025 |                      634.83   |                      634.83   |    3.2e+08 |                nan |                          nan |             nan |                 nan |                   nan |    1.55e+07 |          nan |
| 75%         |         2025 |          9.40064e+09 |                        1 |                  9.40064e+09 |                    2025 |                     1167      |                     1167      |    3.2e+08 |                nan |                          nan |             nan |                 nan |                   nan |    1.55e+07 |          nan |
| max         |         2025 |          9.40064e+09 |                        1 |                  9.40064e+09 |                    2025 |                     7199.1    |                     7199.1    |    3.2e+08 |                nan |                          nan |             nan |                 nan |                   nan |    1.55e+07 |          nan |
```

### 4. Missing Values (Nulls)
```markdown
| Column                     |   Null Count | Percentage   |
|:---------------------------|-------------:|:-------------|
| invoiceReference           |          120 | 100.0%       |
| invoiceReferenceFiscalYear |          120 | 100.0%       |
| salesDocument              |          120 | 100.0%       |
| salesDocumentItem          |          120 | 100.0%       |
| assignmentReference        |          120 | 100.0%       |
| costCenter                 |          120 | 100.0%       |
```

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `plants`

### 1. Basic Information
- **Rows**: 44
- **Columns**: 14

### 2. Data Types
```markdown
| Column                        | Type   |
|:------------------------------|:-------|
| plant                         | object |
| plantName                     | object |
| valuationArea                 | object |
| plantCustomer                 | object |
| plantSupplier                 | object |
| factoryCalendar               | object |
| defaultPurchasingOrganization | object |
| salesOrganization             | object |
| addressId                     | int64  |
| plantCategory                 | object |
| distributionChannel           | int64  |
| division                      | int64  |
| language                      | object |
| isMarkedForArchiving          | bool   |
```

### 3. Statistical Description
```markdown
| Statistic   |   addressId |   distributionChannel |   division |
|:------------|------------:|----------------------:|-----------:|
| count       |      44     |                    44 |         44 |
| mean        |     602.795 |                    80 |         99 |
| std         |     330.952 |                     0 |          0 |
| min         |      22     |                    80 |         99 |
| 25%         |     132.75  |                    80 |         99 |
| 50%         |     799.5   |                    80 |         99 |
| 75%         |     810.25  |                    80 |         99 |
| max         |     902     |                    80 |         99 |
```

### 4. Missing Values (Nulls)
No missing values found in any columns.

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `product_descriptions`

### 1. Basic Information
- **Rows**: 69
- **Columns**: 3

### 2. Data Types
```markdown
| Column             | Type   |
|:-------------------|:-------|
| product            | object |
| language           | object |
| productDescription | object |
```

### 3. Statistical Description
No numeric columns available to describe.

### 4. Missing Values (Nulls)
No missing values found in any columns.

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `product_plants`

### 1. Basic Information
- **Rows**: 3,036
- **Columns**: 9

### 2. Data Types
```markdown
| Column                     | Type   |
|:---------------------------|:-------|
| product                    | object |
| plant                      | object |
| countryOfOrigin            | object |
| regionOfOrigin             | object |
| productionInvtryManagedLoc | object |
| availabilityCheckType      | object |
| fiscalYearVariant          | object |
| profitCenter               | object |
| mrpType                    | object |
```

### 3. Statistical Description
No numeric columns available to describe.

### 4. Missing Values (Nulls)
No missing values found in any columns.

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `product_storage_locations`

### 1. Basic Information
- **Rows**: 16,723
- **Columns**: 5

### 2. Data Types
```markdown
| Column                         | Type    |
|:-------------------------------|:--------|
| product                        | object  |
| plant                          | object  |
| storageLocation                | object  |
| physicalInventoryBlockInd      | object  |
| dateOfLastPostedCntUnRstrcdStk | float64 |
```

### 3. Statistical Description
```markdown
| Statistic   |   dateOfLastPostedCntUnRstrcdStk |
|:------------|---------------------------------:|
| count       |                                0 |
| mean        |                              nan |
| std         |                              nan |
| min         |                              nan |
| 25%         |                              nan |
| 50%         |                              nan |
| 75%         |                              nan |
| max         |                              nan |
```

### 4. Missing Values (Nulls)
```markdown
| Column                         |   Null Count | Percentage   |
|:-------------------------------|-------------:|:-------------|
| dateOfLastPostedCntUnRstrcdStk |        16723 | 100.0%       |
```

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `products`

### 1. Basic Information
- **Rows**: 69
- **Columns**: 17

### 2. Data Types
```markdown
| Column                       | Type    |
|:-----------------------------|:--------|
| product                      | object  |
| productType                  | object  |
| crossPlantStatus             | object  |
| crossPlantStatusValidityDate | float64 |
| creationDate                 | object  |
| createdByUser                | object  |
| lastChangeDate               | object  |
| lastChangeDateTime           | object  |
| isMarkedForDeletion          | bool    |
| productOldId                 | object  |
| grossWeight                  | float64 |
| weightUnit                   | object  |
| netWeight                    | float64 |
| productGroup                 | object  |
| baseUnit                     | object  |
| division                     | int64   |
| industrySector               | object  |
```

### 3. Statistical Description
```markdown
| Statistic   |   crossPlantStatusValidityDate |   grossWeight |   netWeight |   division |
|:------------|-------------------------------:|--------------:|------------:|-----------:|
| count       |                              0 |       69      |     69      |     69     |
| mean        |                            nan |        0.0347 |      0.0309 |      1.029 |
| std         |                            nan |        0.0417 |      0.0383 |      0.169 |
| min         |                            nan |        0.012  |      0.01   |      1     |
| 25%         |                            nan |        0.012  |      0.01   |      1     |
| 50%         |                            nan |        0.012  |      0.01   |      1     |
| 75%         |                            nan |        0.012  |      0.01   |      1     |
| max         |                            nan |        0.11   |      0.1    |      2     |
```

### 4. Missing Values (Nulls)
```markdown
| Column                       |   Null Count | Percentage   |
|:-----------------------------|-------------:|:-------------|
| crossPlantStatusValidityDate |           69 | 100.0%       |
```

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
- **`crossPlantStatusValidityDate`**: Contains 69 missing values.

---

## Dataset: `sales_order_headers`

### 1. Basic Information
- **Rows**: 100
- **Columns**: 24

### 2. Data Types
```markdown
| Column                      | Type    |
|:----------------------------|:--------|
| salesOrder                  | int64   |
| salesOrderType              | object  |
| salesOrganization           | object  |
| distributionChannel         | int64   |
| organizationDivision        | int64   |
| salesGroup                  | object  |
| salesOffice                 | object  |
| soldToParty                 | int64   |
| creationDate                | object  |
| createdByUser               | object  |
| lastChangeDateTime          | object  |
| totalNetAmount              | float64 |
| overallDeliveryStatus       | object  |
| overallOrdReltdBillgStatus  | object  |
| overallSdDocReferenceStatus | object  |
| transactionCurrency         | object  |
| pricingDate                 | object  |
| requestedDeliveryDate       | object  |
| headerBillingBlockReason    | object  |
| deliveryBlockReason         | object  |
| incotermsClassification     | object  |
| incotermsLocation1          | object  |
| customerPaymentTerms        | object  |
| totalCreditCheckStatus      | object  |
```

### 3. Statistical Description
```markdown
| Statistic   |   salesOrder |   distributionChannel |   organizationDivision |   soldToParty |   totalNetAmount |
|:------------|-------------:|----------------------:|-----------------------:|--------------:|-----------------:|
| count       |     100      |              100      |                    100 | 100           |          100     |
| mean        |  740556      |               10.82   |                     99 |   3.197e+08   |          708.783 |
| std         |      29.0115 |                1.0287 |                      0 |   1.71446e+06 |         2507.39  |
| min         |  740506      |                5      |                     99 |   3.1e+08     |          118.64  |
| 25%         |  740531      |               11      |                     99 |   3.2e+08     |          215.25  |
| 50%         |  740556      |               11      |                     99 |   3.2e+08     |          307.075 |
| 75%         |  740580      |               11      |                     99 |   3.2e+08     |          436.635 |
| max         |  740605      |               11      |                     99 |   3.2e+08     |        19021.3   |
```

### 4. Missing Values (Nulls)
No missing values found in any columns.

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `sales_order_items`

### 1. Basic Information
- **Rows**: 167
- **Columns**: 13

### 2. Data Types
```markdown
| Column                  | Type    |
|:------------------------|:--------|
| salesOrder              | int64   |
| salesOrderItem          | int64   |
| salesOrderItemCategory  | object  |
| material                | object  |
| requestedQuantity       | int64   |
| requestedQuantityUnit   | object  |
| transactionCurrency     | object  |
| netAmount               | float64 |
| materialGroup           | object  |
| productionPlant         | object  |
| storageLocation         | object  |
| salesDocumentRjcnReason | object  |
| itemBillingBlockReason  | object  |
```

### 3. Statistical Description
```markdown
| Statistic   |   salesOrder |   salesOrderItem |   requestedQuantity |   netAmount |
|:------------|-------------:|-----------------:|--------------------:|------------:|
| count       |     167      |         167      |            167      |     167     |
| mean        |  740558      |          21.018  |              2.012  |     424.421 |
| std         |      30.3252 |          19.3458 |              5.1214 |    1078.19  |
| min         |  740506      |          10      |              1      |       0     |
| 25%         |  740534      |          10      |              1      |       0     |
| 50%         |  740556      |          10      |              1      |     216.1   |
| 75%         |  740586      |          30      |              1      |     363.56  |
| max         |  740605      |         120      |             48      |    9966.1   |
```

### 4. Missing Values (Nulls)
No missing values found in any columns.

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

## Dataset: `sales_order_schedule_lines`

### 1. Basic Information
- **Rows**: 179
- **Columns**: 6

### 2. Data Types
```markdown
| Column                        | Type   |
|:------------------------------|:-------|
| salesOrder                    | int64  |
| salesOrderItem                | int64  |
| scheduleLine                  | int64  |
| confirmedDeliveryDate         | object |
| orderQuantityUnit             | object |
| confdOrderQtyByMatlAvailCheck | int64  |
```

### 3. Statistical Description
```markdown
| Statistic   |   salesOrder |   salesOrderItem |   scheduleLine |   confdOrderQtyByMatlAvailCheck |
|:------------|-------------:|-----------------:|---------------:|--------------------------------:|
| count       |      179     |         179      |       179      |                        179      |
| mean        |   740556     |          20.5028 |         1.067  |                          1.8771 |
| std         |       29.694 |          18.8511 |         0.2508 |                          4.9714 |
| min         |   740506     |          10      |         1      |                          0      |
| 25%         |   740534     |          10      |         1      |                          1      |
| 50%         |   740555     |          10      |         1      |                          1      |
| 75%         |   740582     |          25      |         1      |                          1      |
| max         |   740605     |         120      |         2      |                         48      |
```

### 4. Missing Values (Nulls)
```markdown
| Column                |   Null Count | Percentage   |
|:----------------------|-------------:|:-------------|
| confirmedDeliveryDate |           12 | 6.7%         |
```

### 5. Duplicates
- **Number of fully duplicated rows**: 0

### 6. Inconsistent IDs / Anomalies
No obvious inconsistencies detected in ID columns based on basic heuristics.

---

