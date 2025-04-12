```python
import copy
from collections import deque

"""
Transforms a 2D grid based on the presence or absence of a specific horizontal 
pattern `(0, 6+, 0)` (a 0, followed by one or more 6s, followed by a 0) 
within any row of the input grid. The grid also contains a background value (6) 
and a single vertical marker line (5).

Transformation Rules:

Case 1: Pattern (0, 6+, 0) is Present
    - All 0s in the input grid are shifted one column to the right in the output grid.
    - The original locations of the input 0s are filled with the background value 6.
    - For every row in the *input* grid that contained the (0, 6+, 0) pattern, 
      the corresponding row in the *output* grid has cells filled with 2s, 
      starting from the column immediately to the right of the marker line (5) 
      and extending to the right edge of the grid.

Case 2: Pattern (0, 6+, 0) is Absent
    - All 0s in the input grid are replaced by the background value 6.
    - The input grid is expected to contain exactly two distinct contiguous shapes 
      formed by 0s.
    - The bounding boxes of these two input shapes are determined.
    - A single rectangular area is filled with 2s in the output grid. The 
      coordinates of this rectangle are derived from a combination of the 
      min/max row/col indices of the two input shapes' bounding boxes:
        - top_row = shape1.min_col
        - bottom_row = shape1.max_row
        - left_col = shape2.min_row + 1
        - right_col = shape2.max_row + 1
      (Where shape1 is the shape with the smaller min_row index).

The marker line (5) is always preserved in its original position.
"""

def find_marker_col(grid: list[list[int]], marker_value: int) -> int:
    """Finds the column index of the first occurrence of the marker value."""
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == marker_value:
                return c
    return -1 # Should not happen based on problem description

def pattern_06plus0(row: list[int]) -> bool:
    """Checks if a row contains the pattern (0, 6+, 0)."""
    n = len(row)
    for i in range(n):
        if row[i] == 0:
            for j in range(i + 2, n): # Need at least one 6 in between
                if row[j] == 0:
                    # Check if all elements between i and j are 6
                    all_sixes = True
                    for k in range(i + 1, j):
                        if row[k] != 6:
                            all_sixes = False
                            break
                    if all_sixes:
                        return True
            # Optimization: if we found a 0 at i, we don't need to re-check
            # pairs starting before the next 0 found after the inner loop.
            # But simpler implementation is fine for typical grid sizes.
    return False

def check_pattern_in_grid(grid: list[list[int]]) -> bool:
    """Checks if the (0, 6+, 0) pattern exists in any row of the grid."""
    for row in grid:
        if pattern_06plus0(row):
            return True
    return False

def find_all_coords(grid: list[list[int]], value: int) -> list[tuple[int, int]]:
    """Finds coordinates of all cells with a specific value."""
    coords = []
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] == value:
                coords.append((r, c))
    return coords

def get_neighbors(r: int, c: int, height: int, width: int) -> list[tuple[int, int]]:
    """Gets valid 4-directional neighbors within grid bounds."""
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def find_shapes(grid: list[list[int]], value: int) -> list[set[tuple[int, int]]]:
    """Finds distinct contiguous shapes of a given value using BFS."""
    height = len(grid)
    width = len(grid[0])
    visited = set()
    shapes = []

    for r in range(height):
        for c in range(width):
            if grid[r][c] == value and (r, c) not in visited:
                # Start BFS for a new shape
                current_shape = set()
                q = deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    curr_r, curr_c = q.popleft()
                    current_shape.add((curr_r, curr_c))
                    
                    for nr, nc in get_neighbors(curr_r, curr_c, height, width):
                        if grid[nr][nc] == value and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                
                if current_shape:
                    shapes.append(current_shape)
                    
    return shapes

def get_bounding_box(shape_coords: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a shape."""
    if not shape_coords:
        return (-1, -1, -1, -1) # Or raise error
        
    min_r = min(r for r, c in shape_coords)
    min_c = min(c for r, c in shape_coords)
    max_r = max(r for r, c in shape_coords)
    max_c = max(c for r, c in shape_coords)
    return min_r, min_c, max_r, max_c

# --------------------------------------------------------------------------

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules based on the (0, 6+, 0) pattern.
    """
    height = len(input_grid)
    width = len(input_grid[0])
    
    # --- Initialization and Analysis ---
    output_grid = copy.deepcopy(input_grid)
    marker_col = find_marker_col(input_grid, 5)
    pattern_found = check_pattern_in_grid(input_grid)
    zero_coords = find_all_coords(input_grid, 0)
    
    # --- Case 1: Pattern (0, 6+, 0) Found ---
    if pattern_found:
        # Step 1: Replace original 0s with 6s
        for r, c in zero_coords:
            if 0 <= r < height and 0 <= c < width:
                 output_grid[r][c] = 6
                 
        # Step 2: Place 0s shifted one column to the right
        for r, c in zero_coords:
            if 0 <= r < height and c + 1 < width: # Check bounds for shift
                 output_grid[r][c + 1] = 0
                 
        # Step 3: Draw horizontal lines of 2s for rows containing the pattern
        for r_in in range(height):
            if pattern_06plus0(input_grid[r_in]): # Check original input row
                for c_out in range(marker_col + 1, width):
                     if 0 <= r_in < height and 0 <= c_out < width: # Bounds check
                         output_grid[r_in][c_out] = 2
                         
    # --- Case 2: Pattern (0, 6+, 0) Not Found ---
    else:
        # Step 1: Replace all 0s with 6s
        for r, c in zero_coords:
             if 0 <= r < height and 0 <= c < width:
                 output_grid[r][c] = 6
                 
        # Step 2: Find the two shapes of 0s in the *original* input
        # Use the pre-calculated zero_coords to potentially speed up find_shapes,
        # but using the standard find_shapes on the input grid is more robust.
        shapes = find_shapes(input_grid, 0)
        
        # Assuming exactly two shapes exist if pattern is not found
        if len(shapes) == 2:
            # Step 3: Calculate bounding boxes
            bboxes = [get_bounding_box(s) for s in shapes]
            
            # Step 4: Sort shapes by min_row to identify Shape 1 and Shape 2
            # Shape 1 has the smaller min_row
            if bboxes[0][0] <= bboxes[1][0]:
                bbox1 = bboxes[0] # r1_min, c1_min, r1_max, c1_max
                bbox2 = bboxes[1] # r2_min, c2_min, r2_max, c2_max
            else:
                bbox1 = bboxes[1]
                bbox2 = bboxes[0]
                
            # Step 5: Calculate output rectangle coordinates
            r1_min, c1_min, r1_max, c1_max = bbox1
            r2_min, c2_min, r2_max, c2_max = bbox2
            
            top_row = c1_min
            bottom_row = r1_max
            left_col = r2_min + 1
            right_col = r2_max + 1
            
            # Step 6: Fill the output rectangle with 2s
            for r in range(top_row, bottom_row + 1):
                for c in range(left_col, right_col + 1):
                    if 0 <= r < height and 0 <= c < width: # Check bounds
                        output_grid[r][c] = 2
        # else: handle cases with not exactly 2 shapes if necessary
        # (e.g., return the grid with 0s replaced by 6s)

    return output_grid
```