
Previous Code:
```python
import copy
import collections

"""
Identifies connected components (shapes) of identical non-zero digits using 8-way adjacency.
Finds all "interior zeros" - zero cells that cannot reach the grid boundary via a path of orthogonally connected zeros.
For each interior zero, determines its enclosing shape by checking orthogonal non-zero neighbors.
Based on the enclosing shape's color (C) and the colors of other shapes in the grid, a fill color (F) is determined:
- C=3 -> F=3
- C=7 -> F=7
- C=8 -> F=1
- C=2 -> F=7
- C=4 -> Depends on the minimum border color (min_obd) of *other* shapes:
    - If min_obd=5 -> F=5
    - If min_obd=3 -> F=6
    - Otherwise -> F=None (no fill)
- Other C (e.g., 5) -> F=None (no fill)
The identified interior zero cells are then filled with the determined fill color F (if F is not None) in the output grid. Cells that are not interior zeros remain unchanged.
"""

def _find_shapes(grid: list[list[int]]) -> tuple[list[dict], dict[tuple[int, int], dict]]:
    """
    Finds all connected components of identical non-zero digits (8-way adjacency).

    Args:
        grid: The input grid.

    Returns:
        A tuple containing:
        - A list of dictionaries, where each dictionary represents a shape
          and contains 'color' (the digit) and 'cells' (a set of (row, col) tuples).
        - A dictionary mapping each cell (r, c) belonging to a shape to its shape object.
    """
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    shapes = []
    cell_to_shape_map = {}

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != 0 and (r, c) not in visited:
                color = grid[r][c]
                shape_cells = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                shape_cells.add((r, c))

                while q:
                    row, col = q.popleft()
                    # Check 8-way neighbors (orthogonal and diagonal)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               (nr, nc) not in visited and grid[nr][nc] == color:
                                visited.add((nr, nc))
                                shape_cells.add((nr, nc))
                                q.append((nr, nc))
                
                current_shape = {'color': color, 'cells': shape_cells}
                shapes.append(current_shape)
                for cell in shape_cells:
                    cell_to_shape_map[cell] = current_shape
                    
    return shapes, cell_to_shape_map

def _find_all_interior_zeros(grid: list[list[int]]) -> set[tuple[int, int]]:
    """
    Finds all zero cells that cannot reach the grid boundary via orthogonal paths of zeros.

    Args:
        grid: The input grid.

    Returns:
        A set of (row, col) tuples representing the interior zero cells.
    """
    rows = len(grid)
    cols = len(grid[0])
    if rows == 0 or cols == 0:
        return set()

    boundary_reachable_zeros = set()
    q = collections.deque()

    # Initialize queue with all boundary zeros
    for r in range(rows):
        for c in [0, cols - 1]:
            if grid[r][c] == 0 and (r, c) not in boundary_reachable_zeros:
                boundary_reachable_zeros.add((r, c))
                q.append((r, c))
    for c in range(cols): # Use range(cols) instead of range(1, cols-1) to include corners
        for r in [0, rows - 1]:
             if grid[r][c] == 0 and (r, c) not in boundary_reachable_zeros:
                boundary_reachable_zeros.add((r, c))
                q.append((r, c))

    # BFS from boundary zeros (orthogonal steps only)
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr][nc] == 0 and (nr, nc) not in boundary_reachable_zeros:
                boundary_reachable_zeros.add((nr, nc))
                q.append((nr, nc))

    # Identify all zeros and subtract the reachable ones
    all_zeros = set()
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                all_zeros.add((r, c))

    interior_zeros = all_zeros - boundary_reachable_zeros
    return interior_zeros

def _determine_fill_color(enclosing_shape: dict, all_shapes: list[dict]) -> int | None:
    """
    Determines the fill color based on the enclosing shape's color and other shapes present.

    Args:
        enclosing_shape: The shape dictionary enclosing the current interior zero.
        all_shapes: A list of all shape dictionaries found in the grid.

    Returns:
        The fill color (int) or None if no fill should occur.
    """
    shape_color = enclosing_shape['color']
    current_shape_cells = enclosing_shape['cells'] # Use cell set for comparison

    if shape_color == 3:
        return 3
    if shape_color == 7:
        return 7
    if shape_color == 8:
        return 1
    if shape_color == 2:
        return 7
    if shape_color == 4:
        other_border_colors = set()
        for shape in all_shapes:
            # Compare by cell sets to ensure distinct shapes are considered
            if shape['cells'] != current_shape_cells: 
                 other_border_colors.add(shape['color'])

        if not other_border_colors:
            return None # No other shapes

        min_obd = min(other_border_colors)
        if min_obd == 5:
            return 5
        if min_obd == 3:
            return 6
        else:
            return None # Min other border color is not 5 or 3
    # Default case (includes C=5 and any other unspecified colors)
    return None


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by filling interior zeros based on enclosing shape rules.
    """
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []
        
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)

    # 1. Identify all shapes and create a map from cell coords to shape objects
    all_shapes, cell_to_shape_map = _find_shapes(input_grid)
    if not all_shapes: # No non-zero shapes, nothing to fill
        return output_grid

    # 2. Identify all interior zeros using boundary flood fill
    all_interior_zeros = _find_all_interior_zeros(input_grid)
    if not all_interior_zeros: # No interior zeros, nothing to fill
        return output_grid
        
    # 3. Iterate through interior zeros, determine fill color, and apply fill
    for rz, cz in all_interior_zeros:
        enclosing_shape = None
        # 3a. Find the enclosing shape by checking orthogonal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = rz + dr, cz + dc
            if 0 <= nr < rows and 0 <= nc < cols and input_grid[nr][nc] != 0:
                # Found a non-zero neighbor, get its shape
                if (nr, nc) in cell_to_shape_map:
                    enclosing_shape = cell_to_shape_map[(nr, nc)]
                    break # Assume the first non-zero neighbor defines the enclosure context
        
        # If no non-zero neighbor found (shouldn't happen for interior zero definition)
        # or if the neighbor isn't mapped (error in shape finding), skip.
        if not enclosing_shape:
            continue 
            
        # 3b. Determine the fill color based on the enclosing shape and context
        fill_color = _determine_fill_color(enclosing_shape, all_shapes)

        # 3c. Apply the fill color to the output grid if determined
        if fill_color is not None:
            # Check if the cell is still 0 in the output grid (safety)
            if output_grid[rz][cz] == 0:
                output_grid[rz][cz] = fill_color

    # 4. Return the modified grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 4 4 4 4 4 0 3 4 6 9 5
0 4 0 4 0 4 0 3 6 7 2 9
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 0 0 3 0 0 0 0 0 0 0
0 3 0 0 3 0 0 7 7 7 7 0
0 3 0 0 3 0 0 7 0 7 7 0
0 0 3 0 3 0 0 7 0 0 7 0
0 0 0 3 0 0 0 7 7 0 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 4 4 4 4 4 0 3 4 6 9 5
0 4 6 4 6 4 0 3 6 7 2 9
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 7 7 7 7 0
0 3 3 3 3 0 0 7 0 7 7 0
0 0 3 3 3 0 0 7 0 0 7 0
0 0 0 3 0 0 0 7 7 0 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 4 4 4 4 4 0 3 4 6 9 5
0 4 0 4 0 4 0 3 6 7 2 9
0 4 4 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 0 0 0 0 0
0 3 3 3 3 0 0 7 7 7 7 0
0 3 3 3 3 0 0 7 7 7 7 0
0 0 3 3 3 0 0 7 7 7 7 0
0 0 0 3 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 8.333333333333314

## Example 2:
Input:
```
2 6 0 0 8 8 8 8 0 0
4 5 0 0 8 0 0 8 0 0
6 8 0 0 8 0 0 8 0 0
8 1 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 4 4 4
0 5 0 0 0 5 0 4 0 4
0 0 5 5 5 5 0 4 4 4
0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 4 4 4
```
Expected Output:
```
2 6 0 0 8 8 8 8 0 0
4 5 0 0 8 1 1 8 0 0
6 8 0 0 8 1 1 8 0 0
8 1 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 4 4 4
0 5 0 0 0 5 0 4 5 4
0 0 5 5 5 5 0 4 4 4
0 0 0 0 0 0 0 4 5 4
0 0 0 0 0 0 0 4 4 4
```
Transformed Output:
```
2 6 0 0 8 8 8 8 0 0
4 5 0 0 8 1 1 8 0 0
6 8 0 0 8 1 1 8 0 0
8 1 0 0 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
0 5 5 5 5 5 0 4 4 4
0 5 0 0 0 5 0 4 0 4
0 0 5 5 5 5 0 4 4 4
0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 4 4 4
```
Match: False
Pixels Off: 2
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 4.0

## Example 3:
Input:
```
0 2 6 0 4 4 4 4 4 0 2 2 2 2 0
0 7 1 0 4 0 0 0 4 0 2 0 2 2 0
0 0 0 0 4 0 0 0 4 0 2 2 0 2 0
0 0 0 0 4 4 4 4 4 0 2 2 2 2 0
```
Expected Output:
```
0 2 6 0 4 4 4 4 4 0 2 2 2 2 0
0 7 1 0 4 0 0 0 4 0 2 7 2 2 0
0 0 0 0 4 0 0 0 4 0 2 2 7 2 0
0 0 0 0 4 4 4 4 4 0 2 2 2 2 0
```
Transformed Output:
```
0 2 6 0 4 4 4 4 4 0 2 2 2 2 0
0 7 1 0 4 0 0 0 4 0 2 7 2 2 0
0 0 0 0 4 0 0 0 4 0 2 2 7 2 0
0 0 0 0 4 4 4 4 4 0 2 2 2 2 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
