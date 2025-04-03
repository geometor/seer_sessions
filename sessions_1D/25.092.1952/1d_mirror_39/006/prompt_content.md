
Previous Code:
```python
"""
Transforms an input grid based on the following rules:
1. Initialize the output grid with the same dimensions as the input grid, filling it entirely with white pixels (0).
2. Find the coordinates (`marker_row`, `marker_col`) of the single maroon pixel (9) in the input grid.
3. Place a maroon pixel (9) at the same coordinates (`marker_row`, `marker_col`) in the output grid.
4. Identify the unique color (`shape_color`) present in the input grid that is neither white (0) nor maroon (9).
5. Collect the set of all coordinates `(r, c)` in the input grid where the pixel value is equal to `shape_color`. These coordinates constitute the "movable shape".
6. If no movable shape pixels are found (i.e., the set of coordinates is empty), return the output grid containing only the maroon pixel.
7. Determine the minimum row index (`shape_top_row`) among all coordinates collected in step 5.
8. For each coordinate `(r, c)` belonging to the movable shape (from the set collected in step 5):
    a. Calculate the pixel's vertical offset relative to the top of its shape: `relative_r = r - shape_top_row`.
    b. Calculate the pixel's target row in the output grid: `new_r = (marker_row + 1) + relative_r`.
    c. Set the pixel at coordinate (`new_r`, `c`) in the output grid to `shape_color`. Ensure this target coordinate is within the grid boundaries before setting the pixel.
9. Return the completed output grid.
"""

import numpy as np
from typing import List, Tuple, Optional, Set

def find_pixel(grid: np.ndarray, color: int) -> Optional[Tuple[int, int]]:
    """Finds the coordinates (row, col) of the first pixel with the specified color."""
    rows, cols = np.where(grid == color)
    if len(rows) > 0:
        # Assuming only one marker pixel per grid based on examples
        return int(rows[0]), int(cols[0])
    return None

def find_colored_shape(grid: np.ndarray) -> Optional[Tuple[Set[Tuple[int, int]], int]]:
    """
    Finds the set of coordinates and the color of the single 
    non-white (0), non-maroon (9) contiguous shape.
    Returns None if no such shape exists.
    """
    shape_pixels: Set[Tuple[int, int]] = set()
    shape_color = -1 
    height, width = grid.shape

    # Find the unique shape color first
    possible_colors = set(np.unique(grid)) - {0, 9}
    if not possible_colors:
        return None # No shape color found
    if len(possible_colors) > 1:
        # Unexpected state based on examples, maybe handle error or pick one?
        # For now, assume only one shape color exists.
        print(f"Warning: Multiple potential shape colors found: {possible_colors}. Choosing one.")
        # We'll just pick one, e.g., the smallest one numerically
        shape_color = min(possible_colors)
    else:
        shape_color = possible_colors.pop()
            
    # Collect all pixels of that color
    rows, cols = np.where(grid == shape_color)
    for r, c in zip(rows, cols):
         shape_pixels.add((int(r), int(c)))

    if not shape_pixels:
        return None # Should not happen if color was found, but check anyway

    return shape_pixels, shape_color


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Initialize the output grid with white pixels (0).
    output_grid = np.zeros_like(input_np)

    # 2. Find the coordinates of the single maroon (9) pixel (marker).
    marker_pos = find_pixel(input_np, 9)
    if marker_pos is None:
        # If no marker pixel, the transformation is undefined. Return empty grid.
        print("Warning: Marker pixel (9) not found in input.")
        return output_grid.tolist() 
    marker_row, marker_col = marker_pos

    # 3. Place the marker pixel in the output grid.
    output_grid[marker_row, marker_col] = 9

    # 4. & 5. Identify the colored shape's pixels and color.
    shape_info = find_colored_shape(input_np)
    
    # 6. If no movable shape is found, return the grid with only the marker pixel.
    if shape_info is None:
        return output_grid.tolist() 
        
    shape_pixels, shape_color = shape_info

    # 7. Determine the top-most row of the shape.
    if not shape_pixels: # Defensive check
         return output_grid.tolist()
    shape_top_row = min(r for r, c in shape_pixels)

    # 8. Calculate new positions and place the shape in the output grid.
    for r, c in shape_pixels:
        # a. Calculate relative row within the shape.
        relative_r = r - shape_top_row
        # b. Calculate the new row in the output grid.
        new_r = (marker_row + 1) + relative_r
        
        # c. Set the pixel in the output grid, checking bounds.
        if 0 <= new_r < height and 0 <= c < width:
            output_grid[new_r, c] = shape_color
        else:
            # Handle cases where the moved shape goes out of bounds.
            # Based on examples, this shouldn't happen, so we can just ignore or log.
            # print(f"Debug: Pixel ({r},{c}) maps to out-of-bounds ({new_r},{c})")
            pass 

    # 9. Return the resulting grid as a list of lists.
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
3 3 3 3 3 3 3 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 3 3 3 3 3 3 3 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 7
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 45.16129032258064

## Example 2:
Input:
```
0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 1 1 1 1 1 1 1 1 1 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 58.064516129032256

## Example 3:
Input:
```
7 7 7 7 7 7 7 7 7 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 58.064516129032256
