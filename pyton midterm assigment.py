import pandas as pd
import numpy as np

# =============================
# INPUT
# =============================
input_file = "beam_input.csv"
output_file = "beam_output.xlsx"

# Read CSV (handles ; or ,)
try:
    df = pd.read_csv(input_file)
except:
    df = pd.read_csv(input_file, sep=';')

# Clean column names
df.columns = df.columns.str.strip()

# Rename columns to standard names
rename_map = {
    'Span_m': 'L',
    'UDL_kN_per_m': 'w',
    'E_MPa': 'E',
    'I_mm4': 'I',
    'Z_mm3': 'Z',
    'fy_MPa': 'fy'
}

df = df.rename(columns=rename_map)

results = []

# =============================
# CALCULATIONS
# =============================
for i, row in df.iterrows():

    # Inputs
    L = row['L']                # m
    w = row['w']                # kN/m
    E = row['E'] * 1e6          # MPa → N/m²
    I = row['I'] * 1e-12        # mm⁴ → m⁴
    fy = row['fy'] * 1e6        # MPa → N/m²
    Z = row['Z'] * 1e-9         # mm³ → m³

    # Convert load
    w_N = w * 1000  # N/m

    # =============================
    # BENDING MOMENT
    # =============================
    Mmax = w_N * L**2 / 8

    # =============================
    # DEFLECTION
    # =============================
    delta = (5 * w_N * L**4) / (384 * E * I)

    # =============================
    # STRESS CHECK
    # =============================
    stress = Mmax / Z
    utilization = stress / fy

    if utilization <= 1:
        status = "SAFE"
    else:
        status = "NOT SAFE"

    # =============================
    # SPAN / DEFLECTION LIMIT CHECK
    # =============================
    limit_ratio = 250  # L/250 (you can change to 300 or 360)

    allowable_deflection = L / limit_ratio

    if delta <= allowable_deflection:
        span_status = "OK"
    else:
        span_status = "NOT OK"

    # =============================
    # STORE RESULTS
    # =============================
    results.append({
        "Beam_ID": i+1,
        "Span (m)": L,
        "Mmax (kN.m)": Mmax / 1000,
        "Deflection (mm)": delta * 1000,
        "Allowable Deflection (mm)": allowable_deflection * 1000,
        "Span Check": span_status,
        "Stress (MPa)": stress / 1e6,
        "Utilization": utilization,
        "Bending Status": status
    })

# =============================
# OUTPUT TO EXCEL
# =============================
output_df = pd.DataFrame(results)
output_df.to_excel(output_file, index=False)

print("✅ Analysis complete!")
print("📁 Results saved to:", output_file)