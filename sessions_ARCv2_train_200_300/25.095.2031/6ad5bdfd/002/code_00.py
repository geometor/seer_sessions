import numpy as np
import json

def parse_grid_str(s):
  lines = s.strip().split('\n')
  return np.array([[int(x) for x in line.split()] for line in lines if line.strip()])

# --- Input Data ---
input_str_1 = """
2 0 0 3 3 0 0 4 4 0 0
2 0 0 0 0 5 0 0 0 0 0
2 0 0 0 0 5 0 0 6 6 0
2 0 0 0 0 0 0 8 0 0 0
2 0 7 7 0 0 0 8 0 0 0
"""
input_str_2 = """
0 0 0 0 8 8
3 0 0 4 0 0
3 0 0 4 0 0
0 0 0 0 0 6
1 1 0 0 0 6
0 0 0 0 0 0
0 0 5 5 0 0
0 0 0 0 0 0
0 0 0 0 0 0
2 2 2 2 2 2
"""
input_str_3 = """
0 4 4 0 0 0 0 0 0 2
0 0 0 5 5 0 0 6 0 2
0 0 0 0 0 0 0 6 0 2
0 9 0 0 8 8 0 0 0 2
0 9 0 0 0 0 0 0 0 2
"""

# --- Parse Grids ---
grid1 = parse_grid_str(input_str_1)
grid2 = parse_grid_str(input_str_2)
grid3 = parse_grid_str(input_str_3)

# --- Analyze Function ---
def analyze_grid(grid, grid_name):
    report = {}
    report["name"] = grid_name
    report["shape"] = grid.shape
    num_rows, num_cols = grid.shape

    # First Column Analysis
    first_col = grid[:, 0]
    report["first_col_unique"] = np.unique(first_col).tolist()
    report["first_col_is_constant"] = len(report["first_col_unique"]) == 1
    # Convert potential numpy int to standard int for JSON serialization
    report["first_col_constant_value"] = int(first_col[0]) if report["first_col_is_constant"] else None
    report["first_col_is_constant_non_zero"] = report["first_col_is_constant"] and report["first_col_constant_value"] != 0

    # Last Column Analysis
    last_col = grid[:, -1]
    report["last_col_unique"] = np.unique(last_col).tolist()
    report["last_col_is_constant"] = len(report["last_col_unique"]) == 1
    # Convert potential numpy int to standard int for JSON serialization
    report["last_col_constant_value"] = int(last_col[0]) if report["last_col_is_constant"] else None
    report["last_col_is_constant_non_zero"] = report["last_col_is_constant"] and report["last_col_constant_value"] != 0

    # Determine Transformation Type based on analysis
    if report["first_col_is_constant_non_zero"]:
        report["transformation_type"] = "Type 1: Left Shift (Preserve First)"
    elif report["last_col_is_constant_non_zero"]:
        report["transformation_type"] = "Type 3: Right Shift (Preserve Last)"
    else:
        report["transformation_type"] = "Type 2: Columnar Gravity"

    return report

# --- Generate Reports ---
report1 = analyze_grid(grid1, "train_1")
report2 = analyze_grid(grid2, "train_2")
report3 = analyze_grid(grid3, "train_3")

# --- Print Reports ---
# Use a custom encoder to handle potential remaining numpy types if needed, although shape is usually tuple of ints.
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, tuple) and all(isinstance(i, (int, float)) for i in obj): # Handle shape tuple
             return list(obj)
        else:
            return super(NpEncoder, self).default(obj)

print("--- Analysis Report ---")
print(json.dumps(report1, indent=2, cls=NpEncoder))
print(json.dumps(report2, indent=2, cls=NpEncoder))
print(json.dumps(report3, indent=2, cls=NpEncoder))
