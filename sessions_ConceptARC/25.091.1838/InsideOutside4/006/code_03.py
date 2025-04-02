# tool_code
import numpy as np
from collections import deque
import json

# --- Helper functions (copied from the provided solution) ---
# [Functions find_pixels, find_adjacent_pixel, find_first_enclosing_color remain the same as the previous attempt]
def find_pixels(grid, color):
    if not isinstance(grid, np.ndarray): grid = np.array(grid)
    # Cast color to the grid's dtype for comparison if necessary
    # Although usually comparison works fine between python int and numpy int
    return list(map(tuple, np.argwhere(grid == color)))

def find_adjacent_pixel(grid, start_coords, target_color):
    if not isinstance(grid, np.ndarray): grid = np.array(grid)
    rows, cols = grid.shape
    initial_coords_set = set(start_coords)
    for r, c in start_coords:
         for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbor_pos = (nr, nc)
                if grid[nr, nc] == target_color and neighbor_pos not in initial_coords_set:
                    return neighbor_pos
    return None

def find_first_enclosing_color(grid, start_pos, excluded_colors):
    if not isinstance(grid, np.ndarray): grid = np.array(grid)
    rows, cols = grid.shape
    if start_pos is None or not (0 <= start_pos[0] < rows and 0 <= start_pos[1] < cols and grid[start_pos] == 0):
         return None
    q = deque([start_pos])
    visited_background = {start_pos}
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < rows and 0 <= nc < cols): continue
            neighbor_pos = (nr, nc)
            neighbor_color = grid[nr, nc]
            if neighbor_color == 0:
                if neighbor_pos not in visited_background:
                    visited_background.add(neighbor_pos)
                    q.append(neighbor_pos)
            else:
                # Perform conversion to standard int here for check
                neighbor_color_int = int(neighbor_color)
                # Ensure excluded colors contains standard ints for comparison
                if neighbor_color_int not in {int(ex) for ex in excluded_colors}:
                    return neighbor_color_int # Return standard int
    return None


# --- Example Data ---
# [Same example data as before]
examples = {
    "1": {"input": [[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,1,1,1,1,1,0,0],[0,1,0,0,0,0,0,0,0,0,0,1,0,0],[0,1,0,3,3,3,3,3,3,0,0,1,0,0],[0,1,0,3,0,0,0,0,3,0,0,1,0,0],[0,1,0,3,0,0,6,0,3,0,0,1,0,0],[0,1,0,3,0,0,0,0,3,0,0,1,0,0],[0,1,0,3,0,0,0,0,3,0,0,1,0,0],[0,1,0,3,3,3,3,3,3,0,0,1,0,0],[0,1,0,0,0,0,0,0,0,0,0,1,0,0],[0,1,1,1,1,1,1,1,1,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]], "change_expected": False },
    "2": {"input": [[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,2,2,2,2,0,0,0,0,0],[0,0,2,2,2,2,0,0,2,0,0,0,0,0],[0,0,2,0,0,0,0,0,2,2,2,2,0,0],[0,0,2,0,4,4,4,4,0,0,0,2,0,0],[2,2,2,0,4,0,0,4,0,6,0,2,0,0],[2,0,0,0,4,4,4,4,0,0,0,2,0,0],[2,0,0,0,0,0,0,0,2,2,2,2,0,0],[2,2,2,2,2,0,0,0,2,0,0,0,0,0],[0,0,0,0,2,0,0,0,2,0,0,0,0,0],[0,0,0,0,2,0,0,0,2,0,0,0,0,0],[0,0,0,0,2,2,2,2,2,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]], "change_expected": True },
    "3": {"input": [[0,3,3,3,3,3,3,3,3,3,3,3,3,3],[0,3,0,0,0,0,7,7,0,0,0,0,0,3],[0,3,0,0,0,7,0,7,0,0,0,0,0,3],[0,3,0,0,7,0,0,7,0,0,0,0,0,3],[0,3,0,7,0,0,0,0,7,0,0,0,0,3],[0,3,7,0,0,0,0,0,0,7,0,0,0,3],[0,3,7,0,0,6,0,0,0,0,7,0,0,3],[0,3,7,0,0,0,0,0,0,0,0,7,0,3],[0,3,7,0,0,0,0,0,0,0,0,0,7,3],[0,3,7,7,7,7,7,7,7,7,7,7,7,3],[0,3,3,3,3,3,3,3,3,3,3,3,3,3],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]], "change_expected": False },
    "4": {"input": [[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,3,3,3,3,3,3,3,3,3,0,0],[0,3,3,0,0,0,0,0,0,0,0,3,3,0],[3,0,0,0,1,1,1,1,1,1,0,0,0,3],[3,0,0,1,1,1,0,0,0,1,1,0,0,3],[3,0,0,1,1,0,0,0,0,0,1,1,0,3],[3,0,0,0,1,0,0,0,0,0,0,1,1,3],[0,3,0,0,0,1,1,0,0,0,0,0,1,3],[0,3,3,0,6,0,0,1,0,0,0,0,1,3],[0,0,3,0,0,0,0,1,1,0,0,1,0,3],[0,0,3,3,3,0,0,0,1,1,1,1,0,3],[0,0,0,0,3,3,3,0,0,0,0,0,0,3],[0,0,0,0,0,0,0,3,3,3,3,3,3,3],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]], "change_expected": True }
}


results = {}

for name, data in examples.items():
    grid_list = data["input"]
    grid = np.array(grid_list, dtype=int) # Specify dtype
    target_pixels = find_pixels(grid, 6)
    c_inner_raw, c_outer_raw = None, None
    condition_met = False
    target_pos_found = None 
    
    if len(target_pixels) == 1:
        target_pos = target_pixels[0]
        target_pos_found = target_pos
        start_pos_inner = find_adjacent_pixel(grid, [target_pos], 0)
        if start_pos_inner:
            # Ensure excluded colors are standard ints
            excluded_inner = {int(c) for c in {0, 6}}
            c_inner_raw = find_first_enclosing_color(grid, start_pos_inner, excluded_inner) 
            if c_inner_raw is not None:
                # Use the raw color (which should be standard int now) to find pixels
                c_inner_pixels = find_pixels(grid, c_inner_raw) 
                if c_inner_pixels:
                    start_pos_outer = find_adjacent_pixel(grid, c_inner_pixels, 0)
                    if start_pos_outer:
                        # Ensure excluded colors are standard ints
                        excluded_outer = {int(c) for c in {0, 6, c_inner_raw}} 
                        c_outer_raw = find_first_enclosing_color(grid, start_pos_outer, excluded_outer)
                        
                        if c_outer_raw is not None:
                            # Comparisons use standard ints
                            c_inner = int(c_inner_raw) # Cast just to be sure
                            c_outer = int(c_outer_raw) # Cast just to be sure
                            if (c_inner == 4 and c_outer == 2) or \
                               (c_inner == 1 and c_outer == 3):
                                condition_met = True

    # Prepare serializable results, ensuring all values are standard Python types
    serializable_result = {
        "target_pos": [int(coord) for coord in target_pos_found] if target_pos_found else None, 
        "C_inner": int(c_inner_raw) if c_inner_raw is not None else None, 
        "C_outer": int(c_outer_raw) if c_outer_raw is not None else None,
        "condition_met": bool(condition_met), # Cast to bool
        "change_expected": bool(data["change_expected"]), # Cast to bool
    }
    # Add derived field last
    serializable_result["logic_matches_expectation"] = serializable_result["condition_met"] == serializable_result["change_expected"]

    results[name] = serializable_result

print(json.dumps(results, indent=2))
