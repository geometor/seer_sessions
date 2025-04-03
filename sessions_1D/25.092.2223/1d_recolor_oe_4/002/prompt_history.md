
## train_1

**input:**
```
0 0 9 9 9 9 9 9 0 0 0 9 9 9 0 9 9 9 0 9 9 9 9 9 0 0 0 9 0 0 0 0
```


**output:**
```
0 0 8 8 8 8 8 8 0 0 0 2 2 2 0 2 2 2 0 2 2 2 2 2 0 0 0 2 0 0 0 0
```


## train_2

**input:**
```
0 0 0 9 9 9 9 0 0 9 0 9 9 9 0 0 9 9 9 0 9 9 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 8 8 8 8 0 0 2 0 2 2 2 0 0 2 2 2 0 8 8 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 9 9 0 9 9 9 9 9 0 9 9 9 9 9 0 9 9 0 0 0 9 9 9 9 0 0 0 0 0
```


**output:**
```
0 0 0 8 8 0 2 2 2 2 2 0 2 2 2 2 2 0 8 8 0 0 0 8 8 8 8 0 0 0 0 0
```

## Perception

The input grid contains a pattern made of maroon pixels (9) on a white background (0). The output grid preserves the white background pixels. The maroon pixels from the input are transformed into either azure pixels (8) or red pixels (2) in the output. The overall shape formed by the non-white pixels remains the same between input and output.

The transformation logic appears to depend on the vertical position (row index) of the maroon pixels relative to the entire maroon shape. Specifically, the maroon pixels located in the topmost row containing any maroon pixels are changed to azure (8). All other maroon pixels (those in rows below the topmost row) are changed to red (2).

## Facts


```yaml
task_context:
  - The input grid contains two colors: white (0) and maroon (9).
  - The output grid contains three colors: white (0), red (2), and azure (8).
  - White pixels in the input remain white in the output.
  - Maroon pixels in the input are transformed into either red or azure pixels in the output.
  - The transformation rule for maroon pixels depends on their row index.

objects:
  - type: background
    color: white (0)
    behavior: remains unchanged between input and output.
  - type: shape
    color: maroon (9) in input
    behavior:
      - transformed into a shape of the same configuration but with different colors (red and azure).
      - the transformation depends on the vertical position within the shape.

properties:
  - min_maroon_row: The smallest row index containing at least one maroon (9) pixel in the input grid.

relationships:
  - position_based_transformation: A maroon pixel's output color depends on its row index relative to the `min_maroon_row`.

transformation:
  - identify the `min_maroon_row`.
  - iterate through each pixel of the input grid:
    - if the pixel color is white (0), the output pixel color is white (0).
    - if the pixel color is maroon (9):
      - if the pixel's row index equals `min_maroon_row`, the output pixel color is azure (8).
      - if the pixel's row index is greater than `min_maroon_row`, the output pixel color is red (2).
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Find the minimum row index (`min_row`) that contains any maroon (9) pixels in the input grid. If no maroon pixels exist, return the copied input grid.
3.  Iterate through each cell `(row, col)` of the input grid.
4.  If the color of the input cell `(row, col)` is maroon (9):
    a.  Check if the current cell's row index `row` is equal to `min_row`.
    b.  If `row` equals `min_row`, set the color of the output cell `(row, col)` to azure (8).
    c.  Otherwise (if `row` is greater than `min_row`), set the color of the output cell `(row, col)` to red (2).
5.  Leave all white (0) cells unchanged in the output grid.
6.
```python
"""
Transforms an input grid by changing the color of maroon (9) pixels based on their row position relative to the topmost row containing any maroon pixels.

1.  Initialize the output grid as a copy of the input grid.
2.  Find the minimum row index (`min_row`) that contains any maroon (9) pixels.
3.  If no maroon pixels are found, return the original grid.
4.  Iterate through each cell of the input grid.
5.  If a cell contains a maroon (9) pixel:
    a. If the cell's row index is equal to `min_row`, change the corresponding output cell to azure (8).
    b. If the cell's row index is greater than `min_row`, change the corresponding output cell to red (2).
6.  Leave all white (0) cells unchanged.
7.  Return the modified output grid.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists or numpy array): The input grid with integer values 0-9.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_array)
    height, width = input_array.shape

    min_maroon_row = -1 # Initialize with a value indicating not found

    # Find the minimum row index containing a maroon (9) pixel
    for r in range(height):
        if 9 in input_array[r, :]:
            min_maroon_row = r
            break # Found the first row, no need to search further

    # If no maroon pixels were found, return the original grid copy
    if min_maroon_row == -1:
        return output_grid

    # Iterate through each cell and apply the transformation rule for maroon pixels
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is maroon
            if input_array[r, c] == 9:
                # If the pixel is in the minimum maroon row, change to azure (8)
                if r == min_maroon_row:
                    output_grid[r, c] = 8
                # If the pixel is in a row below the minimum maroon row, change to red (2)
                elif r > min_maroon_row:
                    output_grid[r, c] = 2
            # White (0) pixels remain unchanged (already handled by the initial copy)

    return output_grid.tolist() # Return as list of lists per ARC standard

```
