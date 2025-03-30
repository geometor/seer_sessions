# Code Used for Metrics:
import numpy as np
from collections import Counter

def analyze_example(input_grid):
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    H = np.count_nonzero(input_np[0, :] == 8)
    R_anchor = next((r for r in range(height) if np.all(input_np[r, :] == 5)), -1)
    R_source = next((r for r in range(height - 1, -1, -1) if np.any(input_np[r, :] != 0)), -1)
    if R_anchor == -1 or R_source == -1: return {"error": "Missing anchor/source"}
    source_row_content = input_np[R_source, :]
    non_white_colors = source_row_content[source_row_content != 0]
    color_counts = Counter(non_white_colors)
    selected_colors = {color for color, count in color_counts.items() if count == H}
    return { "H": H, "R_anchor": R_anchor, "R_source": R_source, "source_color_counts": dict(color_counts), "selected_colors (count==H)": selected_colors }

# Example inputs simplified for analysis
examples_data = [
    [[8,8,8,0,0,0,0,0,0,0], [0]*10, [0]*10, [0]*10, [0]*10, [0]*10, [5]*10, [0]*10, [8,6,4,3,4,7,3,8,3,7], [0]*10],
    [[8,0,0,0,0,0,0,0,0,0], [0]*10, [0]*10, [0]*10, [0]*10, [0]*10, [5]*10, [0]*10, [6,6,4,6,2,1,9,2,9,4], [0]*10],
    [[8,8,8,0,0,0,0,0,0,0], [0]*10, [0]*10, [0]*10, [0]*10, [0]*10, [5]*10, [0]*10, [4,1,4,4,6,3,1,6,3,6], [0]*10],
    [[8,8,0,0,0,0,0,0,0,0], [0]*10, [0]*10, [0]*10, [0]*10, [0]*10, [5]*10, [0]*10, [2,3,3,2,3,1,1,3,1,1], [0]*10],
    [[8,8,8,8,0,0,0,0,0,0], [0]*10, [0]*10, [0]*10, [0]*10, [0]*10, [5]*10, [0]*10, [2,1,2,1,2,1,1,2,2,2], [0]*10],
    [[8,0,0,0,0,0,0,0,0,0], [0]*10, [0]*10, [0]*10, [0]*10, [0]*10, [5]*10, [0]*10, [1,3,1,1,1,1,4,1,1,1], [0]*10],
]

analysis_results = [analyze_example(ex) for ex in examples_data]
# Mapping numpy int types to standard int for display clarity if needed
# analysis_results = [ {k: (int(v) if isinstance(v, np.integer) else (set(int(i) for i in v) if isinstance(v, set) else ({int(ck):cv for ck,cv in v.items()} if k == 'source_color_counts' else v))) for k,v in res.items()} for res in analysis_results]
# print(analysis_results) # (Output formatted below)