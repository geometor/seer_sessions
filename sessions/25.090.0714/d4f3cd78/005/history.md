
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

Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 5 5 5 8 5 5 0 0
0 0 5 0 0 8 0 5 0 0
0 0 5 0 0 8 0 5 0 0
0 0 5 0 0 8 0 5 0 0
0 0 5 5 5 5 5 5 0 0
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.0

## Example 2:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 5 5 0 0
0 0 5 0 0 8 0 5 0 0
0 0 5 0 0 8 0 5 0 0
0 0 5 0 0 8 0 5 0 0
0 0 5 0 0 8 0 5 0 0
0 0 5 5 5 8 5 5 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 8 0 0 0 0
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 24.0
**General Assessment:**

The previous code correctly identified the gray shape, the gap column, the vertical positioning, and the logic for drawing the exterior azure line. The core failure lies in the method used to fill the interior of the gray shape. The `find_enclosed_background` function, which uses BFS from the grid borders to identify non-reachable background pixels, incorrectly assumes the shape topologically seals the interior. However, the shape has a vertical gap, allowing the BFS to "leak" into the interior space from the outside, thus failing to identify most of the interior pixels as enclosed.

**Strategy:**

The primary strategy is to replace the interior filling mechanism. Instead of identifying enclosed pixels by checking reachability from the *outside*, we will use a flood fill algorithm starting from a known *inside* pixel.

1.  **Identify a Seed Pixel:** Find a background (0) pixel guaranteed to be within the area intended for filling. A reliable method is to look adjacent (e.g., left or right) to the gray pixels in the identified `gap_column`, but between the top and bottom gray pixels of that column.
2.  **Flood Fill:** Perform a standard flood fill (BFS or DFS) starting from the seed pixel. The fill should spread to adjacent background (0) pixels and stop at the gray (5) boundary pixels. This correctly mimics filling the area visually contained by the gray shape.
3.  **Retain Other Logic:** Keep the existing logic for identifying the gray shape, calculating the gap column, determining the shape's vertical position relative to the grid center, and drawing the exterior line, as these parts functioned correctly according to the failed examples' outputs.

**Metrics Analysis:**

The code execution confirms the observations:
*   **Shape/Palette:** Output shapes and color palettes matched the expected ones.
*   **Pixel Mismatch:** The `pixels_off` count (9 for Ex1, 12 for Ex2) corresponds exactly to the number of interior pixels that *should* have been filled with azure (8) but were left as background (0).
*   **Color Counts:** The `transformed_counts` show significantly fewer azure (8) pixels and correspondingly more background (0) pixels compared to `output_counts`, confirming the fill failure.
*   **Fill Analysis:** The explicit check `(output_arr == 8) & (transformed_arr == 0)` confirms that all mismatched pixels were cases where an expected azure fill was missing. No pixels were incorrectly changed *to* azure.

**Refined YAML Facts:**


```yaml
task_description: Fill the interior of a C-shaped gray container with azure, and add a vertical azure line extending outwards from the container's gap, with the line's direction based on the container's vertical position.

elements:
  - element: background
    color: white (0)
    role: Canvas.
  - element: container
    color: gray (5)
    properties:
      - Forms a single connected component, typically C-shaped or bracket-shaped.
      - Acts as a boundary defining an interior region.
      - Has a vertical gap (a column with fewer gray pixels than adjacent columns within its span).
    role: Defines the area to be filled and provides reference points for the exterior line.
  - element: fill_color
    color: azure (8)
    role: Used to fill the interior region and create the exterior line.

relationships:
  - type: containment (visual)
    element1: container (gray)
    element2: background (white)
    description: The gray container visually encloses a region of the white background, accessible via the gap.
  - type: adjacency
    element1: fill_color (azure)
    element2: container (gray)
    description: The azure fill touches the inner boundary of the gray container. The azure line touches the outer boundary (top or bottom edge) of the gray container at the gap column.
  - type: spatial
    element1: container (gray)
    element2: grid
    description: The vertical center of mass of the container relative to the grid's vertical center determines the direction of the exterior azure line.

actions:
  - action: identify_container
    input: grid
    output: Coordinates of the single connected gray (5) object.
  - action: find_gap_column
    input: container coordinates, grid dimensions
    output: Column index of the vertical gap (minimum gray pixels within container's column span).
  - action: identify_seed_pixel
    input: container coordinates, gap_column, grid
    output: Coordinates of one background (0) pixel inside the visually contained area, suitable for starting a flood fill. (e.g., adjacent to a gray pixel in the gap column, between the top and bottom gray pixels of that column).
  - action: flood_fill_interior
    input: grid, seed_pixel
    output: Modify the grid by changing all reachable background (0) pixels from the seed (stopping at non-background) to azure (8).
  - action: determine_vertical_center
    input: container coordinates
    output: The average row index of the container pixels.
  - action: determine_extension_direction
    input: container_vertical_center, grid_height
    output: Direction (up or down) for the exterior line based on whether the container center is below or above/at the grid center.
  - action: find_line_start_row
    input: container coordinates, gap_column, direction
    output: The row index adjacent to the container's edge (topmost or bottommost gray pixel in the gap column) from which the line should start.
  - action: draw_exterior_line
    input: grid (potentially already filled), gap_column, start_row, direction, grid_height
    output: Modify the grid by adding a vertical azure (8) line in the gap column, starting from `start_row` and extending to the grid boundary in the specified `direction`, only overwriting background (0) pixels.
```


**Refined Natural Language Program:**

1.  Make a copy of the input grid to serve as the output grid.
2.  Identify all connected gray (5) pixels, representing the 'container'.
3.  Find the column index (`gap_column`) within the horizontal span of the container that contains the minimum number of gray pixels. This is the container's gap.
4.  Find a single background (0) 'seed' pixel that lies within the area visually enclosed by the container. A reliable method is to find a background pixel adjacent (left or right) to a gray pixel in the `gap_column`, at a row between the topmost and bottommost gray pixel in that column.
5.  Perform a flood fill starting from the `seed_pixel`: Change the seed pixel and all reachable adjacent background (0) pixels in the output grid to azure (8). The fill stops at non-background pixels (e.g., the gray container boundary).
6.  Calculate the vertical center row of the gray container pixels.
7.  Compare the container's vertical center to the grid's vertical center row.
8.  If the container's center is below the grid's center:
    *   Find the topmost row (`min_r_gap`) of the gray container within the `gap_column`.
    *   Set the starting row for the exterior line to `min_r_gap - 1` and the direction to upwards.
9.  If the container's center is at or above the grid's center:
    *   Find the bottommost row (`max_r_gap`) of the gray container within the `gap_column`.
    *   Set the starting row for the exterior line to `max_r_gap + 1` and the direction to downwards.
10. Draw the exterior line: Iterate from the `start_row` towards the grid edge (top or bottom depending on direction). For each pixel in the `gap_column`, if it is currently background (0) in the output grid, change it to azure (8).
11. The final modified grid is the result.**General Assessment:**

The initial code successfully identified the gray 'container' object, located its vertical 'gap', determined the container's relative vertical position (upper/lower half), and correctly drew the exterior azure line based on this position. The critical failure occurred during the interior fill step. The `find_enclosed_background` function, relying on reachability from the grid borders, failed because the container's gap allowed the search to access the interior, thus incorrectly classifying the interior pixels as *not* enclosed.

**Strategy for Resolution:**

The core strategy is to replace the flawed `find_enclosed_background` method with a standard flood fill algorithm initiated from *within* the container's visually bounded area.

1.  **Seed Identification:** Implement logic to reliably find a single background (0) pixel located inside the area to be filled. A good approach is to examine pixels adjacent to the gray pixels within the identified `gap_column`.
2.  **Flood Fill:** Use the identified seed pixel to start a flood fill (e.g., using BFS). This fill will change background (0) pixels to azure (8) and naturally stop at the gray (5) boundaries, correctly filling the visually contained region.
3.  **Retain Correct Logic:** Preserve the existing, functional code for identifying the container, finding the gap column, calculating the vertical center, determining the exterior line's direction, and drawing the line.

**Metrics Analysis:**

| Metric              | Example 1 (Expected) | Example 1 (Actual) | Example 2 (Expected) | Example 2 (Actual) | Notes                                        |
| :------------------ | :------------------- | :----------------- | :------------------- | :----------------- | :------------------------------------------- |
| Shape Match         | True                 | True               | True                 | True               | Output grid dimensions are correct.          |
| Palette Match       | True                 | True               | True                 | True               | Output uses the correct set of colors (0,5,8). |
| **Count Match**     | **True**             | **False**          | **True**             | **False**          | **Major discrepancy due to fill error.**     |
| \- White (0) Count  | 65                   | 74                 | 62                   | 74                 | Actual has more white (less fill).           |
| \- Gray (5) Count   | 17                   | 17                 | 19                   | 19                 | Gray container pixels are preserved.         |
| \- Azure (8) Count  | 18                   | 9                  | 19                   | 7                  | Actual has fewer azure pixels (less fill).   |
| **Pixels Match**    | **True**             | **False**          | **True**             | **False**          | **Overall output grid is incorrect.**        |
| **Pixels Off**      | **0**                | **9**              | **0**                | **12**             | **Number of pixels wrongly colored.**        |
| Missing Fill (8->0) | 0                    | 9                  | 0                    | 12                 | All errors are missing azure fill pixels.    |
| Wrong Fill (X->8)   | 0                    | 0                  | 0                    | 0                  | No pixels were incorrectly changed *to* azure. |

The metrics confirm that the shape identification, gap location, and exterior line drawing were likely correct, as the gray pixels are unchanged and the *number* of azure pixels added for the line (Ex1: 6 external; Ex2: 3 external) plus the few filled interior pixels matches the total azure count in the actual output (Ex1: 6+3=9; Ex2: 3+4=7). The `Pixels Off` count directly reflects the number of interior pixels that failed to be filled.

**YAML Facts:**


```yaml
task_description: Fill the visually enclosed area of a C-shaped gray container with azure, and draw a vertical azure line extending from the container's gap to the grid edge, directed away from the container's vertical center.

elements:
  - element: background
    color: white (0)
    role: Canvas.
  - element: container
    color: gray (5)
    properties:
      - Forms a single connected object.
      - Resembles a 'C' or bracket shape, creating a visually enclosed region.
      - Has a vertical gap (column within its span with the minimum number of gray pixels).
    role: Defines the area for interior filling and reference points/direction for the exterior line.
  - element: fill_color
    color: azure (8)
    role: Color used for both the interior fill and the exterior line.

relationships:
  - type: visual_containment
    element1: container (gray)
    element2: background (white)
    description: The container bounds a region of the background that needs filling, accessible via the gap.
  - type: adjacency
    element1: fill_color (azure)
    element2: container (gray)
    description: The azure fill is adjacent to the inner edge of the container. The exterior azure line is adjacent to the top or bottom edge of the container in the gap column.
  - type: relative_position
    element1: container (gray)
    element2: grid
    description: The vertical center of the container relative to the grid's vertical center determines if the exterior line extends upwards or downwards.

actions:
  - action: copy_input
    input: grid
    output: working_grid (a mutable copy).
  - action: identify_object
    input: working_grid, color=gray(5)
    output: coordinates of the container pixels.
  - action: find_gap_column
    input: container_coordinates, grid_dimensions
    output: column_index corresponding to the vertical gap.
  - action: find_interior_seed
    input: working_grid, container_coordinates, gap_column
    output: coordinates (row, col) of a background(0) pixel suitable for starting flood fill (e.g., horizontally adjacent to a gray pixel in the gap column, between the vertical bounds of the gap).
  - action: flood_fill
    input: working_grid, seed_coordinates, target_color=background(0), fill_color=azure(8)
    output: Modify working_grid by filling the connected area of target_color starting from seed with fill_color.
  - action: calculate_vertical_center
    input: container_coordinates
    output: average_row_index.
  - action: determine_line_direction_and_start
    input: average_row_index, grid_height, container_coordinates, gap_column
    output: line_start_row, line_direction (up/down).
  - action: draw_vertical_line
    input: working_grid, gap_column, line_start_row, line_direction, grid_height, fill_color=azure(8), overwrite_color=background(0)
    output: Modify working_grid by drawing the line, only changing pixels matching overwrite_color.
```


**Refined Natural Language Program:**

1.  Create a mutable copy of the input grid (`working_grid`).
2.  Identify all gray (5) pixels constituting the 'container' object.
3.  Determine the horizontal range (min/max columns) occupied by the container.
4.  Within this range, find the column (`gap_column`) containing the minimum number of gray pixels.
5.  Find a background (0) 'seed' pixel within the visually enclosed area. Locate this by checking background pixels horizontally adjacent to gray pixels in the `gap_column`, ensuring the row is between the topmost and bottommost gray pixels of that column.
6.  Perform a flood fill on `working_grid` starting from the `seed_pixel`: Change the seed and all connected background (0) pixels to azure (8). The fill stops when encountering non-background pixels (like the gray container).
7.  Calculate the average row index of the gray container pixels (its vertical center).
8.  Compare the container's vertical center to the grid's vertical center.
9.  If the container's center is below the grid's center:
    *   Find the row of the topmost gray pixel in the `gap_column`.
    *   Set the `line_start_row` to the row above it, and `direction` to upwards.
10. If the container's center is at or above the grid's center:
    *   Find the row of the bottommost gray pixel in the `gap_column`.
    *   Set the `line_start_row` to the row below it, and `direction` to downwards.
11. Draw the exterior line on `working_grid`: Starting from `line_start_row`, iterate towards the grid edge (row 0 if upwards, last row if downwards) along the `gap_column`. If a pixel in this column is currently background (0), change it to azure (8).
12. Return the modified `working_grid`.
