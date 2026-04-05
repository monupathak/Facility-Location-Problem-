"""
Warehouse Network Optimizer — Streamlit App
============================================
Run:  streamlit run warehouse_app.py
Deps: pip install streamlit openpyxl pandas numpy xlsxwriter
"""

import io
import math
import numpy as np
import pandas as pd
import streamlit as st

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Warehouse Network Optimizer",
    page_icon="🏭",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS (dark industrial theme matching original UI) ────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@300;400;500&family=Syne:wght@400;600;700;800&display=swap');

/* ── Global ── */
html, body, [class*="css"] {
    font-family: 'DM Mono', monospace !important;
    background-color: #0a0a0f;
    color: #e8e8f0;
}
.stApp { background-color: #0a0a0f; }

/* ── Grid background ── */
.stApp::before {
    content: '';
    position: fixed;
    inset: 0;
    background-image:
        linear-gradient(rgba(108,99,255,0.025) 1px, transparent 1px),
        linear-gradient(90deg, rgba(108,99,255,0.025) 1px, transparent 1px);
    background-size: 40px 40px;
    pointer-events: none;
    z-index: 0;
}

/* ── Main content block ── */
.block-container {
    padding: 2.5rem 3rem 4rem !important;
    max-width: 1000px;
}

/* ── Header ── */
.app-tag {
    font-size: 11px;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #6c63ff;
    margin-bottom: 8px;
    display: flex;
    align-items: center;
    gap: 8px;
}
.app-tag::before {
    content: '';
    display: inline-block;
    width: 20px;
    height: 1px;
    background: #6c63ff;
}
.app-title {
    font-family: 'Syne', sans-serif !important;
    font-size: 42px;
    font-weight: 800;
    line-height: 1.1;
    letter-spacing: -0.02em;
    color: #e8e8f0;
    margin-bottom: 8px;
}
.app-title span { color: #6c63ff; }
.app-subtitle {
    color: #6b6b80;
    font-size: 13px;
    line-height: 1.7;
    margin-bottom: 40px;
    max-width: 560px;
}

/* ── Section labels ── */
.section-label {
    font-size: 10px;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: #6c63ff;
    font-weight: 500;
    margin-bottom: 12px;
}

/* ── Cards ── */
.card {
    background: #111118;
    border: 1px solid #2a2a38;
    border-radius: 12px;
    padding: 24px 28px;
    margin-bottom: 16px;
}
.card-success {
    background: rgba(0,229,192,0.04);
    border-color: rgba(0,229,192,0.2);
}
.card-warn {
    background: rgba(255,107,107,0.04);
    border-color: rgba(255,107,107,0.2);
}

/* ── Stat cards ── */
.stat-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 12px;
    margin-bottom: 20px;
}
.stat-card {
    background: #1a1a24;
    border: 1px solid #2a2a38;
    border-radius: 10px;
    padding: 18px 16px;
}
.stat-label {
    font-size: 10px;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #6b6b80;
    margin-bottom: 8px;
}
.stat-value {
    font-family: 'Syne', sans-serif;
    font-size: 28px;
    font-weight: 800;
    color: #e8e8f0;
    line-height: 1;
}
.stat-value.accent  { color: #6c63ff; }
.stat-value.success { color: #00e5c0; }
.stat-value.warn    { color: #ffb347; }
.stat-sub {
    font-size: 10px;
    color: #6b6b80;
    margin-top: 5px;
}

/* ── Coverage bar ── */
.bar-wrap { margin: 16px 0 8px; }
.bar-labels {
    display: flex;
    justify-content: space-between;
    font-size: 10px;
    color: #6b6b80;
    margin-bottom: 6px;
}
.bar-track {
    height: 6px;
    background: #2a2a38;
    border-radius: 3px;
    overflow: hidden;
    position: relative;
}
.bar-legend {
    display: flex;
    gap: 20px;
    font-size: 11px;
    color: #6b6b80;
    margin-top: 10px;
}
.leg-dot {
    display: inline-block;
    width: 8px;
    height: 8px;
    border-radius: 1px;
    margin-right: 5px;
    vertical-align: middle;
}

/* ── Warehouse table ── */
.wh-table {
    width: 100%;
    border-collapse: collapse;
    font-size: 12px;
}
.wh-table th {
    text-align: left;
    font-size: 10px;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #6b6b80;
    padding: 8px 12px;
    border-bottom: 1px solid #2a2a38;
    font-weight: 400;
}
.wh-table td {
    padding: 12px;
    border-bottom: 1px solid rgba(42,42,56,0.5);
    vertical-align: middle;
}
.wh-table tr:last-child td { border-bottom: none; }
.wh-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: rgba(108,99,255,0.12);
    border: 1px solid rgba(108,99,255,0.25);
    color: #6c63ff;
    padding: 3px 8px;
    border-radius: 4px;
    font-size: 11px;
}
.wh-dot {
    width: 6px;
    height: 6px;
    background: #00e5c0;
    border-radius: 50%;
    display: inline-block;
}

/* ── Cost rows ── */
.cost-row {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 12px 0;
    border-bottom: 1px solid #2a2a38;
    font-size: 13px;
}
.cost-row:last-child { border-bottom: none; }
.cost-lbl { color: #6b6b80; font-size: 11px; }
.cost-val {
    font-family: 'Syne', sans-serif;
    font-weight: 700;
    font-size: 16px;
    color: #e8e8f0;
}
.cost-val.pos { color: #00e5c0; }
.cost-val.neg { color: #ff6b6b; }

/* ── File uploader ── */
[data-testid="stFileUploader"] {
    background: #1a1a24 !important;
    border: 1px dashed #2a2a38 !important;
    border-radius: 8px !important;
}
[data-testid="stFileUploader"]:hover {
    border-color: #6c63ff !important;
}

/* ── Slider ── */
[data-testid="stSlider"] > div > div > div > div {
    background: #6c63ff !important;
}
[data-testid="stSlider"] > div > div > div {
    background: #2a2a38 !important;
}

/* ── Button ── */
.stButton > button {
    width: 100%;
    background: #6c63ff !important;
    color: white !important;
    border: none !important;
    border-radius: 8px !important;
    padding: 14px 0 !important;
    font-family: 'Syne', sans-serif !important;
    font-size: 15px !important;
    font-weight: 700 !important;
    letter-spacing: 0.02em !important;
    cursor: pointer;
    transition: all 0.2s !important;
}
.stButton > button:hover {
    background: #7c74ff !important;
    box-shadow: 0 8px 24px rgba(108,99,255,0.35) !important;
    transform: translateY(-1px) !important;
}

/* ── Download button ── */
.dl-btn-wrap .stDownloadButton > button {
    background: transparent !important;
    border: 1px solid #00e5c0 !important;
    color: #00e5c0 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 12px !important;
    padding: 10px 20px !important;
    border-radius: 8px !important;
    font-weight: 500 !important;
}
.dl-btn-wrap .stDownloadButton > button:hover {
    background: rgba(0,229,192,0.08) !important;
    box-shadow: 0 0 20px rgba(0,229,192,0.15) !important;
}

/* ── Divider ── */
.divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, #2a2a38, transparent);
    margin: 32px 0;
}

/* ── Log box ── */
.log-box {
    background: #080810;
    border: 1px solid #2a2a38;
    border-radius: 8px;
    padding: 14px 16px;
    font-size: 11px;
    color: #6b6b80;
    line-height: 1.9;
    font-family: 'DM Mono', monospace;
    white-space: pre-wrap;
}

/* ── Metric overrides ── */
[data-testid="stMetric"] {
    background: #1a1a24;
    border: 1px solid #2a2a38;
    border-radius: 10px;
    padding: 16px;
}
[data-testid="stMetricLabel"] { color: #6b6b80 !important; font-size: 11px !important; }
[data-testid="stMetricValue"] {
    font-family: 'Syne', sans-serif !important;
    font-size: 26px !important;
    font-weight: 800 !important;
    color: #e8e8f0 !important;
}

/* ── Info/success boxes ── */
.stAlert { border-radius: 8px !important; }

/* ── Dataframe ── */
[data-testid="stDataFrame"] {
    background: #111118 !important;
    border: 1px solid #2a2a38 !important;
    border-radius: 8px !important;
}
</style>
""", unsafe_allow_html=True)

# ── Constants ──────────────────────────────────────────────────────────────────
COVERAGE_RADIUS  = 500
TRUCK_CAPACITY   = 10
COST_PER_TRUCK   = 2
PRODUCT_PLANT    = {1: 1, 2: 2, 3: 3, 4: 4, 5: 4}

# ══════════════════════════════════════════════════════════════════════════════
# HEURISTIC CORE (same logic as warehouse_heuristic_v2.py)
# ══════════════════════════════════════════════════════════════════════════════

def run_heuristic(uploaded_file, coverage_target: float, log_fn):
    xl = pd.ExcelFile(uploaded_file)

    # ── Load sheets ──
    log_fn("Loading sheets...", "accent")
    customers_df = xl.parse("Customers")
    demand_df    = xl.parse("Demand")
    dist_raw     = xl.parse("Distances")

    # ── Parse distance matrices ──
    log_fn("Parsing distance matrices...", "accent")
    plant_cust_raw = dist_raw[["Plant ID", "Customer ID", "Distance"]].dropna()
    plant_cust_raw.columns = ["plant_id", "customer_id", "distance_mi"]
    plant_cust_raw = plant_cust_raw.astype({"plant_id": int, "customer_id": int})
    plant_cust_matrix = plant_cust_raw.pivot(
        index="plant_id", columns="customer_id", values="distance_mi"
    )

    cust_cust_raw = dist_raw[["Customer ID.1", "Customer ID.2", "Distance.1"]].dropna()
    cust_cust_raw.columns = ["from_customer", "to_customer", "distance_mi"]
    cust_cust_raw = cust_cust_raw.astype({"from_customer": int, "to_customer": int})
    cust_cust_matrix = cust_cust_raw.pivot(
        index="from_customer", columns="to_customer", values="distance_mi"
    )

    # ── Base year demand ──
    base_year = sorted(demand_df["Time Period"].unique())[0]
    log_fn(f"Base year: {base_year}")
    demand_2012 = demand_df[demand_df["Time Period"] == base_year].copy()
    demand_2012["source_plant"] = demand_2012["Product ID"].map(PRODUCT_PLANT)

    total_demand_tons = demand_2012["Demand (in tonnes)"].sum()
    target_tons = coverage_target * total_demand_tons
    log_fn(f"Total demand: {total_demand_tons:,.1f} tons")
    log_fn(f"Target ({coverage_target*100:.0f}%): {target_tons:,.1f} tons")

    # ── Step A: Product-aware plant coverage ──
    log_fn("Computing plant coverage (product-aware)...", "accent")
    plant_covered_pairs = []
    plant_covered_set   = set()
    plant_covered_tons  = 0.0

    for _, row in demand_2012.iterrows():
        cid   = int(row["Customer ID"])
        pid   = int(row["Product ID"])
        plant = int(row["source_plant"])
        tons  = float(row["Demand (in tonnes)"])
        dist  = plant_cust_matrix.loc[plant, cid] if cid in plant_cust_matrix.columns else math.inf

        if dist <= COVERAGE_RADIUS:
            plant_covered_pairs.append({
                "customer_id": cid, "product_id": pid,
                "source_plant": plant, "distance_mi": round(dist, 2),
                "covered_tons": tons
            })
            plant_covered_set.add((cid, pid))
            plant_covered_tons += tons

    plant_coverage_pct = plant_covered_tons / total_demand_tons * 100
    log_fn(f"Plant coverage (corrected): {plant_covered_tons:,.1f} tons ({plant_coverage_pct:.1f}%)")

    # ── Step B: Residual demand ──
    demand_2012["plant_covered"] = demand_2012.apply(
        lambda r: (int(r["Customer ID"]), int(r["Product ID"])) in plant_covered_set, axis=1
    )
    residual_demand = (
        demand_2012[~demand_2012["plant_covered"]]
        .groupby("Customer ID")["Demand (in tonnes)"]
        .sum()
        .reset_index()
        .rename(columns={"Customer ID": "customer_id", "Demand (in tonnes)": "residual_tons"})
    )
    total_per_customer = (
        demand_2012.groupby("Customer ID")["Demand (in tonnes)"]
        .sum()
        .reset_index()
        .rename(columns={"Customer ID": "customer_id", "Demand (in tonnes)": "annual_tons"})
    )

    customers = customers_df[["ID", "City", "State", "Latitude", "Longitude"]].copy()
    customers.columns = ["customer_id", "city", "state", "lat", "lon"]
    customers = (customers
                 .merge(total_per_customer, on="customer_id")
                 .merge(residual_demand, on="customer_id", how="left"))
    customers["residual_tons"] = customers["residual_tons"].fillna(0.0)
    customers["needs_wh"] = customers["residual_tons"] > 0

    log_fn(f"Residual demand for warehouses: {customers['residual_tons'].sum():,.1f} tons")

    # Early exit if plants already cover target
    if plant_covered_tons >= target_tons:
        log_fn("Plants alone meet target — no warehouses needed!", "success")
        return _build_results([], customers, demand_2012, plant_cust_matrix,
                              cust_cust_matrix, plant_covered_tons,
                              plant_coverage_pct, total_demand_tons, target_tons,
                              coverage_target)

    # ── Step C: Greedy loop ──
    log_fn("Running greedy heuristic on residual demand...", "accent")
    uncovered_mask  = customers["needs_wh"].values.copy()
    candidate_ids   = customers["customer_id"].tolist()
    cust_idx        = {cid: i for i, cid in enumerate(customers["customer_id"])}
    residual_arr    = customers["residual_tons"].values
    needs_wh_arr    = customers["needs_wh"].values

    warehouses_placed = []
    coverage_trace    = []
    iteration = 0

    while True:
        wh_covered = residual_arr[(~uncovered_mask) & needs_wh_arr].sum()
        total_cov  = plant_covered_tons + wh_covered
        pct        = total_cov / total_demand_tons * 100

        coverage_trace.append({
            "warehouses_placed"  : iteration,
            "plant_covered_tons" : round(plant_covered_tons, 1),
            "wh_covered_tons"    : round(wh_covered, 1),
            "total_covered_tons" : round(total_cov, 1),
            "coverage_pct"       : round(pct, 2),
            "gap_tons"           : round(total_demand_tons - total_cov, 1),
        })

        if total_cov >= target_tons:
            log_fn(f"Target reached after {iteration} warehouse(s)! ({pct:.2f}%)", "success")
            break

        best_score, best_id, best_mask = -1, None, None
        for cand_id in candidate_ids:
            dists = cust_cust_matrix.loc[cand_id] if cand_id in cust_cust_matrix.index else {}
            newly = np.array([
                uncovered_mask[cust_idx[cid]] and needs_wh_arr[cust_idx[cid]]
                and (dists.get(cid, math.inf) if hasattr(dists, "get") else
                     (dists[cid] if cid in dists.index else math.inf)) <= COVERAGE_RADIUS
                for cid in customers["customer_id"]
            ])
            score = residual_arr[newly].sum()
            if score > best_score:
                best_score, best_id, best_mask = score, cand_id, newly

        if best_id is None or best_score == 0:
            log_fn("Warning: no candidate can improve coverage further.", "warn")
            break

        iteration += 1
        whr = customers[customers["customer_id"] == best_id].iloc[0]
        cum_pct = (plant_covered_tons + wh_covered + best_score) / total_demand_tons * 100

        warehouses_placed.append({
            "warehouse_id"            : iteration,
            "customer_site_id"        : best_id,
            "city"                    : whr["city"],
            "state"                   : whr["state"],
            "latitude"                : round(float(whr["lat"]), 4),
            "longitude"               : round(float(whr["lon"]), 4),
            "newly_covered_tons"      : round(best_score, 1),
            "cumulative_coverage_pct" : round(cum_pct, 2),
        })
        uncovered_mask = uncovered_mask & ~best_mask
        log_fn(f"  WH{iteration}: {whr['city']}, {whr['state']}  "
               f"+{best_score:,.0f} tons  ({cum_pct:.1f}% cumulative)")

    return _build_results(warehouses_placed, customers, demand_2012, plant_cust_matrix,
                          cust_cust_matrix, plant_covered_tons, plant_coverage_pct,
                          total_demand_tons, target_tons, coverage_target)


def _build_results(warehouses_placed, customers, demand_2012, plant_cust_matrix,
                   cust_cust_matrix, plant_covered_tons, plant_coverage_pct,
                   total_demand_tons, target_tons, coverage_target):

    # ── Customer assignment ──
    def assign(row):
        cid = row["customer_id"]
        best_dist = plant_cust_matrix[cid].min() if cid in plant_cust_matrix.columns else math.inf
        best_type = "Plant"
        best_id   = int(plant_cust_matrix[cid].idxmin()) if cid in plant_cust_matrix.columns else 0
        for wh in warehouses_placed:
            d = (cust_cust_matrix.loc[wh["customer_site_id"], cid]
                 if wh["customer_site_id"] in cust_cust_matrix.index and
                    cid in cust_cust_matrix.columns else math.inf)
            if d < best_dist:
                best_dist, best_type, best_id = d, "Warehouse", wh["warehouse_id"]
        return pd.Series({
            "nearest_facility_type": best_type,
            "nearest_facility_id"  : best_id,
            "nearest_distance_mi"  : round(best_dist, 1),
            "within_500mi"         : best_dist <= COVERAGE_RADIUS,
        })

    assign_extra = customers.apply(assign, axis=1)
    customer_assign_df = pd.concat([
        customers[["customer_id", "city", "state", "lat", "lon",
                   "annual_tons", "residual_tons", "needs_wh"]],
        assign_extra
    ], axis=1)

    # ── Cost comparison ──
    before_by_cust = {}
    for _, row in demand_2012.iterrows():
        cid   = int(row["Customer ID"])
        plant = int(row["source_plant"])
        tons  = float(row["Demand (in tonnes)"])
        dist  = (plant_cust_matrix.loc[plant, cid]
                 if cid in plant_cust_matrix.columns else 0)
        cost  = math.ceil(tons / TRUCK_CAPACITY) * dist * COST_PER_TRUCK
        before_by_cust[cid] = before_by_cust.get(cid, 0) + cost

    after_rows = []
    for _, crow in customer_assign_df.iterrows():
        cid      = crow["customer_id"]
        fac_type = crow["nearest_facility_type"]
        fac_id   = crow["nearest_facility_id"]
        near_d   = crow["nearest_distance_mi"]
        ann_tons = crow["annual_tons"]
        before_c = before_by_cust.get(cid, 0)

        if fac_type == "Plant":
            after_cost = before_c
        else:
            wh_site = warehouses_placed[fac_id - 1]["customer_site_id"]
            inbound = 0
            for prod_id, plant_id in PRODUCT_PLANT.items():
                prod_tons = demand_2012[
                    (demand_2012["Customer ID"] == cid) &
                    (demand_2012["Product ID"] == prod_id)
                ]["Demand (in tonnes)"].sum()
                if prod_tons > 0:
                    d_pw = (plant_cust_matrix.loc[plant_id, wh_site]
                            if wh_site in plant_cust_matrix.columns else 0)
                    inbound += math.ceil(prod_tons / TRUCK_CAPACITY) * d_pw * COST_PER_TRUCK
            outbound   = math.ceil(ann_tons / TRUCK_CAPACITY) * near_d * COST_PER_TRUCK
            after_cost = inbound + outbound

        saving = before_c - after_cost
        after_rows.append({
            "customer_id"           : cid,
            "city"                  : crow["city"],
            "state"                 : crow["state"],
            "annual_tons"           : round(ann_tons, 1),
            "served_by"             : fac_type,
            "nearest_distance_mi"   : near_d,
            "before_transport_cost" : round(before_c),
            "after_transport_cost"  : round(after_cost),
            "cost_saving"           : round(saving),
            "saving_pct"            : round(saving / before_c * 100, 1) if before_c else 0,
        })

    cost_df = pd.DataFrame(after_rows)
    total_before = cost_df["before_transport_cost"].sum()
    total_after  = cost_df["after_transport_cost"].sum()
    final_pct    = (plant_covered_tons +
                    sum(w["newly_covered_tons"] for w in warehouses_placed)) / total_demand_tons * 100

    return {
        "warehouses_df"      : pd.DataFrame(warehouses_placed),
        "customer_assign_df" : customer_assign_df,
        "cost_df"            : cost_df,
        "plant_coverage_pct" : plant_coverage_pct,
        "plant_covered_tons" : plant_covered_tons,
        "total_demand_tons"  : total_demand_tons,
        "target_tons"        : target_tons,
        "coverage_target"    : coverage_target,
        "total_before"       : total_before,
        "total_after"        : total_after,
        "final_coverage_pct" : final_pct,
    }


def build_excel_output(res) -> bytes:
    buf = io.BytesIO()
    with pd.ExcelWriter(buf, engine="openpyxl") as writer:
        net  = res["total_before"] - res["total_after"]
        netp = net / res["total_before"] * 100 if res["total_before"] else 0
        pd.DataFrame({
            "Metric": [
                "Total annual demand (tons)", "Coverage target (%)",
                "Plant-only coverage (%) — corrected", "Warehouses needed",
                "Final coverage (%)",
                "Transport cost BEFORE ($)", "Transport cost AFTER ($)",
                "Net cost change ($)", "Net cost change (%)",
            ],
            "Value": [
                round(res["total_demand_tons"], 1),
                round(res["coverage_target"] * 100, 0),
                round(res["plant_coverage_pct"], 2),
                len(res["warehouses_df"]),
                round(res["final_coverage_pct"], 2),
                round(res["total_before"]),
                round(res["total_after"]),
                round(net),
                round(netp, 2),
            ],
        }).to_excel(writer, sheet_name="Executive Summary", index=False)

        if not res["warehouses_df"].empty:
            res["warehouses_df"].to_excel(writer, sheet_name="Warehouses", index=False)

        res["customer_assign_df"].to_excel(writer, sheet_name="Customer Assignment", index=False)
        res["cost_df"].to_excel(writer, sheet_name="Cost Comparison", index=False)
    return buf.getvalue()


# ══════════════════════════════════════════════════════════════════════════════
# UI
# ══════════════════════════════════════════════════════════════════════════════

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-tag">Operations Research · Supply Chain</div>
<div class="app-title">Warehouse Network<br><span>Optimizer</span></div>
<div class="app-subtitle">
  Greedy coverage heuristic — finds the minimum number of warehouses to meet your
  service threshold, using your actual demand and distance data.
</div>
""", unsafe_allow_html=True)

# ── Inputs ────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([3, 2], gap="large")

with col1:
    st.markdown('<div class="section-label">01 · Data Input</div>', unsafe_allow_html=True)
    uploaded = st.file_uploader(
        "Upload Excel file",
        type=["xlsx", "xls"],
        label_visibility="collapsed",
        help="Requires sheets: Customers, Demand, Distances"
    )
    if uploaded:
        st.success(f"✓  {uploaded.name}", icon=None)

with col2:
    st.markdown('<div class="section-label">02 · Coverage Threshold</div>', unsafe_allow_html=True)
    threshold_pct = st.slider(
        "Coverage target (%)",
        min_value=0, max_value=100, value=80, step=1,
        label_visibility="collapsed",
        format="%d%%"
    )
    st.markdown(
        f'<div style="font-family:\'Syne\',sans-serif;font-size:36px;font-weight:800;'
        f'color:#6c63ff;margin-top:4px">{threshold_pct}%</div>'
        f'<div style="font-size:11px;color:#6b6b80;margin-top:2px">'
        f'of demand within 500 miles of a facility</div>',
        unsafe_allow_html=True
    )

st.markdown("<br>", unsafe_allow_html=True)
st.markdown('<div class="section-label">03 · Run Heuristic</div>', unsafe_allow_html=True)
run_clicked = st.button("Run Warehouse Optimizer", disabled=uploaded is None)

# ── Run ───────────────────────────────────────────────────────────────────────
if run_clicked and uploaded:

    log_lines = []

    def log_fn(msg, kind=""):
        color_map = {"accent": "#00e5c0", "success": "#00e5c0", "warn": "#ffb347", "": "#6b6b80"}
        color = color_map.get(kind, "#6b6b80")
        log_lines.append(f'<span style="color:{color}">› {msg}</span>')

    log_placeholder = st.empty()

    with st.spinner(""):
        try:
            # Patch log to update UI live-ish
            res = run_heuristic(uploaded, threshold_pct / 100, log_fn)
            log_placeholder.markdown(
                f'<div class="log-box">' + "<br>".join(log_lines) + "</div>",
                unsafe_allow_html=True,
            )
        except Exception as e:
            st.error(f"Error: {e}")
            st.stop()

    # ── Divider ──
    st.markdown('<div class="divider"></div>', unsafe_allow_html=True)

    # ── Results header + download ──
    r1, r2 = st.columns([3, 1])
    with r1:
        st.markdown(
            '<div style="font-family:\'Syne\',sans-serif;font-size:22px;'
            'font-weight:700;color:#e8e8f0;margin-bottom:4px">Results</div>',
            unsafe_allow_html=True
        )
    with r2:
        excel_bytes = build_excel_output(res)
        st.markdown('<div class="dl-btn-wrap">', unsafe_allow_html=True)
        st.download_button(
            label="⬇  Download Excel Report",
            data=excel_bytes,
            file_name="warehouse_heuristic_output.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # ── Stat cards ──
    net      = res["total_before"] - res["total_after"]
    net_pct  = net / res["total_before"] * 100 if res["total_before"] else 0
    n_wh     = len(res["warehouses_df"])
    fin_pct  = res["final_coverage_pct"]
    plt_pct  = res["plant_coverage_pct"]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Warehouses Needed", n_wh, help="Minimum facilities to hit the coverage target")
    c2.metric("Final Coverage", f"{fin_pct:.1f}%", delta=f"target {threshold_pct}%")
    c3.metric("Plant-Only Coverage", f"{plt_pct:.1f}%",
              help="Corrected: only counts source plant within 500 mi per product")
    c4.metric("Transport Cost Δ",
              f"{'-' if net >= 0 else '+'}{abs(net_pct):.1f}%",
              delta=f"{'saving' if net >= 0 else 'increase'}",
              delta_color="normal" if net >= 0 else "inverse")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Coverage bar ──
    plant_pct_bar = min(res["plant_covered_tons"] / res["total_demand_tons"] * 100, 100)
    wh_tons  = sum(w["newly_covered_tons"] for w in res["warehouses_df"].to_dict("records"))
    wh_pct_bar   = min(wh_tons / res["total_demand_tons"] * 100, 100 - plant_pct_bar)
    tgt_pct  = threshold_pct

    st.markdown(f"""
    <div class="card">
      <div class="section-label" style="margin-bottom:14px">Coverage Breakdown</div>
      <div class="bar-wrap">
        <div class="bar-labels">
          <span>0%</span>
          <span style="color:#ff6b6b">Target: {tgt_pct}%</span>
          <span>100%</span>
        </div>
        <div class="bar-track" style="height:8px">
          <div style="position:absolute;left:0;top:0;height:100%;width:{plant_pct_bar:.1f}%;
                      background:#6b6b80;border-radius:3px"></div>
          <div style="position:absolute;left:{plant_pct_bar:.1f}%;top:0;height:100%;
                      width:{wh_pct_bar:.1f}%;background:#00e5c0;border-radius:3px"></div>
          <div style="position:absolute;left:{tgt_pct}%;top:-3px;height:14px;width:2px;
                      background:#ff6b6b;border-radius:1px"></div>
        </div>
      </div>
      <div class="bar-legend">
        <span><span class="leg-dot" style="background:#6b6b80"></span>Plant coverage ({plant_pct_bar:.1f}%)</span>
        <span><span class="leg-dot" style="background:#00e5c0"></span>Warehouse added ({wh_pct_bar:.1f}%)</span>
        <span><span class="leg-dot" style="background:#ff6b6b;width:2px;border-radius:1px"></span>Target ({tgt_pct}%)</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Warehouse table ──
    if not res["warehouses_df"].empty:
        rows_html = ""
        for _, w in res["warehouses_df"].iterrows():
            rows_html += f"""
            <tr>
              <td><span class="wh-badge"><span class="wh-dot"></span>WH{int(w['warehouse_id'])}</span></td>
              <td>{w['city']}</td>
              <td>{w['state']}</td>
              <td style="color:#6b6b80">{w['latitude']:.4f}</td>
              <td style="color:#6b6b80">{w['longitude']:.4f}</td>
              <td>{w['newly_covered_tons']:,.0f} tons</td>
              <td style="color:#00e5c0;font-weight:600">{w['cumulative_coverage_pct']}%</td>
            </tr>"""

        st.markdown(f"""
        <div class="card">
          <div class="section-label" style="margin-bottom:16px">Warehouse Locations</div>
          <table class="wh-table">
            <thead><tr>
              <th>#</th><th>City</th><th>State</th>
              <th>Latitude</th><th>Longitude</th>
              <th>Demand Covered</th><th>Cumulative %</th>
            </tr></thead>
            <tbody>{rows_html}</tbody>
          </table>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.info("Plants alone meet the coverage target — no warehouses needed.")

    # ── Cost comparison ──
    net_class = "pos" if net >= 0 else "neg"
    net_sign  = "-" if net >= 0 else "+"
    st.markdown(f"""
    <div class="card">
      <div class="section-label" style="margin-bottom:4px">Transport Cost Comparison</div>
      <div class="cost-row">
        <span class="cost-lbl">Before — direct from source plants</span>
        <span class="cost-val">${res['total_before']:,.0f}</span>
      </div>
      <div class="cost-row">
        <span class="cost-lbl">After — with warehouse network</span>
        <span class="cost-val">${res['total_after']:,.0f}</span>
      </div>
      <div class="cost-row">
        <span class="cost-lbl">Net change</span>
        <span class="cost-val {net_class}">{net_sign}${abs(net):,.0f} ({abs(net_pct):.1f}%)</span>
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Customer assignment table (expandable) ──
    with st.expander("Customer Assignment Detail", expanded=False):
        display_cols = ["customer_id", "city", "state", "annual_tons",
                        "nearest_facility_type", "nearest_facility_id",
                        "nearest_distance_mi", "within_500mi"]
        st.dataframe(
            res["customer_assign_df"][display_cols].style.applymap(
                lambda v: "color: #00e5c0" if v == "Warehouse" else "",
                subset=["nearest_facility_type"]
            ),
            use_container_width=True, height=320
        )

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="margin-top:60px;padding-top:24px;border-top:1px solid #2a2a38;
            font-size:11px;color:#3a3a50;text-align:center;letter-spacing:0.08em">
  WAREHOUSE NETWORK OPTIMIZER · GREEDY COVERAGE HEURISTIC · SCENARIO 1
</div>
""", unsafe_allow_html=True)