
## train_1

**input:**
```
0 0 0 0 0 3 0
0 0 0 0 0 0 0
0 0 0 0 0 3 0
2 0 2 0 2 0 2
0 0 0 0 0 3 0
0 0 0 0 0 0 0
0 0 0 0 0 3 0
```


**output:**
```
0 0 0 0 0 3 0
0 0 0 0 0 3 0
0 0 0 0 0 3 0
2 2 2 2 2 2 2
0 0 0 0 0 3 0
0 0 0 0 0 3 0
0 0 0 0 0 3 0
```


## train_2

**input:**
```
0 0 0 0 0 0
0 0 0 0 0 6
4 0 4 0 4 0
0 0 0 0 0 6
0 0 0 0 0 0
0 0 0 0 0 6
```


**output:**
```
0 0 0 0 0 6
0 0 0 0 0 6
4 4 4 4 4 4
0 0 0 0 0 6
0 0 0 0 0 6
0 0 0 0 0 6
```


## train_3

**input:**
```
0 0 0 0 0 0
9 0 0 0 0 0
0 5 0 5 0 5
9 0 0 0 0 0
0 0 0 0 0 0
9 0 0 0 0 0
```


**output:**
```
9 0 0 0 0 0
9 0 0 0 0 0
5 5 5 5 5 5
9 0 0 0 0 0
9 0 0 0 0 0
9 0 0 0 0 0
```

Okay, let's analyze the task examples.

**Perception of the Elements:**

The input and output grids have the same dimensions in all examples. The transformation involves changing some white pixels (color 0) to other colors based on patterns within rows and columns.

1.  **Rows:** In each example, there is at least one row that initially contains pixels of a single non-white color interspersed with white pixels. In the output, all the white pixels in that specific row are replaced by that non-white color, effectively "completing" the horizontal line of color.
2.  **Columns:** Similarly, there is at least one column in each input that contains pixels of a single non-white color mixed with white pixels. In the output, the white pixels within that column are filled with the non-white color, completing the vertical line.
3.  **Independence:** The row-filling and column-filling operations appear to happen based on the *original* state of the input grid. A white pixel that belongs to both a "completable" row and a "completable" column might be targeted by both operations. The examples show that the operation related to the specific row or column takes precedence for filling that pixel. Example 1 is key: the pixel at (3, 5) is white. Row 3 should be filled with red (2), and Column 5 should be filled with green (3). In the output, pixel (3, 5) becomes red (2), and the other white pixels in column 5 become green (3). This suggests row operations might have priority, or perhaps both operations happen concurrently on a copy of the grid. A simpler explanation matching the output is that row changes affect the row, and column changes affect the column, and the effects are combined. Let's assume the operations are applied independently to a copy of the input.

**Facts:**


```yaml
task_type: grid_transformation
dimensionality: 2D
grid_properties:
  size_preservation: true # Output grid has the same dimensions as the input grid
pixel_colors_used:
  - white (0)
  - red (2)
  - green (3)
  - yellow (4)
  - gray (5)
  - magenta (6)
  - maroon (9)
objects:
  - type: line_segment
    attributes:
      orientation: [horizontal, vertical]
      composition: Consists of pixels of a single non-white color and potentially white (0) pixels.
actions:
  - name: identify_completable_lines
    inputs: input_grid
    outputs: list_of_rows, list_of_columns
    criteria:
      - A row or column contains pixels of exactly one non-white color, plus potentially white pixels.
  - name: fill_line_gaps
    inputs: grid, line_identifier (row index or column index), fill_color
    outputs: modified_grid
    description: Replaces all white (0) pixels along the specified line (row or column) in the grid with the fill_color.
relationships:
  - The fill_color for a line is determined by the single non-white color present in that line in the original input grid.
  - The filling action is applied independently for each identified completable row and column, modifying a copy of the input grid.
```


**Natural Language Program:**

1.  Create a working copy of the input grid. This copy will become the output grid.
2.  Examine each row of the **original input grid**.
3.  For a given row, determine the set of unique non-white colors present within it.
4.  If this set contains exactly one color (let's call this `row_color`), then iterate through all pixels in this row **in the working copy grid**. For any pixel in this row that is currently white (0), change its color to `row_color`.
5.  Examine each column of the **original input grid**.
6.  For a given column, determine the set of unique non-white colors present within it.
7.  If this set contains exactly one color (let's call this `col_color`), then iterate through all pixels in this column **in the working copy grid**. For any pixel in this column that is currently white (0), change its color to `col_color`.
8.  Return the final state of the working copy grid as the result.
```python
import numpy as np
from typing import List, Set, Tuple

"""
Transforms the input grid based on row and column completion rules.

1. Creates a copy of the input grid to serve as the output grid.
2. Identifies rows in the original input grid that contain exactly one unique non-white color alongside white (0) pixels.
3. For each such identified row, fills all white (0) pixels in that corresponding row of the output grid with the identified non-white color.
4. Identifies columns in the original input grid that contain exactly one unique non-white color alongside white (0) pixels.
5. For each such identified column, fills all white (0) pixels in that corresponding column of the output grid with the identified non-white color.
6. Returns the modified output grid.

The row and column filling operations are performed sequentially (rows first, then columns), modifying the same output grid. The check for whether a pixel should be filled is based on its state in the *current* output grid (i.e., it must be white (0) at the time of the fill operation). The determination of *which* rows/columns to fill and *what* color to use is based solely on the original input grid.
"""

def _get_unique_non_white(line: np.ndarray) -> Set[int]:
    """Finds the unique non-white colors in a 1D array (row or column)."""
    return set(color for color in line if color != 0)

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the row and column completion transformation to the input grid.
    """
    # Convert input to numpy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # --- Row Processing ---
    # Iterate through each row of the *original* input grid
    for r in range(height):
        row = input_np[r, :]
        # Find unique non-white colors in this row
        unique_colors = _get_unique_non_white(row)

        # Check if the row is 'completable' (exactly one non-white color)
        if len(unique_colors) == 1:
            fill_color = unique_colors.pop()
            # Iterate through the pixels of this row in the *output* grid
            for c in range(width):
                # If the pixel in the output grid is currently white, fill it
                if output_np[r, c] == 0:
                    output_np[r, c] = fill_color

    # --- Column Processing ---
    # Iterate through each column of the *original* input grid
    for c in range(width):
        col = input_np[:, c]
        # Find unique non-white colors in this column
        unique_colors = _get_unique_non_white(col)

        # Check if the column is 'completable' (exactly one non-white color)
        if len(unique_colors) == 1:
            fill_color = unique_colors.pop()
            # Iterate through the pixels of this column in the *output* grid
            for r in range(height):
                # If the pixel in the output grid is currently white, fill it
                if output_np[r, c] == 0:
                    output_np[r, c] = fill_color

    # Convert the final numpy array back to a list of lists
    return output_np.tolist()

```
