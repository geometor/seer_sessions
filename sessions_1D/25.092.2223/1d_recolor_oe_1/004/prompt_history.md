
## train_1

**input:**
```
0 0 0 2 2 2 2 0 2 2 2 2 2 0 0 0 2 0 0 2 0 0 0
```


**output:**
```
0 0 0 9 9 9 9 0 7 7 7 7 7 0 0 0 7 0 0 7 0 0 0
```


## train_2

**input:**
```
0 0 0 2 2 2 2 2 2 0 0 2 2 2 2 2 0 2 0 2 2 2 0
```


**output:**
```
0 0 0 9 9 9 9 9 9 0 0 7 7 7 7 7 0 7 0 7 7 7 0
```


## train_3

**input:**
```
0 2 2 0 0 2 2 2 0 0 2 2 2 0 2 2 2 0 0 2 2 2 0
```


**output:**
```
0 9 9 0 0 7 7 7 0 0 7 7 7 0 7 7 7 0 0 7 7 7 0
```

Okay, analyzing the provided examples to understand the transformation logic.

**Perception:**

1.  **Input/Output Size:** The input and output grids have the same dimensions in all examples.
2.  **Colors:** The input grids contain only white (0) and red (2) pixels. The output grids contain white (0), maroon (9), and orange (7) pixels.
3.  **Static Pixels:** White pixels (0) in the input remain white (0) in the output at the same locations.
4.  **Dynamic Pixels:** Red pixels (2) in the input are transformed into either maroon (9) or orange (7) in the output.
5.  **Transformation Clue:** The color change for red pixels seems to depend on their vertical relationship with other red pixels. Specifically, if a red pixel has another red pixel directly below it, it transforms differently than if it doesn't.
    *   In `train_1`, the top row of `2`s becomes `9`s because they have `2`s below them (in the next row, same column implicitly, as part of the larger red shape). The middle row of `2`s becomes `7`s as they have white `0`s below them. The isolated bottom `2`s also become `7`s as they have white `0`s below them.
    *   This pattern holds for `train_2` and `train_3` as well. Red pixels with a red pixel directly underneath become maroon (9). All other red pixels become orange (7).

**Facts:**


```yaml
task_description: Recolor red pixels based on vertical adjacency.
elements:
  - element: pixel
    properties:
      - color: Can be white(0), red(2) in input; white(0), maroon(9), orange(7) in output.
      - position: Defined by row and column index.
relationships:
  - type: spatial
    description: Vertical adjacency between pixels. Specifically, whether a pixel has another pixel of the same color directly below it.
transformation:
  - type: conditional_recoloring
    input_color: red(2)
    output_colors: [maroon(9), orange(7)]
    condition:
      - based_on: pixel below
      - rule: If the pixel directly below a red(2) pixel is also red(2), the original pixel becomes maroon(9).
      - rule: Otherwise (if the pixel below is not red(2) or if it's the last row), the red(2) pixel becomes orange(7).
  - type: identity
    input_color: white(0)
    output_color: white(0)
    condition: Always applied to white pixels.
grid_properties:
  - size: Input and output grids have identical dimensions.
```


**Natural Language Program:**

1.  Create a new grid with the same dimensions as the input grid.
2.  Iterate through each cell (pixel) of the input grid using its row and column index.
3.  For the current cell at `(row, col)`:
    a.  If the color of the input cell is white (0), set the color of the corresponding cell `(row, col)` in the new grid to white (0).
    b.  If the color of the input cell is red (2):
        i.  Check if there is a cell directly below it (i.e., if `row + 1` is a valid row index within the grid).
        ii. If there is a cell below AND the color of the input cell at `(row + 1, col)` is also red (2), set the color of the cell `(row, col)` in the new grid to maroon (9).
        iii. Otherwise (if there is no cell below or the cell below is not red), set the color of the cell `(row, col)` in the new grid to orange (7).
4.  Return the new grid as the output.
```python
import numpy as np

"""
Recolor red pixels based on vertical adjacency.

1. Create an output grid with the same dimensions as the input grid.
2. Iterate through each cell (pixel) of the input grid.
3. If the input cell is white (0), the output cell remains white (0).
4. If the input cell is red (2):
    a. Check if there is a cell directly below it within the grid boundaries.
    b. If there is a cell below and it is also red (2), the output cell becomes maroon (9).
    c. Otherwise (no cell below or the cell below is not red), the output cell becomes orange (7).
5. Return the modified grid.
"""

def transform(input_grid):
    """
    Transforms the input grid according to the recoloring rules based on vertical adjacency.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    height, width = input_grid.shape

    # Initialize output_grid as a copy of the input grid.
    # This handles the white(0) pixels correctly by default.
    output_grid = np.copy(input_grid)

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is red (2)
            if input_grid[r, c] == 2:
                # Check if there is a row below the current row
                is_red_below = False
                if r + 1 < height:
                    # Check if the pixel directly below is also red (2)
                    if input_grid[r + 1, c] == 2:
                        is_red_below = True
                
                # Apply the transformation rule
                if is_red_below:
                    output_grid[r, c] = 9 # Change to maroon
                else:
                    output_grid[r, c] = 7 # Change to orange
            # No action needed for white (0) pixels as we started with a copy

    return output_grid

```
```python
import numpy as np
from typing import List, Tuple, Set

"""
Recolor vertical segments of red(2) pixels based on whether they are the first segment encountered when scanning from top to bottom, left to right.

1. Create an output grid as a copy of the input grid.
2. Find all contiguous vertical segments of red(2) pixels.
3. Keep track of the starting row (minimum row index) for each segment.
4. Identify the overall minimum starting row among all found segments.
5. Recolor the pixels of the segment(s) that start at this minimum row to maroon(9).
6. Recolor the pixels of all other red(2) segments to orange(7).
7. White(0) pixels remain unchanged.
"""

def find_vertical_red_segments(input_grid: np.ndarray) -> Tuple[List[Tuple[int, List[Tuple[int, int]]]], int]:
    """
    Finds all contiguous vertical segments of red(2) pixels.

    Args:
        input_grid: The input numpy array grid.

    Returns:
        A tuple containing:
        - A list of segments, where each segment is a tuple: (start_row, list_of_coordinates).
        - The minimum start row found across all segments.
    """
    height, width = input_grid.shape
    visited_pixels: Set[Tuple[int, int]] = set()
    red_segments: List[Tuple[int, List[Tuple[int, int]]]] = []
    min_start_row = height  # Initialize with a value larger than any possible row index

    # Iterate through grid, column by column, then row by row
    for c in range(width):
        for r in range(height):
            # If pixel is red and not yet part of a found segment
            if input_grid[r, c] == 2 and (r, c) not in visited_pixels:
                current_segment_pixels: List[Tuple[int, int]] = []
                current_row = r
                # Scan downwards to find the full vertical segment
                while current_row < height and input_grid[current_row, c] == 2:
                    pixel_coord = (current_row, c)
                    # Only add if not visited (this check might be redundant given the outer check, but safe)
                    if pixel_coord not in visited_pixels:
                         current_segment_pixels.append(pixel_coord)
                         visited_pixels.add(pixel_coord)
                    else:
                        # If we hit a visited pixel in the same column scan, break
                        # This handles cases where segments might technically touch corners
                        # but we process based on the top-most unvisited pixel.
                        # In simple vertical lines, this break won't be hit mid-segment.
                         break
                    current_row += 1

                # If a segment was found (at least one pixel)
                if current_segment_pixels:
                    segment_start_row = r # The starting row is the 'r' where we initiated the search
                    red_segments.append((segment_start_row, current_segment_pixels))
                    min_start_row = min(min_start_row, segment_start_row)

    return red_segments, min_start_row

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by recoloring vertical red segments.

    Args:
        input_grid: The input numpy array grid.

    Returns:
        The transformed numpy array grid.
    """
    # Initialize output_grid as a copy
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Find all vertical red segments and the minimum starting row
    red_segments, first_segment_start_row = find_vertical_red_segments(input_grid)

    # Check if any red segments were found
    if not red_segments:
        return output_grid # No red pixels, return the copy

    # Recolor the segments based on their start row
    for start_row, pixel_list in red_segments:
        # Determine the color based on whether it's the first segment
        new_color = 9 if start_row == first_segment_start_row else 7 # 9: maroon, 7: orange

        # Apply the color to all pixels in the segment
        for r, c in pixel_list:
            output_grid[r, c] = new_color

    return output_grid
```
