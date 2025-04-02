
Previous Code:
```python
"""
Transforms the input grid by filling specific white regions (holes) based on a conditional color mapping. 
A white region is considered a 'fillable hole' if:
1. It is not connected to the grid border via 4-way adjacent white pixels (i.e., it's not part of the outer background).
2. All non-white pixels adjacent (8-way) to any pixel within the hole have the same single color (the boundary color).
3. No pixel within the hole is adjacent (8-way) to any background white pixel.

The color used to fill these holes depends on the set of unique boundary colors found across *all* fillable holes in the grid:
- If the set of boundary colors is {Red(2), Yellow(4)}, the mapping is Red(2)->Green(3), Yellow(4)->Orange(7).
- If the set is {Red(2), Yellow(4), Orange(7)}, the mapping is Red(2)->Orange(7), Yellow(4)->Green(3), Orange(7)->Green(3).
The original boundary shapes remain unchanged.
"""

import numpy as np
from collections import deque

def get_neighbors(r, c, height, width, connectivity=8):
    """ Gets 8-way (default) or 4-way neighbors within grid bounds. """
    neighbors = []
    steps = [(-1, 0), (1, 0), (0, -1), (0, 1)] # 4-way
    if connectivity == 8:
        steps.extend([(-1, -1), (-1, 1), (1, -1), (1, 1)]) # Add diagonals

    for dr, dc in steps:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def transform(input_grid):
    # Convert input to NumPy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    height, width = input_grid_np.shape

    # 1. Identify background white pixels (connected to border, 4-way)
    is_background = np.zeros_like(input_grid_np, dtype=bool)
    q_background = deque()

    for r in range(height):
        for c in [0, width - 1]:
            if input_grid_np[r, c] == 0 and not is_background[r, c]:
                is_background[r, c] = True
                q_background.append((r, c))
    for c in range(width):
         for r in [0, height - 1]:
            if input_grid_np[r, c] == 0 and not is_background[r, c]:
                is_background[r, c] = True
                q_background.append((r, c))

    while q_background:
        r, c = q_background.popleft()
        for nr, nc in get_neighbors(r, c, height, width, connectivity=4):
            if input_grid_np[nr, nc] == 0 and not is_background[nr, nc]:
                is_background[nr, nc] = True
                q_background.append((nr, nc))

    # 2. & 3. & 4. Identify hole candidates and filter for fillable holes
    visited = is_background.copy() # Start visited mask including background
    fillable_holes = []
    global_boundary_colors = set()

    for r in range(height):
        for c in range(width):
            # Start BFS for unvisited white pixels (potential holes)
            if input_grid_np[r, c] == 0 and not visited[r, c]:
                q_hole = deque([(r, c)])
                visited[r, c] = True
                current_hole_pixels = []
                boundary_colors_found = set()
                touches_background = False
                hole_visited_local = set([(r,c)]) # Track visited within this specific BFS

                while q_hole:
                    hr, hc = q_hole.popleft()
                    current_hole_pixels.append((hr, hc))
                    visited[hr, hc] = True # Mark as globally visited

                    # Check 8-way neighbors
                    for nr, nc in get_neighbors(hr, hc, height, width, connectivity=8):
                        neighbor_color = input_grid_np[nr, nc]
                        if neighbor_color == 0: # White neighbor
                            if is_background[nr, nc]:
                                touches_background = True # Condition 3 check
                            elif (nr, nc) not in hole_visited_local:
                                hole_visited_local.add((nr, nc))
                                q_hole.append((nr, nc))
                        else: # Non-white neighbor (part of the boundary)
                            boundary_colors_found.add(neighbor_color) # For Condition 1 check

                # Filter based on conditions after exploring the whole component
                # Condition 1: Enclosed by a single color
                is_single_boundary = len(boundary_colors_found) == 1
                # Condition 3: Does not touch background white
                is_isolated = not touches_background

                if is_single_boundary and is_isolated:
                    boundary_color = boundary_colors_found.pop() # Get the single boundary color
                    fillable_holes.append((current_hole_pixels, boundary_color))
                    global_boundary_colors.add(boundary_color) # Add to global set for map determination

    # 5. & 6. Determine the fill color mapping based on the global set of boundary colors
    fill_map = {}
    global_boundary_colors_set = frozenset(global_boundary_colors)

    # Define known mappings based on training examples
    mapping_rules = {
        frozenset({2, 4}): {2: 3, 4: 7}, # Red(2), Yellow(4) -> Red:Green(3), Yellow:Orange(7)
        frozenset({2, 4, 7}): {2: 7, 4: 3, 7: 3} # Red(2), Yellow(4), Orange(7) -> Red:Orange(7), Yellow:Green(3), Orange:Green(3)
    }

    # Select the appropriate map if the observed set of boundary colors is known
    if global_boundary_colors_set in mapping_rules:
        fill_map = mapping_rules[global_boundary_colors_set]

    # 7. Fill the identified fillable holes in the output grid using the map
    if fill_map: # Only fill if a valid mapping was found
        for hole_pixels, boundary_color in fillable_holes:
            # Check if the boundary color has a defined fill color in the current map
            if boundary_color in fill_map:
                fill_color = fill_map[boundary_color]
                # Color the pixels belonging to this hole
                for r_fill, c_fill in hole_pixels:
                    output_grid[r_fill, c_fill] = fill_color

    # 8. Return the modified grid as a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 2 2 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0
0 0 0 4 0 0 0 4 0 0
0 0 0 4 4 4 4 4 0 0
```
Expected Output:
```
0 2 2 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0
0 0 0 4 7 7 7 4 0 0
0 0 0 4 4 4 4 4 0 0
```
Transformed Output:
```
0 2 2 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0
0 0 0 4 7 7 7 4 0 0
0 0 0 4 4 4 4 4 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0 0 0 4 0 4
0 2 2 2 2 2 2 2 2 0 0 4 0 4
0 2 0 0 0 0 0 0 2 0 0 4 0 4
0 2 0 0 0 0 0 0 2 0 0 4 4 4
0 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 0 7
0 0 7 7 7 7 7 7 7 0 0 7 0 7
0 0 7 0 0 0 0 0 7 0 0 7 0 7
0 0 7 7 7 7 7 7 7 0 0 7 0 7
0 0 0 0 0 0 0 0 0 0 0 7 0 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 2 2 2 2 2 2 2 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 4 4
0 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 0 0 0 0 0 0 0 0 0 0 4 3 4
0 2 2 2 2 2 2 2 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 3 4
0 2 7 7 7 7 7 7 2 0 0 4 4 4
0 2 2 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 7 3 3 3 3 3 7 0 0 7 3 7
0 0 7 7 7 7 7 7 7 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 3 7
0 0 0 0 0 0 0 0 0 0 0 7 7 7
```
Match: False
Pixels Off: 5
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 5.102040816326536
