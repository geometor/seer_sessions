# Gather relative coordinates of yellow neighbors for changing white pixels
import numpy as np

def get_yellow_neighbor_rel_coords(grid, r, c):
    """Gets the relative (dr, dc) coordinates of yellow neighbors."""
    rel_coords = set()
    rows, cols = grid.shape
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue # Skip self
            nr, nc = r + dr, c + dc
            # Check bounds and if neighbor is yellow (4)
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == 4:
                rel_coords.add((dr, dc))
    # Return as frozenset for hashability (useful for sets of patterns)
    return frozenset(rel_coords)

# Example 1 Input/Output
input1 = np.array([
    [0,0,0,0,0,0,0,0,0], [4,4,4,0,0,0,0,0,0], [0,4,4,0,0,0,0,0,0],
    [4,4,4,0,0,0,0,0,0], [0,0,0,0,0,4,4,4,0], [0,0,0,0,0,0,4,0,0],
    [0,0,0,0,0,0,4,0,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]
])
output1 = np.array([
    [0,0,0,0,0,0,0,0,0], [4,4,4,0,0,0,0,0,0], [7,4,4,0,0,0,0,0,0],
    [4,4,4,0,0,0,0,0,0], [0,0,0,0,0,4,4,4,0], [0,0,0,0,0,7,4,7,0],
    [0,0,0,0,0,7,4,7,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]
])

# Example 2 Input/Output
input2 = np.array([
    [0,0,0,0,0,0,0,0,0], [4,4,4,0,0,0,0,0,0], [4,0,4,0,0,0,0,0,0],
    [0,0,4,0,0,0,0,0,0], [0,0,0,0,0,4,4,0,0], [0,0,0,0,0,0,4,4,0],
    [0,0,0,0,0,4,0,4,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]
])
output2 = np.array([
    [0,0,0,0,0,0,0,0,0], [4,4,4,0,0,0,0,0,0], [4,7,4,0,0,0,0,0,0],
    [7,7,4,0,0,0,0,0,0], [0,0,0,0,0,4,4,7,0], [0,0,0,0,0,7,4,4,0],
    [0,0,0,0,0,4,7,4,0], [0,0,0,0,0,0,0,0,0], [0,0,0,0,0,0,0,0,0]
])

metrics = {
    "example1": {"changed_pixels": []},
    "example2": {"changed_pixels": []}
}

# Helper to analyze pixels that change
def analyze_changed_pixels(grid_in, grid_out, metrics_list_changed):
    rows, cols = grid_in.shape
    for r in range(rows):
        for c in range(cols):
            if grid_in[r, c] == 0 and grid_out[r, c] == 7: # Changed White -> Orange
                rel_coords = get_yellow_neighbor_rel_coords(grid_in, r, c)
                num_neighbors = len(rel_coords)
                # Convert frozenset to sorted tuple list for consistent printing/reading
                rel_coords_list = sorted(list(rel_coords))
                metrics_list_changed.append({
                    "coords": (r, c),
                    "yellow_neighbors": num_neighbors,
                    "rel_coords": rel_coords_list
                })

analyze_changed_pixels(input1, output1, metrics["example1"]["changed_pixels"])
analyze_changed_pixels(input2, output2, metrics["example2"]["changed_pixels"])

# Print metrics nicely
import json
print("Neighbor analysis for pixels changing White -> Orange:")
print(json.dumps(metrics, indent=2))

# List unique patterns (as sets of relative coordinates) for changed pixels
changed_patterns = set()
all_inputs = {'example1': input1, 'example2': input2}
for ex in metrics:
    current_input = all_inputs[ex]
    for p in metrics[ex]["changed_pixels"]:
         # Use the function again to get the frozenset representation
         pattern = get_yellow_neighbor_rel_coords(current_input, p["coords"][0], p["coords"][1])
         changed_patterns.add(pattern)

print("\nUnique relative coordinate patterns causing change (raw frozensets):")
print(changed_patterns)

print("\nUnique relative coordinate patterns causing change (sorted lists):")
# Print sorted lists for readability
unique_patterns_sorted = sorted([sorted(list(p)) for p in changed_patterns])
for pattern in unique_patterns_sorted:
     print(pattern)