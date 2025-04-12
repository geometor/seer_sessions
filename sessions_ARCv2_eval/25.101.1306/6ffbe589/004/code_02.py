import collections
import numpy as np

# --- Helper Functions ---

def find_objects(grid: list[list[int]], background_color: int = 0) -> list[tuple[set[tuple[int, int]], int]]:
    grid_np = np.array(grid, dtype=int)
    height, width = grid_np.shape
    if height == 0 or width == 0: return []
    visited = np.zeros_like(grid_np, dtype=bool)
    objects = []
    for r in range(height):
        for c in range(width):
            if grid_np[r, c] != background_color and not visited[r, c]:
                current_object_coords = set()
                q = collections.deque([(r, c)])
                visited[r, c] = True
                obj_size = 0
                min_obj_r, max_obj_r = r, r
                min_obj_c, max_obj_c = c, c
                while q:
                    row, col = q.popleft()
                    current_object_coords.add((row, col))
                    obj_size += 1
                    min_obj_r = min(min_obj_r, row)
                    max_obj_r = max(max_obj_r, row)
                    min_obj_c = min(min_obj_c, col)
                    max_obj_c = max(max_obj_c, col)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue 
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < height and 0 <= nc < width:
                                if grid_np[nr, nc] != background_color and not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    q.append((nr, nc))
                if current_object_coords:
                     # Also store bbox with object info for tie-breaking
                     objects.append({'coords': current_object_coords, 
                                     'size': obj_size, 
                                     'bbox': (min_obj_r, max_obj_r, min_obj_c, max_obj_c)})
    return objects

def get_bounding_box(coords: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    if not coords: return (0, -1, 0, -1) 
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, max_r, min_c, max_c

def format_grid(grid):
    if not grid: return "[]"
    return "\n".join(["[" + ", ".join(map(str, row)) + "]" for row in grid])

# --- Input Data (as before) ---
train_inputs = {
    "train_1": [
        [0,0,0,0,0,0,0,0,3,0,3,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,0,0], [0,0,0,0,0,0,3,3,8,8,0,8,8,8,0,8,0,3,0,0], [0,0,0,0,0,0,0,3,8,0,8,8,0,8,8,8,8,3,0,0], [0,0,0,0,0,0,0,3,0,8,0,0,6,0,0,8,0,3,0,0], [0,0,0,0,0,0,0,3,8,8,6,6,6,6,0,8,8,3,3,0], [0,0,0,0,0,0,0,3,8,0,0,6,0,6,0,0,8,3,0,0], [0,0,0,0,0,0,0,3,8,8,0,6,6,6,6,8,8,3,3,0], [0,0,0,0,0,0,0,3,0,8,0,0,6,0,0,8,0,3,0,0], [0,0,0,0,0,0,3,3,8,8,8,8,0,8,8,8,8,3,0,0], [0,0,0,0,0,0,0,3,0,8,0,8,8,8,0,8,0,3,0,0], [0,0,0,0,0,0,0,3,3,3,3,3,3,3,3,3,3,3,0,0], [0,0,0,0,0,0,0,0,0,0,0,3,3,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,8,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,3,0,0,0,6,6,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ],
    "train_2": [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,5,0,5,0,5,5,5,5,0,5,0,0,0,0], [0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,5,0,0,3,3,3,3,0,0,5,0,0,0,0], [0,0,0,0,0,0,0,3,3,0,4,0,0,3,0,5,0,0,0,0], [0,0,0,0,0,0,5,0,3,0,4,4,0,3,3,0,0,0,0,0], [0,0,0,0,0,0,5,0,3,0,4,4,4,3,0,5,0,0,0,0], [0,0,0,0,0,0,5,0,3,0,0,0,0,3,0,5,0,0,0,0], [0,0,0,0,0,0,5,0,0,3,3,3,3,0,0,5,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,5,0,5,5,0,5,5,5,0,5,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ],
    "train_3": [
        [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,4,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0], [0,4,0,4,0,4,0,4,0,4,0,0,0,0,0,0,0,0,0,0], [0,0,4,0,4,0,4,0,4,0,4,0,0,0,0,0,0,0,0,0], [0,4,0,0,0,0,1,0,0,4,0,0,0,0,0,0,0,0,0,0], [0,0,4,0,1,0,0,1,1,0,4,0,0,0,0,0,0,0,0,0], [0,4,0,0,1,2,2,0,1,4,0,0,0,0,0,0,0,0,0,0], [0,0,4,1,0,2,2,1,0,0,4,0,0,0,0,0,0,0,0,0], [0,4,0,0,1,1,0,0,0,4,0,0,0,0,0,0,0,0,0,0], [0,0,4,0,0,1,1,0,0,0,4,0,0,0,0,0,0,0,0,0], [0,4,0,4,0,4,0,4,0,4,0,0,0,0,0,0,0,0,0,0], [0,0,4,0,4,0,4,0,4,0,4,0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
    ]
}
train_outputs = {
    "train_1": [
        [0,0,0,3,0,0,0,0,0,0,3,0,0], [0,3,3,3,3,3,3,3,3,3,3,3,0], [0,3,0,8,0,8,8,8,0,8,0,3,3], [0,3,8,8,8,8,0,8,8,8,8,3,0], [0,3,0,8,0,0,6,0,0,8,0,3,3], [3,3,8,8,6,6,6,6,0,8,8,3,0], [3,3,8,0,0,6,0,6,0,0,8,3,0], [0,3,8,8,0,6,6,6,6,8,8,3,0], [0,3,0,8,0,0,6,0,0,8,0,3,0], [0,3,8,8,8,8,0,8,8,0,8,3,0], [0,3,0,8,0,8,8,8,0,8,8,3,0], [0,3,3,3,3,3,3,3,3,3,3,3,0], [0,0,0,0,0,3,0,3,0,0,0,0,0]
     ],
    "train_2": [
        [5,0,5,0,5,5,5,5,0,5], [0,0,0,0,0,0,3,0,0,0], [5,0,0,3,3,3,3,0,0,5], [0,0,3,0,0,0,0,3,3,5], [5,3,3,0,4,4,4,3,0,0], [5,0,3,0,4,4,0,3,0,5], [5,0,3,0,4,0,0,3,0,5], [5,0,0,3,3,3,3,0,0,5], [0,0,0,0,0,3,0,0,0,0], [5,0,5,5,0,5,5,5,0,5]
    ],
    "train_3": [
        [0,4,0,4,0,4,0,4,0,4], [4,0,4,0,4,0,4,0,4,0], [0,4,0,1,1,0,0,0,0,4], [4,0,0,1,0,1,0,0,4,0], [0,4,1,0,2,2,0,1,0,4], [4,0,0,0,2,2,1,1,4,0], [0,4,0,1,1,0,1,0,0,4], [4,0,0,0,0,1,0,0,4,0], [0,4,0,4,0,4,0,4,0,4], [4,0,4,0,4,0,4,0,4,0]
    ]
}

# --- Analysis ---
results_log = []
for name, input_grid in train_inputs.items():
    log_entry = f"--- Analyzing {name} ---\n"
    objects = find_objects(input_grid) # Now returns list of dicts
    
    if not objects:
        log_entry += "No non-background objects found.\n"
        results_log.append(log_entry)
        continue

    # Sort objects deterministically: size desc, then bbox top row asc, then bbox left col asc
    objects.sort(key=lambda obj: (obj['size'], -obj['bbox'][0], -obj['bbox'][2]), reverse=True)
    
    log_entry += f"Found {len(objects)} objects. Sizes: {[obj['size'] for obj in objects]}\n"

    # Select the largest object based on the sorted list
    largest_object_info = objects[0]
    largest_object_coords = largest_object_info['coords']
    largest_size = largest_object_info['size']
    
    log_entry += f"Selected largest object size: {largest_size}\n"
    
    # Get its bounding box
    min_r, max_r, min_c, max_c = get_bounding_box(largest_object_coords)
    log_entry += f"Bounding box coordinates: (min_r={min_r}, max_r={max_r}, min_c={min_c}, max_c={max_c})\n"
    log_entry += f"Slicing rows: {min_r} to {max_r + 1} (exclusive)\n"
    log_entry += f"Slicing cols: {min_c} to {max_c + 1} (exclusive)\n"


    # Perform the crop based on these coordinates
    cropped_grid = []
    if max_r >= min_r and max_c >= min_c:
        # Python slicing: input_grid[start_row:end_row] gives rows from start_row up to (but not including) end_row
        # Slicing cols: row[start_col:end_col] gives columns from start_col up to (but not including) end_col
        cropped_grid = [row[min_c : max_c + 1] for row in input_grid[min_r : max_r + 1]]
    else:
        log_entry += "Invalid bounding box calculated.\n"
        
    # Compare with expected output
    expected_output_grid = train_outputs[name]
    
    log_entry += "Calculated Cropped Grid:\n" + format_grid(cropped_grid) + "\n"
    log_entry += "\nExpected Output Grid:\n" + format_grid(expected_output_grid) + "\n"
    
    is_match = cropped_grid == expected_output_grid
    log_entry += f"\nMatch: {is_match}\n"
    log_entry += ("-" * 20) + "\n"
    results_log.append(log_entry)

print("\n".join(results_log))

# Verify exact match for all examples
all_match = all(["Match: True" in log for log in results_log])
print(f"Overall Result: All training examples match = {all_match}")