
## train_1

**input:**
```
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 0 0 5 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 0 0 5 0 0 0 0 0 0 0
0 0 2 0 5 0 0 5 0 0 0 0 0 0 0
0 0 5 0 5 0 0 5 0 0 0 0 0 0 0
0 0 5 0 5 0 0 5 0 0 0 0 0 0 0
0 0 2 0 2 0 0 2 0 0 0 0 0 0 0
```


**output:**
```
2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 0 0 5 0 0 2 0 0 0 0 0 0 0
0 0 2 0 5 0 0 2 0 0 0 0 0 0 0
0 0 5 0 5 0 0 2 0 0 0 0 0 0 0
0 0 5 0 5 0 0 2 0 0 0 0 0 0 0
0 0 2 0 2 0 0 2 0 0 0 0 0 0 0
```


## train_2

**input:**
```
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 2 0 0 0 3 0 0 0
0 0 3 0 0 0 3 0 0 0
0 0 3 0 0 0 3 0 0 0
0 0 2 0 0 0 2 0 0 0
```


**output:**
```
2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 0 0 0 0 2 0 0 0
0 0 2 0 0 0 2 0 0 0
0 0 3 0 0 0 2 0 0 0
0 0 3 0 0 0 2 0 0 0
0 0 2 0 0 0 2 0 0 0
```


## train_3

**input:**
```
1 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 3 0 0 0 0
0 0 7 0 0 0 0 0 0 0 5 0 0 0 0
0 0 7 0 0 1 0 0 0 0 5 0 0 3 0
0 0 7 0 0 7 0 1 0 0 5 0 0 5 0
0 0 7 0 0 7 0 7 0 0 5 0 0 5 0
0 0 1 0 0 1 0 1 0 0 3 0 0 3 0
```


**output:**
```
1 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 3 0 0 0 0
0 0 1 0 0 0 0 0 0 0 5 0 0 0 0
0 0 1 0 0 1 0 0 0 0 5 0 0 3 0
0 0 1 0 0 7 0 1 0 0 5 0 0 3 0
0 0 1 0 0 7 0 7 0 0 5 0 0 3 0
0 0 1 0 0 1 0 1 0 0 3 0 0 3 0
```

*   **Perception:**
    *   The task involves transforming an input grid into an output grid of the same dimensions.
    *   The transformation operates independently on each column.
    *   The core operation involves identifying specific vertical patterns within a column.
    *   The pattern consists of a non-white pixel (let's call it the "trigger" color) positioned directly above a contiguous vertical segment of pixels of a *different* non-white color (let's call this the "target" color).
    *   When this pattern is found, the entire contiguous vertical segment of the target color is replaced with the trigger color.
    *   Pixels that are not part of such a target segment, or trigger pixels themselves, remain unchanged. White pixels (color 0) act as separators and are never triggers or targets.

*   **YAML Facts:**
    
```yaml
    task_description: Modifies vertical color segments based on the color of the pixel directly above them.
    grid_properties:
      - dimensions: Input and output grids have identical height and width.
      - pixel_colors: Uses integers 0-9, representing different colors. Color 0 (white) is treated as background/empty space.
    objects:
      - name: Pixel
        properties:
          - color: Integer 0-9.
          - position: (row, column) coordinates.
      - name: Vertical Segment
        properties:
          - color: The single color making up the segment (must be non-white).
          - column_index: The column in which the segment resides.
          - start_row: The row index of the top pixel in the segment.
          - end_row: The row index of the bottom pixel in the segment.
          - contiguity: All pixels between start_row and end_row in the same column have the same color.
    relationships:
      - type: Adjacency (Vertical)
        description: A pixel at (r, c) is directly above a pixel at (r+1, c).
      - type: Pattern Identification
        condition: |
          Exists a pixel P1 at (r, c) with non-white color C1 (trigger).
          Exists a pixel P2 at (r+1, c) with non-white color C2 (target), where C1 != C2.
          P2 is the start of a contiguous vertical segment S of color C2.
    actions:
      - name: Recolor Segment
        input:
          - Trigger Pixel P1 (color C1)
          - Target Segment S (color C2) starting directly below P1.
        output:
          - All pixels within Segment S change their color from C2 to C1.
    transformation_scope: Column-based; operations within one column do not affect other columns.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the output grid.
    2.  Iterate through each column index `c` from left to right (0 to width-1).
    3.  For the current column `c`, iterate through each row index `r` from top to bottom (0 to height-2, as we need to look at the pixel below).
    4.  Let `trigger_pixel_color` be the color of the pixel at `(r, c)`.
    5.  Let `pixel_below_color` be the color of the pixel at `(r+1, c)`.
    6.  Check if `trigger_pixel_color` is not white (0), `pixel_below_color` is not white (0), and `trigger_pixel_color` is different from `pixel_below_color`.
    7.  If all conditions in step 6 are true:
        a.  Identify the contiguous vertical segment of `pixel_below_color` starting at `(r+1, c)` and extending downwards. Let this segment run from row `r+1` to row `k`.
        b.  Change the color of all pixels in the output grid from `(r+1, c)` down to `(k, c)` to `trigger_pixel_color`.
        c.  Since the change propagates downwards, potentially modifying pixels we would have checked later in this column, advance the row iterator `r` to `k` to avoid re-processing the just-modified segment or incorrectly triggering off a newly changed pixel. (Alternatively, simply continue the loop from `r+1` after modification, assuming only one such trigger-target interaction per column matters based on examples, or that modified pixels cannot act as new triggers). *Correction based on thought process re-evaluation: Modifying the grid in place and continuing the scan from `r+1` correctly handles the examples.*
    8.  After iterating through all rows in the current column, move to the next column.
    9.  Once all columns are processed, return the modified output grid.
```python
import numpy as np

"""
This transformation modifies vertical segments in a grid based on the color of the pixel directly above them.

The rule operates independently on each column.
1. Iterate through each column of the input grid.
2. For each column, iterate through the rows from top to bottom, checking each pixel (r, c) and the one directly below it (r+1, c).
3. Identify a "trigger" pixel at (r, c) if its color (C1) is not white (0).
4. Identify a potential "target" segment starting at (r+1, c) if its color (C2) is not white (0) and C1 is different from C2.
5. If such a trigger and potential target start are found:
    a. Determine the full extent of the contiguous vertical segment of color C2 starting at (r+1, c) and extending downwards. Let this segment end at row k.
    b. In the output grid, change the color of all pixels in this segment, from row r+1 to row k in column c, to the trigger color C1.
6. Pixels not part of a segment modified this way retain their original color. White pixels (0) act as boundaries and are never triggers or targets.
7. The process continues iterating through the rows and columns. Modifications are made to a copy of the grid, ensuring that the original pixel colors are used for subsequent checks within the same column scan.
"""

def find_vertical_segment_end(grid, start_row, col, target_color):
    """
    Finds the end row index of a contiguous vertical segment of a specific color.

    Args:
        grid (np.array): The input grid.
        start_row (int): The starting row index of the segment.
        col (int): The column index of the segment.
        target_color (int): The color of the segment pixels.

    Returns:
        int: The row index of the last pixel in the segment.
    """
    height = grid.shape[0]
    end_row = start_row
    # Iterate downwards from the row below the starting row
    for r in range(start_row + 1, height):
        if grid[r, col] == target_color:
            # If the color matches, extend the segment end
            end_row = r
        else:
            # If the color doesn't match, the segment ends at the previous row
            break
    return end_row

def transform(input_grid):
    """
    Transforms the input grid by recoloring vertical segments based on the pixel above.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each column
    for c in range(width):
        # Iterate through rows, stopping one before the last row
        # as we need to check the pixel below (r+1)
        for r in range(height - 1):
            # Get the color of the current pixel (potential trigger)
            trigger_color = input_grid[r, c]
            # Get the color of the pixel below (potential target segment start)
            target_start_color = input_grid[r + 1, c]

            # Check the conditions for transformation:
            # 1. Trigger pixel is not white (0)
            # 2. Target start pixel is not white (0)
            # 3. Trigger color is different from target color
            if trigger_color != 0 and target_start_color != 0 and trigger_color != target_start_color:
                
                # Find the full vertical segment of the target color starting from r+1
                segment_start_row = r + 1
                segment_end_row = find_vertical_segment_end(input_grid, segment_start_row, c, target_start_color)

                # Recolor the identified segment in the output grid with the trigger color
                # Use slicing for efficient modification: [start_row : end_row + 1] includes end_row
                output_grid[segment_start_row : segment_end_row + 1, c] = trigger_color

                # Note: We continue iterating r normally. The check condition uses the original
                # input_grid colors, so changes made to output_grid do not affect
                # subsequent trigger/target identification within the same column scan.

    return output_grid
```
