
## train_1

**input:**
```
3 8 8 8 8 8 8 0 8 8 8 8 8 8 8 8 8 8 3
0 0 0 7 7 7 0 0 0 7 7 7 0 0 0 0 0 0 0
3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3
0 0 0 0 0 7 7 7 0 0 0 0 7 7 7 0 0 0 0
3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3
0 0 7 7 7 0 0 7 7 7 0 0 0 0 7 7 7 0 0
3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3
0 0 0 0 7 7 7 0 0 0 7 7 7 0 0 0 0 0 0
3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 8 8 3
0 0 0 0 0 0 0 7 7 7 0 0 0 0 0 0 0 0 0
3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3
0 0 0 0 7 7 7 0 0 0 0 0 7 7 7 0 0 0 0
8 8 0 8 8 8 8 8 0 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 6 8 8 0 8 8 6 8 8 8 8 8 8 8 8
0 0 0 8 6 8 0 0 0 8 6 8 0 0 0 0 0 0 0
3 3 8 8 6 8 6 8 8 8 6 8 8 6 8 8 8 8 8
0 0 0 0 0 8 6 8 0 0 0 0 8 6 8 0 0 0 0
8 8 8 6 8 8 6 8 6 8 8 8 8 6 8 6 8 8 8
0 0 8 6 8 0 0 8 6 8 0 0 0 0 8 6 8 0 0
3 3 8 6 8 6 8 8 6 8 8 6 8 8 8 6 8 3 3
0 0 0 0 8 6 8 0 0 0 8 6 8 0 0 0 0 0 0
3 8 8 8 8 6 8 8 6 8 8 6 8 8 3 0 8 8 3
0 0 0 0 0 0 0 8 6 8 0 0 0 0 0 0 0 0 0
8 8 8 8 8 6 8 8 6 8 8 8 8 6 8 8 8 8 8
0 0 0 0 8 6 8 0 0 0 0 0 8 6 8 0 0 0 0
8 8 0 3 8 6 8 8 0 3 8 8 8 6 8 8 8 8 3
```


## train_2

**input:**
```
3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3
0 0 0 7 7 7 0 0 0 0 0 0 0 0 0 0
3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3
0 0 0 0 0 0 0 0 0 0 0 7 7 7 0 0
3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3
0 0 0 0 0 7 7 7 0 0 0 0 0 0 0 0
3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3
0 0 7 7 7 0 0 0 0 0 7 7 7 0 0 0
3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3
0 0 0 0 0 0 7 7 7 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 6 8 8 8 8 8 8 8 8 8 8 8
0 0 0 8 6 8 0 0 0 0 0 0 0 0 0 0
3 3 8 8 6 8 8 8 8 8 8 8 6 8 8 8
0 0 0 0 0 0 0 0 0 0 0 8 6 8 0 0
8 8 8 8 8 8 6 8 8 8 8 8 6 8 3 3
0 0 0 0 0 8 6 8 0 0 0 0 0 0 0 0
8 8 8 6 8 8 6 8 8 8 8 6 8 8 8 8
0 0 8 6 8 0 0 0 0 0 8 6 8 0 0 0
3 3 8 6 8 8 8 6 8 8 8 6 8 8 3 3
0 0 0 0 0 0 8 6 8 0 0 0 0 0 0 0
3 8 8 8 8 8 8 6 8 8 8 8 8 8 8 3
```

Okay, let's break down the transformation.

**Perception of Elements:**

1.  **Grid Structure:** The input and output are grids of numbers (representing colors or states). The dimensions remain the same.
2.  **Key Pattern:** The core pattern in the input seems to be horizontal sequences of `7 7 7`.
3.  **Transformation Colors:**
    *   `7`: The primary color being transformed.
    *   `8`: Acts as a replacement color for the outer `7`s and sometimes as a background color that gets modified.
    *   `6`: A new color appearing in the output, replacing the middle `7` and sometimes replacing `8`s vertically adjacent to the middle `7`.
    *   `3`: A color that appears in the output, often replacing other colors (`0`, `8`, `3`) adjacent (orthogonally or diagonally) to the original outer `7` locations.
    *   `0`: Background color, sometimes changed to `3` if adjacent to outer `7` locations.
4.  **Transformation Logic:** The transformation involves several rules applied based on the position relative to the `7 7 7` patterns.
    *   A direct replacement rule for `7 7 7`.
    *   A rule affecting `8`s vertically adjacent to the *center* of the pattern.
    *   A rule affecting *any* color adjacent (including diagonals) to the *outer* parts of the pattern.
    *   A precedence or interaction logic seems necessary when a cell qualifies for multiple rules.

**YAML Facts:**

```yaml
Grid:
  Properties:
    - dimensions (height, width)
    - cells containing single digits (0-8)
Objects:
  - Pattern:
      Type: Horizontal sequence
      Value: [7, 7, 7]
      Properties:
        - center_cell_location: (r, c)
        - outer_cell_locations: [(r, c-1), (r, c+1)]
Actions:
  - Identify: Locate all instances of the [7, 7, 7] Pattern in the input grid.
  - Transform: Modify cell values in the output grid based on proximity and value relative to identified patterns.
  - Rules:
      - Rule_Core:
          Input: Cells at outer_cell_locations and center_cell_location of a Pattern.
          Output: Change outer cells to 8, center cell to 6.
          Priority: Highest.
      - Rule_Vertical_Neighbor:
          Input: Cell (r_neighbor, c_center) where input value is 8 AND (r_neighbor, c_center) is vertically adjacent to a center_cell_location (r_center, c_center).
          Output: Change cell (r_neighbor, c_center) to 6.
          Priority: Medium-High (overrides Rule_Adjacent_Neighbor if conflict involves same-row orthogonal Outer 7).
      - Rule_Adjacent_Neighbor:
          Input: Cell (r_adj, c_adj) that is orthogonally or diagonally adjacent to any outer_cell_location from any Pattern.
          Output: Change cell (r_adj, c_adj) to 3.
          Priority: Medium-Low (overridden by Rule_Vertical_Neighbor if conflict involves same-row orthogonal Outer 7, overrides Copy).
      - Rule_Copy:
          Input: Any cell not modified by other rules.
          Output: Keep the original input value.
          Priority: Lowest.
Relationships:
  - Adjacency:
      Type: Orthogonal (Up, Down, Left, Right)
      Used_by: Rule_Vertical_Neighbor (specifically vertical), Rule_Adjacent_Neighbor (conflict resolution part)
  - Adjacency:
      Type: Orthogonal and Diagonal (8 neighbors)
      Used_by: Rule_Adjacent_Neighbor (initial condition)
  - Proximity: Relative positioning to center_cell_location and outer_cell_locations drives the application of rules.
  - Conflict Resolution: Specific conditions determine precedence when a cell meets criteria for both Rule_Vertical_Neighbor and Rule_Adjacent_Neighbor.
```

**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Find all locations `(r, c)` which are the center of a horizontal `7 7 7` pattern in the input grid. Store these as `Center7Locations`.
3.  Identify all corresponding left `(r, c-1)` and right `(r, c+1)` locations for each center found. Store these as `Outer7Locations`.
4.  Create a temporary record of changes based on the following rules, evaluated for *every* cell `(r, c)` using the *input* grid values and locations identified above:
    a.  **Core Change:** If `(r, c)` is in `Center7Locations`, record a change to `6`. If `(r, c)` is in `Outer7Locations`, record a change to `8`.
    b.  **Vertical 6 Change:** If the input value at `(r, c)` is `8` AND `(r, c)` is vertically adjacent to any location in `Center7Locations`, record a change to `6`.
    c.  **Adjacent 3 Change:** If `(r, c)` is orthogonally or diagonally adjacent to any location in `Outer7Locations`, record a change to `3`. Also note if any of the triggering `Outer7Locations` were *orthogonally* adjacent and in the *same row* `r`.
5.  Apply the recorded changes to the output grid using the following precedence for each cell `(r, c)`:
    a.  If a **Core Change** (to 8 or 6) was recorded for `(r, c)`, apply it.
    b.  Else if both a **Vertical 6 Change** and an **Adjacent 3 Change** were recorded:
        i.  If the **Adjacent 3 Change** was triggered by an *orthogonal* neighbor in the *same row* `r`, apply the **Vertical 6 Change** (output is 6).
        ii. Otherwise, apply the **Adjacent 3 Change** (output is 3).
    c.  Else if only a **Vertical 6 Change** was recorded, apply it (output is 6).
    d.  Else if only an **Adjacent 3 Change** was recorded, apply it (output is 3).
    e.  Else (no changes recorded for this cell), keep the original input value (already copied in step 1).
6.  Return the final output grid.
```python
import copy

"""
Transforms a grid based on the location of horizontal '7 7 7' patterns.

1.  Identifies all horizontal sequences of '7 7 7' in the input grid.
2.  Modifies the grid based on proximity to these patterns:
    a.  The outer '7's of the pattern are changed to '8'.
    b.  The center '7' of the pattern is changed to '6'.
    c.  Input '8's vertically adjacent to the center '7' of a pattern are changed to '6'.
    d.  Any cell (regardless of initial value) orthogonally or diagonally adjacent 
        to the *outer* '7's of a pattern is changed to '3'.
3.  Handles precedence:
    a.  The core '7 7 7' transformation (to '8 6 8') takes highest priority.
    b.  If a cell qualifies for both the vertical '6' change (Rule 2c) and the 
        adjacent '3' change (Rule 2d):
        i.  If the adjacent '3' change was triggered by an outer '7' in the *same row* 
            (i.e., horizontally adjacent), the vertical '6' change takes precedence.
        ii. Otherwise (triggered by diagonal or different row outer '7'), the adjacent '3' 
            change takes precedence.
    c.  If a cell qualifies for only one of Rule 2c or 2d, that rule is applied.
    d.  If a cell is not affected by any rule, its value remains unchanged.
"""

def find_777_patterns(grid: list[list[int]]) -> tuple[set[tuple[int, int]], set[tuple[int, int]]]:
    """
    Finds the locations of the center and outer cells of all '7 7 7' patterns.

    Args:
        grid: The input grid.

    Returns:
        A tuple containing two sets:
        - center_locations: Set of (row, col) tuples for the middle '7'.
        - outer_locations: Set of (row, col) tuples for the left and right '7's.
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    center_locations = set()
    outer_locations = set()

    for r in range(height):
        for c in range(1, width - 1):
            if grid[r][c-1] == 7 and grid[r][c] == 7 and grid[r][c+1] == 7:
                center_locations.add((r, c))
                outer_locations.add((r, c - 1))
                outer_locations.add((r, c + 1))
    return center_locations, outer_locations

def get_neighbors(r: int, c: int, height: int, width: int, diagonal: bool = True) -> list[tuple[int, int]]:
    """
    Gets valid neighbor coordinates for a given cell.

    Args:
        r: Row index of the cell.
        c: Column index of the cell.
        height: Grid height.
        width: Grid width.
        diagonal: Whether to include diagonal neighbors.

    Returns:
        A list of valid (row, col) neighbor coordinates.
    """
    neighbors = []
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue
            if not diagonal and abs(dr) + abs(dc) > 1:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.

    Args:
        input_grid: The 2D list representing the input grid.

    Returns:
        The 2D list representing the transformed output grid.
    """
    if not input_grid or not input_grid[0]:
        return []

    height = len(input_grid)
    width = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)

    # Find all '7 7 7' patterns
    center_7_locations, outer_7_locations = find_777_patterns(input_grid)

    # --- Stage 1: Apply Core Rule (Highest Priority) ---
    modified_by_core = set()
    # Change center 7s to 6
    for r, c in center_7_locations:
        output_grid[r][c] = 6
        modified_by_core.add((r, c))
    # Change outer 7s to 8
    for r, c in outer_7_locations:
        output_grid[r][c] = 8
        modified_by_core.add((r, c))

    # --- Stage 2: Identify Potential Changes for Other Rules ---
    potential_vertical_6_locations = set()
    # Map locations potentially changed to 3 to whether the trigger was horizontal
    potential_adjacent_3_info = {} # (r, c) -> bool (True if same-row trigger)

    for r in range(height):
        for c in range(width):
            # Check for Vertical 6 Rule
            if input_grid[r][c] == 8:
                # Check cell above
                if r > 0 and (r - 1, c) in center_7_locations:
                    potential_vertical_6_locations.add((r, c))
                # Check cell below
                if r < height - 1 and (r + 1, c) in center_7_locations:
                    potential_vertical_6_locations.add((r, c))

            # Check for Adjacent 3 Rule
            is_adjacent_to_outer_7 = False
            triggered_by_same_row = False
            neighbors = get_neighbors(r, c, height, width, diagonal=True)
            for nr, nc in neighbors:
                if (nr, nc) in outer_7_locations:
                    is_adjacent_to_outer_7 = True
                    if nr == r: # Triggering outer 7 is in the same row
                        triggered_by_same_row = True
                        # We only need one same-row trigger to mark it True
                        # break # Optimization removed: need to check all neighbors for potential_adjacent_3_info population

            if is_adjacent_to_outer_7:
                 # Store whether *any* same-row trigger occurred for this cell
                 if (r,c) not in potential_adjacent_3_info:
                     potential_adjacent_3_info[(r,c)] = triggered_by_same_row
                 elif not potential_adjacent_3_info[(r,c)]: # Only upgrade to True if currently False
                     potential_adjacent_3_info[(r,c)] = triggered_by_same_row


    # --- Stage 3: Apply Remaining Rules with Precedence ---
    for r in range(height):
        for c in range(width):
            # Skip cells already modified by the core rule
            if (r, c) in modified_by_core:
                continue

            is_potential_vertical_6 = (r, c) in potential_vertical_6_locations
            is_potential_adjacent_3 = (r, c) in potential_adjacent_3_info

            if is_potential_vertical_6 and is_potential_adjacent_3:
                # Conflict: Apply precedence logic
                triggered_by_same_row_adj = potential_adjacent_3_info[(r, c)]
                if triggered_by_same_row_adj:
                    # Vertical 6 wins if Adjacent 3 was triggered by same-row outer 7
                    output_grid[r][c] = 6
                else:
                    # Adjacent 3 wins otherwise
                    output_grid[r][c] = 3
            elif is_potential_vertical_6:
                # Only Vertical 6 applies
                output_grid[r][c] = 6
            elif is_potential_adjacent_3:
                # Only Adjacent 3 applies
                output_grid[r][c] = 3
            # Else: No rules apply, keep the original value (already copied)

    return output_grid
```
