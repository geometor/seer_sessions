import numpy as np

# --- Data ---
grid1_in = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 3, 3, 3, 3, 3, 3, 3, 0, 0],
    [6, 0, 3, 3, 0, 0, 0, 0, 3, 0, 0, 6],
    [0, 0, 3, 0, 0, 6, 0, 0, 3, 0, 0, 0],
    [0, 0, 3, 3, 0, 6, 0, 6, 3, 0, 6, 0],
    [0, 0, 0, 3, 0, 0, 0, 0, 3, 0, 0, 0],
    [6, 0, 0, 3, 0, 0, 6, 0, 0, 3, 0, 0],
    [0, 0, 3, 3, 0, 0, 0, 0, 0, 3, 0, 0],
    [0, 0, 0, 3, 3, 3, 0, 0, 0, 3, 0, 0],
    [0, 0, 0, 0, 0, 3, 3, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
grid1_out_exp = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
grid1_out_code = np.array([ # From previous execution result
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6],
    [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0, 0], # Differs at (3,5)
    [0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 6, 0], # Differs at (4,5)
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [6, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0], # Differs at (6,6)
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

grid2_in = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 4, 4, 0, 0],
    [0, 0, 4, 4, 0, 0, 1, 0, 0, 0, 4, 0, 4, 0, 0],
    [0, 0, 4, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 4, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 4, 0],
    [4, 0, 1, 0, 4, 4, 0, 0, 0, 4, 0, 0, 0, 4, 0],
    [4, 4, 0, 0, 0, 4, 4, 4, 4, 0, 0, 0, 4, 4, 0],
    [0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0],
    [0, 0, 4, 4, 0, 1, 0, 0, 0, 0, 0, 4, 4, 0, 0],
    [0, 0, 0, 4, 4, 0, 0, 1, 0, 0, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 4, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 4, 4, 4, 4, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
grid2_out_exp = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
grid2_out_code = np.array([ # From previous execution result
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0], # Differs at (10,7)
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 0, 0, 0],
    [0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])

# --- Analysis Functions ---
def check_neighbors_for_color(grid: np.ndarray, r: int, c: int, color_to_find: int) -> bool:
    rows, cols = grid.shape
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0: continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                if grid[nr, nc] == color_to_find:
                    return True
    return False

def analyze_mismatch(grid_in, grid_out_exp, grid_out_code, target_color, context_color):
    mismatches = []
    rows, cols = grid_in.shape
    for r in range(rows):
        for c in range(cols):
            if grid_out_code[r, c] != grid_out_exp[r, c]:
                pixel_val = grid_in[r,c]
                is_target = pixel_val == target_color
                code_kept = grid_out_code[r, c] == target_color
                exp_kept = grid_out_exp[r, c] == target_color
                is_adj_to_context = check_neighbors_for_color(grid_in, r, c, context_color)
                mismatches.append({
                    "coords": (r, c),
                    "input_val": pixel_val,
                    "is_target": is_target,
                    "code_output": grid_out_code[r, c],
                    "expected_output": grid_out_exp[r, c],
                    "code_kept_target": code_kept,
                    "exp_kept_target": exp_kept,
                    "is_adj_to_context": is_adj_to_context
                })
    return mismatches

# --- Run Analysis ---
target1, context1 = 6, 3
mismatches1 = analyze_mismatch(grid1_in, grid1_out_exp, grid1_out_code, target1, context1)
print("--- Train 1 Mismatches ---")
for m in mismatches1:
    print(m)

target2, context2 = 1, 4
mismatches2 = analyze_mismatch(grid2_in, grid2_out_exp, grid2_out_code, target2, context2)
print("\n--- Train 2 Mismatches ---")
for m in mismatches2:
    print(m)

# Verify adjacency specifically for the problematic points
print("\n--- Adjacency Re-Verification ---")
prob1 = [(3,5), (4,5), (6,6)]
for r, c in prob1:
    adj = check_neighbors_for_color(grid1_in, r, c, context1)
    print(f"T1 ({r},{c})={grid1_in[r,c]} adjacent to {context1}? {adj}")

prob2 = [(10,7)]
for r, c in prob2:
    adj = check_neighbors_for_color(grid2_in, r, c, context2)
    print(f"T2 ({r},{c})={grid2_in[r,c]} adjacent to {context2}? {adj}")