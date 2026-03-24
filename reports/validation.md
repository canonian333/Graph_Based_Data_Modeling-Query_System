# O2C Graph Integrity Validation Report

This report details the operational state of the graph data, flagging any integrity issues, orphaned data, or broken business flows.

## 1. Orphaned Nodes
Nodes disconnected from any other entity. Flagged in graph as `:Orphaned`.

| Node Label | Orphan Count |
| :--- | :--- |
| Plant | 39 |
| CompanyCode | 1 |

## 2. Missing Key Relationships
Entities structurally missing required conceptual edges. Flagged in graph as `:Incomplete`.

| Structural Flow Check | Missing Count |
| :--- | :--- |
| SalesOrder Missing Items | 0 |
| SalesOrderItem Missing Product | 0 |
| DeliveryItem Missing Plant | 0 |
| BillingDoc Missing Customer | 0 |

## 3. Broken Business Flows
End-to-End O2C process bottlenecks or disjointed transactions. Flagged as `:BrokenFlow`.

| Business Process Check | Broken Flow Count |
| :--- | :--- |
| Ordered Not Shipped | 14 |
| Shipped Not Billed | 137 |
| Billed No Accounting | 40 |

## Data Engineering Action
Problematic nodes have successfully been annotated as queryable metadata within the graph. You can inspect the flagged entries using the following Cypher queries:
```cypher
// Find Orphaned Nodes
MATCH (n:Orphaned) RETURN labels(n) AS Entity, n.id AS ID, n.validationFlags AS Flags LIMIT 10;

// Find Incompletable Structure
MATCH (n:Incomplete) RETURN labels(n) AS Entity, n.id AS ID, n.validationFlags AS Flags LIMIT 10;

// Find Broken Business Processes (e.g. Shipped but not billed)
MATCH (n:BrokenFlow) RETURN labels(n) AS Entity, n.id AS ID, n.validationFlags AS Flags LIMIT 10;
```
