
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

**Perception of Elements:**

The task involves transforming a grid containing a single gray (5) shape on a white (0) background. The gray shape acts as a boundary or container. The transformation involves two main parts:

1.  **Filling the Interior:** The area enclosed by the gray shape, which is initially white, is filled with azure (8) pixels. This suggests a flood-fill or region-filling operation starting from a point inside the shape's boundary.
2.  **Adding an Exterior Line:** A vertical line of azure (8) pixels is added outside the gray shape. This line appears to be aligned with a vertical gap or axis of symmetry in the gray shape. The direction of this line (upwards or downwards) seems dependent on the vertical position of the gray shape within the grid. If the shape is predominantly in the lower half, the line extends upwards from the top edge. If the shape is predominantly in the upper half, the line extends downwards from the bottom edge. The line extends all the way to the grid boundary.

**YAML Facts:**


```yaml
task_description: Fill the interior of a gray shape with azure and add a vertical azure line extending outwards from the shape's gap, directed away from the shape's vertical center.

elements:
  - element: background
    color: white (0)
    role: Canvas for the main object.
  - element: shape
    color: gray (5)
    properties:
      - Forms a single connected component.
      - Acts as a boundary, enclosing a region of the background.
      - Has a vertical gap or opening, typically on one side (right side in examples).
    role: Defines the area to be filled and the reference for the exterior line.
  - element: fill_color
    color: azure (8)
    role: Used to fill the interior region and create the exterior line.

relationships:
  - type: containment
    element1: shape (gray)
    element2: background (white)
    description: The gray shape encloses a region of the white background.
  - type: adjacency
    element1: fill_color (azure)
    element2: shape (gray)
    description: The azure fill touches the inner boundary of the gray shape. The azure line touches the outer boundary (top or bottom edge) of the gray shape.
  - type: spatial
    element1: shape (gray)
    element2: grid
    description: The vertical position of the shape within the grid determines the direction of the exterior azure line.

actions:
  - action: identify_shape
    input: grid
    output: The single connected gray (5) object.
  - action: identify_interior
    input: grid, shape
    output: The white (0) region enclosed by the shape.
  - action: fill_interior
    input: interior_region
    output: Change the color of the interior region to azure (8).
  - action: identify_gap_column
    input: shape
    output: The column index corresponding to the vertical gap/symmetry axis of the shape.
  - action: determine_vertical_position
    input: shape, grid
    output: Whether the shape is primarily in the upper or lower half of the grid.
  - action: determine_extension_edge_and_direction
    input: shape, vertical_position
    output: The starting row (top or bottom edge of the shape) and direction (up or down) for the exterior line.
  - action: draw_exterior_line
    input: grid, gap_column, start_row, direction
    output: Add a vertical azure (8) line in the gap column, starting from the determined edge and extending to the grid boundary in the specified direction.
```


**Natural Language Program:**

1.  Identify the single connected object composed of gray (5) pixels in the input grid.
2.  Identify the region of white (0) pixels that is completely enclosed by the gray object.
3.  Change the color of all pixels within this enclosed region to azure (8).
4.  Determine the column index (or indices) that corresponds to the vertical opening or axis of symmetry of the gray object (where the shape is discontinuous vertically, observed on the right side in the examples). Let this be the `gap_column`.
5.  Find the vertical midpoint or center of mass of the gray object.
6.  Compare the object's vertical midpoint to the grid's vertical midpoint.
7.  If the object's midpoint is in the lower half of the grid:
    *   Find the topmost row (`start_row`) of the gray object within the `gap_column`.
    *   Change the color of pixels in the `gap_column` from `start_row - 1` up to the top edge of the grid (row 0) to azure (8).
8.  If the object's midpoint is in the upper half of the grid (or exactly centered):
    *   Find the bottommost row (`start_row`) of the gray object within the `gap_column`.
    *   Change the color of pixels in the `gap_column` from `start_row + 1` down to the bottom edge of the grid to azure (8).
9.  Leave the original gray (5) object unchanged.
10. The resulting grid is the output.
```python
import numpy as np
from scipy.ndimage import binary_fill_holes
from typing import List, Tuple

"""
Transformation Rule:

1. Identify the single connected object composed of gray (5) pixels.
2. Fill the area enclosed by this gray object with azure (8) pixels.
3. Find the vertical "gap" column within the horizontal span of the gray object. This is the column with the minimum number of gray pixels.
4. Determine the vertical center of the gray object.
5. Compare the object's center to the grid's center to decide the direction of an exterior line (upwards if the object is lower, downwards if the object is upper or centered).
6. Draw a vertical line of azure (8) pixels in the identified "gap" column, starting from the edge of the gray object (top edge for upwards line, bottom edge for downwards line) and extending to the grid boundary.
"""

def find_gap_column(grid: np.ndarray, gray_coords: List[Tuple[int, int]]) -> int:
    """
    Finds the column index corresponding to the vertical gap or axis of symmetry.
    This is identified as the column within the shape's horizontal bounds
    that contains the minimum number of gray pixels.
    """
    if not gray_coords:
        return -1 # Should not happen with valid inputs

    min_c = min(c for r, c in gray_coords)
    max_c = max(c for r, c in gray_coords)

    min_gray_count = float('inf')
    gap_col = -1

    # Create a quick lookup for gray pixels
    gray_set = set(gray_coords)

    # Iterate through columns within the horizontal span
    for c in range(min_c, max_c + 1):
        count = 0
        # Count gray pixels specifically in this column
        # Need grid dimensions for this check
        height = grid.shape[0]
        for r in range(height):
             if (r,c) in gray_set:
                 count += 1

        # If this column has fewer gray pixels than the minimum found so far
        # Note: We need to ensure this column is *part* of the gap area,
        # not just an empty column between disconnected parts (if that were possible).
        # The minimum count approach inherently finds the narrowest part.
        # If count is 0, it's not part of the shape's span in a meaningful way for gap finding.
        if count > 0 and count < min_gray_count:
            min_gray_count = count
            gap_col = c
        # Handle ties: if a new column has the *same* minimum count,
        # the current logic keeps the first one found (lowest column index).
        # Based on examples, the gap seems unique.

    # If the minimum count is found at the absolute min/max column, re-evaluate.
    # Based on examples, the gap column is internal.
    # Let's refine: Iterate from min_c + 1 to max_c - 1?
    # Ex1: min_c=2, max_c=7. Range 2-7. Counts: c2=5, c3=2, c4=2, c5=1, c6=2, c7=5. Min count 1 at c=5. Correct.
    # Ex2: min_c=2, max_c=7. Range 2-7. Counts: c2=7, c3=2, c4=2, c5=2, c6=1, c7=7. Min count 1 at c=6. Correct.
    # The original range min_c to max_c works.

    if gap_col == -1 and min_c <= max_c: # Handle cases like single column shapes?
        gap_col = min_c # Default, though unlikely based on task structure

    return gap_col


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation: fills the interior of a gray 'C' shape
    and adds an exterior line aligned with the shape's gap.
    """
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape
    gray_color = 5
    fill_color = 8
    background_color = 0

    # 1. Identify gray pixels
    gray_coords = list(zip(*np.where(input_grid == gray_color)))
    if not gray_coords:
        return output_grid # No shape found

    # 2. Fill the enclosed area
    # Create a binary mask of the gray shape
    gray_mask = (input_grid == gray_color)
    # Use binary_fill_holes to fill the interior including the border
    filled_mask = binary_fill_holes(gray_mask)
    # Identify the interior pixels (filled area minus the original border)
    interior_mask = filled_mask & ~gray_mask
    # Fill the interior in the output grid
    output_grid[interior_mask] = fill_color

    # 3. Find the gap column
    gap_column = find_gap_column(input_grid, gray_coords)
    if gap_column == -1:
         print("Warning: Could not determine gap column.")
         return output_grid # Or handle error appropriately

    # 4. Determine vertical center of the gray object
    if not gray_coords: # Should be caught earlier, but safety check
         return output_grid
    shape_center_r = sum(r for r, c in gray_coords) / len(gray_coords)

    # 5. Compare shape center to grid center
    grid_center_r = (height - 1) / 2.0

    # 6. Determine line direction and start/end points
    gray_rows_in_gap_col = [r for r, c in gray_coords if c == gap_column]

    if not gray_rows_in_gap_col:
         # This might happen if the gap column calculation finds a column
         # that *only* contains interior points (count = 0), which shouldn't occur with current logic.
         # Or if the shape is weird. Add robustness.
         # Maybe the min count > 0 check in find_gap_column handles this.
         # If find_gap_column returned a valid column, it must have gray pixels.
         print(f"Warning: No gray pixels found in determined gap column {gap_column}.")
         return output_grid


    min_r_gap = min(gray_rows_in_gap_col)
    max_r_gap = max(gray_rows_in_gap_col)

    if shape_center_r > grid_center_r:
        # Shape is lower than center -> Draw line upwards
        # Start from the row above the topmost gray pixel in the gap column
        start_row = min_r_gap - 1
        end_row = -1 # Go up to row 0 (exclusive end for range)
        step = -1
    else:
        # Shape is upper or centered -> Draw line downwards
        # Start from the row below the bottommost gray pixel in the gap column
        start_row = max_r_gap + 1
        end_row = height # Go down to last row (exclusive end for range)
        step = 1

    # Draw the line
    for r in range(start_row, end_row, step):
        # Check bounds just in case, though range should handle it
        if 0 <= r < height:
            # Only draw if the pixel is currently background
            # The examples show the line overwriting background only.
            if output_grid[r, gap_column] == background_color:
                output_grid[r, gap_column] = fill_color

    return output_grid
```
```python
import numpy as np
from collections import deque
from typing import List, Tuple, Set

"""
Transformation Rule:

1. Identify the single connected object composed of gray (5) pixels.
2. Identify all background (0) pixels that are enclosed by the gray object (i.e., cannot reach the grid boundary by moving only through background pixels).
3. Fill this enclosed background area with azure (8) pixels.
4. Find the vertical "gap" column within the horizontal span of the gray object. This is the column with the minimum number of gray pixels within the object's bounding box columns.
5. Determine the vertical center of the gray object.
6. Compare the object's center to the grid's center to decide the direction of an exterior line (upwards if the object is lower, downwards if the object is upper or centered).
7. Draw a vertical line of azure (8) pixels in the identified "gap" column, starting from the edge of the gray object (top edge for upwards line, bottom edge for downwards line) and extending to the grid boundary, only overwriting background (0) pixels.
"""

def find_gap_column(grid: np.ndarray, gray_coords: List[Tuple[int, int]]) -> int:
    """
    Finds the column index corresponding to the vertical gap.
    Identified as the column within the shape's horizontal bounds
    that contains the minimum number of gray pixels.
    """
    if not gray_coords:
        return -1

    min_c = min(c for r, c in gray_coords)
    max_c = max(c for r, c in gray_coords)

    min_gray_count = float('inf')
    gap_col = -1

    gray_set = set(gray_coords)
    height = grid.shape[0]

    for c in range(min_c, max_c + 1):
        count = 0
        for r in range(height):
             if (r,c) in gray_set:
                 count += 1

        # Only consider columns that actually contain gray pixels
        if count > 0 and count < min_gray_count:
            min_gray_count = count
            gap_col = c
        # If counts are equal, keep the first one found (lowest index).

    if gap_col == -1 and min_c <= max_c: # Fallback for unusual shapes
         # If no column strictly within min/max had gray pixels or if shape is 1-col wide
         # Re-check the edges or pick the first column if single column shape
         min_edge_count = sum(1 for r in range(height) if (r, min_c) in gray_set)
         max_edge_count = sum(1 for r in range(height) if (r, max_c) in gray_set) if min_c != max_c else float('inf')

         if min_edge_count > 0 and min_edge_count <= max_edge_count:
              gap_col = min_c
         elif max_edge_count > 0 and max_edge_count < min_edge_count:
             gap_col = max_c
         elif min_edge_count > 0: # If only min_c has gray pixels
             gap_col = min_c
         else: # Should not happen if gray_coords is not empty
             pass # gap_col remains -1

    return gap_col

def find_enclosed_background(grid: np.ndarray) -> Set[Tuple[int, int]]:
    """
    Finds background (0) pixels enclosed by non-background pixels.
    Uses BFS starting from boundary background pixels.
    """
    height, width = grid.shape
    background_color = 0
    visited = set()
    queue = deque()

    # Add all background pixels on the border to the queue and visited set
    for r in range(height):
        for c in [0, width - 1]:
            if grid[r, c] == background_color and (r, c) not in visited:
                visited.add((r, c))
                queue.append((r, c))
    for c in range(1, width - 1): # Avoid double-adding corners
        for r in [0, height - 1]:
            if grid[r, c] == background_color and (r, c) not in visited:
                visited.add((r, c))
                queue.append((r, c))

    # Perform BFS to find all reachable background pixels from the border
    while queue:
        r, c = queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                if grid[nr, nc] == background_color and (nr, nc) not in visited:
                    visited.add((nr, nc))
                    queue.append((nr, nc))

    # Identify enclosed background pixels (those not visited)
    enclosed = set()
    for r in range(height):
        for c in range(width):
            if grid[r, c] == background_color and (r, c) not in visited:
                enclosed.add((r, c))

    return enclosed


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation: fills the enclosed interior of a gray shape
    and adds an exterior line aligned with the shape's gap.
    """
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape
    gray_color = 5
    fill_color = 8
    background_color = 0

    # 1. Identify gray pixels
    gray_coords = list(zip(*np.where(input_grid == gray_color)))
    if not gray_coords:
        return output_grid # No shape found

    # 2. Find enclosed background pixels using BFS from borders
    enclosed_pixels = find_enclosed_background(input_grid)

    # 3. Fill the enclosed area
    for r, c in enclosed_pixels:
        output_grid[r, c] = fill_color

    # 4. Find the gap column
    gap_column = find_gap_column(input_grid, gray_coords)
    if gap_column == -1:
         # print("Warning: Could not determine gap column.")
         return output_grid # Or handle error appropriately

    # 5. Determine vertical center of the gray object
    shape_center_r = sum(r for r, c in gray_coords) / len(gray_coords)

    # 6. Compare shape center to grid center
    grid_center_r = (height - 1) / 2.0

    # 7. Determine line direction and start/end points
    gray_rows_in_gap_col = sorted([r for r, c in gray_coords if c == gap_column])

    if not gray_rows_in_gap_col:
         # This case should be less likely now with the refined gap finding,
         # but handle defensively.
         # print(f"Warning: No gray pixels found in determined gap column {gap_column}.")
         return output_grid

    min_r_gap = gray_rows_in_gap_col[0]
    max_r_gap = gray_rows_in_gap_col[-1]

    # Decide direction: If shape center is strictly lower than grid center, line goes up.
    # Otherwise (higher or exactly centered), line goes down.
    if shape_center_r > grid_center_r:
        # Shape is lower -> Draw line upwards
        start_row = min_r_gap - 1
        end_row = -1 # Exclusive end for range going upwards
        step = -1
    else:
        # Shape is upper or centered -> Draw line downwards
        start_row = max_r_gap + 1
        end_row = height # Exclusive end for range going downwards
        step = 1

    # 8. Draw the line, only on background pixels
    for r in range(start_row, end_row, step):
        # Check bounds just in case
        if 0 <= r < height:
            # Only draw if the pixel is currently background
            # Check original input grid or current output grid?
            # The output grid might have filled pixels near the gap.
            # Examples show the line only replaces background. Let's use output_grid state before drawing.
            if output_grid[r, gap_column] == background_color:
                 output_grid[r, gap_column] = fill_color
            # Alternative: check input_grid[r, gap_column] == background_color
            # Let's stick with output_grid state check first. Seems safer if fill touches the gap.

    return output_grid
```
```python
import numpy as np
from collections import deque
from typing import List, Tuple, Set, Optional

"""
Transformation Rule:

1.  Identify the single connected object composed of gray (5) pixels (the 'container').
2.  Find the vertical "gap" column within the horizontal span of the container. This is the column with the minimum number of gray pixels within the container's bounding box columns.
3.  Identify a background (0) seed pixel within the area visually enclosed by the container (often adjacent to or within the gap column).
4.  Perform a flood fill starting from the seed pixel, changing connected background (0) pixels to azure (8), stopping at the gray (5) container boundary.
5.  Determine the vertical center of mass of the gray container.
6.  Compare the container's center to the grid's vertical center.
7.  If the container is lower, draw a vertical azure (8) line upwards from the top edge of the container in the gap column to the grid boundary, overwriting only background (0) pixels.
8.  If the container is higher or centered, draw a similar line downwards from the bottom edge of the container in the gap column.
"""

# Define color constants
BACKGROUND_COLOR = 0
CONTAINER_COLOR = 5
FILL_COLOR = 8

def find_objects(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates of pixels with the specified color."""
    return list(zip(*np.where(grid == color)))

def find_gap_column(grid: np.ndarray, obj_coords: List[Tuple[int, int]]) -> int:
    """
    Finds the column index corresponding to the vertical gap.
    Identified as the column within the object's horizontal bounds
    that contains the minimum number of object pixels (color specified implicitly by obj_coords).
    """
    if not obj_coords:
        return -1

    min_c = min(c for r, c in obj_coords)
    max_c = max(c for r, c in obj_coords)

    min_obj_count = float('inf')
    gap_col = -1

    obj_set = set(obj_coords)
    height = grid.shape[0]

    # Iterate through columns within the object's horizontal span
    for c in range(min_c, max_c + 1):
        count = 0
        for r in range(height):
             if (r,c) in obj_set:
                 count += 1

        # Only consider columns that actually contain object pixels
        if count > 0 and count < min_obj_count:
            min_obj_count = count
            gap_col = c
        # If counts are equal, the current logic keeps the first one found (lowest column index).

    # Fallback if no gap found within the span (e.g., solid rectangle - unlikely for this task)
    if gap_col == -1 and obj_coords:
        # Check counts at the boundary columns if they weren't picked
        min_edge_count = sum(1 for r in range(height) if (r, min_c) in obj_set)
        max_edge_count = sum(1 for r in range(height) if (r, max_c) in obj_set) if min_c != max_c else float('inf')

        if min_edge_count > 0 and min_edge_count <= max_edge_count:
             gap_col = min_c
        elif max_edge_count > 0: # Check only if different from min_c
             gap_col = max_c
        elif min_edge_count > 0: # Should have been caught by loop if min_c == max_c
             gap_col = min_c

    return gap_col

def find_interior_seed(grid: np.ndarray, obj_coords: List[Tuple[int, int]], gap_column: int) -> Optional[Tuple[int, int]]:
    """Finds a background pixel suitable for starting a flood fill inside the container."""
    if gap_column == -1 or not obj_coords:
        return None

    height, width = grid.shape
    obj_set = set(obj_coords)
    gray_rows_in_gap_col = sorted([r for r, c in obj_coords if c == gap_column])

    if not gray_rows_in_gap_col:
        return None # Gap column has no container pixels? Should not happen if find_gap_column is correct.

    min_r_gap = gray_rows_in_gap_col[0]
    max_r_gap = gray_rows_in_gap_col[-1]

    # Strategy 1: Check *within* the gap column, between the top/bottom gray pixels
    for r in range(min_r_gap + 1, max_r_gap):
        if grid[r, gap_column] == BACKGROUND_COLOR:
            return (r, gap_column)

    # Strategy 2: Check adjacent columns (left/right) next to gray pixels in the gap column
    for r in range(min_r_gap, max_r_gap + 1): # Include the boundary rows
         # Check left neighbor
         c_left = gap_column - 1
         if 0 <= c_left < width and grid[r, c_left] == BACKGROUND_COLOR and (r,c_left) not in obj_set:
             # Ensure the checked point is not part of the container itself (unlikely but safe)
             return (r, c_left)
         # Check right neighbor
         c_right = gap_column + 1
         if 0 <= c_right < width and grid[r, c_right] == BACKGROUND_COLOR and (r,c_right) not in obj_set:
             return (r, c_right)

    # If still no seed, maybe the gap is wider? This logic might need extension for complex cases,
    # but should cover the examples.
    # print("Warning: Could not find interior seed pixel.")
    return None


def flood_fill(grid: np.ndarray, seed: Tuple[int, int], target_color: int, fill_color: int):
    """Performs flood fill on the grid starting from the seed coordinate."""
    height, width = grid.shape
    if not (0 <= seed[0] < height and 0 <= seed[1] < width):
        return # Seed out of bounds
    if grid[seed[0], seed[1]] != target_color:
        return # Seed pixel is not the target color

    queue = deque([seed])
    visited = {seed}
    grid[seed[0], seed[1]] = fill_color

    while queue:
        r, c = queue.popleft()

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            if 0 <= nr < height and 0 <= nc < width:
                neighbor = (nr, nc)
                if neighbor not in visited and grid[nr, nc] == target_color:
                    visited.add(neighbor)
                    grid[nr, nc] = fill_color
                    queue.append(neighbor)


def calculate_vertical_center(obj_coords: List[Tuple[int, int]]) -> float:
    """Calculates the average row index (vertical center) of the object."""
    if not obj_coords:
        return -1.0
    return sum(r for r, c in obj_coords) / len(obj_coords)

def draw_vertical_line(grid: np.ndarray, column: int, start_row: int, direction: int, fill_color: int, overwrite_color: int):
    """Draws a vertical line, overwriting only pixels of a specific color."""
    height = grid.shape[0]
    r = start_row
    while 0 <= r < height:
        if grid[r, column] == overwrite_color:
            grid[r, column] = fill_color
        r += direction
        # Stop if we hit a non-background pixel? Examples suggest line goes all the way. Stick to boundary limit.


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation: fills the interior of a gray container
    and adds an exterior line aligned with the container's gap.
    """
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # 1. Identify the gray container
    container_coords = find_objects(output_grid, CONTAINER_COLOR)
    if not container_coords:
        return output_grid # No container found

    # 2. Find the gap column
    gap_column = find_gap_column(output_grid, container_coords)
    if gap_column == -1:
        # print("Warning: Could not determine gap column.")
        return output_grid # Cannot proceed without gap

    # 3. Find a seed pixel for flood fill
    seed_pixel = find_interior_seed(output_grid, container_coords, gap_column)

    # 4. Perform flood fill if seed is found
    if seed_pixel:
        flood_fill(output_grid, seed_pixel, BACKGROUND_COLOR, FILL_COLOR)
    # else:
        # print("Warning: No seed pixel found, skipping fill.")

    # 5. Calculate vertical center of the container
    shape_center_r = calculate_vertical_center(container_coords)

    # 6. Determine grid's vertical center
    grid_center_r = (height - 1) / 2.0

    # 7. Determine line direction and start point
    gray_rows_in_gap_col = sorted([r for r, c in container_coords if c == gap_column])
    if not gray_rows_in_gap_col:
         # Should be caught by gap column check, but safeguard
         # print("Warning: No container pixels in gap column for line drawing.")
         return output_grid

    min_r_gap = gray_rows_in_gap_col[0]
    max_r_gap = gray_rows_in_gap_col[-1]

    line_start_row = -1
    line_direction = 0

    if shape_center_r > grid_center_r:
        # Shape is lower -> Draw line upwards
        line_start_row = min_r_gap - 1
        line_direction = -1
    else:
        # Shape is upper or centered -> Draw line downwards
        line_start_row = max_r_gap + 1
        line_direction = 1

    # 8. Draw the exterior line
    if line_direction != 0:
         draw_vertical_line(output_grid, gap_column, line_start_row, line_direction, FILL_COLOR, BACKGROUND_COLOR)

    return output_grid
```
