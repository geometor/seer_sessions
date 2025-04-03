
## train_1

**input:**
```
3 3 3 3 3 3 3 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 1 1 1 1 1 1 1 1 1 0 0
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0
```

Okay, let's analyze the task examples.

**Perception of Task Elements:**

1.    **Grid Structure:** Both input and output are grids of pixels represented by numbers 0-9. The grid dimensions remain constant between input and output (5x6 in all examples).
2.    **Key Colors:**
    *   White (0) acts as the background.
    *   Maroon (9) appears as a single, isolated pixel in each input. Its position is crucial.
    *   Another color (Green(3), Blue(1), or Orange(7) in the examples) forms a contiguous shape (object).
3.    **Object Identification:**
    *   There is always exactly one maroon pixel.
    *   There is always exactly one connected shape made of a single color other than white or maroon.
4.    **Spatial Relationship (Input):** The colored shape (non-maroon, non-white) is always located entirely in rows *above* the row containing the maroon pixel.
5.    **Transformation:** The primary transformation involves moving the colored shape.
    *   The maroon pixel remains fixed in its original position in the output grid.
    *   The colored shape is moved vertically downwards.
    *   The background of the output grid is white, except for the maroon pixel and the relocated colored shape.
6.    **Movement Rule:** The colored shape is translated vertically such that its topmost row in the input grid is repositioned to start in the row immediately *below* the row containing the maroon pixel. The shape's internal structure and horizontal position are preserved during this translation.

**Facts:**


```yaml
Grid:
  - Type: Input
    Properties:
      - Dimensions: Constant HxW (e.g., 5x6)
      - Contains:
          - Background: White pixels (0)
          - Maroon_Pixel: One pixel with color Maroon (9)
          - Colored_Shape: One contiguous object of a single color (not 0 or 9)
  - Type: Output
    Properties:
      - Dimensions: Same as Input HxW
      - Contains:
          - Background: White pixels (0)
          - Maroon_Pixel: Same pixel, same position as in Input
          - Colored_Shape: Same shape as in Input, different position

Objects:
  - Name: Maroon_Pixel
    Properties:
      - Color: Maroon (9)
      - Count: 1
      - Role: Anchor / Reference point
      - Position_Change: None (Input position == Output position)
  - Name: Colored_Shape
    Properties:
      - Color: Any color except White (0) or Maroon (9)
      - Count: 1 (contiguous block)
      - Initial_Location: Located entirely in rows above the Maroon_Pixel's row
      - Transformation: Vertical translation downwards
      - Structure_Change: None (Shape and color preserved)
      - Final_Location: Relocated to start in the row immediately below the Maroon_Pixel's row, maintaining horizontal position and relative vertical structure.

Relationships:
  - The Maroon_Pixel defines a horizontal boundary.
  - The Colored_Shape exists above this boundary in the input.
  - The transformation moves the Colored_Shape to exist below this boundary in the output.
  - The vertical starting position of the Colored_Shape in the output is directly determined by the row index of the Maroon_Pixel.

Action:
  - Identify the Maroon_Pixel's row (`maroon_row`).
  - Identify all pixels belonging to the Colored_Shape.
  - Determine the topmost row of the Colored_Shape (`shape_top_row`).
  - Create a new grid filled with White (0).
  - Copy the Maroon_Pixel to its original position in the new grid.
  - For each pixel `(r, c)` of the Colored_Shape in the input:
    - Calculate its relative row within the shape: `relative_r = r - shape_top_row`.
    - Calculate its new row in the output grid: `new_r = (maroon_row + 1) + relative_r`.
    - Copy the pixel's color to position `(new_r, c)` in the output grid.
```


**Natural Language Program:**

1.  Initialize the output grid with the same dimensions as the input grid, filling it entirely with white pixels (0).
2.  Locate the single maroon pixel (9) in the input grid. Let its row index be `maroon_row` and its column index be `maroon_col`.
3.  Copy the maroon pixel (9) to the same position (`maroon_row`, `maroon_col`) in the output grid.
4.  Identify all pixels in the input grid that are not white (0) and not maroon (9). These pixels constitute the "colored shape". Record their color (`shape_color`) and their original coordinates `(r, c)`.
5.  Find the minimum row index among all pixels belonging to the colored shape. Let this be `shape_top_row`.
6.  For each pixel `(r, c)` belonging to the colored shape in the input grid:
    a.  Calculate its row position relative to the top of the shape: `relative_r = r - shape_top_row`.
    b.  Calculate the new row position for this pixel in the output grid: `new_r = (maroon_row + 1) + relative_r`.
    c.  Set the pixel at coordinates (`new_r`, `c`) in the output grid to the `shape_color`.
7.  The resulting grid is the final output.
```python
import numpy as np
from typing import List, Tuple, Optional, Set

"""
1. Initialize the output grid with the same dimensions as the input grid, filling it entirely with white pixels (0).
2. Locate the single maroon pixel (9) in the input grid. Let its row index be `maroon_row` and its column index be `maroon_col`.
3. Copy the maroon pixel (9) to the same position (`maroon_row`, `maroon_col`) in the output grid.
4. Identify all pixels in the input grid that are not white (0) and not maroon (9). These pixels constitute the "colored shape". Record their color (`shape_color`) and their original coordinates `(r, c)`.
5. Find the minimum row index among all pixels belonging to the colored shape. Let this be `shape_top_row`.
6. For each pixel `(r, c)` belonging to the colored shape in the input grid:
    a. Calculate its row position relative to the top of the shape: `relative_r = r - shape_top_row`.
    b. Calculate the new row position for this pixel in the output grid: `new_r = (maroon_row + 1) + relative_r`.
    c. Set the pixel at coordinates (`new_r`, `c`) in the output grid to the `shape_color`.
7. The resulting grid is the final output.
"""

def find_pixel(grid: np.ndarray, color: int) -> Optional[Tuple[int, int]]:
    """Finds the coordinates (row, col) of the first pixel with the specified color."""
    rows, cols = np.where(grid == color)
    if len(rows) > 0:
        return int(rows[0]), int(cols[0])
    return None

def find_colored_shape(grid: np.ndarray) -> Optional[Tuple[Set[Tuple[int, int]], int]]:
    """Finds the set of coordinates and the color of the non-white, non-maroon shape."""
    shape_pixels = set()
    shape_color = -1
    height, width = grid.shape

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0 and color != 9:
                # Found a potential part of the shape
                if shape_color == -1:
                    shape_color = color
                elif color != shape_color:
                    # This indicates an unexpected state (multiple colors)
                    # For this task, assume only one shape color exists
                    continue 
                
                shape_pixels.add((r, c))

    if not shape_pixels:
        return None # No shape found

    return shape_pixels, shape_color


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by moving a colored shape vertically, positioning
    it just below a fixed maroon pixel.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Initialize the output grid with white pixels (0).
    output_grid = np.zeros_like(input_np)

    # 2. Locate the single maroon pixel (9).
    maroon_pos = find_pixel(input_np, 9)
    if maroon_pos is None:
        # Handle error: Maroon pixel not found (though problem constraints imply it exists)
        # For now, return the empty grid or raise an error. Let's return empty.
        return output_grid.tolist() 
    maroon_row, maroon_col = maroon_pos

    # 3. Copy the maroon pixel to the output grid.
    output_grid[maroon_row, maroon_col] = 9

    # 4. Identify the colored shape's pixels and color.
    shape_info = find_colored_shape(input_np)
    if shape_info is None:
        # No colored shape found, only the maroon pixel exists.
        return output_grid.tolist() 
        
    shape_pixels, shape_color = shape_info

    # 5. Find the top-most row of the shape.
    if not shape_pixels: # Should be redundant due to check above, but safe
         return output_grid.tolist()
    shape_top_row = min(r for r, c in shape_pixels)

    # 6. Calculate new positions and place the shape in the output grid.
    for r, c in shape_pixels:
        # a. Calculate relative row within the shape.
        relative_r = r - shape_top_row
        # b. Calculate the new row in the output grid.
        new_r = (maroon_row + 1) + relative_r
        
        # Check bounds before writing (optional but good practice)
        if 0 <= new_r < height and 0 <= c < width:
             # c. Set the pixel in the output grid.
            output_grid[new_r, c] = shape_color
        else:
            # This case implies the shape goes out of bounds after moving.
            # The problem examples don't show this, so we might assume it fits.
            # If required, error handling or clipping logic could be added here.
            pass 

    # 7. Return the resulting grid as a list of lists.
    return output_grid.tolist()
```
