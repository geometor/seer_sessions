
## train_1

**input:**
```
8 8 8 0 0 0
8 0 0 0 0 0
8 0 0 0 0 0
8 0 0 0 0 0
8 8 8 0 0 0
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0
0 8 8 8 8 0
0 8 8 8 8 0
0 8 8 8 8 0
0 0 0 0 0 0
0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 7 7 7 7 0 0 0
0 0 0 7 7 7 7 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0
0 0 6 0 0 0
0 6 0 0 0 0
6 0 0 0 0 0
0 6 0 0 0 0
0 0 6 0 0 0
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 6 6 0 0
0 6 6 6 6 0
0 0 6 6 0 0
0 0 0 0 0 0
```

Okay, let's break down the transformation logic based on the provided examples.

## Perception

1.  **Input/Output Format:** Both input and output are 2D grids of integers. The primary value seems to be 0 (representing background), with one other non-zero integer present in the input (e.g., 8, 7, 6), which acts as the 'color'.
2.  **Core Transformation:** The transformation identifies the non-zero elements in the input grid and uses their positions to define a rectangular area in the output grid. This output rectangle is then filled with the same non-zero 'color' found in the input.
3.  **Bounding Box:** The key first step appears to be finding the minimal bounding box that encloses all non-zero cells in the input grid. Let's denote its corners as (min_row, min_col) and (max_row, max_col).
4.  **Output Rectangle Calculation:** The output rectangle's boundaries seem derived from the input bounding box, but with modifications:
    *   The top row of the output rectangle is one row below the top of the input bounding box (`min_row + 1`).
    *   The bottom row of the output rectangle is one row above the bottom of the input bounding box (`max_row - 1`).
    *   The leftmost column of the output rectangle is one column to the right of the left edge of the input bounding box (`min_col + 1`).
    *   The rightmost column of the output rectangle seems more complex. It depends on the original rightmost column (`max_c`) and the *width* of the input bounding box (`width = max_c - min_c + 1`). The relationship observed across examples is `output_max_col = max_c + (5 - width)`.
5.  **Filling:** The calculated rectangular area in the output grid is filled entirely with the non-zero 'color' identified from the input. All other cells in the output grid are set to 0.

## Facts


```yaml
task_elements:
  - object: grid
    description: A 2D array of integer values.
    properties:
      - dimensions: [height, width]
      - cells: A list or array of cell objects/values.
  - object: cell
    description: An individual element within the grid.
    properties:
      - coordinates: [row, column]
      - value: The integer number stored in the cell (e.g., 0, 8, 7, 6).
      - is_background: Boolean (true if value is 0).
      - color: The non-zero value if present.
  - object: bounding_box
    description: The smallest rectangle enclosing a set of points (non-zero cells).
    properties:
      - min_row: The minimum row index.
      - max_row: The maximum row index.
      - min_col: The minimum column index.
      - max_col: The maximum column index.
      - height: max_row - min_row + 1
      - width: max_col - min_col + 1
  - object: output_rectangle
    description: The rectangular area to be filled in the output grid.
    properties:
      - top_row: Derived row index for the top edge.
      - bottom_row: Derived row index for the bottom edge.
      - left_col: Derived column index for the left edge.
      - right_col: Derived column index for the right edge.
      - fill_color: The color used to fill the rectangle.

relationships:
  - type: defines
    subject: Non-zero cells in the input grid
    object: Bounding box properties (min/max row/col, color)
  - type: derives
    subject: Input bounding box properties (min/max row/col, width)
    object: Output rectangle properties (top/bottom row, left/right col)
  - type: contains
    subject: Output grid
    object: Output rectangle (filled with color) and background cells (filled with 0)

actions:
  - name: identify_non_zero_cells
    input: input_grid
    output: list_of_coordinates, non_zero_color
  - name: calculate_bounding_box
    input: list_of_coordinates
    output: bounding_box_object
  - name: calculate_output_rectangle_coords
    input: bounding_box_object
    output: output_rectangle_coordinates [top_row, bottom_row, left_col, right_col]
    logic:
      - width = bbox.max_col - bbox.min_col + 1
      - k = 5 - width
      - top_row = bbox.min_row + 1
      - bottom_row = bbox.max_row - 1
      - left_col = bbox.min_col + 1
      - right_col = bbox.max_col + k
  - name: create_output_grid
    input: input_grid_dimensions
    output: output_grid (initialized with 0s)
  - name: fill_rectangle
    input: output_grid, output_rectangle_coordinates, fill_color
    output: modified_output_grid
```


## Natural Language Program

1.  Initialize an output grid with the same dimensions as the input grid, filling all cells with 0.
2.  Scan the input grid to find all cells containing a non-zero value.
3.  If no non-zero cells are found, return the initialized (all zeros) output grid.
4.  Identify the specific non-zero value (the `color`).
5.  Determine the minimum and maximum row indices (`min_r`, `max_r`) and minimum and maximum column indices (`min_c`, `max_c`) among all identified non-zero cells. This defines the input `bounding_box`.
6.  Calculate the width of the input `bounding_box`: `width = max_c - min_c + 1`.
7.  Calculate a column adjustment factor `k` based on the width: `k = 5 - width`.
8.  Define the boundaries for the `output_rectangle` to be filled in the output grid:
    *   `out_min_r = min_r + 1`
    *   `out_max_r = max_r - 1`
    *   `out_min_c = min_c + 1`
    *   `out_max_c = max_c + k`
9.  Iterate through all cells in the output grid whose coordinates `(r, c)` satisfy `out_min_r <= r <= out_max_r` and `out_min_c <= c <= out_max_c`.
10. Set the value of these cells to the identified non-zero `color`.
11. Return the final output grid.
```python
import math
import copy

def find_non_zero_elements(grid: list[list[int]]) -> tuple[list[tuple[int, int]], int | None]:
    """
    Finds all non-zero elements in the grid.

    Args:
        grid: The input grid.

    Returns:
        A tuple containing:
        - A list of (row, col) coordinates of non-zero elements.
        - The non-zero value (color) found, or None if none found.
          Assumes only one non-zero color exists besides 0.
    """
    coords = []
    color = None
    height = len(grid)
    if height == 0:
        return [], None
    width = len(grid[0])
    
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                coords.append((r, c))
                if color is None:
                    color = grid[r][c]
                elif color != grid[r][c]:
                    # Handle cases with multiple non-zero colors if necessary,
                    # but based on examples, assume only one.
                    pass 
                    
    return coords, color

def calculate_bounding_box(coords: list[tuple[int, int]]) -> tuple[int, int, int, int] | None:
    """
    Calculates the min/max row/col for the bounding box of given coordinates.

    Args:
        coords: A list of (row, col) coordinates.

    Returns:
        A tuple (min_r, max_r, min_c, max_c), or None if coords is empty.
    """
    if not coords:
        return None

    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    
    return min_r, max_r, min_c, max_c

"""
Identifies the non-zero elements in the input grid to determine a color and a bounding box.
Calculates the boundaries of a new rectangle within the output grid based on the input bounding box dimensions. 
The output rectangle's top/bottom rows are inset by 1 from the input box.
The output rectangle's left column is inset by 1 from the input box.
The output rectangle's right column is calculated based on the input box's right column and width: right_col = max_c + (5 - width).
Fills this calculated rectangle in the output grid with the identified color, leaving the rest as 0.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the bounding box of its non-zero elements.
    
    Args:
        input_grid: A 2D list of integers representing the input state.

    Returns:
        A 2D list of integers representing the transformed output state.
    """
    
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize output_grid with zeros
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # Find non-zero elements and their color
    non_zero_coords, color = find_non_zero_elements(input_grid)

    # If no non-zero elements, return the zero grid
    if not non_zero_coords or color is None:
        return output_grid

    # Calculate the bounding box of non-zero elements
    bbox = calculate_bounding_box(non_zero_coords)
    if bbox is None: # Should not happen if non_zero_coords is not empty
         return output_grid 
    min_r, max_r, min_c, max_c = bbox

    # Calculate the width of the input bounding box
    bbox_width = max_c - min_c + 1
    
    # Calculate the column adjustment factor k
    # Note: The rule k = 5 - width seems specific. Let's use it directly.
    k = 5 - bbox_width

    # Define the boundaries for the output rectangle
    out_min_r = min_r + 1
    out_max_r = max_r - 1
    out_min_c = min_c + 1
    out_max_c = max_c + k  # Adjusted right boundary

    # Fill the calculated rectangle in the output grid with the color
    # Ensure the calculated rows/cols are valid ranges
    if out_min_r <= out_max_r and out_min_c <= out_max_c:
         # Iterate through the rows and columns of the target rectangle
         for r in range(out_min_r, out_max_r + 1):
             # Ensure row is within grid bounds (might be unnecessary if logic guarantees it)
             if 0 <= r < height:
                 for c in range(out_min_c, out_max_c + 1):
                     # Ensure column is within grid bounds
                     if 0 <= c < width:
                         output_grid[r][c] = color

    return output_grid
```
```python
"""
Identifies the non-zero elements in the input grid to determine a color, count, and a bounding box.
Calculates the boundaries of a new rectangle within the output grid based on the input bounding box dimensions and the count of non-zero points.
The output rectangle's top/bottom rows are inset by 1 from the input box (min_r + 1, max_r - 1).
The output rectangle's left column is inset by 1 from the input box (min_c + 1).
The output rectangle's right column is calculated based on the input box's right column (max_c), width (w = max_c - min_c + 1), and the count of non-zero points (N). A base offset k_base = 4 - w is calculated. If N > 6, the final offset k = k_base + 1, otherwise k = k_base. The final right column is max_c + k.
Fills this calculated rectangle in the output grid with the identified color, leaving the rest as 0.
"""

import math
import copy

def find_non_zero_elements(grid: list[list[int]]) -> tuple[list[tuple[int, int]], int | None, int]:
    """
    Finds all non-zero elements in the grid, their count, and the color.

    Args:
        grid: The input grid.

    Returns:
        A tuple containing:
        - A list of (row, col) coordinates of non-zero elements.
        - The non-zero value (color) found, or None if none found.
          Assumes only one non-zero color exists besides 0.
        - The count (N) of non-zero elements.
    """
    coords = []
    color = None
    count = 0
    height = len(grid)
    if height == 0:
        return [], None, 0
    width = len(grid[0])
    
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                coords.append((r, c))
                count += 1
                if color is None:
                    color = grid[r][c]
                # No need to check for multiple colors based on problem constraints
                    
    return coords, color, count

def calculate_bounding_box(coords: list[tuple[int, int]]) -> tuple[int, int, int, int] | None:
    """
    Calculates the min/max row/col for the bounding box of given coordinates.

    Args:
        coords: A list of (row, col) coordinates.

    Returns:
        A tuple (min_r, max_r, min_c, max_c), or None if coords is empty.
    """
    if not coords:
        return None

    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    
    return min_r, max_r, min_c, max_c


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the bounding box and count of its non-zero elements.
    """
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize output_grid with zeros
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # Find non-zero elements, their color, and their count
    non_zero_coords, color, non_zero_count = find_non_zero_elements(input_grid)

    # If no non-zero elements, return the zero grid
    if not non_zero_coords or color is None:
        return output_grid

    # Calculate the bounding box of non-zero elements
    bbox = calculate_bounding_box(non_zero_coords)
    if bbox is None: # Should not happen if non_zero_coords is not empty
         return output_grid 
    min_r, max_r, min_c, max_c = bbox

    # Calculate the width of the input bounding box
    bbox_width = max_c - min_c + 1
    
    # Calculate the base column adjustment factor k_base
    k_base = 4 - bbox_width

    # Calculate the final column adjustment factor k based on count N
    if non_zero_count > 6:
      k = k_base + 1
    else:
      k = k_base
      
    # Define the boundaries for the output rectangle
    out_min_r = min_r + 1
    out_max_r = max_r - 1
    out_min_c = min_c + 1
    out_max_c = max_c + k  # Adjusted right boundary based on width and count

    # Fill the calculated rectangle in the output grid with the color
    # Ensure the calculated rows/cols define a valid rectangle
    if out_min_r <= out_max_r and out_min_c <= out_max_c:
         # Iterate through the rows and columns of the target rectangle
         for r in range(out_min_r, out_max_r + 1):
             # Ensure row is within grid bounds (important check)
             if 0 <= r < height:
                 for c in range(out_min_c, out_max_c + 1):
                     # Ensure column is within grid bounds (important check)
                     if 0 <= c < width:
                         output_grid[r][c] = color

    return output_grid
```

Previous Code:
```python
"""
Identifies the non-zero elements in the input grid to determine a color, count, and a bounding box.
Calculates the boundaries of a new rectangle within the output grid based on the input bounding box dimensions and the count of non-zero points.
The output rectangle's top/bottom rows are inset by 1 from the input box (min_r + 1, max_r - 1).
The output rectangle's left column is inset by 1 from the input box (min_c + 1).
The output rectangle's right column is calculated based on the input box's right column (max_c), width (w = max_c - min_c + 1), and the count of non-zero points (N). A base offset k_base = 4 - w is calculated. If N > 6, the final offset k = k_base + 1, otherwise k = k_base. The final right column is max_c + k.
Fills this calculated rectangle in the output grid with the identified color, leaving the rest as 0.
"""

import math
import copy

def find_non_zero_elements(grid: list[list[int]]) -> tuple[list[tuple[int, int]], int | None, int]:
    """
    Finds all non-zero elements in the grid, their count, and the color.

    Args:
        grid: The input grid.

    Returns:
        A tuple containing:
        - A list of (row, col) coordinates of non-zero elements.
        - The non-zero value (color) found, or None if none found.
          Assumes only one non-zero color exists besides 0.
        - The count (N) of non-zero elements.
    """
    coords = []
    color = None
    count = 0
    height = len(grid)
    if height == 0:
        return [], None, 0
    width = len(grid[0])
    
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                coords.append((r, c))
                count += 1
                if color is None:
                    color = grid[r][c]
                # No need to check for multiple colors based on problem constraints
                    
    return coords, color, count

def calculate_bounding_box(coords: list[tuple[int, int]]) -> tuple[int, int, int, int] | None:
    """
    Calculates the min/max row/col for the bounding box of given coordinates.

    Args:
        coords: A list of (row, col) coordinates.

    Returns:
        A tuple (min_r, max_r, min_c, max_c), or None if coords is empty.
    """
    if not coords:
        return None

    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    
    return min_r, max_r, min_c, max_c


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the bounding box and count of its non-zero elements.
    """
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize output_grid with zeros
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # Find non-zero elements, their color, and their count
    non_zero_coords, color, non_zero_count = find_non_zero_elements(input_grid)

    # If no non-zero elements, return the zero grid
    if not non_zero_coords or color is None:
        return output_grid

    # Calculate the bounding box of non-zero elements
    bbox = calculate_bounding_box(non_zero_coords)
    if bbox is None: # Should not happen if non_zero_coords is not empty
         return output_grid 
    min_r, max_r, min_c, max_c = bbox

    # Calculate the width of the input bounding box
    bbox_width = max_c - min_c + 1
    
    # Calculate the base column adjustment factor k_base
    k_base = 4 - bbox_width

    # Calculate the final column adjustment factor k based on count N
    if non_zero_count > 6:
      k = k_base + 1
    else:
      k = k_base
      
    # Define the boundaries for the output rectangle
    out_min_r = min_r + 1
    out_max_r = max_r - 1
    out_min_c = min_c + 1
    out_max_c = max_c + k  # Adjusted right boundary based on width and count

    # Fill the calculated rectangle in the output grid with the color
    # Ensure the calculated rows/cols define a valid rectangle
    if out_min_r <= out_max_r and out_min_c <= out_max_c:
         # Iterate through the rows and columns of the target rectangle
         for r in range(out_min_r, out_max_r + 1):
             # Ensure row is within grid bounds (important check)
             if 0 <= r < height:
                 for c in range(out_min_c, out_max_c + 1):
                     # Ensure column is within grid bounds (important check)
                     if 0 <= c < width:
                         output_grid[r][c] = color

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
8 8 8 0 0 0
8 0 0 0 0 0
8 0 0 0 0 0
8 0 0 0 0 0
8 8 8 0 0 0
0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0
0 8 8 8 8 0
0 8 8 8 8 0
0 8 8 8 8 0
0 0 0 0 0 0
0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0
0 8 8 8 8 0
0 8 8 8 8 0
0 8 8 8 8 0
0 0 0 0 0 0
0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 7 0 0 0 0 0 0 0
0 0 0 7 0 0 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 7 7 7 7 0 0 0
0 0 0 7 7 7 7 0 0 0
0 0 0 0 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0
0 0 0 7 7 7 0 0 0 0
0 0 0 7 7 7 0 0 0 0
0 0 0 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 4.0

## Example 3:
Input:
```
0 0 0 0 0 0
0 0 6 0 0 0
0 6 0 0 0 0
6 0 0 0 0 0
0 6 0 0 0 0
0 0 6 0 0 0
```
Expected Output:
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 6 6 0 0
0 6 6 6 6 0
0 0 6 6 0 0
0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0
0 0 0 0 0 0
0 6 6 6 0 0
0 6 6 6 0 0
0 6 6 6 0 0
0 0 0 0 0 0
```
Match: False
Pixels Off: 3
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 16.666666666666686
## General Assessment and Strategy

The previous code accurately identified the core transformation involving finding the bounding box of non-zero elements in the input and drawing a related rectangle in the output. It correctly applied the transformation for the first example. However, it failed on the subsequent examples because the calculation for the right boundary (`out_max_c`) of the output rectangle was incorrect. The initial rule involving the bounding box width (`width = max_c - min_c + 1`) and the count of non-zero points (`N`) proved not generalizable.

The strategy is to revise the calculation for the output rectangle boundaries based on a comparative analysis of all three training examples. The metrics gathered reveal a consistent and simpler relationship between the input bounding box coordinates and the output rectangle coordinates. Specifically, the top, bottom, and left boundaries follow the `+1` or `-1` inset rule observed initially, while the right boundary (`out_max_c`) appears consistently related to the input's right boundary (`max_c_in`) by a fixed offset.

## Metrics

| Example | Input Grid Dims | Color | Input BBox (min\_r, max\_r, min\_c, max\_c) | Input BBox Dims (H, W) | Input Non-Zero Count (N) | Output BBox (min\_r, max\_r, min\_c, max\_c) | Output BBox Dims (H, W) | Rule Check: out\_max\_c == max\_c\_in + 2 |
| :------ | :---------------- | :---- | :---------------------------------------- | :--------------------- | :----------------------- | :----------------------------------------- | :---------------------- | :---------------------------------------- |
| 1       | (6, 6)            | 8     | (0, 4, 0, 2)                              | (5, 3)                 | 8                        | (1, 3, 1, 4)                               | (3, 4)                  | 4 == 2 + 2 (True)                         |
| 2       | (10, 10)          | 7     | (3, 8, 2, 4)                              | (6, 3)                 | 7                        | (4, 7, 3, 6)                               | (4, 4)                  | 6 == 4 + 2 (True)                         |
| 3       | (6, 6)            | 6     | (1, 5, 0, 2)                              | (5, 3)                 | 5                        | (2, 4, 1, 4)                               | (3, 4)                  | 4 == 2 + 2 (True)                         |

The analysis confirms the following relationships for determining the output rectangle coordinates (`out_min_r`, `out_max_r`, `out_min_c`, `out_max_c`) from the input bounding box coordinates (`min_r_in`, `max_r_in`, `min_c_in`, `max_c_in`):
*   `out_min_r = min_r_in + 1`
*   `out_max_r = max_r_in - 1`
*   `out_min_c = min_c_in + 1`
*   `out_max_c = max_c_in + 2`

## Facts


```yaml
task_elements:
  - object: grid
    description: A 2D array of integer values representing the state.
    properties:
      - dimensions: [height, width]
      - cells: A list/array of cell values.
      - type: Either 'input' or 'output'.
  - object: cell
    description: An individual element within a grid.
    properties:
      - coordinates: [row, column]
      - value: The integer number (0 for background, non-zero for color).
      - color: The non-zero value if present.
  - object: input_bounding_box
    description: The smallest rectangle enclosing all non-zero cells in the input grid.
    properties:
      - min_row: The minimum row index (min_r_in).
      - max_row: The maximum row index (max_r_in).
      - min_col: The minimum column index (min_c_in).
      - max_col: The maximum column index (max_c_in).
      - derived_from: Non-zero cells in the input grid.
  - object: output_rectangle
    description: The rectangular area filled with color in the output grid.
    properties:
      - top_row: Row index for the top edge (out_min_r).
      - bottom_row: Row index for the bottom edge (out_max_r).
      - left_col: Column index for the left edge (out_min_c).
      - right_col: Column index for the right edge (out_max_c).
      - fill_color: The non-zero color identified from the input grid.
      - derived_from: Coordinates of the input_bounding_box.

relationships:
  - type: defines
    subject: Non-zero cells in input_grid
    object: input_bounding_box properties (min/max row/col) and fill_color for output_rectangle.
  - type: calculates
    subject: input_bounding_box coordinates (min_r_in, max_r_in, min_c_in, max_c_in)
    object: output_rectangle coordinates (out_min_r, out_max_r, out_min_c, out_max_c)
    rule: out_min_r=min_r_in+1, out_max_r=max_r_in-1, out_min_c=min_c_in+1, out_max_c=max_c_in+2
  - type: contains
    subject: output_grid
    object: output_rectangle (filled with fill_color) and background cells (value 0).

actions:
  - name: initialize_output_grid
    input: input_grid_dimensions
    output: output_grid (filled with 0s)
  - name: find_input_features
    input: input_grid
    output: non_zero_coordinates, fill_color
    description: Locates all non-zero cells and identifies the single non-zero color. Returns empty list and None color if input is all zeros.
  - name: calculate_input_bounding_box
    input: non_zero_coordinates
    output: input_bounding_box object (min_r_in, max_r_in, min_c_in, max_c_in)
    description: Computes the minimum bounding box containing the specified coordinates. Returns None if no coordinates provided.
  - name: calculate_output_rectangle_coords
    input: input_bounding_box object
    output: output_rectangle_coordinates [out_min_r, out_max_r, out_min_c, out_max_c]
    logic: Apply the coordinate transformation rules (min_r_in+1, max_r_in-1, min_c_in+1, max_c_in+2).
  - name: fill_output_rectangle
    input: output_grid, output_rectangle_coordinates, fill_color
    output: modified_output_grid
    description: Sets the value of cells within the calculated output rectangle coordinates to the fill_color, respecting grid boundaries.
```


## Natural Language Program

1.  Create a new output grid with the same dimensions as the input grid and initialize all its cells to 0.
2.  Scan the input grid to find the coordinates of all non-zero cells and identify their value (the `color`).
3.  If no non-zero cells exist in the input grid, return the initialized (all zeros) output grid.
4.  Calculate the `input_bounding_box` by finding the minimum and maximum row (`min_r_in`, `max_r_in`) and column (`min_c_in`, `max_c_in`) indices among the non-zero cell coordinates.
5.  Determine the coordinates of the `output_rectangle` using the input bounding box coordinates:
    *   Set the top row `out_min_r = min_r_in + 1`.
    *   Set the bottom row `out_max_r = max_r_in - 1`.
    *   Set the left column `out_min_c = min_c_in + 1`.
    *   Set the right column `out_max_c = max_c_in + 2`.
6.  Iterate through each cell `(r, c)` within the calculated `output_rectangle` boundaries (i.e., where `out_min_r <= r <= out_max_r` and `out_min_c <= c <= out_max_c`).
7.  For each such cell `(r, c)`, if it falls within the actual dimensions of the output grid (i.e., `0 <= r < height` and `0 <= c < width`), set its value to the identified `color`.
8.  Return the modified output grid.
