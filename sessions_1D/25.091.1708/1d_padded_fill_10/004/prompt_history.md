
## train_1

**input:**
```
0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0
```


## train_2

**input:**
```
7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 0 0 0 0 0 0 0
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0
```

**Perception of Task Elements:**

The input grids are sparsely populated with a single non-white color against a white background. The non-white pixels appear scattered, often forming a rough diagonal pattern. The output grids maintain the same dimensions as the inputs. The transformation involves filling rows with the non-white color. Specifically, for each row, the filling starts from the column where the first non-white pixel occurs in the input row and extends all the way to the right edge of the grid. If a row in the input contains only white pixels, the corresponding row in the output remains entirely white. The color used for filling is the same as the non-white color found in the input grid.

**YAML Facts:**


```yaml
task_description: Fill rows to the right starting from the first non-white pixel.
grid_properties:
  - dimensions: Input and output grids have identical height and width.
  - background_color: White (0) is the predominant background color.
objects:
  - object: Trigger Pixel
    description: The leftmost non-white pixel in each row of the input grid.
    properties:
      - color: Varies across examples (green, orange, red), but is consistent within a single example.
      - role: Determines the fill color and the starting column for the fill operation in its row.
  - object: Fill Area
    description: The region in the output grid that gets filled with the non-white color.
    properties:
      - color: Same as the Trigger Pixel color for that example.
      - location: Starts at the column of the Trigger Pixel and extends to the rightmost column within the same row.
actions:
  - action: Identify Fill Color
    description: Determine the single non-white color present in the input grid.
  - action: Scan Rows
    description: Process the input grid row by row.
  - action: Find Trigger
    description: For each row, locate the column index of the first (leftmost) non-white pixel.
  - action: Fill Right
    description: In the output grid, for each row containing a trigger pixel, color all cells from the trigger pixel's column to the right edge of the grid with the identified fill color.
relationships:
  - relationship: Row Correspondence
    description: Each row in the output grid corresponds directly to the row at the same index in the input grid.
  - relationship: Trigger-Fill Dependency
    description: The presence and column position of a Trigger Pixel in an input row determine if and where the Fill Area starts in the corresponding output row.
    properties:
      - If no Trigger Pixel exists in an input row, the output row remains white.
      - The Fill Area always uses the color of the Trigger Pixel.
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2.  Identify the single non-white color present in the input grid. Let this be the `fill_color`.
3.  Iterate through each row of the input grid, from top to bottom (row index `r`).
4.  For the current row `r`, scan from left to right (column index `c`) to find the first column `start_c` where the pixel color matches the `fill_color`.
5.  If such a `start_c` is found for row `r`:
    a.  Iterate through the columns of the output grid for row `r`, starting from `start_c` up to the last column.
    b.  Set the color of each pixel in this range (`output_grid[r][c]` where `c >= start_c`) to the `fill_color`.
6.  If no pixel matching the `fill_color` is found in the input row `r`, the corresponding output row `r` remains unchanged (all white).
7.  After processing all rows, return the completed output grid.
```python
"""
Fill rows to the right starting from the first non-white pixel.

1. Initialize an output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2. Identify the single non-white color present in the input grid. Let this be the `fill_color`.
3. Iterate through each row of the input grid, from top to bottom (row index `r`).
4. For the current row `r`, scan from left to right (column index `c`) to find the first column `start_c` where the pixel color matches the `fill_color`.
5. If such a `start_c` is found for row `r`:
    a. Iterate through the columns of the output grid for row `r`, starting from `start_c` up to the last column.
    b. Set the color of each pixel in this range (`output_grid[r][c]` where `c >= start_c`) to the `fill_color`.
6. If no pixel matching the `fill_color` is found in the input row `r`, the corresponding output row `r` remains unchanged (all white).
7. After processing all rows, return the completed output grid.
"""

import numpy as np

def find_fill_color(grid):
    """Finds the first non-zero color in the grid."""
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0:
                return grid[r, c]
    return 0 # Return background color if no non-zero color is found

def find_first_occurrence_index(row, color):
    """Finds the index of the first occurrence of a color in a row."""
    indices = np.where(row == color)[0]
    if len(indices) > 0:
        return indices[0]
    return None # Return None if color not found in the row

def transform(input_grid):
    """
    Transforms the input grid by filling rows to the right starting from the 
    first occurrence of the non-white color in that row.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output grid with the same dimensions, filled with white (0)
    output_array = np.zeros_like(input_array)

    # Identify the fill color (the single non-white color in the input)
    fill_color = find_fill_color(input_array)
    
    # If the grid is all white or no fill color identified, return the white grid
    if fill_color == 0:
        return output_array.tolist()

    # Iterate through each row of the input grid
    for r in range(height):
        input_row = input_array[r, :]
        
        # Find the column index of the first occurrence of the fill color in the current row
        start_c = find_first_occurrence_index(input_row, fill_color)
        
        # If the fill color is found in this row
        if start_c is not None:
            # Fill the output row from the start column to the right edge with the fill color
            output_array[r, start_c:] = fill_color
        # Else: the row remains white (as initialized)

    # Convert the output numpy array back to a list of lists
    return output_array.tolist()

```
```python
"""
Fill the horizontal segment between the first and last non-white pixel in each row of the input grid.

1. Create an output grid with the same dimensions as the input grid, initially filled with the background color (white, 0).
2. Scan the input grid to find the first pixel that is not white (0). If no such pixel exists, return the all-white output grid. Let the color of this first non-white pixel be `fill_color`.
3. Iterate through each row of the input grid, using its index `r` (from 0 to height-1).
4. For the current input row `r`:
    a. Find all column indices `c` where the pixel `input_grid[r][c]` equals the `fill_color`.
    b. If such indices exist:
        i. Find the minimum index (`start_c`) and the maximum index (`end_c`).
        ii. In the output grid's row `r`, set the color of all pixels from column `start_c` to column `end_c` (inclusive) to the `fill_color`.
    c. If no such indices exist, the output row `r` remains white.
5. After iterating through all rows, return the completed output grid.
"""

import numpy as np

def find_fill_color(grid):
    """Finds the first non-zero color in the grid."""
    unique_colors = np.unique(grid)
    non_zero_colors = unique_colors[unique_colors != 0]
    if len(non_zero_colors) > 0:
        return non_zero_colors[0] # Assume only one non-zero color based on examples
    return 0 # Return background color if no non-zero color is found

def find_row_boundaries(row, color):
    """
    Finds the minimum and maximum column indices of a given color in a row.
    Returns (min_index, max_index) or None if the color is not found.
    """
    indices = np.where(row == color)[0]
    if len(indices) > 0:
        return np.min(indices), np.max(indices)
    return None

def transform(input_grid):
    """
    Transforms the input grid by filling the horizontal segment between the 
    first and last occurrence of the non-white color in each row.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output grid with the same dimensions, filled with white (0)
    output_array = np.zeros_like(input_array)

    # Identify the fill color (the single non-white color in the input)
    fill_color = find_fill_color(input_array)
    
    # If the grid is all white or no fill color identified, return the white grid
    if fill_color == 0:
        return output_array.tolist()

    # Iterate through each row of the input grid
    for r in range(height):
        input_row = input_array[r, :]
        
        # Find the start and end column indices for the fill color in this row
        boundaries = find_row_boundaries(input_row, fill_color)
        
        # If the fill color is found in this row (boundaries exist)
        if boundaries is not None:
            start_c, end_c = boundaries
            # Fill the output row segment from start_c to end_c (inclusive)
            output_array[r, start_c : end_c + 1] = fill_color
        # Else: the row remains white (as initialized)

    # Convert the output numpy array back to a list of lists
    return output_array.tolist()

```
