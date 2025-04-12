
Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
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
Expected Output:
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
Transformed Output:
```
3 8 3 3 3 3 3 0 3 3 3 3 3 8 8 8 8 8 3
0 0 3 8 6 8 3 0 3 8 6 8 3 0 0 0 0 0 0
3 8 3 3 3 3 3 3 3 3 3 3 3 3 3 3 8 8 3
0 0 0 0 3 8 6 8 3 0 0 3 8 6 8 3 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 3 8 6 8 3 3 8 6 8 3 0 0 3 8 6 8 3 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
0 0 0 3 8 6 8 3 0 3 8 6 8 3 0 0 0 0 0
3 8 8 3 3 3 3 3 3 3 3 3 3 3 8 0 8 8 3
0 0 0 0 0 0 3 8 6 8 3 0 0 0 0 0 0 0 0
3 8 8 3 3 3 3 3 3 3 3 3 3 3 3 3 8 8 3
0 0 0 3 8 6 8 3 0 0 0 3 8 6 8 3 0 0 0
8 8 0 3 3 3 3 3 0 8 8 3 3 3 3 3 8 8 8
```
Match: False
Pixels Off: 124
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 100.40485829959515

## Example 2:
Input:
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
Expected Output:
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
Transformed Output:
```
3 8 3 3 3 3 3 8 8 8 8 8 8 8 8 3
0 0 3 8 6 8 3 0 0 0 0 0 0 0 0 0
3 8 3 3 3 3 3 8 8 8 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0 3 8 6 8 3 0
3 8 8 8 3 3 3 3 3 8 3 3 3 3 3 3
0 0 0 0 3 8 6 8 3 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 8 3
0 3 8 6 8 3 0 0 0 3 8 6 8 3 0 0
3 3 3 3 3 3 3 3 3 3 3 3 3 3 8 3
0 0 0 0 0 3 8 6 8 3 0 0 0 0 0 0
8 8 8 8 8 3 3 3 3 3 8 8 8 8 8 8
```
Match: False
Pixels Off: 76
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 86.36363636363636
