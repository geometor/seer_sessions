# Tool code block - Recalculate Metrics for Condition
import numpy as np
from collections import Counter

def find_background_color(grid: np.ndarray) -> int:
    counts = Counter(grid.flatten())
    if not counts: return 0
    if grid.size > 0:
        zero_count = counts.get(0, 0)
        most_frequent_color, most_frequent_count = counts.most_common(1)[0] if counts else (0, 0)
        if zero_count == most_frequent_count or zero_count > grid.size * 0.5:
             background_color = 0
        else:
             background_color = most_frequent_color
    else:
        background_color = 0
    return background_color

def find_target_columns(grid: np.ndarray, background_color: int) -> tuple[int | None, int | None]:
    rows, cols = grid.shape
    non_bg_cols = set()
    if grid.size == 0: return None, None
    for c in range(cols):
        if np.any(grid[:, c] != background_color):
            non_bg_cols.add(c)
    sorted_cols = sorted(list(non_bg_cols))
    C1 = sorted_cols[-1] if sorted_cols else None
    C2 = sorted_cols[-2] if len(sorted_cols) > 1 else None
    return C1, C2

def find_topmost_non_background(grid: np.ndarray, col_idx: int | None, background_color: int) -> tuple[int | None, int | None]:
    height = grid.shape[0]
    if col_idx is None or col_idx < 0 or col_idx >= grid.shape[1]: return None, None
    column_data = grid[:, col_idx]
    non_bg_indices = np.where(column_data != background_color)[0]
    if non_bg_indices.size == 0: return None, None
    R_top = non_bg_indices[0]
    V_top = grid[R_top, col_idx]
    return R_top, V_top

# Example Data
examples = [
    {"input": [[0,0,0,0,0,0,0],[0,0,0,0,0,2,0],[0,0,0,0,0,0,0],[0,0,0,4,4,8,0],[0,0,0,4,0,8,0],[0,0,4,4,0,8,0],[0,4,0,0,0,8,0]]}, # 7x7
    {"input": [[7,7,7,7,4,7,7,7,7,7,7,7],[7,7,7,7,4,7,7,7,7,7,7,7],[7,7,7,7,4,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,7,7,7,7,7,7],[7,7,7,7,7,7,3,2,7,7,7,7],[7,7,7,7,7,3,7,2,7,7,7,7],[7,7,7,7,7,3,7,2,7,7,7,7],[7,7,7,3,3,7,7,2,7,7,7,7],[7,7,7,7,7,7,7,2,7,7,7,7],[7,7,7,7,7,7,7,2,7,7,7,7],[7,7,7,7,7,7,7,2,7,7,7,7]]}, # 12x12
    {"input": [[1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,2,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,2,1,1,1,1,1,7,7,1,1,1],[1,1,1,1,1,1,2,1,1,1,1,1,7,1,1,1,1],[1,1,1,1,1,1,2,1,1,1,1,7,7,1,1,1],[1,1,1,1,1,1,2,1,7,7,7,1,1,1,1,1,1],[1,1,1,1,1,1,2,7,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,9,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,9,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,9,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],[1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]]}, # 17x17
    {"input": [[0,0,0,0,0,0,0,0,0,0],[0,0,0,3,0,0,0,0,0,0],[0,0,3,0,0,0,0,0,0,0],[0,0,0,3,0,0,0,0,0,0],[0,0,0,8,5,0,0,0,0,0],[0,0,0,8,5,0,0,0,0,0],[0,0,8,0,5,0,0,0,0,0],[0,0,8,0,5,0,0,0,0,0],[0,8,8,0,5,0,0,0,0,0],[0,0,0,0,5,0,0,0,0,0]]}, # 10x10
    {"input": [[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,3,0,0,0,0,0],[0,0,0,3,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,9,6,0,0,0],[0,0,0,9,0,6,0,0,0],[9,9,9,0,0,6,0,0,0],[9,0,0,0,0,6,0,0,0]]}  # 9x9
]

results = []
print("Metrics for H_Combined condition:")
for i, ex in enumerate(examples):
    input_np = np.array(ex["input"], dtype=int)
    bg = find_background_color(input_np)
    C1, C2 = find_target_columns(input_np, bg)
    R1, V1 = find_topmost_non_background(input_np, C1, bg)
    R2, V2 = find_topmost_non_background(input_np, C2, bg)
    
    # Determine condition R1 < R2, handle None cases
    condition_met = False
    condition_str = "N/A"
    if R1 is not None and R2 is not None:
        condition_met = R1 < R2
        condition_str = f"{R1} < {R2} is {condition_met}"
    elif R1 is None or R2 is None:
        condition_str = f"R1={R1}, R2={R2} (one is None)" # Falls into ELSE case

    results.append({
        "Example": i + 1,
        "bg": bg,
        "C1": C1, "R1": R1, "V1": V1,
        "C2": C2, "R2": R2, "V2": V2,
        "Condition (R1 < R2)": condition_str,
        "Rule Applied": "H11c" if condition_met else "H_DownProp"
    })

# Print results formatted
for res in results:
    print(f"Ex {res['Example']}: bg={res['bg']}, C1={res['C1']}, R1={res['R1']}, V1={res['V1']}, C2={res['C2']}, R2={res['R2']}, V2={res['V2']}. Condition: {res['Condition (R1 < R2)']}. Rule: {res['Rule Applied']}")
