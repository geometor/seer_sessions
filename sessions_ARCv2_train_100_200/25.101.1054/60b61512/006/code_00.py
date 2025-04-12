import numpy as np

def apply_2x2_rule(input_grid: list[list[int]]) -> list[list[int]]:
    """Applies only the 2x2 rule (3 yellow + 1 white -> orange)."""
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape
    target_color = 4  # yellow
    background_color = 0 # white
    fill_color = 7     # orange

    for r in range(height - 1):
        for c in range(width - 1):
            block = input_np[r:r+2, c:c+2]
            target_count = np.count_nonzero(block == target_color)

            if target_count == 3:
                non_target_indices = np.where(block != target_color)
                if len(non_target_indices[0]) == 1:
                    rel_r, rel_c = non_target_indices[0][0], non_target_indices[1][0]
                    if block[rel_r, rel_c] == background_color:
                        abs_r, abs_c = r + rel_r, c + rel_c
                        output_np[abs_r, abs_c] = fill_color
    return output_np.tolist()

def compare_grids(grid1_list, grid2_list):
    """Compares two grids and lists differing pixel coordinates and values."""
    grid1 = np.array(grid1_list)
    grid2 = np.array(grid2_list)
    diff_pixels = []
    if grid1.shape != grid2.shape:
        return "Grids have different shapes!"
    rows, cols = grid1.shape
    for r in range(rows):
        for c in range(cols):
            if grid1[r, c] != grid2[r, c]:
                diff_pixels.append({
                    "coords": (r, c),
                    "grid1_val": grid1[r, c],
                    "grid2_val": grid2[r, c]
                })
    return diff_pixels

# --- Example 1 ---
input1 = [
    [0,0,0,0,0,0,0,0,0], [4,4,4,0,0,0,0,0,0], [0,4,4,0,0,0,0,0,0],
    [4,4,4,0,0,0,0,0,0], [0,0,0,0,0,4,4,4,0], [0,0,0,0,0,0,4,0,0],
    [0,0,0,0,0,0,4,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]
]
expected1 = [
    [0,0,0,0,0,0,0,0,0], [4,4,4,0,0,0,0,0,0], [7,4,4,0,0,0,0,0,0],
    [4,4,4,0,0,0,0,0,0], [0,0,0,0,0,4,4,4,0], [0,0,0,0,0,7,4,7,0],
    [0,0,0,0,0,7,4,7,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]
]
predicted1 = apply_2x2_rule(input1)
diff1 = compare_grids(predicted1, expected1)
print("--- Example 1 Discrepancies (Predicted vs Expected) ---")
print(diff1)

# --- Example 2 ---
input2 = [
    [0,0,0,0,0,0,0,0,0], [4,4,4,0,0,0,0,0,0], [4,0,4,0,0,0,0,0,0],
    [0,0,4,0,0,0,0,0,0], [0,0,0,0,0,4,4,0,0], [0,0,0,0,0,0,4,4,0],
    [0,0,0,0,0,4,0,4,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]
]
expected2 = [
    [0,0,0,0,0,0,0,0,0], [4,4,4,0,0,0,0,0,0], [4,7,4,0,0,0,0,0,0],
    [7,7,4,0,0,0,0,0,0], [0,0,0,0,0,4,4,7,0], [0,0,0,0,0,7,4,4,0],
    [0,0,0,0,0,4,7,4,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]
]
predicted2 = apply_2x2_rule(input2)
diff2 = compare_grids(predicted2, expected2)
print("\n--- Example 2 Discrepancies (Predicted vs Expected) ---")
print(diff2)
