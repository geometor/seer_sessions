
## train_1

**input:**
```
7 7 7 7 7 7 7
7 8 7 7 7 7 7
7 8 7 2 7 7 7
7 8 7 2 7 7 7
7 8 7 2 7 7 7
7 8 7 2 7 7 7
```


**output:**
```
7 7 7 7 7 7 7
7 8 7 7 7 7 7
7 8 7 2 7 7 7
7 8 7 2 7 7 7
7 8 7 2 7 7 7
7 8 7 2 7 5 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7
7 7 7 7 7 7 7
7 7 7 7 7 7 7
7 7 7 8 7 7 7
7 8 7 8 7 7 7
7 8 7 8 7 7 7
```


**output:**
```
7 7 7 7 7 7 7
7 7 7 7 7 5 7
7 7 7 7 7 5 7
7 7 7 8 7 5 7
7 8 7 8 7 5 7
7 8 7 8 7 5 7
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 2 7 7 7 7 7
7 7 7 8 7 2 7 7 7 7 7
7 7 7 8 7 2 7 7 7 7 7
7 7 7 8 7 2 7 8 7 7 7
7 8 7 8 7 2 7 8 7 7 7
7 8 7 8 7 2 7 8 7 7 7
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 2 7 7 7 7 7
7 7 7 8 7 2 7 7 7 7 7
7 7 7 8 7 2 7 7 7 5 7
7 7 7 8 7 2 7 8 7 5 7
7 8 7 8 7 2 7 8 7 5 7
7 8 7 8 7 2 7 8 7 5 7
```

*   **Perception:** The input grids contain a background of orange (7) pixels and one or more vertical lines composed of azure (8) or red (2) pixels. The output grids are identical to the input grids, except for the addition of a new vertical gray (5) line. The position and vertical extent of this gray line depend on the properties of the rightmost vertical line object in the input and the total number of vertical line objects.

*   **Facts YAML:**
    
```yaml
    background_color: 7 # orange
    input_object_colors: [2, 8] # red, azure
    output_object_color: 5 # gray
    objects:
      - type: vertical_line
        properties:
          - color: 2 # red
          - color: 8 # azure
          - column_index
          - start_row
          - end_row
    actions:
      - identify_vertical_lines: Find all contiguous vertical segments of non-background colors.
      - find_rightmost_line: Determine the vertical line with the highest column index.
      - count_lines: Count the total number of identified vertical lines.
      - calculate_new_column: New column index = column index of rightmost line + 2.
      - determine_new_line_extent:
          condition: Color of the rightmost line.
          condition_value_1: Red (2)
          result_1: Start row = End row = End row of the rightmost line.
          condition_value_2: Azure (8)
          sub_condition: Total number of vertical lines.
          sub_condition_value_1: 2
          sub_result_1: Start row = max(0, Start row of the rightmost line - 2), End row = End row of the rightmost line.
          sub_condition_value_2: 3
          sub_result_2: Start row = max(0, Start row of the rightmost line - 1), End row = End row of the rightmost line.
      - draw_line: Add a vertical line of gray (5) pixels at the calculated column and row extent onto a copy of the input grid.
    relationships:
      - The position (column) of the new gray line is relative to the rightmost input vertical line (+2 columns).
      - The vertical extent (start/end rows) of the new gray line depends on the color and start/end rows of the rightmost input vertical line, and sometimes the total count of vertical lines.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct vertical line objects in the input grid. A vertical line object consists of contiguous pixels of the same non-orange color (red or azure) all located in the same column.
    2.  If no vertical line objects are found, return the input grid unchanged.
    3.  Determine the vertical line object with the largest column index (the "rightmost line"). Note its color (`color_R`), column index (`col_R`), topmost row index (`start_R`), and bottommost row index (`end_R`).
    4.  Count the total number of vertical line objects identified (`num_objects`).
    5.  Calculate the column index for the new gray line: `col_G = col_R + 2`.
    6.  Calculate the end row for the new gray line: `end_G = end_R`.
    7.  Calculate the start row for the new gray line (`start_G`) based on the color of the rightmost line and the total number of lines:
        *   If `color_R` is red (2), set `start_G = end_G`.
        *   If `color_R` is azure (8):
            *   If `num_objects` is 2, set `start_G = max(0, start_R - 2)`.
            *   If `num_objects` is 3, set `start_G = max(0, start_R - 1)`.
            *   (Assume behavior for other counts is undefined by examples, proceed only if count is 2 or 3 when rightmost is azure).
    8.  Create a copy of the input grid.
    9.  If `col_G` is a valid column index within the grid's width, draw a vertical line of gray (5) pixels in column `col_G` from row `start_G` to `end_G` (inclusive) onto the copied grid.
    10. Return the modified grid.
```python
import numpy as np
from typing import List, Dict, Tuple

"""
Identify all distinct vertical line objects (contiguous non-orange pixels in a column).
If no lines exist, return the input.
Find the rightmost vertical line (highest column index).
Note its color (color_R), column index (col_R), start row (start_R), and end row (end_R).
Count the total number of vertical lines (num_objects).
Calculate the target column for the new gray line: col_G = col_R + 2.
Calculate the target end row for the new gray line: end_G = end_R.
Calculate the target start row (start_G) based on color_R and num_objects:
- If color_R is red (2), start_G = end_G.
- If color_R is azure (8):
    - If num_objects is 2, start_G = max(0, start_R - 2).
    - If num_objects is 3, start_G = max(0, start_R - 1).
    - Otherwise, no line is drawn.
Create a copy of the input grid.
If col_G is within the grid bounds and the conditions for start_G calculation were met, draw a vertical gray (5) line in column col_G from start_G to end_G (inclusive) on the copied grid.
Return the modified grid.
"""

def find_vertical_lines(grid: np.ndarray, background_color: int = 7) -> List[Dict]:
    """
    Finds all contiguous vertical segments of non-background colors.

    Args:
        grid: The input numpy array representing the grid.
        background_color: The integer value representing the background color.

    Returns:
        A list of dictionaries, where each dictionary represents a vertical line
        and contains 'color', 'col', 'start_row', 'end_row'.
    """
    lines = []
    rows, cols = grid.shape
    for c in range(cols):
        current_line_start = -1
        current_line_color = -1
        for r in range(rows):
            pixel_color = grid[r, c]
            # Start of a potential new line
            if pixel_color != background_color and current_line_start == -1:
                current_line_start = r
                current_line_color = pixel_color
            # Continuation of the current line (same color)
            elif pixel_color == current_line_color and current_line_start != -1:
                continue # Just keep going
            # End of the current line (different color or background)
            elif current_line_start != -1:
                lines.append({
                    'color': current_line_color,
                    'col': c,
                    'start_row': current_line_start,
                    'end_row': r - 1
                })
                # Check if the current pixel starts a new line
                if pixel_color != background_color:
                    current_line_start = r
                    current_line_color = pixel_color
                else:
                    current_line_start = -1
                    current_line_color = -1
        # End of column, check if a line was ongoing
        if current_line_start != -1:
            lines.append({
                'color': current_line_color,
                'col': c,
                'start_row': current_line_start,
                'end_row': rows - 1
            })
    return lines

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by adding a gray vertical line based on the
    properties of the rightmost existing vertical line and the total number
    of vertical lines.

    Args:
        input_grid: The input numpy array.

    Returns:
        The transformed numpy array.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape
    background_color = 7
    new_line_color = 5 # gray

    # 1. Identify all distinct vertical line objects
    vertical_lines = find_vertical_lines(input_grid, background_color)

    # 2. If no vertical line objects are found, return the input grid unchanged.
    if not vertical_lines:
        return output_grid

    # 3. Determine the rightmost line
    rightmost_line = max(vertical_lines, key=lambda line: line['col'])
    color_R = rightmost_line['color']
    col_R = rightmost_line['col']
    start_R = rightmost_line['start_row']
    end_R = rightmost_line['end_row']

    # 4. Count the total number of vertical line objects identified
    num_objects = len(vertical_lines)

    # 5. Calculate the column index for the new gray line
    col_G = col_R + 2

    # 6. Calculate the end row for the new gray line
    end_G = end_R

    # 7. Calculate the start row for the new gray line (start_G)
    start_G = -1 # Initialize to invalid value
    if color_R == 2: # red
        start_G = end_G
    elif color_R == 8: # azure
        if num_objects == 2:
            start_G = max(0, start_R - 2)
        elif num_objects == 3:
            start_G = max(0, start_R - 1)
        # else: start_G remains -1, indicating no line should be drawn

    # 8. Create a copy of the input grid (already done)

    # 9. If col_G is valid and start_G was calculated, draw the line
    if start_G != -1 and 0 <= col_G < cols:
        # Ensure start_G is not less than 0 and end_G is within grid height
        valid_start_G = max(0, start_G)
        valid_end_G = min(rows - 1, end_G)

        # Ensure start <= end before drawing
        if valid_start_G <= valid_end_G:
             # Draw the vertical line
            for r in range(valid_start_G, valid_end_G + 1):
                 # Check row bounds just in case, although covered by valid_end_G
                 if 0 <= r < rows:
                    output_grid[r, col_G] = new_line_color

    # 10. Return the modified grid
    return output_grid
```
