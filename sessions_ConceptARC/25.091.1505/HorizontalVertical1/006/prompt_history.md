
## train_1

**input:**
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


**output:**
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


## train_2

**input:**
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


**output:**
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

Okay, let's break down the task based on the provided examples.

## Perception of Task Elements

1.  **Input/Output Grids:** Both input and output are grids of pixels with different colors. The grid dimensions remain the same.
2.  **Background Color:** The background is consistently white (0).
3.  **Objects:** The inputs contain distinct shapes (objects) made of non-white colors (Red=2, Yellow=4, Orange=7 in the examples). These shapes often form boundaries or enclosures.
4.  **Transformation Core:** The primary transformation involves identifying regions of white (0) pixels that are completely enclosed by a single non-white color.
5.  **Filling Action:** These enclosed white regions are filled with a new color in the output grid. The original enclosing boundary shape remains unchanged.
6.  **Fill Color Determination:** The color used to fill the enclosed region depends on the color of the enclosing boundary. However, the specific mapping rule (boundary color -> fill color) appears to depend on the *set* of all boundary colors present in the entire input grid.
    *   In `train_1`, the boundary colors are Red (2) and Yellow (4). The mapping is Red->Green(3), Yellow->Orange(7).
    *   In `train_2`, the boundary colors are Red (2), Yellow (4), and Orange (7). The mapping is Red->Orange(7), Yellow->Green(3), Orange->Green(3).
7.  **Fill Colors Used:** The colors used for filling are Green (3) and Orange (7).
8.  **Connectivity:** Identifying enclosed regions requires checking 8-way adjacency (including diagonals). A white region is considered enclosed by color C if all its adjacent non-white pixels are of color C.

## YAML Facts


```yaml
task_description: Fill enclosed white regions based on boundary color, where the fill rule depends on the set of boundary colors present globally.

elements:
  - element: grid
    properties:
      - background_color: white (0)
      - dimensions: unchanged between input and output

  - element: object
    description: Contiguous regions of non-white pixels. In examples, these form shapes with boundaries.
    properties:
      - color: Red(2), Yellow(4), Orange(7) observed in examples.
      - role: Can form boundaries enclosing white regions.

  - element: enclosed_region
    description: A connected component of white (0) pixels where all adjacent non-white pixels (8-way connectivity) share the same single color C.
    properties:
      - initial_color: white (0)
      - boundary_color: The single color C surrounding the region.
      - state_change: Filled with a new color F in the output.

relationships:
  - relationship: boundary_to_fill_mapping
    description: The fill color F depends on the boundary color C. This mapping itself is conditional.
    conditions:
      - condition: Global set of boundary colors S = {Red(2), Yellow(4)}
        mapping: {Red(2): Green(3), Yellow(4): Orange(7)}
      - condition: Global set of boundary colors S = {Red(2), Yellow(4), Orange(7)}
        mapping: {Red(2): Orange(7), Yellow(4): Green(3), Orange(7): Green(3)}
    target_fill_colors: Green(3), Orange(7)

actions:
  - action: identify_enclosed_regions
    description: Find all connected white regions completely bounded by a single non-white color C.
    inputs: input_grid
    outputs: list of enclosed_regions, set of all boundary_colors S found.

  - action: determine_fill_map
    description: Select the correct boundary_color -> fill_color mapping based on the global set S.
    inputs: set S
    outputs: mapping function/dictionary

  - action: fill_regions
    description: Apply the determined fill color to each identified enclosed region in the output grid.
    inputs: input_grid, identified_regions, fill_map
    outputs: output_grid
```


## Natural Language Program

1.  Create a copy of the input grid, which will become the output grid.
2.  Scan the input grid to identify all connected regions of white (0) pixels.
3.  For each white region, examine all adjacent pixels (up, down, left, right, and diagonals). Collect the colors of all non-white adjacent pixels.
4.  If a white region has adjacent non-white pixels, and *all* of these non-white pixels are of the *same* single color `C`, then this white region is an "enclosed region" bounded by color `C`.
5.  Keep track of all unique boundary colors `C` found across all enclosed regions in the grid. Let `S` be the set of these unique boundary colors.
6.  Determine the rule for mapping boundary colors (`C`) to fill colors (`F`) based on the set `S`:
    *   If the set `S` contains only Red (2) and Yellow (4), use the mapping: Red(2) -> Green(3), Yellow(4) -> Orange(7).
    *   If the set `S` contains Red (2), Yellow (4), and Orange (7), use the mapping: Red(2) -> Orange(7), Yellow(4) -> Green(3), Orange(7) -> Green(3).
    *   (Assume these are the only relevant cases based on training data).
7.  For each identified enclosed region:
    *   Get its boundary color `C`.
    *   Find the corresponding fill color `F` using the mapping rule determined in step 6.
    *   Change the color of all white pixels within this enclosed region to the fill color `F` in the output grid.
8.  Return the modified output grid.
```python
import numpy as np
from collections import deque

"""
Identifies connected regions of white (0) pixels that are completely enclosed by a single non-white color.
The fill color used for these enclosed regions depends on the global set of boundary colors found in the entire grid.

1. Find all connected components of white pixels.
2. For each white component, check its adjacent non-white neighbors.
3. If all non-white neighbors of a component have the same single color C, it's an "enclosed region" with boundary color C.
4. Collect all unique boundary colors C found across the grid into a set S.
5. Determine the fill color mapping based on S:
   - If S = {Red(2), Yellow(4)}, map: Red(2)->Green(3), Yellow(4)->Orange(7).
   - If S = {Red(2), Yellow(4), Orange(7)}, map: Red(2)->Orange(7), Yellow(4)->Green(3), Orange(7)->Green(3).
6. Create a copy of the input grid.
7. For each enclosed region, fill its white pixels with the corresponding fill color determined by the mapping rule in the copied grid.
8. Return the modified grid.
"""

def get_neighbors(r, c, height, width):
    """ Gets 8-way neighbors within grid bounds. """
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def find_enclosed_regions(input_grid):
    """
    Finds white regions enclosed by a single color using BFS.

    Returns:
        tuple: (list of (region_pixels, boundary_color), set of all_boundary_colors)
               region_pixels is a list of (r, c) tuples for the white pixels.
    """
    height, width = input_grid.shape
    visited = np.zeros_like(input_grid, dtype=bool)
    enclosed_regions = []
    all_boundary_colors = set()

    for r in range(height):
        for c in range(width):
            # Start BFS if white and not visited
            if input_grid[r, c] == 0 and not visited[r, c]:
                q = deque([(r, c)])
                visited[r, c] = True
                current_region_pixels = []
                boundary_colors_found = set()
                is_enclosed_candidate = True # Assume enclosed until proven otherwise

                while q:
                    curr_r, curr_c = q.popleft()
                    current_region_pixels.append((curr_r, curr_c))

                    # Check neighbors
                    for nr, nc in get_neighbors(curr_r, curr_c, height, width):
                        neighbor_color = input_grid[nr, nc]
                        if neighbor_color == 0: # White neighbor
                            if not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                        else: # Non-white neighbor
                            boundary_colors_found.add(neighbor_color)

                # Check if the region qualifies as enclosed after BFS
                if boundary_colors_found and len(boundary_colors_found) == 1:
                     boundary_color = boundary_colors_found.pop() # Get the single boundary color
                     enclosed_regions.append((current_region_pixels, boundary_color))
                     all_boundary_colors.add(boundary_color) # Add to global set

    return enclosed_regions, all_boundary_colors


def transform(input_grid):
    """
    Transforms the input grid by filling enclosed white regions based on boundary color rules.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    height, width = input_grid_np.shape

    # 1. & 2. & 3. Find enclosed regions and their boundary colors
    regions_found, global_boundary_colors = find_enclosed_regions(input_grid_np)

    # 4. Determine the fill color mapping based on the global set of boundary colors
    fill_map = {}
    # Convert set to tuple for matching dictionary keys if needed, or just use set comparison
    global_boundary_colors_set = frozenset(global_boundary_colors)

    # Define known mappings based on training examples
    mapping_rules = {
        frozenset({2, 4}): {2: 3, 4: 7}, # Red(2), Yellow(4) -> Red:Green(3), Yellow:Orange(7)
        frozenset({2, 4, 7}): {2: 7, 4: 3, 7: 3} # Red(2), Yellow(4), Orange(7) -> Red:Orange(7), Yellow:Green(3), Orange:Green(3)
    }

    if global_boundary_colors_set in mapping_rules:
        fill_map = mapping_rules[global_boundary_colors_set]
    # else: handle unknown cases if necessary, here we assume one of the known cases applies

    # 5. & 6. Fill the regions in the output grid
    if fill_map: # Only fill if a valid mapping was found
        for region_pixels, boundary_color in regions_found:
            if boundary_color in fill_map:
                fill_color = fill_map[boundary_color]
                for r, c in region_pixels:
                    # Ensure we only fill pixels that were originally white
                    # (This check might be redundant if find_enclosed_regions is correct, but adds safety)
                    if output_grid[r, c] == 0:
                        output_grid[r, c] = fill_color

    # 7. Return the modified grid
    return output_grid.tolist()
```
```python
import numpy as np
from collections import deque

"""
Identifies connected regions of white (0) pixels that are 'holes' within shapes (i.e., not connected to the grid border background).
For each such hole, determines if it is enclosed by a single non-white color C.
Collects all such unique boundary colors C found across all qualifying holes into a global set S.
Determines a fill color mapping based on the global set S:
 - If S = {Red(2), Yellow(4)}, map: Red(2)->Green(3), Yellow(4)->Orange(7).
 - If S = {Red(2), Yellow(4), Orange(7)}, map: Red(2)->Orange(7), Yellow(4)->Green(3), Orange(7)->Green(3).
Fills only the qualifying holes (white pixels not connected to the border, enclosed by a single color) using the determined fill color based on their boundary color C.
The original shapes/boundaries remain unchanged.
"""

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

def find_holes_and_boundaries(input_grid):
    """
    Finds white regions not connected to the border (holes) and checks if they
    are enclosed by a single color.

    Returns:
        tuple: (list of (hole_pixels, boundary_color), set of all_boundary_colors)
               hole_pixels is a list of (r, c) tuples for the white pixels in the hole.
    """
    height, width = input_grid.shape
    visited = np.zeros_like(input_grid, dtype=bool)
    holes_info = []
    all_boundary_colors = set()

    # 1. Identify 'true background' white pixels connected to the border using BFS
    q = deque()
    for r in range(height):
        if input_grid[r, 0] == 0 and not visited[r, 0]:
            visited[r, 0] = True
            q.append((r, 0))
        if input_grid[r, width - 1] == 0 and not visited[r, width - 1]:
            visited[r, width - 1] = True
            q.append((r, width - 1))
    for c in range(width):
        if input_grid[0, c] == 0 and not visited[0, c]:
            visited[0, c] = True
            q.append((0, c))
        if input_grid[height - 1, c] == 0 and not visited[height - 1, c]:
            visited[height - 1, c] = True
            q.append((height - 1, c))

    while q:
        r, c = q.popleft()
        for nr, nc in get_neighbors(r, c, height, width, connectivity=4): # Use 4-way for background fill
            if input_grid[nr, nc] == 0 and not visited[nr, nc]:
                visited[nr, nc] = True
                q.append((nr, nc))

    # 2. Find connected components of remaining (unvisited) white pixels (these are potential holes)
    for r in range(height):
        for c in range(width):
            # Start BFS for unvisited white pixels (potential holes)
            if input_grid[r, c] == 0 and not visited[r, c]:
                q_hole = deque([(r, c)])
                visited[r, c] = True
                current_hole_pixels = []
                boundary_colors_found = set()
                is_valid_hole = True # Assume valid until proven otherwise (e.g., touches >1 color)

                # Use a temporary visited set for the current hole search to avoid interference
                # between boundary color checks of different holes. Re-use the main 'visited'
                # to ensure we don't start BFS for the same hole multiple times.
                hole_q = deque([(r, c)])
                hole_visited_local = set([(r, c)]) # Track visited within this specific hole BFS

                while hole_q:
                    curr_r, curr_c = hole_q.popleft()
                    current_hole_pixels.append((curr_r, curr_c))
                    visited[curr_r, curr_c] = True # Mark as globally visited

                    # Check 8-way neighbors to find boundary colors
                    for nr, nc in get_neighbors(curr_r, curr_c, height, width, connectivity=8):
                        neighbor_color = input_grid[nr, nc]
                        if neighbor_color == 0: # White neighbor
                            if (nr, nc) not in hole_visited_local:
                                # Check if it's part of the background fill
                                # If a white neighbor is connected to the background, this isn't a true hole
                                # Revisit this logic - the outer BFS should have marked all background cells already
                                # If input_grid[nr,nc]==0 and visited[nr,nc] is True, it means it's background

                                # Add to queue if it's white and not visited locally yet
                                hole_visited_local.add((nr, nc))
                                hole_q.append((nr, nc))
                        else: # Non-white neighbor (part of the boundary)
                            boundary_colors_found.add(neighbor_color)

                # 3. Check if the hole is enclosed by a single color
                if boundary_colors_found and len(boundary_colors_found) == 1:
                     boundary_color = boundary_colors_found.pop() # Get the single boundary color
                     holes_info.append((current_hole_pixels, boundary_color))
                     all_boundary_colors.add(boundary_color) # Add to global set

    return holes_info, all_boundary_colors


def transform(input_grid):
    """
    Transforms the input grid by filling enclosed 'hole' white regions based on boundary color rules.
    Holes are white regions not connected to the grid border.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = input_grid_np.copy()
    height, width = input_grid_np.shape

    # Find holes and their boundary colors
    holes_found, global_boundary_colors = find_holes_and_boundaries(input_grid_np)

    # Determine the fill color mapping based on the global set of boundary colors
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

    # Fill the identified holes in the output grid using the map
    if fill_map: # Only fill if a valid mapping was found
        for hole_pixels, boundary_color in holes_found:
            # Check if the boundary color has a defined fill color in the current map
            if boundary_color in fill_map:
                fill_color = fill_map[boundary_color]
                # Color the pixels belonging to this hole
                for r, c in hole_pixels:
                    output_grid[r, c] = fill_color

    # Return the modified grid as a list of lists
    return output_grid.tolist()
```
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
