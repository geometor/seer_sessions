
Previous Code:
```python
import numpy as np
from collections import deque, namedtuple

BoundingBox = namedtuple("BoundingBox", ["min_row", "max_row", "min_col", "max_col"])

def find_connected_components(grid, ignore_color=0):
    """
    Finds all connected components (objects) in the grid, ignoring a specific color.
    Uses BFS.
    Returns a list of tuples: (color, set_of_coordinates).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != ignore_color and not visited[r, c]:
                color = grid[r, c]
                component_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_pixels.add((r, c))

                while q:
                    row, col = q.popleft()
                    
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               not visited[nr, nc] and grid[nr, nc] == color:
                                visited[nr, nc] = True
                                component_pixels.add((nr, nc))
                                q.append((nr, nc))
                
                if component_pixels:
                     components.append((color, component_pixels))
                     
    return components

def find_largest_object(grid, ignore_color=0):
    """
    Finds the largest connected component (object) in the grid, ignoring the background color.
    Returns the color and pixels of the largest object, or (None, None) if no object found.
    """
    components = find_connected_components(grid, ignore_color)
    if not components:
        return None, None

    largest_component = max(components, key=lambda item: len(item[1]))
    return largest_component[0], largest_component[1]


def get_bounding_box(pixels):
    """
    Calculates the bounding box for a set of pixel coordinates.
    Returns a BoundingBox named tuple, or None if pixels set is empty.
    """
    if not pixels:
        return None
    
    rows = [r for r, c in pixels]
    cols = [c for r, c in pixels]
    
    return BoundingBox(min(rows), max(rows), min(cols), max(cols))

def find_active_color(grid, main_shape_color, bbox, ignore_color=0):
    """
    Finds the color (other than background and main shape color) that exists
    both inside and outside the given bounding box.
    """
    rows, cols = grid.shape
    candidate_colors = set(np.unique(grid)) - {ignore_color, main_shape_color}

    for color in candidate_colors:
        found_inside = False
        found_outside = False
        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == color:
                    is_inside = (bbox.min_row <= r <= bbox.max_row and 
                                 bbox.min_col <= c <= bbox.max_col)
                    if is_inside:
                        found_inside = True
                    else:
                        found_outside = True
                if found_inside and found_outside:
                    return color # Found the active color
    return None # No active color found


def transform(input_grid):
    """
    Transforms the input grid based on the observed pattern:
    1. Identifies the main solid shape (largest non-background object) and its bounding box.
    2. Identifies the 'active color' present both inside and outside the main shape's bounding box.
    3. Removes active color pixels from inside the main shape's bounding box.
    4. Moves active color pixels from outside the bounding box:
        - If vertically aligned with the box, move 3 columns right.
        - If horizontally aligned with the box, move to the top edge (min_row) of the box.
    """
    
    # Find the main shape (largest non-background object)
    main_shape_color, main_shape_pixels = find_largest_object(input_grid, ignore_color=0)
    
    if main_shape_color is None or main_shape_pixels is None:
        # Cannot identify main shape, return input unchanged
        return input_grid.copy()
        
    # Determine the bounding box of the main shape
    bbox = get_bounding_box(main_shape_pixels)
    if bbox is None:
         # Should not happen if main_shape_pixels is not None, but safety check
        return input_grid.copy()

    # Identify the active color
    active_color = find_active_color(input_grid, main_shape_color, bbox, ignore_color=0)
    
    if active_color is None:
        # Cannot identify active color, return input unchanged
        return input_grid.copy()
        
    # Initialize output_grid as a copy of input_grid
    output_grid = input_grid.copy()
    rows, cols = input_grid.shape
    
    # Store movements to apply later to avoid conflicts during iteration
    movements = [] # List of tuples: (target_r, target_c, color)

    # Iterate through the input grid to process active color pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == active_color:
                # Check if the pixel is inside the bounding box
                is_inside = (bbox.min_row <= r <= bbox.max_row and 
                             bbox.min_col <= c <= bbox.max_col)

                if is_inside:
                    # Remove active color pixels from inside the bbox
                    output_grid[r, c] = 0 
                else:
                    # Remove active color pixel from its original outside position
                    output_grid[r, c] = 0 
                    
                    # Determine target position for movement
                    target_r, target_c = -1, -1 # Initialize invalid target

                    # Check if pixel is vertically aligned (within column span of bbox)
                    if bbox.min_col <= c <= bbox.max_col:
                        target_r, target_c = r, c + 3
                    # Check if pixel is horizontally aligned (within row span of bbox)
                    elif bbox.min_row <= r <= bbox.max_row:
                         target_r, target_c = bbox.min_row, c
                         
                    # Check if target is valid and within grid bounds before adding movement
                    if 0 <= target_r < rows and 0 <= target_c < cols:
                         movements.append((target_r, target_c, active_color))

    # Apply the stored movements to the output grid
    for r, c, color in movements:
        # Check bounds again just in case (e.g., if multiple pixels move to same spot, last one wins)
         if 0 <= r < rows and 0 <= c < cols:
            output_grid[r, c] = color

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0
0 0 2 0 3 0 0 2 0 0 0 0
0 0 2 0 3 0 0 2 0 0 0 0
3 3 2 3 3 3 3 2 3 3 3 3
0 0 2 0 3 0 0 2 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
3 3 2 2 2 2 2 2 3 3 3 3
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
3 3 2 2 2 2 2 2 3 3 3 3
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 0 0 0 0 2 0 0 0 0
0 0 2 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 3 0 0 0 0
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
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 0 0 0
0 0 1 0 0 8 0 0 1 0 0 0
0 0 1 0 0 8 0 0 1 0 0 0
8 8 1 8 8 8 8 8 1 8 8 8
0 0 1 0 0 8 0 0 1 0 0 0
0 0 1 0 0 8 0 0 1 0 0 0
0 0 1 1 1 1 1 1 1 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
8 8 1 1 1 1 1 1 1 8 8 8
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
8 8 1 1 1 1 1 1 1 8 8 8
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0
0 0 1 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 3:
Input:
```
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 3 0 4 0 3 0 0 0
4 4 4 4 3 4 4 4 3 4 4 4
0 0 0 0 3 0 4 0 3 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
4 4 4 4 3 3 3 3 3 4 4 4
0 0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 0 0 4 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 4 0 0
4 4 4 4 3 3 3 3 3 4 4 4
0 0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 3 0 0 0
0 0 0 0 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 4 0 0
```
Match: False
Pixels Off: 14
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 9.722222222222214
**Analysis of Metrics and Discrepancy:**

*   The metrics confirm the main shape (green, 3), its bounding box (rows 3-7, cols 4-8), and the active color (yellow, 4).
*   The classification of active pixels (inside, outside-vertical, outside-horizontal) is correct.
*   The calculation of *expected* target locations for vertical pixels (original column + 3) seems correct: `c=6` becomes `c=9`.
*   The calculation of *expected* target locations for horizontal pixels (original column, min\_row of bbox) seems correct: `r=5` becomes `r=3`.
*   The `transform` function code implements these rules:
    *   Vertical: `target_r, target_c = r, c + 3` (Correct)
    *   Horizontal: `target_r, target_c = bbox.min_row, c` (Correct)
*   **The Discrepancy:** The `transformed_output_ex3` printed by the `tool_code` block *does not match* the `Transformed Output` reported in the initial problem description. The `tool_code` output *does* seem to match the *expected output* for the vertical pixels (they are in column 9). Let's re-check the provided initial `Transformed Output` log vs the `tool_code` output.

    *Initial Log's Transformed Output (Example 3):* Vertically aligned pixels are in col 9. Horizontally aligned pixels are in row 3, but look shifted right by 1 (cols 1,2,3,4 -> row 3 cols 1,2,3,4 ; cols 10,11,12 -> row 3 cols 10,11,12) - Wait, I misread the initial log output completely. Let me diff it carefully.

    *Initial Log's Transformed Output:*
    
```
    ... | Col 8 | Col 9 | Col 10 | ...
    ... |   0   |   4   |    0   | ... (Row 0)
    ... |   0   |   4   |    0   | ... (Row 1)
    ... |   0   |   4   |    0   | ... (Row 2)
    ... |   3   |   4   |    4   | ... (Row 3) <- Horizontal move: cols 9, 10, 11 -> row 3, cols 9, 10, 11
    ... |   3   |   0   |    0   | ... (Row 4)
    ... |   3   |   0   |    0   | ... (Row 5)
    ... |   3   |   0   |    0   | ... (Row 6)
    ... |   3   |   0   |    0   | ... (Row 7)
    ... |   0   |   4   |    0   | ... (Row 8)
    ... |   0   |   4   |    0   | ... (Row 9)
    ... |   0   |   4   |    0   | ... (Row 10)
    ... |   0   |   4   |    0   | ... (Row 11)
    ```

    *Code Output's Transformed Output:*
    
```
    ... | Col 8 | Col 9 | Col 10 | ...
    ... |   0   |   4   |    0   | ... (Row 0)
    ... |   0   |   4   |    0   | ... (Row 1)
    ... |   0   |   4   |    0   | ... (Row 2)
    ... |   3   |   4   |    4   | ... (Row 3) <- Horizontal move: cols 9, 10, 11 -> row 3, cols 9, 10, 11
    ... |   3   |   0   |    0   | ... (Row 4)
    ... |   3   |   0   |    0   | ... (Row 5)
    ... |   3   |   0   |    0   | ... (Row 6)
    ... |   3   |   0   |    0   | ... (Row 7)
    ... |   0   |   4   |    0   | ... (Row 8)
    ... |   0   |   4   |    0   | ... (Row 9)
    ... |   0   |   4   |    0   | ... (Row 10)
    ... |   0   |   4   |    0   | ... (Row 11)
    ```

    *Expected Output:*
    
```
    ... | Col 8 | Col 9 | Col 10 | ...
    ... |   4   |   0   |    0   | ... (Row 0) <- Vert move: col 6 -> col 9
    ... |   4   |   0   |    0   | ... (Row 1)
    ... |   4   |   0   |    0   | ... (Row 2)
    ... |   3   |   4   |    4   | ... (Row 3) <- Horiz move: cols 0-3, 9-11 -> row 3
    ... |   3   |   0   |    0   | ... (Row 4)
    ... |   3   |   0   |    0   | ... (Row 5)
    ... |   3   |   0   |    0   | ... (Row 6)
    ... |   3   |   0   |    0   | ... (Row 7)
    ... |   4   |   0   |    0   | ... (Row 8)
    ... |   4   |   0   |    0   | ... (Row 9)
    ... |   4   |   0   |    0   | ... (Row 10)
    ... |   4   |   0   |    0   | ... (Row 11)
    ```

    Okay, the `tool_code` output (which reflects the actual code execution) is different from BOTH the initial log's `Transformed Output` *and* the `Expected Output`.

    The `tool_code` output correctly moved the *horizontally* aligned pixels (from row 5 to row 3). It *incorrectly* moved the *vertically* aligned pixels (from column 6) to column 9 (c+3), while the expected output has them staying in column 8.

    Let's re-examine the expected outputs carefully.
    Example 1: Vertically aligned (col 4) -> col 7 (4+3=7). Horizontally aligned (row 5) -> row 2 (bbox.min_row). Matches logic.
    Example 2: Vertically aligned (col 5) -> col 8 (5+3=8). Horizontally aligned (row 6) -> row 3 (bbox.min_row). Matches logic.
    Example 3: Vertically aligned (col 6) -> col 8 (Expected) vs col 9 (Code). Horizontally aligned (row 5) -> row 3 (bbox.min_row). Matches logic.

    **Conclusion:** The issue lies *only* in the vertical movement rule for Example 3. The code consistently applies `c+3`, but for Example 3, the expected shift is only `c+2` (from 6 to 8). Examples 1 and 2 both follow the `c+3` rule.

    Why the difference? Is there something unique about Example 3?
    *   Input Grid Size: 12x12 (Same as others)
    *   Main Shape Color: 3 (Green)
    *   Active Color: 4 (Yellow)
    *   Bounding Box: rows 3-7, cols 4-8
    *   Vertical Pixels: col 6
    *   Horizontal Pixels: row 5

    Is the shift amount related to the dimensions or position of the bounding box?
    *   Example 1: BBox (2-7, 2-7). Vertical shift = 3. `bbox.min_col = 2`.
    *   Example 2: BBox (3-9, 2-8). Vertical shift = 3. `bbox.min_col = 2`.
    *   Example 3: BBox (3-7, 4-8). Vertical shift = 2 (Expected). `bbox.min_col = 4`.

    Hypothesis: The vertical shift amount is `bbox.min_col - 1`?
    *   Example 1: `2 - 1 = 1` (Incorrect, shift is 3)
    Hypothesis: The vertical shift amount is related to the *width* of the bounding box?
    *   Example 1: Width = 7-2+1 = 6. Shift = 3.
    *   Example 2: Width = 8-2+1 = 7. Shift = 3.
    *   Example 3: Width = 8-4+1 = 5. Shift = 2 (Expected).

    This doesn't look consistent either. `Width / 2` rounded? Ex1: 6/2=3. Ex2: 7/2=3.5->3? Ex3: 5/2=2.5->2? This seems plausible. Let's assume integer division or floor.
    *   Example 1: `floor(6/2) = 3`. Matches.
    *   Example 2: `floor(7/2) = 3`. Matches.
    *   Example 3: `floor(5/2) = 2`. Matches.

    Revised Hypothesis: The vertical shift for active pixels outside the bounding box but aligned with its columns is `floor(bbox_width / 2)`.

    Let's re-evaluate the horizontal movement. It moves to `bbox.min_row`. This seems consistent across all examples.

    Final check on the logic:
    1. Find the largest non-background object (main shape).
    2. Find its bounding box.
    3. Find the 'active' color (present both inside and outside the bbox).
    4. Remove active color pixels from *inside* the bbox.
    5. Move active color pixels from *outside* the bbox:
        a. If the pixel is in the same column range as the bbox (vertically aligned): move it right by `floor(bbox_width / 2)` columns.
        b. If the pixel is in the same row range as the bbox (horizontally aligned): move it to the `bbox.min_row` row, keeping its original column.

This revised logic seems to fit all three examples.## General Assessment

The provided code successfully implements the transformation logic derived from the first example for the first two training pairs. However, it fails on the third example.

The core logic identifies a 'main shape', its bounding box, and an 'active color' present both inside and outside this box. It then removes the active color from inside the box and relocates the active color pixels from outside.

The failure on Example 3 indicates that the rule for relocating the *vertically aligned* active color pixels (those outside the box but sharing columns with it) was not general enough. The initial code used a fixed shift of +3 columns. The results from Example 3 show that the required shift was +2 columns.

By comparing the bounding boxes across the examples, a new hypothesis emerges: the vertical shift distance might be related to the width of the bounding box. Specifically, `floor(bbox_width / 2)` seems to match the required shift (3, 3, and 2) for the three examples respectively. The rule for moving horizontally aligned pixels (to the `bbox.min_row`) appears consistent.

The strategy will be to refine the natural language program and subsequently the code to incorporate this dynamic calculation for the vertical shift based on the bounding box width.

## Metrics Gathering (Example 3)

Based on the `tool_code` execution:

*   **Input Grid (Example 3):** 12x12
*   **Main Shape Color:** 3 (green)
*   **Main Shape Pixels:** A '+' shape.
*   **Bounding Box (bbox):** `BoundingBox(min_row=3, max_row=7, min_col=4, max_col=8)`
    *   `bbox_width = max_col - min_col + 1 = 8 - 4 + 1 = 5`
    *   `bbox_height = max_row - min_row + 1 = 7 - 3 + 1 = 5`
    *   `floor(bbox_width / 2) = floor(5 / 2) = 2`
*   **Active Color:** 4 (yellow) - Found both inside and outside the bbox.
*   **Active Pixels Inside BBox:** `[{'r': 4, 'c': 6}, {'r': 5, 'c': 5}, {'r': 5, 'c': 6}, {'r': 5, 'c': 7}, {'r': 6, 'c': 6}]`
*   **Active Pixels Outside BBox (Vertically Aligned):** Column 6, rows 0, 1, 2, 8, 9, 10, 11.
    *   Original Coordinates: `(r, 6)` for r in {0,1,2,8,9,10,11}
    *   Expected Target Coordinates: `(r, 6 + floor(bbox_width/2))` => `(r, 6 + 2)` => `(r, 8)`
*   **Active Pixels Outside BBox (Horizontally Aligned):** Row 5, columns 0, 1, 2, 3, 9, 10, 11.
    *   Original Coordinates: `(5, c)` for c in {0,1,2,3,9,10,11}
    *   Expected Target Coordinates: `(bbox.min_row, c)` => `(3, c)`
*   **Code Output Discrepancy:** The previous code calculated the vertical shift as `c + 3`, resulting in target column `6 + 3 = 9`. The expected output requires a target column of `8`.

## YAML Documentation of Facts


```yaml
task_context:
  problem_description: |-
    The task involves identifying a main shape, its bounding box, and an 'active' color present both inside and outside the box. Pixels of the active color inside the box are removed. Pixels of the active color outside the box are moved based on their alignment with the box.
  grid_properties:
    size: Variable, examples are 12x12.
    background_color: 0 (white)

objects:
  - object_type: main_shape
    description: The largest contiguous block of non-background pixels. Its color varies between examples (red, blue, green).
    properties:
      - color: The color of the largest object.
      - pixels: Set of coordinates forming the object.
      - bounding_box: The smallest rectangle enclosing the object.
        attributes: [min_row, max_row, min_col, max_col, width, height]
  - object_type: active_pixels
    description: Pixels of a specific color ('active color') that are not part of the main shape and are present both inside and outside the main shape's bounding box.
    properties:
      - color: The 'active' color (green, azure, yellow in examples).
      - location_category:
          - inside_bbox: Pixels within the main shape's bounding box.
          - outside_bbox_vertical: Pixels outside the bbox but sharing columns (min_col <= c <= max_col).
          - outside_bbox_horizontal: Pixels outside the bbox but sharing rows (min_row <= r <= max_row).

actions:
  - action: identify_main_shape
    inputs: [input_grid]
    outputs: [main_shape_object]
    description: Find the largest connected component of non-background pixels.
  - action: calculate_bounding_box
    inputs: [main_shape_object]
    outputs: [bounding_box]
  - action: identify_active_color
    inputs: [input_grid, main_shape_color, bounding_box]
    outputs: [active_color]
    description: Find the color (other than background and main shape color) present both inside and outside the bounding box.
  - action: process_active_pixels
    inputs: [input_grid, active_color, bounding_box]
    outputs: [output_grid]
    description: Create the output grid by applying rules to the active pixels.
    sub_actions:
      - rule: remove_inside_pixels
        target: Active pixels inside the bounding box.
        effect: Change their color to background (0).
      - rule: move_outside_vertical_pixels
        target: Active pixels outside the bounding box and vertically aligned (same column range).
        effect: Change their original location to background (0) and move them horizontally.
        details: New column = original_column + floor(bounding_box_width / 2). Row remains the same.
      - rule: move_outside_horizontal_pixels
        target: Active pixels outside the bounding box and horizontally aligned (same row range).
        effect: Change their original location to background (0) and move them vertically.
        details: New row = bounding_box.min_row. Column remains the same.

relationships:
  - type: alignment
    entity1: active_pixel (outside bbox)
    entity2: bounding_box
    description: An active pixel outside the bbox can be vertically aligned (within the column span) or horizontally aligned (within the row span).
  - type: dependency
    entity1: vertical_shift_distance
    entity2: bounding_box_width
    description: The distance to shift vertically aligned pixels depends on the width of the bounding box (`floor(width / 2)`).

```


## Natural Language Program

1.  **Identify Objects:**
    *   Find the largest connected component of non-background pixels (the "main shape"). Determine its color and the set of its pixel coordinates.
    *   Calculate the bounding box (minimum/maximum row/column) encompassing the main shape. Determine its width (`max_col - min_col + 1`).
    *   Identify the "active color": Scan the grid for a color (that is not the background color or the main shape's color) which has at least one pixel inside the bounding box and at least one pixel outside the bounding box.

2.  **Prepare Output:** Create a copy of the input grid to serve as the output grid.

3.  **Apply Transformations:** Iterate through each pixel of the input grid.
    *   If a pixel has the identified "active color":
        *   Check if the pixel's coordinates `(r, c)` are *inside* the main shape's bounding box (`bbox.min_row <= r <= bbox.max_row` and `bbox.min_col <= c <= bbox.max_col`).
            *   If **inside**, set the corresponding pixel in the *output grid* to the background color (0).
        *   If the pixel is *outside* the bounding box:
            *   Set the pixel's original location `(r, c)` in the *output grid* to the background color (0).
            *   Determine its alignment relative to the bounding box:
                *   If **vertically aligned** (`bbox.min_col <= c <= bbox.max_col`): Calculate the target column `target_c = c + floor(bbox_width / 2)`. If `target_c` is within the grid bounds, set the pixel `(r, target_c)` in the *output grid* to the active color.
                *   If **horizontally aligned** (`bbox.min_row <= r <= bbox.max_row`): The target row is `target_r = bbox.min_row`. Set the pixel `(target_r, c)` in the *output grid* to the active color. (Note: Assume vertical/horizontal alignment are mutually exclusive for pixels outside the box based on examples).

4.  **Return Result:** Return the modified output grid.

**(Self-Correction Note:** The previous program used a fixed vertical shift of +3. This revised program calculates the shift dynamically based on the bounding box width (`floor(bbox_width / 2)`) to accommodate all training examples.)

