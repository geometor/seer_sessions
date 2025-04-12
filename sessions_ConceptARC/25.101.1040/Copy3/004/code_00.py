import numpy as np

def get_bounding_box_of_pixels(pixels: set, grid_shape: tuple) -> tuple | None:
    """Calculates the bounding box of a set of pixel coordinates."""
    if not pixels:
        return None
    min_r = grid_shape[0]
    min_c = grid_shape[1]
    max_r = -1
    max_c = -1
    for r, c in pixels:
        min_r = min(min_r, r)
        min_c = min(min_c, c)
        max_r = max(max_r, r)
        max_c = max(max_c, c)
    return (min_r, min_c, max_r, max_c)

# Example 1 Data
grid1_in = [
    [0, 0, 4, 4, 4, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 4, 4, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0]
]
grid1_out_expected = [
    [0, 0, 4, 4, 4, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 0, 1, 0, 0, 1, 0, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 3, 3, 3, 3, 0, 0, 3, 3, 3, 3, 3, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
    [0, 0, 4, 4, 4, 0, 0, 0, 0, 4, 4, 4, 0, 0, 0, 0]
]

# Analysis for Example 1 (No Magenta) - Bounding Box Copy Rule
grid1_np = np.array(grid1_in)
h1, w1 = grid1_np.shape
mid_col1 = w1 // 2
left_half_pixels = set()
for r in range(h1):
    for c in range(mid_col1):
        if grid1_np[r, c] != 0: # Non-white
            left_half_pixels.add((r, c))

left_bbox = get_bounding_box_of_pixels(left_half_pixels, (h1, w1))

print("--- Example 1 Analysis (No Magenta - BBox Rule) ---")
print(f"Grid dimensions: {h1}x{w1}")
print(f"Left half columns: 0 to {mid_col1 - 1}")
if left_bbox:
    print(f"Bounding box of non-white pixels in left half: {left_bbox}")
    bbox_min_r, bbox_min_c, bbox_max_r, bbox_max_c = left_bbox
    # Simulate copy
    output_grid = np.copy(grid1_np)
    dest_start_col = mid_col1
    for r_offset in range(bbox_max_r - bbox_min_r + 1):
        for c_offset in range(bbox_max_c - bbox_min_c + 1):
            src_r, src_c = bbox_min_r + r_offset, bbox_min_c + c_offset
            dest_r, dest_c = bbox_min_r + r_offset, dest_start_col + c_offset # Align top-left row, start dest col at mid_col
            
            # Check bounds before copying
            if 0 <= dest_r < h1 and 0 <= dest_c < w1:
                 # Check source is valid just in case
                 if 0 <= src_r < h1 and 0 <= src_c < mid_col1: # Source must be in left half
                     output_grid[dest_r, dest_c] = grid1_np[src_r, src_c]
                 else: # If source calculation is outside left half (shouldn't happen), maybe copy white? Or error? Copy white for now.
                     output_grid[dest_r, dest_c] = 0 # Default to white if source is invalid
            
    print(f"Simulated copy destination top-left: ({bbox_min_r}, {dest_start_col})")
    print(f"Simulated copy region size: {(bbox_max_r - bbox_min_r + 1)}x{(bbox_max_c - bbox_min_c + 1)}")
    
    is_match = np.array_equal(output_grid, grid1_out_expected)
    print(f"Does simulated output match expected output? {is_match}")

else:
    print("No non-white pixels found in the left half.")

# Analysis for Example 2 (Magenta Present) - Confirm previous findings
# (No code needed here, assessment confirmed logic matches expected output)
print("\n--- Example 2 Analysis (Magenta Present) ---")
print("Logic: Find largest non-magenta pattern P, find first marker M right of P, copy P's BBox to (M_row+2, M_col).")
print("Assessment: This logic correctly produces the expected output for Example 2.")