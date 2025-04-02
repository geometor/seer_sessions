# tool_code
import numpy as np
from collections import deque
import json

# --- Helper functions (copied from the provided solution) ---
def find_pixels(grid, color):
    return list(map(tuple, np.argwhere(grid == color)))

def find_adjacent_pixel(grid, start_coords, target_color):
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
    rows, cols = grid.shape
    if start_pos is None or not (0 <= start_pos[0] < rows and 0 <= start_pos[1] < cols and grid[start_pos] == 0):
         return None # Added None check for start_pos
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
                # Convert numpy int type to standard python int for comparison and return
                neighbor_color_int = int(neighbor_color)
                if neighbor_color_int not in excluded_colors:
                    return neighbor_color_int # Return standard int
    return None

# --- Example Data ---
# [Same example data as before]
examples = {
    "1": {
        "input": [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,1,1,1,1,1,1,0,0],[0,1,0,0,0,0,0,0,0,0,0,1,0,0],[0,1,0,3,3,3,3,3,3,0,0,1,0,0],[0,1,0,3,0,0,0,0,3,0,0,1,0,0],[0,1,0,3,0,0,6,0,3,0,0,1,0,0],[0,1,0,3,0,0,0,0,3,0,0,1,0,0],[0,1,0,3,0,0,0,0,3,0,0,1,0,0],[0,1,0,3,3,3,3,3,3,0,0,1,0,0],[0,1,0,0,0,0,0,0,0,0,0,1,0,0],[0,1,1,1,1,1,1,1,1,1,1,1,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ],
        "change_expected": False
    },
    "2": {
        "input": [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,2,2,2,2,0,0,0,0,0],[0,0,2,2,2,2,0,0,2,0,0,0,0,0],[0,0,2,0,0,0,0,0,2,2,2,2,0,0],[0,0,2,0,4,4,4,4,0,0,0,2,0,0],[2,2,2,0,4,0,0,4,0,6,0,2,0,0],[2,0,0,0,4,4,4,4,0,0,0,2,0,0],[2,0,0,0,0,0,0,0,2,2,2,2,0,0],[2,2,2,2,2,0,0,0,2,0,0,0,0,0],[0,0,0,0,2,0,0,0,2,0,0,0,0,0],[0,0,0,0,2,0,0,0,2,0,0,0,0,0],[0,0,0,0,2,2,2,2,2,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ],
        "change_expected": True
    },
    "3": {
        "input": [
            [0,3,3,3,3,3,3,3,3,3,3,3,3,3],[0,3,0,0,0,0,7,7,0,0,0,0,0,3],[0,3,0,0,0,7,0,7,0,0,0,0,0,3],[0,3,0,0,7,0,0,7,0,0,0,0,0,3],[0,3,0,7,0,0,0,0,7,0,0,0,0,3],[0,3,7,0,0,0,0,0,0,7,0,0,0,3],[0,3,7,0,0,6,0,0,0,0,7,0,0,3],[0,3,7,0,0,0,0,0,0,0,0,7,0,3],[0,3,7,0,0,0,0,0,0,0,0,0,7,3],[0,3,7,7,7,7,7,7,7,7,7,7,7,3],[0,3,3,3,3,3,3,3,3,3,3,3,3,3],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ],
        "change_expected": False
    },
    "4": {
        "input": [
            [0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,3,3,3,3,3,3,3,3,3,0,0],[0,3,3,0,0,0,0,0,0,0,0,3,3,0],[3,0,0,0,1,1,1,1,1,1,0,0,0,3],[3,0,0,1,1,1,0,0,0,1,1,0,0,3],[3,0,0,1,1,0,0,0,0,0,1,1,0,3],[3,0,0,0,1,0,0,0,0,0,0,1,1,3],[0,3,0,0,0,1,1,0,0,0,0,0,1,3],[0,3,3,0,6,0,0,1,0,0,0,0,1,3],[0,0,3,0,0,0,0,1,1,0,0,1,0,3],[0,0,3,3,3,0,0,0,1,1,1,1,0,3],[0,0,0,0,3,3,3,0,0,0,0,0,0,3],[0,0,0,0,0,0,0,3,3,3,3,3,3,3],[0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        ],
        "change_expected": True
    }
}

results = {}

for name, data in examples.items():
    grid = np.array(data["input"])
    target_pixels = find_pixels(grid, 6)
    c_inner, c_outer = None, None
    condition_met = False
    target_pos_found = None # Initialize here
    
    if len(target_pixels) == 1:
        target_pos = target_pixels[0]
        target_pos_found = target_pos # Store the found position
        start_pos_inner = find_adjacent_pixel(grid, [target_pos], 0)
        if start_pos_inner:
            # Need to ensure excluded colors are standard ints
            c_inner = find_first_enclosing_color(grid, start_pos_inner, {0, 6})
            if c_inner is not None:
                c_inner_pixels = find_pixels(grid, c_inner)
                if c_inner_pixels:
                    start_pos_outer = find_adjacent_pixel(grid, c_inner_pixels, 0)
                    if start_pos_outer:
                        # Need to ensure excluded colors are standard ints
                        c_outer = find_first_enclosing_color(grid, start_pos_outer, {0, 6, c_inner})
                        
                        if c_outer is not None:
                             # Evaluate Condition
                            if (c_inner == 4 and c_outer == 2) or \
                               (c_inner == 1 and c_outer == 3):
                                condition_met = True

    # Convert results to JSON serializable types
    serializable_result = {
        "target_pos": target_pos_found,
        "C_inner": c_inner,
        "C_outer": c_outer,
        "condition_met": condition_met,
        "change_expected": data["change_expected"],
        "logic_matches_expectation": condition_met == data["change_expected"]
    }
    results[name] = serializable_result


print(json.dumps(results, indent=2))
