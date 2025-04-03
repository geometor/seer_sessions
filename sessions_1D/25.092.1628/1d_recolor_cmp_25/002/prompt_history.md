
## train_1

**input:**
```
0 0 7 7 7 7 0 0 7 7 7 7 7 7 7 0 0 7 7 7 7 0 0 0 7 0 0
```


**output:**
```
0 0 7 7 7 7 0 0 9 9 9 9 9 9 9 0 0 7 7 7 7 0 0 0 7 0 0
```


## train_2

**input:**
```
0 0 7 0 7 7 7 0 7 7 7 7 0 7 0 0 0 7 7 7 7 7 0 0 0 0 0
```


**output:**
```
0 0 7 0 7 7 7 0 7 7 7 7 0 7 0 0 0 9 9 9 9 9 0 0 0 0 0
```


## train_3

**input:**
```
0 0 7 0 0 0 7 7 0 0 7 7 7 0 0 7 0 0 7 7 7 7 0 0 7 7 7
```


**output:**
```
0 0 7 0 0 0 7 7 0 0 7 7 7 0 0 7 0 0 9 9 9 9 0 0 7 7 7
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of Elements:**

1.  **Grid Structure:** The inputs and outputs are grids of pixels. The examples provided (train_1, train_2, train_3) consistently show input and output grids of the same dimensions (4 rows x 8 columns).
2.  **Colors Used:** The input grids use white (0) and orange (7). The output grids use white (0), orange (7), and maroon (9). Maroon (9) seems to be introduced as part of the transformation.
3.  **Transformation Focus:** The changes between input and output appear localized to a single row in each example.
    *   In `train_1`, the second row changes: `7 7 7 7 7 7 7 0` becomes `9 9 9 9 9 9 9 0`.
    *   In `train_2`, the third row changes: `0 7 7 7 7 7 0 0` becomes `0 9 9 9 9 9 0 0`.
    *   In `train_3`, the third row changes: `0 0 7 7 7 7 0 0` becomes `0 0 9 9 9 9 0 0`.
4.  **Identifying the Target Row:** The row that gets modified seems to be selected based on a property related to the orange (7) pixels within it. Let's examine the horizontal contiguous sequences of orange pixels in each input:
    *   **train_1:**
        *   Row 0: Max length 4 (`7 7 7 7`)
        *   Row 1: Max length 7 (`7 7 7 7 7 7 7`)
        *   Row 2: Max length 4 (`7 7 7 7`)
        *   Row 3: Max length 1 (`7`)
        *   *Result:* Row 1 (max length 7) is modified.
    *   **train_2:**
        *   Row 0: Max length 3 (`7 7 7`)
        *   Row 1: Max length 4 (`7 7 7 7`)
        *   Row 2: Max length 5 (`7 7 7 7 7`)
        *   Row 3: Max length 0
        *   *Result:* Row 2 (max length 5) is modified.
    *   **train_3:**
        *   Row 0: Max length 2 (`7 7`)
        *   Row 1: Max length 3 (`7 7 7`)
        *   Row 2: Max length 4 (`7 7 7 7`)
        *   Row 3: Max length 3 (`7 7 7`)
        *   *Result:* Row 2 (max length 4) is modified.
5.  **Rule Synthesis:** The transformation identifies the row containing the single longest contiguous horizontal sequence of orange (7) pixels. Within that specific row *only*, all orange (7) pixels are changed to maroon (9). All other pixels in the grid retain their original colors. The examples do not show ties for the longest sequence; if a tie occurred, a tie-breaking rule (e.g., first row encountered) might be needed, but based *only* on these examples, we assume a unique row contains the longest segment.

**Facts:**


```yaml
task_description: Identify the row with the longest continuous horizontal segment of orange (7) pixels and change all orange pixels in that row to maroon (9).

grid_properties:
  - dimensions: Constant between input and output.
  - colors_input: [white (0), orange (7)]
  - colors_output: [white (0), orange (7), maroon (9)] # Maroon (9) replaces orange (7) under specific conditions.

objects:
  - type: grid_row
    properties:
      - index: Vertical position (0-based from top).
      - pixels: Sequence of color values.
  - type: horizontal_segment
    properties:
      - color: The color of the contiguous pixels (focus on orange (7)).
      - length: Number of contiguous pixels.
      - location: The row index and starting/ending column indices.

relationships:
  - type: contains
    subject: grid_row
    object: horizontal_segment
    description: Each row may contain one or more horizontal segments of various colors.

actions:
  - action: find_max_segment
    input: input_grid
    parameters:
      - color_to_find: orange (7)
      - dimension: horizontal
    output:
      - target_row_index: Index of the row containing the longest segment.
      - max_length: Length of the longest segment.
    details: Iterates through rows, finds the longest contiguous horizontal run of the specified color in each, and identifies the overall maximum length and the corresponding row index. Assumes uniqueness based on examples.
  - action: update_row_color
    input:
      - input_grid
      - target_row_index
    parameters:
      - color_from: orange (7)
      - color_to: maroon (9)
    output: output_grid
    details: Creates a copy of the input grid. In the row specified by target_row_index, changes all pixels with color_from to color_to. Leaves all other pixels unchanged.

transformation_logic:
  1. Analyze the input grid to find the row containing the longest contiguous horizontal sequence of orange (7) pixels (find_max_segment).
  2. Identify the index of this target row.
  3. Modify the target row by changing all orange (7) pixels to maroon (9) (update_row_color).
  4. Return the modified grid.
```


**Natural Language Program:**

1.  Initialize variables `max_length_found` to 0 and `target_row_index` to -1.
2.  Iterate through each row of the input grid, keeping track of the current `row_index`.
3.  For the current row, find the length of the longest contiguous horizontal sequence of orange (7) pixels.
4.  If this length is greater than `max_length_found`, update `max_length_found` to this new length and set `target_row_index` to the current `row_index`.
5.  After iterating through all rows, create the output grid as a copy of the input grid.
6.  If a `target_row_index` was found (i.e., it's not -1), iterate through each pixel in the row specified by `target_row_index` in the output grid.
7.  If a pixel in this target row has the color orange (7), change its color to maroon (9).
8.  Return the final output grid.
```python
"""
Identify the row with the longest continuous horizontal segment of orange (7) pixels.
Then, change all orange (7) pixels in that specific row to maroon (9).
All other pixels remain unchanged.
"""

import numpy as np

def _find_longest_horizontal_segment(row, color):
    """Finds the length of the longest contiguous segment of a given color in a row."""
    max_length = 0
    current_length = 0
    for pixel in row:
        if pixel == color:
            current_length += 1
        else:
            max_length = max(max_length, current_length)
            current_length = 0
    # Check after the loop finishes in case the segment extends to the end
    max_length = max(max_length, current_length)
    return max_length

def transform(input_grid):
    """
    Transforms the input grid based on the rule:
    1. Find the row with the longest horizontal run of orange (7).
    2. Change all orange (7) pixels in that row to maroon (9).
    """
    input_array = np.array(input_grid, dtype=int)
    output_grid = input_array.copy() # Initialize output_grid as a copy

    target_color = 7
    replacement_color = 9
    
    max_length_found = -1 # Use -1 to handle cases with no target color
    target_row_index = -1

    # Iterate through each row to find the one with the longest segment of the target color
    for r_idx, row in enumerate(input_array):
        current_max_length = _find_longest_horizontal_segment(row, target_color)
        
        # Update if this row has a longer segment
        if current_max_length > max_length_found:
            max_length_found = current_max_length
            target_row_index = r_idx

    # Change output pixels in the identified target row
    if target_row_index != -1: # Check if the target color was found at all
        # Iterate through the pixels of the target row in the output grid
        for c_idx in range(output_grid.shape[1]):
            if output_grid[target_row_index, c_idx] == target_color:
                output_grid[target_row_index, c_idx] = replacement_color

    # Convert back to list of lists if necessary, matching ARC format
    return output_grid.tolist()
```
