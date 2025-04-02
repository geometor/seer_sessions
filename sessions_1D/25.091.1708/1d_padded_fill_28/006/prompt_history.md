
## train_1

**input:**
```
0 0 0 5 0 5 0 0 0 0 0 0 5 0 5 0 0 0 0 0 0 5 0 5 0 0 0
```


**output:**
```
0 0 0 5 5 5 0 0 0 0 0 0 5 5 5 0 0 0 0 0 0 5 5 5 0 0 0
```


## train_2

**input:**
```
3 0 0 3 0 0 0 0 0 3 0 0 3 0 0 0 0 0 3 0 0 3 0 0 0 0 0
```


**output:**
```
3 3 3 3 0 0 0 0 0 3 3 3 3 0 0 0 0 0 3 3 3 3 0 0 0 0 0
```


## train_3

**input:**
```
0 0 6 0 0 0 6 0 0 0 0 6 0 0 0 6 0 0 0 0 6 0 0 0 6 0 0
```


**output:**
```
0 0 6 6 6 6 6 0 0 0 0 6 6 6 6 6 0 0 0 0 6 6 6 6 6 0 0
```

Okay, let's analyze the transformation.

## Perception of Elements

1.  **Input Grid Structure**: The input grids contain a background color (white, 0) and exactly one other color (gray, green, or magenta in the examples).
2.  **Non-Background Objects**: The non-background color forms two distinct vertical lines of the same height (3 pixels in all examples).
3.  **Spacing**: These vertical lines are separated by one or more columns of the background color.
4.  **Output Grid Structure**: The output grids retain the same dimensions and background color as the input.
5.  **Transformation**: The transformation fills the rectangular area defined by the bounding box of the non-background pixels in the input grid with that same non-background color. Specifically, it fills the space *between* the two vertical lines, including the columns of the lines themselves, over the same rows occupied by the lines.

## YAML Facts Documentation


```yaml
task_description: Fill the rectangular bounding box defined by a non-background color.

elements:
  - element: grid
    description: A 2D array of pixels with integer values representing colors.
  - element: background_pixel
    value: 0
    color: white
    description: The most frequent pixel color, typically filling most of the grid.
  - element: foreground_pixel
    description: The single pixel color present in the input grid that is not the background color. Varies between examples (gray, green, magenta).
  - element: vertical_lines
    description: In the input, the foreground pixels form two distinct, parallel vertical lines of the same height and color.
    properties:
      - height: Consistent within an example (e.g., 3 pixels tall).
      - color: The foreground color.
      - separation: Separated horizontally by one or more background pixels.
  - element: filled_rectangle
    description: In the output, the area spanning horizontally between the leftmost and rightmost foreground pixels and vertically between the topmost and bottommost foreground pixels is filled entirely with the foreground color.
    properties:
      - color: Same as the foreground color from the input.
      - bounds: Defined by the minimum and maximum row and column indices of the foreground pixels in the input.

relationships:
  - type: defines
    subject: foreground_pixels_in_input
    object: bounding_box
    description: The locations of all foreground pixels in the input define a minimum bounding box (minimum/maximum row and column).
  - type: transforms_to
    subject: input_grid
    object: output_grid
    description: The input grid is transformed into the output grid.
  - type: fills
    subject: transformation_rule
    object: bounding_box_in_output
    description: The transformation rule fills the calculated bounding box in the output grid with the foreground color.

actions:
  - action: identify_foreground_color
    description: Find the single color in the input grid that is not the background color (white, 0).
  - action: determine_bounding_box
    description: Find the minimum row, maximum row, minimum column, and maximum column containing any pixel of the foreground color in the input grid.
  - action: create_output_grid
    description: Initialize an output grid of the same dimensions as the input, filled with the background color (white, 0).
  - action: fill_rectangle
    description: Set the color of all pixels within the determined bounding box (inclusive) in the output grid to the identified foreground color.
```


## Natural Language Program

1.  Identify the single non-white color (`C`) present in the input grid.
2.  Find the minimum row index (`min_row`), maximum row index (`max_row`), minimum column index (`min_col`), and maximum column index (`max_col`) of all pixels with color `C` in the input grid. This defines the bounding box of the color `C`.
3.  Create a new grid with the same dimensions as the input grid, initially filled entirely with white (0).
4.  Fill the rectangular region in the new grid from `min_row` to `max_row` (inclusive) and from `min_col` to `max_col` (inclusive) with the color `C`.
5.  The resulting grid is the output.
```python
import numpy as np

def find_foreground_color(grid):
    """Finds the single non-background (non-zero) color in the grid."""
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return color
    # Should not happen based on task description, but handle just in case
    return 0 

def find_bounding_box(grid, color):
    """Finds the min/max row/col for a given color."""
    rows, cols = np.where(grid == color)
    if rows.size == 0: # No pixels of this color found
        return None, None, None, None 
    min_row = np.min(rows)
    max_row = np.max(rows)
    min_col = np.min(cols)
    max_col = np.max(cols)
    return min_row, max_row, min_col, max_col

def transform(input_grid):
    """
    Identifies the single non-white color in the input grid, determines its 
    bounding box (minimum and maximum row and column), and fills this 
    rectangular area in the output grid with that color, leaving the rest 
    of the grid white (0).
    """
    # Convert input list of lists to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    
    # 1. Identify the single non-white color (C)
    foreground_color = find_foreground_color(input_array)
    
    # If no foreground color is found (e.g., all background), return the input as is
    # or an empty grid of the same size? Let's return a copy filled with background.
    if foreground_color == 0:
         return np.zeros_like(input_array).tolist()

    # 2. Find the bounding box of the foreground color
    min_row, max_row, min_col, max_col = find_bounding_box(input_array, foreground_color)

    # Handle case where bounding box wasn't found (shouldn't happen if foreground_color > 0)
    if min_row is None:
        return np.zeros_like(input_array).tolist()

    # 3. Create a new grid with the same dimensions, filled with background (0)
    output_array = np.zeros_like(input_array)

    # 4. Fill the rectangular region defined by the bounding box with the foreground color
    # Slicing is inclusive of the start index and exclusive of the end index,
    # so we add 1 to max_row and max_col.
    output_array[min_row:max_row+1, min_col:max_col+1] = foreground_color
    
    # 5. Convert the output numpy array back to a list of lists and return
    return output_array.tolist()
```
```python
"""
Identifies the single non-background color in the input grid, determines its 
bounding box (minimum and maximum row and column), and fills this 
rectangular area in the output grid with that color, leaving the rest 
of the grid white (0).
"""

import numpy as np

def find_foreground_color(grid: np.ndarray) -> int:
    """
    Finds the single non-background (non-zero) color in the grid.
    Assumes exactly one non-background color exists if any.
    Returns 0 if only the background color is present.
    """
    unique_colors = np.unique(grid)
    for color in unique_colors:
        if color != 0:
            return int(color) # Return the first non-zero color found
    return 0 # Return 0 if only background color (0) is found

def find_bounding_box(grid: np.ndarray, color: int) -> tuple | None:
    """
    Finds the min row, max row, min col, max col for a given color.
    Returns None if the color is not found in the grid.
    """
    rows, cols = np.where(grid == color)
    if rows.size == 0: # No pixels of this color found
        return None
    min_row = np.min(rows)
    max_row = np.max(rows)
    min_col = np.min(cols)
    max_col = np.max(cols)
    return int(min_row), int(max_row), int(min_col), int(max_col)

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by filling the bounding box of the foreground color.
    
    Args:
        input_grid: A list of lists representing the input grid.
        
    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    
    # Determine grid dimensions (needed for output creation)
    height, width = input_array.shape
    
    # Identify the single non-background color (C)
    foreground_color = find_foreground_color(input_array)
    
    # Create an output grid with the same dimensions, filled with background (0)
    # This also handles the case where no foreground color is found (foreground_color = 0)
    # as the bounding box won't be calculated/filled.
    output_array = np.zeros_like(input_array)

    # Proceed only if a foreground color exists
    if foreground_color != 0:
        # Find the bounding box of the foreground color
        bounding_box = find_bounding_box(input_array, foreground_color)
        
        # Should always find a box if foreground_color > 0, but check defensively
        if bounding_box is not None:
            min_row, max_row, min_col, max_col = bounding_box
            
            # Fill the rectangular region defined by the bounding box with the foreground color
            # Numpy slicing is [start_row:end_row, start_col:end_col]
            # where end_row and end_col are *exclusive*. Add 1 to max_row/max_col.
            output_array[min_row:max_row+1, min_col:max_col+1] = foreground_color
    
    # Convert the output numpy array back to a list of lists and return
    return output_array.tolist()
```
```python
"""
Transforms the input grid by identifying the single non-background foreground color, 
finding all rows containing this color, determining the overall horizontal extent 
(minimum and maximum columns) of the color across these rows, and then filling 
this horizontal extent with the foreground color *only* on those specific rows 
in the output grid. The rest of the output grid remains the background color (0).
"""

import numpy as np

def find_foreground_locations(grid: np.ndarray) -> tuple | None:
    """
    Finds the foreground color, the rows it appears in, and its min/max column extent.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple containing:
        - foreground_color (int): The non-zero color found.
        - unique_rows (list[int]): Sorted list of unique row indices containing the color.
        - min_col (int): The minimum column index where the color appears.
        - max_col (int): The maximum column index where the color appears.
        Returns None if no non-zero color is found.
    """
    unique_colors = np.unique(grid)
    foreground_color = 0
    for color in unique_colors:
        if color != 0:
            foreground_color = int(color)
            break
            
    if foreground_color == 0:
        return None # No foreground color found

    rows, cols = np.where(grid == foreground_color)
    
    if rows.size == 0: # Should not happen if foreground_color != 0, but safety check
        return None
        
    unique_rows = sorted(list(np.unique(rows)))
    min_col = int(np.min(cols))
    max_col = int(np.max(cols))
    
    return foreground_color, unique_rows, min_col, max_col

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    
    Args:
        input_grid: A list of lists representing the input grid.
        
    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize output grid with the same shape, filled with background color (0)
    output_array = np.zeros_like(input_array)
    
    # Find the foreground color, its rows, and its horizontal extent
    locations = find_foreground_locations(input_array)
    
    # If a foreground color and its locations were found
    if locations:
        foreground_color, unique_rows, min_col, max_col = locations
        
        # Iterate through only the rows where the foreground color was originally present
        for r in unique_rows:
            # Fill the horizontal span (min_col to max_col) on this specific row
            # Numpy slicing is [start:end], where end is exclusive, so add 1 to max_col
            output_array[r, min_col:max_col + 1] = foreground_color
            
    # Convert the output numpy array back to a list of lists and return
    return output_array.tolist()
```
