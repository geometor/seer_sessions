
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 5 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 5 5 5 5 5 0 0
```


**output:**
```
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 5 5 5 8 5 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 5 5 5 5 5 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 5 5 5 0 5 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 8 8 8 8 5 0 0
0 0 5 5 5 8 5 5 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

**Perception of Elements:**

1.  **Grid Structure**: The input and output are both 10x10 grids containing numerical values.
2.  **Colors/Numbers**:
    *   `0`: Appears to be the background color.
    *   `5`: Represents the pixels forming a distinct shape in the input. This shape remains unchanged in the output.
    *   `8`: Appears only in the output. It's used to fill an area enclosed by the shape (5) and to draw a vertical line extending from that shape.
3.  **Shape**: The pixels with value 5 form a single, connected, closed shape in both examples. The shape resembles a 'U' or 'C' with a horizontal bar that has a single-pixel gap.
4.  **Transformation - Filling**: The primary transformation involves filling the area enclosed by the shape (5). The background pixels (0) inside the shape are changed to 8.
5.  **Transformation - Vertical Line**: An additional vertical line of 8s is drawn in column 5 (0-indexed). This line extends from the row containing the horizontal bar of the shape (specifically, the row with the gap) towards the nearest grid edge (top or bottom), away from the main body of the filled shape.

**YAML Facts:**


```yaml
task_description: Fill the interior of a shape defined by color 5 with color 8, and draw a vertical line (color 8) in column 5 extending from the shape's horizontal bar away from the filled interior towards the nearest grid edge.

elements:
  - object: Grid
    properties:
      - size: 10x10
      - type: 2D array of integers
  - object: Background
    properties:
      - color_value: 0
  - object: ShapeBoundary
    properties:
      - color_value: 5
      - role: Defines the boundary of a region
      - structure: Forms a single connected, closed component with a horizontal bar containing a single pixel gap.
  - object: Fill
    properties:
      - color_value: 8
      - role: Fills the interior region enclosed by ShapeBoundary
  - object: VerticalLine
    properties:
      - color_value: 8
      - column_index: 5
      - role: Extends vertically from the ShapeBoundary's horizontal bar

actions:
  - action: IdentifyShapeInterior
    description: Find the connected region of Background pixels enclosed by ShapeBoundary pixels.
  - action: FloodFill
    input: Grid, InteriorRegionStartPoint, FillColor (8)
    output: Modified Grid with InteriorRegion filled
    description: Change the color value of pixels within the identified interior region to the FillColor.
  - action: IdentifyHorizontalBar
    input: Grid, ShapeBoundaryColor (5)
    output: RowIndexOfBar
    description: Find the row index containing the horizontal segment of the ShapeBoundary with a gap.
  - action: DrawVerticalLine
    input: Grid, ColumnIndex (5), StartRow, EndRow, LineColor (8)
    output: Modified Grid with vertical line
    description: Change the color value of pixels in the specified column between StartRow and EndRow (inclusive) to LineColor.

relationships:
  - type: Enclosure
    subject: ShapeBoundary (5)
    object: InteriorRegion (0 changing to 8)
    description: The ShapeBoundary surrounds the InteriorRegion.
  - type: Extension
    subject: VerticalLine (8)
    object: ShapeBoundary (5)
    description: The VerticalLine starts at the row of the ShapeBoundary's horizontal bar (with the gap) in column 5 and extends away from the filled interior towards the nearest vertical edge of the grid.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all pixels with the background color `0` that are enclosed within the shape formed by pixels with color `5`. (This can be done using a flood fill algorithm starting from a known interior point, or by iterating through pixels and checking for enclosure).
3.  Change the color of these enclosed background pixels from `0` to `8` in the output grid.
4.  Locate the row index (`bar_row`) containing the horizontal segment of the shape `5` which has a single-pixel gap (e.g., `5 5 5 0 5 5`).
5.  Determine the minimum (`min_fill_row`) and maximum (`max_fill_row`) row indices of the area filled with `8` in step 3.
6.  If the `bar_row` is above the filled area (`bar_row < min_fill_row`), then draw a vertical line of `8`s in column 5 from `bar_row` up to row 0 (inclusive).
7.  If the `bar_row` is below the filled area (`bar_row > max_fill_row`), then draw a vertical line of `8`s in column 5 from `bar_row` down to the last row of the grid (row 9, inclusive).
8.  Return the modified output grid.
```python
import copy
from collections import deque
import numpy as np

"""
This program transforms a 10x10 grid based on the following rules:
1. It identifies a shape outlined by the number 5 on a background of 0.
2. It fills the interior region enclosed by the shape (5) with the number 8. The interior region consists of pixels initially having the value 0.
3. It identifies a horizontal segment of the shape (5) that contains a single-pixel gap (a 0 surrounded by 5s horizontally) located specifically in column 5.
4. It draws a vertical line using the number 8 in column 5. This line extends from the row containing the gap towards the nearest top or bottom edge of the grid, stopping at the edge. The direction of extension (up or down) is away from the main body of the filled area.
"""

def find_gap_row(grid: np.ndarray, shape_color: int, background_color: int, gap_col: int) -> int | None:
    """
    Finds the row index containing the specific gap pattern (shape_color, background_color, shape_color)
    horizontally centered at gap_col.
    """
    height, width = grid.shape
    for r in range(height):
        # Check if gap_col is valid and potentially has neighbors
        if 0 < gap_col < width - 1:
            # Check the specific pattern: shape_color, background_color at gap_col, shape_color
            if (grid[r, gap_col] == background_color and
                    grid[r, gap_col - 1] == shape_color and
                    grid[r, gap_col + 1] == shape_color):
                return r
    return None # Return None if no such row is found


def flood_fill(grid: np.ndarray, start_row: int, start_col: int, fill_color: int, target_color: int, boundary_color: int):
    """
    Performs flood fill starting from (start_row, start_col).
    Fills target_color with fill_color, stopping at boundary_color or grid edges.
    Modifies the grid in place.
    """
    height, width = grid.shape
    if not (0 <= start_row < height and 0 <= start_col < width):
        print(f"Warning: Start point ({start_row}, {start_col}) out of bounds.")
        return
    if grid[start_row, start_col] != target_color:
        # print(f"Warning: Start point ({start_row}, {start_col}) is not the target color {target_color}. Found {grid[start_row, start_col]}. Fill not started.")
        # Try adjacent cells to the original intended start point if the heuristic failed slightly
        potential_starts = []
        for dr, dc in [(0,1), (0,-1), (1,0), (-1,0)]:
             nr, nc = start_row + dr, start_col + dc
             if 0 <= nr < height and 0 <= nc < width and grid[nr, nc] == target_color:
                 potential_starts.append((nr, nc))
        if not potential_starts:
             print(f"Warning: Start point ({start_row}, {start_col}) and its neighbours are not the target color {target_color}. Fill not started.")
             return
        start_row, start_col = potential_starts[0] # Use the first valid neighbour


    q = deque([(start_row, start_col)])
    visited = set([(start_row, start_col)])
    grid[start_row, start_col] = fill_color

    while q:
        r, c = q.popleft()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if not (0 <= nr < height and 0 <= nc < width):
                continue

            # Check if already visited
            if (nr, nc) in visited:
                continue

            # Check if it's the target color (and not boundary)
            if grid[nr, nc] == target_color:
                visited.add((nr, nc))
                grid[nr, nc] = fill_color
                q.append((nr, nc))
            elif grid[nr,nc] != boundary_color: # Treat anything else other than boundary as visited to prevent issues near fill start
                 visited.add((nr, nc))


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by filling the interior of a shape (5) with 8
    and drawing a vertical line (8) from a gap in the shape towards the nearest edge.
    """
    # Convert to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape

    shape_color = 5
    background_color = 0
    fill_color = 8
    gap_col = 5 # The column where the gap is expected

    # 1. Find the row with the gap
    gap_row = find_gap_row(output_grid, shape_color, background_color, gap_col)

    if gap_row is None:
        print("Warning: Gap row not found. Cannot proceed with filling or line drawing.")
        return output_grid.tolist() # Return copy of original if pattern not found

    # 2. Find a starting point for flood fill (heuristically determined)
    # Assume the interior is connected vertically across the gap row.
    # Try one row below the gap first, in the gap column.
    start_row_fill = gap_row + 1
    start_col_fill = gap_col
    if not (0 <= start_row_fill < height and output_grid[start_row_fill, start_col_fill] == background_color):
        # If below doesn't work (e.g., gap is at bottom of shape), try above.
        start_row_fill = gap_row - 1
        if not (0 <= start_row_fill < height and output_grid[start_row_fill, start_col_fill] == background_color):
             # If neither above nor below works directly at gap column, try adjacent columns
             if 0 <= gap_row + 1 < height and output_grid[gap_row+1, gap_col-1] == background_color:
                 start_row_fill = gap_row + 1
                 start_col_fill = gap_col - 1
             elif 0 <= gap_row + 1 < height and output_grid[gap_row+1, gap_col+1] == background_color:
                 start_row_fill = gap_row + 1
                 start_col_fill = gap_col + 1
             elif 0 <= gap_row - 1 < height and output_grid[gap_row-1, gap_col-1] == background_color:
                 start_row_fill = gap_row - 1
                 start_col_fill = gap_col - 1
             elif 0 <= gap_row - 1 < height and output_grid[gap_row-1, gap_col+1] == background_color:
                 start_row_fill = gap_row - 1
                 start_col_fill = gap_col + 1
             else:
                 print(f"Warning: Could not find a suitable start point for flood fill near gap at ({gap_row}, {gap_col}).")
                 # Attempt to find *any* background cell adjacent to a shape cell as a last resort
                 found_start = False
                 for r in range(height):
                     for c in range(width):
                         if output_grid[r,c] == background_color:
                             is_neighbor_shape = False
                             for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                                 nr, nc = r + dr, c + dc
                                 if 0 <= nr < height and 0 <= nc < width and output_grid[nr, nc] == shape_color:
                                     is_neighbor_shape = True
                                     break
                             if is_neighbor_shape:
                                 # Found a potential start, but need to ensure it's INSIDE
                                 # This simple check isn't guaranteed to be inside.
                                 # A more robust method would be needed, perhaps ray casting
                                 # For this specific problem structure, the heuristic near the gap is preferred.
                                 # If the heuristic fails, it suggests an unexpected shape variation.
                                 pass # Cannot reliably find start point if heuristic fails

                 # If still no start point found by heuristic, filling might fail or be incorrect.
                 # The original heuristic is likely sufficient for the given examples.


    # 3. Perform flood fill for the interior
    flood_fill(output_grid, start_row_fill, start_col_fill, fill_color, background_color, shape_color)

    # 4. Find the vertical extent of the filled area
    filled_rows = np.where(np.any(output_grid == fill_color, axis=1))[0]
    if len(filled_rows) == 0:
         # Fill might not have happened if start point wasn't found or was wrong
         # Find min/max rows based on the shape itself as a fallback
         shape_rows = np.where(np.any(output_grid == shape_color, axis=1))[0]
         if len(shape_rows) > 0:
             min_fill_row = np.min(shape_rows)
             max_fill_row = np.max(shape_rows)
             print("Warning: Fill color not found after flood fill attempt. Using shape bounds for line drawing logic.")
         else:
              min_fill_row = gap_row # Fallback to gap_row itself
              max_fill_row = gap_row
              print("Warning: Fill color and shape color not found. Line drawing fallback may be inaccurate.")

    else:
        min_fill_row = np.min(filled_rows)
        max_fill_row = np.max(filled_rows)


    # 5. Draw the vertical line
    # Determine direction: extend away from the main filled area
    if gap_row < min_fill_row : # Gap is above the filled area, draw line upwards
        for r in range(0, gap_row + 1): # Include the gap row itself
             if 0 <= r < height and 0 <= gap_col < width: # Boundary check for safety
                # Only draw if the cell isn't part of the original shape boundary
                if grid[r, gap_col] != shape_color:
                    output_grid[r, gap_col] = fill_color
    elif gap_row > max_fill_row: # Gap is below the filled area, draw line downwards
        for r in range(gap_row, height): # Include the gap row itself
             if 0 <= r < height and 0 <= gap_col < width: # Boundary check for safety
                 # Only draw if the cell isn't part of the original shape boundary
                 if grid[r, gap_col] != shape_color:
                     output_grid[r, gap_col] = fill_color
    # else: # Gap row is within the filled area bounds, line might only appear at the gap row itself if it was 0 initially
         # Check if the gap position itself should be filled (it was background_color initially)
    if grid[gap_row, gap_col] == background_color:
         output_grid[gap_row, gap_col] = fill_color


    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```
```python
import numpy as np
from collections import deque

"""
Transforms a 10x10 grid by:
1. Identifying a shape outlined by color 5 on a background of color 0.
2. Finding a specific gap (0 surrounded horizontally by 5s) in column 5 within this shape.
3. Flood-filling the interior region enclosed by the shape (5) starting from a point adjacent to the gap, changing background pixels (0) to fill color (8). The shape boundary (5) is respected and not crossed.
4. Determining the vertical extent (min/max rows) of the filled area.
5. Drawing a vertical line using fill color (8) in column 5. This line extends from the gap row towards the nearest grid edge (top or bottom), directed away from the main body of the filled area. The line does not overwrite the shape boundary pixels (5).
"""

def find_gap_row(grid: np.ndarray, shape_color: int, background_color: int, gap_col: int) -> int | None:
    """
    Finds the row index containing the specific gap pattern (shape_color, background_color, shape_color)
    horizontally centered at gap_col.

    Args:
        grid: The numpy array representing the grid.
        shape_color: The color value of the shape boundary.
        background_color: The color value of the background/gap.
        gap_col: The specific column index to check for the gap pattern.

    Returns:
        The row index of the gap, or None if not found.
    """
    height, width = grid.shape
    for r in range(height):
        # Check if gap_col is within bounds to have neighbors
        if 0 < gap_col < width - 1:
            # Check the specific pattern: shape_color, background_color at gap_col, shape_color
            if (grid[r, gap_col] == background_color and
                    grid[r, gap_col - 1] == shape_color and
                    grid[r, gap_col + 1] == shape_color):
                return r
    return None # Return None if no such row is found


def find_interior_seed_point(grid: np.ndarray, gap_row: int, gap_col: int, background_color: int) -> tuple[int, int] | None:
    """
    Finds a suitable background_color seed point adjacent to the gap, likely inside the shape.

    Args:
        grid: The numpy array representing the grid.
        gap_row: The row index of the identified gap.
        gap_col: The column index of the identified gap.
        background_color: The color value to look for (the fill target).

    Returns:
        A tuple (row, col) of a seed point, or None if no suitable point is found nearby.
    """
    height, width = grid.shape
    potential_seeds = []
    # Prioritize vertical neighbors first
    if gap_row + 1 < height and grid[gap_row + 1, gap_col] == background_color:
        potential_seeds.append((gap_row + 1, gap_col))
    if gap_row - 1 >= 0 and grid[gap_row - 1, gap_col] == background_color:
        potential_seeds.append((gap_row - 1, gap_col))

    # If vertical neighbors aren't suitable, check diagonals or horizontals (less common for these shapes)
    if not potential_seeds:
         # Try adjacent columns in the rows next to the gap row
         for dr in [-1, 1]:
             nr = gap_row + dr
             if 0 <= nr < height:
                 for dc in [-1, 1]:
                     nc = gap_col + dc
                     if 0 <= nc < width and grid[nr, nc] == background_color:
                         potential_seeds.append((nr, nc))

    return potential_seeds[0] if potential_seeds else None


def flood_fill_interior(grid: np.ndarray, start_row: int, start_col: int, fill_color: int, target_color: int, boundary_color: int):
    """
    Performs flood fill starting from (start_row, start_col) on the grid.
    Fills target_color with fill_color, stopping at boundary_color or grid edges.
    Modifies the grid in place. Ensures it doesn't leak outside the boundary.

    Args:
        grid: The numpy array representing the grid (will be modified).
        start_row: The row index of the seed point.
        start_col: The column index of the seed point.
        fill_color: The color to fill with.
        target_color: The color to be replaced.
        boundary_color: The color that acts as a barrier.
    """
    height, width = grid.shape
    # Check if start point is valid and is the target color
    if not (0 <= start_row < height and 0 <= start_col < width and grid[start_row, start_col] == target_color):
        # print(f"Warning: Flood fill start point ({start_row}, {start_col}) is invalid or not target color {target_color}. Found {grid[start_row, start_col]}.")
        return # Do nothing if the start point isn't correct

    q = deque([(start_row, start_col)])
    visited = set([(start_row, start_col)]) # Keep track to avoid cycles and redundant checks
    grid[start_row, start_col] = fill_color # Fill the starting point

    while q:
        r, c = q.popleft()

        # Explore neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if not (0 <= nr < height and 0 <= nc < width):
                continue

            # Check if already visited
            if (nr, nc) in visited:
                continue

            # Add to visited regardless of color initially to prevent re-queuing
            visited.add((nr, nc))

            # Check if it's the target color (and not boundary)
            if grid[nr, nc] == target_color:
                grid[nr, nc] = fill_color
                q.append((nr, nc))
            # Note: We only add target_color cells to the queue. boundary_color or fill_color cells
            # are implicitly acting as boundaries for this fill instance.

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the rules: find gap, flood fill interior, draw vertical line.
    """
    # initialize output_grid
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape

    # Define constants
    shape_color = 5
    background_color = 0
    fill_color = 8
    gap_col = 5 # The specific column where the gap is expected

    # --- Step 1: Find the Gap ---
    gap_row = find_gap_row(output_grid, shape_color, background_color, gap_col)

    if gap_row is None:
        # print("Warning: Gap row not found. Returning original grid.")
        return output_grid.tolist() # Return copy of original if pattern not found

    # --- Step 2: Find Interior Seed Point ---
    seed_point = find_interior_seed_point(output_grid, gap_row, gap_col, background_color)

    if seed_point is None:
        # print(f"Warning: Could not find a suitable seed point near gap at ({gap_row}, {gap_col}). Returning grid without fill.")
         # Still attempt to draw the line based on shape bounds if fill fails
         pass # Continue to line drawing logic, fill step will be skipped essentially
    else:
        # --- Step 3: Flood Fill Interior ---
        seed_row, seed_col = seed_point
        flood_fill_interior(output_grid, seed_row, seed_col, fill_color, background_color, shape_color)

    # --- Step 4: Determine Filled Region Bounds ---
    filled_rows_indices = np.where(np.any(output_grid == fill_color, axis=1))[0]
    shape_rows_indices = np.where(np.any(output_grid == shape_color, axis=1))[0]

    if len(filled_rows_indices) > 0:
        min_fill_row = np.min(filled_rows_indices)
        max_fill_row = np.max(filled_rows_indices)
    elif len(shape_rows_indices) > 0: # Fallback if fill failed or area was empty
        # print("Warning: Fill color not found. Using shape bounds for line drawing logic.")
        min_fill_row = np.min(shape_rows_indices)
        max_fill_row = np.max(shape_rows_indices)
         # Make sure gap_row itself doesn't trigger weird bounds if it's outside the main shape part
        if gap_row < min_fill_row: max_fill_row = max(max_fill_row, gap_row)
        if gap_row > max_fill_row: min_fill_row = min(min_fill_row, gap_row)

    else:
        # print("Warning: Fill color and shape color not found. Line drawing may be inaccurate.")
        # Cannot reliably determine direction, maybe just fill the gap pixel if it exists
        min_fill_row = gap_row
        max_fill_row = gap_row

    # --- Step 5: Draw Vertical Line ---
    # Determine direction: extend away from the main filled/shape area relative to the gap row
    if gap_row < min_fill_row: # Gap is above the filled/shape area, draw line upwards
        # Iterate from grid top edge (row 0) up to and including the gap row
        for r in range(0, gap_row + 1):
            if 0 <= r < height: # Redundant check, loop ensures this, but safe
                # Only draw if the cell isn't part of the original shape boundary
                # Check original grid state for shape boundary
                if grid[r, gap_col] != shape_color:
                    output_grid[r, gap_col] = fill_color
    elif gap_row > max_fill_row: # Gap is below the filled/shape area, draw line downwards
        # Iterate from the gap row down to the grid bottom edge
        for r in range(gap_row, height):
            if 0 <= r < height: # Redundant check
                 # Only draw if the cell isn't part of the original shape boundary
                 # Check original grid state for shape boundary
                if grid[r, gap_col] != shape_color:
                    output_grid[r, gap_col] = fill_color
    else: # Gap row is within or adjacent to the filled/shape area bounds
        # The fill should handle the gap pixel itself if it was background
        # Check if the gap position itself was originally background and should be fill_color
        if grid[gap_row, gap_col] == background_color:
             output_grid[gap_row, gap_col] = fill_color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```
