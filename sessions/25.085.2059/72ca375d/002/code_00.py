# tool_code with corrected find_objects
import numpy as np
from collections import Counter, deque

# Corrected find_objects function
def find_objects(grid):
    """
    Finds all contiguous objects of the same non-white color in the grid.
    Uses 4-connectivity.
    Returns a list of objects, sorted by color index.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and (r, c) not in visited:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                current_obj_visited_in_loop = {(r, c)} # Track visited within this object search

                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and \
                           (nr, nc) not in visited and \
                           (nr, nc) not in current_obj_visited_in_loop:
                            visited.add((nr, nc))
                            current_obj_visited_in_loop.add((nr, nc))
                            q.append((nr, nc))

                if obj_coords:
                    # Calculate bounding box for potential future use
                    min_r = min(coord[0] for coord in obj_coords)
                    max_r = max(coord[0] for coord in obj_coords)
                    min_c = min(coord[1] for coord in obj_coords)
                    max_c = max(coord[1] for coord in obj_coords)
                    bbox = (min_r, min_c, max_r, max_c)

                    objects.append({
                        'color': color,
                        'coords': obj_coords,
                        'size': len(obj_coords),
                        'bbox': bbox
                    })

    # Sort objects by color index
    objects.sort(key=lambda obj: obj['color'])
    return objects

# Example 1 Input
grid1 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 4, 0, 0, 0, 0, 0, 0],
    [0, 0, 4, 4, 0, 0, 8, 8, 8, 0],
    [0, 0, 0, 0, 0, 0, 8, 0, 8, 8],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 2, 2, 0, 0, 0, 0],
    [0, 2, 2, 2, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
objects1 = find_objects(grid1)
print(f"Example 1 Objects (Sorted by Color): {[{'color': obj['color'], 'size': obj['size']} for obj in objects1]}")
expected_output_obj1_color = 4 # Yellow

# Example 2 Input
grid2 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 2, 2, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 2, 2, 2, 0, 0, 7, 7, 0],
    [0, 0, 0, 0, 0, 0, 7, 0, 7, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 6, 6, 6, 6, 0, 0, 0],
    [0, 0, 0, 0, 6, 6, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
objects2 = find_objects(grid2)
print(f"Example 2 Objects (Sorted by Color): {[{'color': obj['color'], 'size': obj['size']} for obj in objects2]}")
expected_output_obj2_color = 6 # Magenta

# Example 3 Input
grid3 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 3, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 3, 0, 0, 5, 0, 0, 5, 0],
    [0, 0, 3, 0, 0, 5, 5, 5, 5, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 8, 8, 8, 0, 0, 0, 0],
    [8, 8, 8, 8, 0, 8, 8, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
objects3 = find_objects(grid3)
print(f"Example 3 Objects (Sorted by Color): {[{'color': obj['color'], 'size': obj['size']} for obj in objects3]}")
expected_output_obj3_color = 5 # Gray

# Analysis
print("\nAnalysis:")
if len(objects1) > 1:
    selected1 = objects1[1] # Select the second object (index 1)
    print(f"Example 1: Selecting second object (color {selected1['color']}). Matches expected ({expected_output_obj1_color}): {selected1['color'] == expected_output_obj1_color}")
else:
    print(f"Example 1: Only {len(objects1)} object(s). Cannot select second.")


if len(objects2) > 1:
    selected2 = objects2[1] # Select the second object (index 1)
    print(f"Example 2: Selecting second object (color {selected2['color']}). Matches expected ({expected_output_obj2_color}): {selected2['color'] == expected_output_obj2_color}")
else:
     print(f"Example 2: Only {len(objects2)} object(s). Cannot select second.")

if len(objects3) > 1:
    selected3 = objects3[1] # Select the second object (index 1)
    print(f"Example 3: Selecting second object (color {selected3['color']}). Matches expected ({expected_output_obj3_color}): {selected3['color'] == expected_output_obj3_color}")
else:
    print(f"Example 3: Only {len(objects3)} object(s). Cannot select second.")
