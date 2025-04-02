# Code used for analysis:
import numpy as np
from scipy.ndimage import label, generate_binary_structure, find_objects as ndi_find_objects

def find_object_pixels(grid_list, color):
    grid = np.array(grid_list, dtype=int)
    return np.argwhere(grid == color)

def count_pixels(grid_list, color):
    grid = np.array(grid_list, dtype=int)
    return np.sum(grid == color)

def check_adjacency(grid_list, color1, color2):
    grid = np.array(grid_list, dtype=int)
    locs1 = find_object_pixels(grid_list, color1)
    if len(locs1) == 0: return False # No objects of color1

    mask2 = (grid == color2)
    structure = generate_binary_structure(2, 2) # 8-connectivity

    # Check if any pixel adjacent to any color1 pixel is color2
    for r, c in locs1:
        # Check 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0: continue # Skip self
                nr, nc = r + dr, c + dc
                # Check bounds
                if 0 <= nr < grid.shape[0] and 0 <= nc < grid.shape[1]:
                    if grid[nr, nc] == color2:
                        return True # Found adjacency
    return False

# Inputs (shortened for brevity)
train_inputs = [
    [[3, 2, 2, 3], [3, 2, 2, 3], [3, 1, 1, 3], [3, 1, 1, 3, 1, 1]], # Example 1 (structure representative)
    [[3, 3, 3, 3, 3, 1, 1], [3, 3, 3, 3, 3, 1, 1], [3, 3, 3, 3, 3, 1, 1, 3], [3, 2, 2, 3]], # Example 2 (structure representative)
    [[2, 2, 2, 1], [2, 2, 2, 1], [3, 0, 0, 0, 1]], # Example 3 (structure representative)
    [[3, 0, 1, 1], [3, 3, 3, 1], [3, 3, 3, 2]] # Example 4 (structure representative)
]
# Complete inputs used in actual tool execution

results = []
for i, input_grid in enumerate(train_inputs): # Using full inputs here
    num_red_pix = count_pixels(input_grid, 2)
    w_adj_b = check_adjacency(input_grid, 0, 1) # White adjacent to Blue?
    r_adj_b = check_adjacency(input_grid, 2, 1) # Red adjacent to Blue?
    r_adj_w = check_adjacency(input_grid, 2, 0) # Red adjacent to White?

    # Apply the refined condition logic
    # Condition for TrueRule (W->B, B->W, R->R) = W adj B AND num_red_pixels > 1
    use_true_rule = w_adj_b and (num_red_pix > 1)
    determined_rule = "RuleSetTrue" if use_true_rule else "RuleSetFalse"

    actual_rule = "RuleSetFalse" if i in [0, 3] else "RuleSetTrue"

    results.append({
        "Example": i + 1,
        "Num Red Pixels": num_red_pix,
        "W adj B?": w_adj_b,
        "R adj B?": r_adj_b,
        "R adj W?": r_adj_w,
        "Determined RuleSet (New Logic)": determined_rule,
        "Actual RuleSet Required": actual_rule,
        "Match": determined_rule == actual_rule
    })

print(results)
