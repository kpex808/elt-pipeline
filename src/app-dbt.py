import duckdb
import streamlit as st

from load_cad_duckdb import DB_PATH

st.title("CAD Dashboard (DuckDB)")

if not DB_PATH.exists():
    st.error("No cad.duckdb yet. Run extract_cad_elt.py, load_cad_duckdb.py, then dbt run.")
    st.stop()

con = duckdb.connect(str(DB_PATH), read_only=True)
kpi = con.execute("SELECT * FROM gold.cad_kpi").df()
flybys = con.execute(
    "SELECT * FROM gold.cad_flybys ORDER BY dist_au ASC LIMIT 100"
).df()
by_day = con.execute(
    "SELECT approach_day, n_approaches FROM gold.cad_by_day ORDER BY approach_day"
).df()
con.close()

row = kpi.iloc[0]
left, mid, right = st.columns(3)
left.metric("Approaches", int(row["n_approaches"]))
mid.metric("Closest (km)", int(row["min_dist_km"]))
right.metric("Max speed (km/s)", round(float(row["max_speed_kms"]), 1))

st.subheader("Upcoming flybys")
st.dataframe(flybys)

st.subheader("Approaches per day")
st.bar_chart(by_day, x="approach_day", y="n_approaches")
