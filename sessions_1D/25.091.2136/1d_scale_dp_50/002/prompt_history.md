
## train_1

**input:**
```
0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 0 0 0 7
```


**output:**
```
0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 7
```


## train_2

**input:**
```
0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 7
```


**output:**
```
0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 7
```


## train_3

**input:**
```
0 0 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 7 0
```


**output:**
```
0 0 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 7 0
```

## Perception
The input and output are single rows of pixels (1D grids).
Each input row contains:
1.  A contiguous block of a single color (e.g., magenta '6' or red '2'). Let's call this the "source color block".
2.  An orange pixel ('7'). Let's call this the "boundary pixel".
3.  White pixels ('0') acting as background, potentially surrounding the source color block and separating it from the boundary pixel.

The transformation involves extending the source color block to the right. The extension fills the white pixels ('0') between the original right edge of the source color block and the boundary pixel ('7') with the source color. The extension stops immediately before the boundary pixel. All other pixels, including those before the source color block, the boundary pixel itself, and any pixels after the boundary pixel, remain unchanged.

## Facts

```yaml
task_type: 1D array transformation
components:
  - type: background
    color: white (0)
    role: empty space, potentially filled
  - type: source_block
    description: A contiguous sequence of pixels of the same color, excluding white (0) and orange (7).
    properties:
      - color: variable (magenta '6' or red '2' in examples)
      - location: identifiable start and end indices
    role: expands to fill space
  - type: boundary_pixel
    color: orange (7)
    role: marks the rightmost limit for the expansion of the source_block
relationships:
  - source_block is always to the left of the boundary_pixel.
  - white (0) pixels may exist between the source_block and the boundary_pixel.
actions:
  - identify: locate the source_block and determine its color and rightmost index.
  - identify: locate the boundary_pixel and determine its index.
  - fill: change the color of all white (0) pixels located between the rightmost index of the source_block and the index of the boundary_pixel to the color of the source_block.
constraints:
  - The source_block color is preserved during filling.
  - The boundary_pixel is never overwritten.
  - Pixels to the left of the source_block and pixels at or after the boundary_pixel remain unchanged.
```


## Natural Language Program
1.  Scan the input row from left to right.
2.  Identify the first pixel that is not white (0) and not orange (7). This marks the start of the source color block. Note its color (let's call it `source_color`) and its index.
3.  Continue scanning to find the end of this contiguous block of `source_color`. Note the index of the last pixel in this block (let's call it `source_end_index`).
4.  Continue scanning from `source_end_index + 1` to find the index of the orange (7) pixel (let's call it `boundary_index`).
5.  Create a copy of the input row to serve as the output row.
6.  Iterate through the indices from `source_end_index + 1` up to (but not including) `boundary_index`.
7.  For each index in this range, change the pixel value in the output row to `source_color`.
8.  Return the modified output row.
```python
import numpy as np

def find_first_of(arr, values):
    """Finds the index and value of the first element in arr that is present in the values set."""
    for i, x in enumerate(arr):
        if x in values:
            return i, x
    return -1, -1 # Not found

def find_first_not_of(arr, values_to_exclude, start_index=0):
    """Finds the index and value of the first element in arr starting from start_index
       that is NOT present in the values_to_exclude set."""
    for i in range(start_index, len(arr)):
        if arr[i] not in values_to_exclude:
            return i, arr[i]
    return -1, -1 # Not found

def find_last_contiguous(arr, value, start_index):
    """Finds the last index of a contiguous block of 'value' starting from start_index."""
    last_index = start_index
    for i in range(start_index + 1, len(arr)):
        if arr[i] == value:
            last_index = i
        else:
            break
    return last_index

def transform(input_grid):
    """
    Transforms the input 1D grid (represented as a list) by extending a colored
    block to the right until it reaches an orange boundary pixel.

    1. Identifies a contiguous block of a single color (not white '0' or orange '7').
    2. Identifies the orange ('7') boundary pixel to the right of the block.
    3. Fills the white ('0') pixels between the end of the block and the boundary
       pixel with the block's color.
    """
    # The input is expected to be a 1D list (single row)
    input_row = input_grid

    # Create a copy to modify for the output
    output_row = list(input_row)

    # Define colors to ignore when looking for the source block start
    ignore_colors = {0, 7} # white and orange

    # 1. Find the start of the source color block
    source_start_index, source_color = find_first_not_of(output_row, ignore_colors)

    # Check if a source block was found
    if source_start_index == -1:
        # No source block found, return the original row (or handle as error)
        return output_row # Or potentially raise an error depending on requirements

    # 2. Find the end of the source color block
    source_end_index = find_last_contiguous(output_row, source_color, source_start_index)

    # 3. Find the boundary pixel (orange '7') starting search after the source block
    boundary_index = -1
    try:
        # Use list.index() for simplicity, specifying the start search position
        boundary_index = output_row.index(7, source_end_index + 1)
    except ValueError:
        # No boundary pixel found after the source block, return unchanged row
        # This case might indicate an unexpected input format based on examples
        return output_row

    # 4. Fill the gap between the source block end and the boundary pixel
    # Iterate from the pixel *after* the source block end up to *before* the boundary
    for i in range(source_end_index + 1, boundary_index):
        # Only fill if the pixel is currently white (optional, but matches description)
        # Based on examples, the space *is* white, but this makes it robust.
        # if output_row[i] == 0:
        output_row[i] = source_color

    # 5. Return the modified row
    return output_row
```
