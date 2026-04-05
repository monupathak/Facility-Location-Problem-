# 🏭 Warehouse Network Optimizer

A **Streamlit-based decision tool** to design a warehouse network using a **greedy coverage heuristic**.

---

## 🚀 Overview

This app helps determine:

- Minimum number of warehouses required  
- Warehouse locations  
- Customer assignment  
- Coverage achieved (vs target)  
- Transport cost impact  

It solves a **Maximal Coverage Location Problem (MCLP)** using a fast, explainable greedy approach.

---

## ⚙️ How It Works

### Objective
Ensure at least **X% of total demand** is within **500 miles** of a plant or warehouse.

---

### Step 1 — Data Processing
- Load Excel file with:
  - `Customers`
  - `Demand`
  - `Distances`
- Parse:
  - Plant → Customer distances
  - Customer → Customer distances
- Aggregate demand per customer (base year)

---

### Step 2 — Plant Coverage
- Check which **(customer, product)** pairs are already within 500 miles of their **source plant**
- Compute:
  - Plant-covered demand
  - Residual demand (needs warehouse)

---

### Step 3 — Greedy Warehouse Placement

Repeat until target coverage is reached:

1. Evaluate all customer locations as candidates  
2. For each candidate:
   - Calculate **uncovered demand within 500 miles**
3. Select the best candidate  
4. Mark covered demand  
5. Add warehouse  

---

### Step 4 — Customer Assignment
Each customer is assigned to the **nearest facility**:
- Plant OR Warehouse

---

### Step 5 — Cost Comparison

#### Before
- Direct shipping from plants

#### After
- If served by warehouse:
  - **Inbound:** Plant → Warehouse  
  - **Outbound:** Warehouse → Customer  

---

## 📂 Input Format

Excel file must contain:

| Sheet | Required | Description |
|------|--------|------------|
| Customers | ✅ | ID, City, State, Latitude, Longitude |
| Demand | ✅ | Customer, Product, Year, Demand |
| Distances | ✅ | Plant→Customer & Customer→Customer |

---

## 📊 Outputs

### UI Dashboard
- Warehouses needed  
- Coverage achieved  
- Cost change  
- Coverage breakdown bar  
- Warehouse table  
- Customer assignment  

---

### Excel Report
Generated file includes:

- **Executive Summary**
- **Warehouses**
- **Customer Assignment**
- **Cost Comparison**

---

## 🧮 Key Assumptions

- Coverage radius = **500 miles**
- Truck capacity = **10 tons**
- Cost = **$2 per truck-mile**
- Products mapped to fixed plants
- Warehouses located only at customer sites
- No capacity constraints
- No warehouse operating cost

---

## 📈 Interpretation of Results

- Warehouses **increase coverage**
- May **increase transport cost** due to:
  - Additional inbound leg
- Cost savings require **network flexibility (Scenario 2)**

---

## 🖥️ How to Run

```bash
pip install streamlit openpyxl pandas numpy xlsxwriter
streamlit run warehouse.py
