import pandas as pd
import numpy as np

# =============================
# INPUT (CSV FILE)
# =============================
input_file = "beam_input.csv"
output_file = "beam_output.xlsx"

# Read CSV (auto handle ; or ,)
try:
    df = pd.read_csv(input_file)
except:
    df = pd.read_csv(input_file, sep=';')

# Clean column names (remove spaces)
df.columns = df.columns.str.strip()

# OPTIONAL: print columns to debug
print("Detected columns:", df.columns)

# Rename common variations automatically
rename_map = {
    'Length': 'L',
    'length': 'L',
    'Span': 'L',
    'Span_m': 'L',
    'Load': 'w',
    'load': 'w',
    'W': 'w',
    'UDL_kN_per_m': 'w',
    'E_MPa': 'E',
    'I_mm4': 'I',
    'Z_mm3': 'Z',
    'fy_MPa': 'fy'
}

df = df.rename(columns=rename_map)

results = []

for i, row in df.iterrows():
    L = row['L']                # m
    w = row['w']                # kN/m
    E = row['E'] * 1e6          # MPa -> N/m2
    I = row['I'] * 1e-12        # mm4 -> m4
    fy = row['fy'] * 1e6        # MPa -> N/m2
    Z = row['Z'] * 1e-9         # mm3 -> m3

    # Convert load to N/m
    w_N = w * 1000

    # =============================
    # MAX BENDING MOMENT
    # =============================
    Mmax = w_N * L**2 / 8      # N.m

    # =============================
    # MAX DEFLECTION
    # =============================
    delta = (5 * w_N * L**4) / (384 * E * I)   # meters

    # =============================
    # DESIGN CHECK
    # =============================
    stress = Mmax / Z          # N/m2
    utilization = stress / fy

    if utilization <= 1:
        status = "SAFE"
    else:
        status = "NOT SAFE"

    results.append({
        "Beam_ID": i+1,
        "Mmax (kN.m)": Mmax / 1000,
        "Deflection (mm)": delta * 1000,
        "Stress (MPa)": stress / 1e6,
        "Utilization": utilization,
        "Status": status
    })

# =============================
# SAVE RESULTS
# =============================
output_df = pd.DataFrame(results)
output_df.to_excel(output_file, index=False)

print("Analysis complete. Results saved to", output_file)

# =============================
# SAMPLE CSV GENERATOR
# =============================
def create_sample_csv():
    data = {
        'L': [6, 8],
        'w': [10, 15],
        'E': [200000, 200000],
        'I': [8.5e8, 1.2e9],
        'fy': [250, 250],
        'Z': [3.4e5, 5.2e5]
    }
    sample_df = pd.DataFrame(data)
    sample_df.to_csv("beam_input.csv", index=False)
    print("Sample CSV created.")

# Uncomment to generate sample file
# create_sample_csv()
