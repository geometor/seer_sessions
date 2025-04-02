
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
6 0 0 6 4 4 0 0 0 0 0 0
0 0 6 0 4 4 4 0 0 0 0 0
0 0 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 0 0
0 0 0 0 3 3 7 0 0 0 0 0
0 0 0 0 3 3 0 7 0 0 0 0
0 0 0 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0 0 0
6 0 0 0 4 4 0 0 0 0 0 0
0 0 0 0 4 4 4 6 6 0 0 0
0 0 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 0 0
0 0 0 0 3 3 0 0 0 0 0 0
0 0 0 0 3 3 0 0 0 0 0 0
0 7 7 3 3 3 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 6 0 0
0 0 3 0 0 0 6 0 6 0
0 3 9 3 0 0 6 9 6 0
3 9 0 0 3 0 0 0 0 0
0 0 9 0 3 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 9 0 0 0 0 0 0 0
0 0 9 0 0 0 0 0 0 0
0 0 9 0 0 0 0 9 0 0
0 0 3 0 0 0 0 6 0 0
0 0 3 0 0 0 6 0 6 0
0 3 0 3 0 0 6 0 6 0
3 0 0 0 3 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0
0 0 0 6 6 0 0 6 0 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0
0 0 6 7 7 7 7 0 6 0 0 0
0 0 6 0 0 0 7 0 6 0 0 0
0 0 6 7 0 7 0 0 6 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 7 0 0 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0
0 0 0 6 6 0 0 6 0 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0
0 0 6 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the examples to understand the transformation.

**Perception of Elements:**

The examples involve grids containing distinct colored objects on a white background. The key transformation seems to involve interactions between objects where one object encloses pixels of another color.

*   **Example 1:** Shows yellow and green shapes, with nearby magenta and orange pixels respectively. In the output, some magenta and orange pixels are removed, and new ones appear elsewhere. This example seems distinct from the others; the magenta/orange pixels are *outside* the main shapes, and the transformation rule isn't immediately obvious or consistent with Examples 2 and 3. The removal seems related to adjacency between same-colored pixels (magenta-magenta, orange-orange), but the placement of new pixels is unclear.
*   **Example 2:** Shows a green shape enclosing maroon pixels and a magenta shape also enclosing maroon pixels. In the output, the enclosed maroon pixels are gone. New maroon pixels appear at the top of the columns where the enclosed pixels were originally located.
*   **Example 3:** Shows a magenta shape enclosing several orange pixels. In the output, the enclosed orange pixels are removed. New orange pixels appear at the top of one specific column (the leftmost column that contained the most enclosed orange pixels). The number of new orange pixels matches the number of distinct rows that contained the removed orange pixels.

**Conclusion:** Examples 2 and 3 demonstrate a consistent pattern: a colored shape encloses pixels of a different color. These enclosed pixels are removed, and new pixels of that same color are added to the top of the grid in the column that originally contained the most enclosed pixels (leftmost in case of a tie). The number of new pixels equals the number of rows involved in the enclosure. Example 1 does not seem to follow this enclosure rule and might represent a different pattern or edge case not fully captured by the other examples. I will focus the documentation and program on the clear enclosure pattern observed in Examples 2 and 3.

**YAML Facts:**


```yaml
Task: Color Fill based on Enclosure

Elements:
  - Grid: A 2D array of pixels with integer values representing colors (0-9). Background is white (0).
  - Objects: Contiguous regions of non-white pixels.
  - Enclosing Object: An object whose pixels form a boundary completely surrounding pixels of a different non-white color.
  - Enclosed Pixels: Non-white pixels located within the boundary of an Enclosing Object of a different color.
  - Enclosed Color: The color of the Enclosed Pixels.

Relationships:
  - Enclosure: An Enclosing Object spatially surrounds Enclosed Pixels. A pixel is enclosed if any path from it to the grid boundary must cross a pixel of the Enclosing Object.

Actions:
  - Identify Enclosures: Find all pairs of (Enclosing Object, Enclosed Pixels of a specific Enclosed Color).
  - Remove: Change the color of all identified Enclosed Pixels to white (0).
  - Analyze Columns: For each Enclosed Color removed:
      - Count how many pixels were removed in each column.
      - Find the maximum count.
      - Identify the column index(es) with the maximum count.
      - Select the minimum (leftmost) column index among those with the maximum count.
  - Analyze Rows: For each Enclosed Color removed:
      - Count the number of unique row indices (`N`) from which pixels were removed.
  - Add: In the selected column, change the color of the top `N` pixels (rows 0 to N-1) to the Enclosed Color.

Properties:
  - Color: The integer value (0-9) of a pixel.
  - Location: The (row, column) index of a pixel.
  - Shape: The configuration of pixels forming an object.
  - Connectivity: Pixels are connected cardinally (up, down, left, right). (Note: Flood fill for enclosure might need to consider diagonals or just ensure no path to edge exists).

Rule Focus: The transformation primarily targets pixels enclosed by objects of a different color, as seen consistently in examples 2 and 3. Example 1's behavior seems different and is not covered by this primary rule.
```


**Natural Language Program:**

1.  Identify all contiguous objects of non-white colors in the input grid.
2.  For each object, determine if it completely encloses any pixels of a *different* non-white color. Perform this check for each potential enclosed color separately.
3.  If an object encloses pixels of a specific color (the "enclosed color"):
    a.  Record the locations (row, column) of all pixels of the enclosed color that are inside the enclosing object.
    b.  Change these enclosed pixels in the grid to white (0).
    c.  Calculate the frequency of each column index among the recorded locations.
    d.  Find the maximum frequency (highest number of enclosed pixels in a single column).
    e.  Identify the column index (or indices) that have this maximum frequency. Choose the smallest (leftmost) column index among them.
    f.  Count the number of unique row indices among the recorded locations. Let this count be `N`.
    g.  In the chosen leftmost column with the maximum frequency, set the color of the pixels in rows 0 to `N-1` to the enclosed color.
4.  Repeat step 3 for all identified enclosures.
5.  The final state of the grid after processing all enclosures is the output. Pixels not involved in an enclosure (neither part of an enclosing object boundary nor an enclosed pixel) remain unchanged.
```python
import numpy as np
from collections import deque, Counter

"""
Identifies pixels of a specific color (C_enclosed) that are enclosed by pixels of any other non-white color. 
Enclosed means that any path from the pixel to the grid boundary must pass through a non-white pixel that is not C_enclosed.

Steps:
1. Iterate through each non-white color `C_enclosed` present in the input grid.
2. For each `C_enclosed`, determine which pixels of this color are enclosed.
   - Perform a Breadth-First Search (BFS) starting from all boundary cells of the grid.
   - The BFS can only travel through white pixels (0) or pixels of color `C_enclosed`.
   - Any pixel of color `C_enclosed` that is *not* reached by this BFS is considered enclosed.
3. Collect all enclosed pixels for all colors. Store them grouped by their original color.
4. Create an output grid, initially a copy of the input.
5. Remove all identified enclosed pixels from the output grid by setting their color to white (0).
6. For each color `C_enclosed` that had enclosed pixels removed:
   a. Calculate the frequency of column indices among the removed pixel locations for this color.
   b. Find the maximum frequency (most pixels removed in a single column).
   c. Identify the column index (or indices) with this maximum frequency. Select the minimum (leftmost) column index among them (`target_col`).
   d. Count the number of unique row indices among the removed pixel locations for this color (`N`).
   e. In the `output_grid`, set the color of the pixels in the `target_col` from row 0 to row `N-1` to `C_enclosed`.
7. Return the final modified output grid.
"""

def find_enclosed_pixels(grid, color_to_check):
    """
    Finds pixels of `color_to_check` that are enclosed.
    Uses BFS starting from the boundary, propagating through white cells and cells of `color_to_check`.
    """
    rows, cols = grid.shape
    reachable = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Add boundary cells to the queue if they are white or the color_to_check
    for r in range(rows):
        for c in [0, cols - 1]:
            if not reachable[r, c] and (grid[r, c] == 0 or grid[r, c] == color_to_check):
                q.append((r, c))
                reachable[r, c] = True
    for c in range(cols):
        for r in [0, rows - 1]:
             if not reachable[r, c] and (grid[r, c] == 0 or grid[r, c] == color_to_check):
                q.append((r, c))
                reachable[r, c] = True

    # Perform BFS
    while q:
        r, c = q.popleft()

        # Explore neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is reachable (white or target color) and not visited
                if not reachable[nr, nc] and (grid[nr, nc] == 0 or grid[nr, nc] == color_to_check):
                    reachable[nr, nc] = True
                    q.append((nr, nc))

    # Identify enclosed pixels (target color pixels that were not reached)
    enclosed_locations = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color_to_check and not reachable[r, c]:
                enclosed_locations.append((r, c))

    return enclosed_locations


def transform(input_grid):
    """
    Applies the enclosure transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    unique_colors = np.unique(input_grid[input_grid != 0]) # Get all non-white colors

    all_removed_pixels_by_color = {}

    # 1. Find all enclosed pixels for each color
    for color in unique_colors:
        enclosed_locations = find_enclosed_pixels(input_grid, color)
        if enclosed_locations:
            all_removed_pixels_by_color[color] = enclosed_locations

    # 2. Remove enclosed pixels from the output grid
    for color, locations in all_removed_pixels_by_color.items():
        for r, c in locations:
            output_grid[r, c] = 0 # Set to white

    # 3. Add new pixels at the top of the target column for each color
    for color, removed_locations in all_removed_pixels_by_color.items():
        if not removed_locations:
            continue

        # a. Calculate column frequencies
        columns = [c for r, c in removed_locations]
        if not columns: continue # Should not happen if removed_locations is not empty, but safety check
        
        col_counts = Counter(columns)
        max_freq = 0
        for col, count in col_counts.items():
             if count > max_freq:
                 max_freq = count
        
        # b. Find leftmost column(s) with max frequency
        candidate_cols = []
        for col, count in col_counts.items():
            if count == max_freq:
                candidate_cols.append(col)
        
        target_col = min(candidate_cols)


        # c. Count unique rows
        unique_rows = set(r for r, c in removed_locations)
        N = len(unique_rows)

        # d. Add pixels to the top of the target column
        for i in range(min(N, rows)): # Ensure we don't write past grid boundary
            output_grid[i, target_col] = color

    return output_grid
```
```python
import numpy as np
from collections import deque, Counter

"""
Transformation Rule:

1. Identify Enclosed Pixels: For each non-white color C present in the grid, find all pixels of color C that are "enclosed". A pixel is considered enclosed if it cannot reach the boundary of the grid by moving only through white (0) pixels or pixels of the same color C. This is determined using a Breadth-First Search (BFS) starting from all boundary cells, propagating only through white cells. Any non-white cell *not* reached by this BFS is potentially enclosed. We then filter these potentially enclosed cells to find those specifically of color C.

2. Remove Enclosed Pixels: Change the color of all identified enclosed pixels (for all colors) to white (0) in a copy of the input grid.

3. Add Indicator Pixels: For each color C for which enclosed pixels were found and removed:
    a. Collect the locations (row, column) of the removed pixels of color C.
    b. Count the frequency of each column index among these locations.
    c. Find the maximum frequency (the highest number of removed pixels in a single column).
    d. Identify all column indices that have this maximum frequency.
    e. Select the minimum (leftmost) column index among those identified in step 3d. Let this be `target_col`.
    f. Count the number of unique row indices among the removed pixel locations for color C. Let this be `N`.
    g. In the `target_col`, change the color of the top `N` pixels (rows 0 to N-1) to color C.

4. Final Grid: The grid after performing steps 2 and 3 for all relevant colors is the final output. If no pixels are enclosed according to the definition in step 1, the output grid is identical to the input grid. This rule specifically addresses the pattern observed in Examples 2 and 3. Example 1 appears to follow a different logic not covered here.
"""

def find_unreachable_non_white(grid):
    """
    Finds all non-white pixels that cannot reach the grid boundary via white cells.
    Uses BFS starting from the boundary, propagating only through white cells (0).
    """
    rows, cols = grid.shape
    reachable = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Add boundary white cells to the queue
    for r in range(rows):
        for c in [0, cols - 1]:
            if not reachable[r, c] and grid[r, c] == 0:
                q.append((r, c))
                reachable[r, c] = True
    for c in range(cols):
        for r in [0, rows - 1]:
             if not reachable[r, c] and grid[r, c] == 0:
                q.append((r, c))
                reachable[r, c] = True

    # Perform BFS through white cells
    while q:
        r, c = q.popleft()

        # Explore neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds and if neighbor is white and not visited
            if 0 <= nr < rows and 0 <= nc < cols and \
               not reachable[nr, nc] and grid[nr, nc] == 0:
                reachable[nr, nc] = True
                q.append((nr, nc))

    # Identify non-white pixels that were not reached
    unreachable_locations = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not reachable[r, c]:
                unreachable_locations.append(((r, c), grid[r,c])) # Store location and color

    return unreachable_locations

def transform(input_grid):
    """
    Applies the enclosure transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Find all potentially enclosed non-white pixels and their colors
    potentially_enclosed_pixels = find_unreachable_non_white(input_grid)

    # Group potentially enclosed pixels by their color
    enclosed_by_color = {}
    for (r, c), color in potentially_enclosed_pixels:
        if color not in enclosed_by_color:
            enclosed_by_color[color] = []
        enclosed_by_color[color].append((r, c))

    # Check if these potentially enclosed pixels are *actually* enclosed
    # (i.e., cannot escape via cells of their own color either)
    # This check is implicitly handled by the BFS logic in find_unreachable_non_white
    # because the BFS *only* travels through white. If a non-white cell isn't
    # reachable via white cells, it's considered enclosed for this problem's definition.

    # Store locations to remove and process later
    all_removed_pixels_by_color = {}

    for color, locations in enclosed_by_color.items():
         if locations: # If any pixels of this color were found to be enclosed
             all_removed_pixels_by_color[color] = locations
             # 2. Remove these enclosed pixels from the output grid
             for r, c in locations:
                 output_grid[r, c] = 0 # Set to white


    # 3. Add new pixels at the top of the target column for each color
    for color, removed_locations in all_removed_pixels_by_color.items():
        if not removed_locations:
            continue

        # a. Get column indices
        columns = [c for r, c in removed_locations]
        if not columns: continue

        # b. Calculate column frequencies
        col_counts = Counter(columns)

        # c. Find maximum frequency
        # Handle case where col_counts might be empty if columns was empty (shouldn't happen with check above)
        if not col_counts: continue
        max_freq = max(col_counts.values())

        # d. Find columns with max frequency
        candidate_cols = [col for col, count in col_counts.items() if count == max_freq]

        # e. Select the minimum (leftmost) column index
        target_col = min(candidate_cols)

        # f. Count unique rows
        unique_rows = set(r for r, c in removed_locations)
        N = len(unique_rows)

        # g. Add pixels to the top of the target column
        for i in range(min(N, rows)): # Ensure we don't write past grid boundary
            output_grid[i, target_col] = color

    return output_grid
```
```python
import numpy as np
from collections import deque, Counter
import math

"""
Transformation Rule:

1.  Identify Unreachable Pixels: Find all non-white pixels in the input grid that cannot reach any boundary cell by moving only through adjacent white (0) pixels. This is done via a Breadth-First Search (BFS) starting from boundary white cells.
2.  Group Unreachable Pixels: Partition the identified unreachable pixels into "Enclosed Groups". An Enclosed Group consists of pixels that:
    a.  All have the same color.
    b.  Form a single connected component using 4-way adjacency (considering only connections between the identified unreachable pixels of that same color).
3.  Process Each Group: For every Enclosed Group found:
    a.  Remove Group Pixels: Change the color of all pixels belonging to the group to white (0) in the output grid.
    b.  Determine Target Column:
        i.  Calculate the frequency of each column index among the group's pixel locations.
        ii. Find the maximum frequency (`max_freq`).
        iii. Identify all column indices (`candidate_cols`) that achieve `max_freq`.
        iv. Apply Tie-breaker:
            - If only one candidate column, select it.
            - If multiple candidates: Calculate the average column index (centroid) of the group's locations. Select the candidate column closest (minimum absolute difference) to the centroid. If still tied (equidistant), select the leftmost (minimum index) tied column.
    c.  Determine Indicator Count (`N`): Count the number of unique row indices among the group's pixel locations.
    d.  Add Indicator Pixels: In the selected target column, change the color of the top `N` pixels (rows 0 to N-1) to the group's color.
4.  Final Grid: The grid after processing all Enclosed Groups is the final output.
(Note: This procedure describes the logic derived primarily from examples 2 and 3; example 1 appears to follow a different pattern not captured by this rule.)
"""

def find_unreachable_non_white(grid):
    """
    Finds all non-white pixels that cannot reach the grid boundary via white cells.
    Uses BFS starting from the boundary, propagating only through white cells (0).
    Returns a set of ((r, c), color) tuples for unreachable non-white pixels.
    """
    rows, cols = grid.shape
    reachable = np.zeros_like(grid, dtype=bool)
    q = deque()
    unreachable_pixels = set() # Using a set for efficient lookup later

    # Initialize BFS queue with boundary white cells
    for r in range(rows):
        for c in [0, cols - 1]:
            if not reachable[r, c] and grid[r, c] == 0:
                q.append((r, c))
                reachable[r, c] = True
    for c in range(cols):
        for r in [0, rows - 1]:
             if not reachable[r, c] and grid[r, c] == 0:
                q.append((r, c))
                reachable[r, c] = True

    # Perform BFS through white cells
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               not reachable[nr, nc] and grid[nr, nc] == 0:
                reachable[nr, nc] = True
                q.append((nr, nc))

    # Identify non-white pixels that were not reached
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not reachable[r, c]:
                unreachable_pixels.add(((r, c), grid[r,c]))

    return unreachable_pixels

def group_pixels(unreachable_pixels, grid_shape):
    """
    Groups unreachable pixels into connected components based on color and adjacency.
    Returns a dictionary {color: [group1_locations, group2_locations, ...]}
    where each group_locations is a list of (r, c) tuples.
    """
    rows, cols = grid_shape
    visited = set()
    groups = {}
    unreachable_locations = {loc for loc, color in unreachable_pixels} # For quick spatial check

    for pixel_loc, color in unreachable_pixels:
        if pixel_loc not in visited:
            current_group = []
            q = deque([pixel_loc])
            visited.add(pixel_loc)

            # BFS within unreachable pixels of the same color
            while q:
                r, c = q.popleft()
                current_group.append((r,c))

                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    neighbor_loc = (nr, nc)

                    # Check bounds, if neighbor is unreachable, same color, and not visited
                    if 0 <= nr < rows and 0 <= nc < cols and \
                       neighbor_loc in unreachable_locations and \
                       grid[nr, nc] == color and \
                       neighbor_loc not in visited:

                        # Check if this neighbor is part of the original unreachable set
                        # (This check might be redundant if unreachable_locations is derived correctly)
                        is_unreachable = False
                        for loc, clr in unreachable_pixels:
                           if loc == neighbor_loc and clr == color:
                               is_unreachable = True
                               break
                        
                        if is_unreachable:
                            visited.add(neighbor_loc)
                            q.append(neighbor_loc)


            # Store the found group
            if color not in groups:
                groups[color] = []
            groups[color].append(current_group)

    return groups


def transform(input_grid):
    """
    Applies the enclosure transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    global grid # Make input_grid accessible to group_pixels for color check
    grid = input_grid

    # 1. Find all non-white pixels unreachable via white cells
    unreachable_pixels_with_color = find_unreachable_non_white(input_grid)

    # 2. Group these pixels by color and connectivity
    enclosed_groups_by_color = group_pixels(unreachable_pixels_with_color, (rows, cols))

    # 3. Process each group
    for color, groups in enclosed_groups_by_color.items():
        for group_locations in groups:
            if not group_locations:
                continue

            # a. Remove group pixels
            for r, c in group_locations:
                output_grid[r, c] = 0

            # b. Determine Target Column
            columns = [c for r, c in group_locations]
            if not columns: continue
            col_counts = Counter(columns)
            max_freq = max(col_counts.values())
            candidate_cols = sorted([col for col, count in col_counts.items() if count == max_freq]) # Sort for leftmost tie-break later

            target_col = -1
            if len(candidate_cols) == 1:
                target_col = candidate_cols[0]
            else:
                # Calculate centroid column
                avg_col = sum(columns) / len(columns)
                min_dist = float('inf')
                best_cols = []
                for col in candidate_cols:
                    dist = abs(col - avg_col)
                    if dist < min_dist:
                        min_dist = dist
                        best_cols = [col]
                    elif dist == min_dist:
                        best_cols.append(col)
                target_col = min(best_cols) # Leftmost if equidistant

            # c. Determine Indicator Count (N)
            unique_rows = set(r for r, c in group_locations)
            N = len(unique_rows)

            # d. Add Indicator Pixels
            for i in range(min(N, rows)): # Ensure we don't write past grid boundary
                output_grid[i, target_col] = color

    return output_grid
```
