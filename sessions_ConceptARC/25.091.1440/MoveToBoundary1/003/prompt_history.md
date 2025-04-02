
## train_1

**input:**
```
0 0 0 0 0 2 0
0 0 0 0 0 2 0
0 1 1 0 0 2 0
0 1 1 0 0 2 0
0 0 0 0 0 2 0
0 0 0 0 0 2 0
0 0 0 0 0 2 0
```


**output:**
```
0 0 0 0 0 2 0
0 0 0 0 0 2 0
0 0 0 1 1 2 0
0 0 0 1 1 2 0
0 0 0 0 0 2 0
0 0 0 0 0 2 0
0 0 0 0 0 2 0
```


## train_2

**input:**
```
0 0 0 0 2 0
0 1 0 0 2 0
0 1 1 0 2 0
0 1 0 0 2 0
0 0 0 0 2 0
0 0 0 0 2 0
```


**output:**
```
0 0 0 0 2 0
0 0 1 0 2 0
0 0 1 1 2 0
0 0 1 0 2 0
0 0 0 0 2 0
0 0 0 0 2 0
```


## train_3

**input:**
```
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
0 0 0 1 1 0 2 0
0 0 1 1 0 0 2 0
0 0 0 1 1 0 2 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
```


**output:**
```
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
0 0 0 0 1 1 2 0
0 0 0 1 1 0 2 0
0 0 0 0 1 1 2 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
```


## train_4

**input:**
```
0 0 0 0 0 0
0 1 1 1 1 1
0 1 0 0 0 1
0 0 0 0 0 0
2 2 2 2 2 2
0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 1 1 1 1 1
0 1 0 0 0 1
2 2 2 2 2 2
0 0 0 0 0 0
```

*   **Perception:**
    *   The input grids contain three colors: white (0) as the background, blue (1) forming an object, and red (2) forming a line.
    *   The red object is always a straight line, either vertical or horizontal.
    *   The blue object is a distinct shape that does not touch the red line.
    *   In the output grid, the red line and the white background remain unchanged.
    *   The blue object moves its position. The shape of the blue object remains the same.
    *   The direction and distance of the blue object's movement seem to depend on the orientation of the red line and the relative position of the blue object to the red line.
    *   When the red line is vertical, the blue object moves 1 step horizontally away from the line (to the right in the examples).
    *   When the red line is horizontal, the blue object moves 2 steps vertically away from the line (downwards in the example).

*   **YAML Facts:**
    
```yaml
    task_description: Move a blue object away from a red line based on the line's orientation.
    elements:
      - object: background
        color: white (0)
        role: static_canvas
      - object: primary_shape
        color: blue (1)
        role: movable_object
        properties:
          - shape: variable (L-shape, plus, compound, U-shape in examples)
          - contiguity: contiguous block of blue pixels
      - object: constraint_line
        color: red (2)
        role: static_constraint
        properties:
          - shape: straight line (vertical or horizontal)
          - contiguity: contiguous block of red pixels
    relationships:
      - type: spatial
        description: The blue object is positioned relative to the red line (left/right or above/below).
      - type: interaction
        description: The red line dictates the movement of the blue object.
    actions:
      - action: identify_objects
        inputs: [input_grid]
        outputs: [blue_object_pixels, red_object_pixels]
      - action: determine_line_orientation
        inputs: [red_object_pixels]
        outputs: [orientation (vertical/horizontal)]
      - action: determine_relative_position
        inputs: [blue_object_pixels, red_object_pixels, orientation]
        outputs: [relative_pos (left/right/above/below)]
      - action: calculate_shift
        inputs: [orientation, relative_pos]
        outputs: [shift_vector (dx, dy)]
        logic:
          - if orientation is vertical, shift is (1, 0) if relative_pos is left, (-1, 0) if right.
          - if orientation is horizontal, shift is (0, 2) if relative_pos is above, (0, -2) if below.
      - action: apply_shift
        inputs: [input_grid, blue_object_pixels, shift_vector]
        outputs: [output_grid]
        logic: Create a new grid, copy the red line and background from the input, place the blue object at the shifted coordinates.
    ```


*   **Natural Language Program:**
    1.  Identify the set of coordinates occupied by the blue pixels (color 1) representing the blue object.
    2.  Identify the set of coordinates occupied by the red pixels (color 2) representing the red line.
    3.  Determine the orientation of the red line:
        *   If all red pixels share the same column index, the line is vertical.
        *   If all red pixels share the same row index, the line is horizontal.
    4.  Determine the shift vector (change in row `dy`, change in column `dx`):
        *   If the red line is vertical:
            *   Determine the column index of the red line (`red_col`).
            *   Find the average column index of the blue object pixels (`blue_avg_col`).
            *   If `blue_avg_col` < `red_col` (blue is left), set the shift vector to `(dx=1, dy=0)`.
            *   If `blue_avg_col` > `red_col` (blue is right), set the shift vector to `(dx=-1, dy=0)`.
        *   If the red line is horizontal:
            *   Determine the row index of the red line (`red_row`).
            *   Find the average row index of the blue object pixels (`blue_avg_row`).
            *   If `blue_avg_row` < `red_row` (blue is above), set the shift vector to `(dx=0, dy=2)`.
            *   If `blue_avg_row` > `red_row` (blue is below), set the shift vector to `(dx=0, dy=-2)`.
    5.  Create the output grid, identical in size to the input grid and initially filled with the background color (white, 0).
    6.  Copy the red line from the input grid to the output grid at its original position.
    7.  For each blue pixel at coordinate `(row, col)` in the input grid, place a blue pixel at `(row + dy, col + dx)` in the output grid.
```python
import numpy as np
from typing import List, Tuple, Dict, Optional

"""
Moves a blue (1) object relative to a red (2) line.
If the red line is vertical, the blue object moves 1 step horizontally away from the line.
If the red line is horizontal, the blue object moves 2 steps vertically away from the line.
The red line and white (0) background remain unchanged.
"""

def find_object_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates of pixels with the specified color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def determine_line_orientation_and_position(pixels: List[Tuple[int, int]]) -> Optional[Tuple[str, int]]:
    """
    Determines if the pixels form a vertical or horizontal line.
    Returns the orientation ('vertical' or 'horizontal') and the fixed coordinate (column or row index).
    Returns None if the pixels don't form a straight line or are empty.
    """
    if not pixels:
        return None

    rows = {r for r, c in pixels}
    cols = {c for r, c in pixels}

    if len(cols) == 1:
        # All pixels share the same column -> vertical line
        return 'vertical', list(cols)[0]
    elif len(rows) == 1:
        # All pixels share the same row -> horizontal line
        return 'horizontal', list(rows)[0]
    else:
        # Not a straight line
        return None

def calculate_average_position(pixels: List[Tuple[int, int]]) -> Optional[Tuple[float, float]]:
    """Calculates the average row and column index for a set of pixels."""
    if not pixels:
        return None
    
    avg_row = sum(r for r, c in pixels) / len(pixels)
    avg_col = sum(c for r, c in pixels) / len(pixels)
    return avg_row, avg_col

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by moving the blue object away from the red line.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Find blue and red pixels
    blue_pixels = find_object_pixels(input_grid, 1)
    red_pixels = find_object_pixels(input_grid, 2)

    # If no blue object or no red line, return the original grid
    if not blue_pixels or not red_pixels:
        return input_grid.copy() # Return a copy to avoid modifying original

    # Determine red line orientation and position
    line_info = determine_line_orientation_and_position(red_pixels)
    if line_info is None:
         # Red pixels don't form a line, return original
        return input_grid.copy()
    orientation, line_pos = line_info

    # Calculate average position of the blue object
    avg_blue_pos = calculate_average_position(blue_pixels)
    if avg_blue_pos is None: # Should not happen if blue_pixels is not empty
        return input_grid.copy()
    blue_avg_row, blue_avg_col = avg_blue_pos

    # Determine the shift vector (dx, dy)
    dx = 0
    dy = 0
    if orientation == 'vertical':
        red_col = line_pos
        # If blue object is to the left (smaller avg col), move right (dx=1)
        # If blue object is to the right (larger avg col), move left (dx=-1)
        dx = 1 if blue_avg_col < red_col else -1
        dy = 0
    elif orientation == 'horizontal':
        red_row = line_pos
        # If blue object is above (smaller avg row), move down (dy=2)
        # If blue object is below (larger avg row), move up (dy=-2)
        dy = 2 if blue_avg_row < red_row else -2
        dx = 0

    # Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros_like(input_grid)

    # Copy the red line from the input to the output
    for r, c in red_pixels:
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
             output_grid[r, c] = 2

    # Apply the shift to the blue pixels and place them in the output grid
    for r, c in blue_pixels:
        new_r, new_c = r + dy, c + dx
        # Check bounds before placing the pixel
        if 0 <= new_r < output_grid.shape[0] and 0 <= new_c < output_grid.shape[1]:
            output_grid[new_r, new_c] = 1
        # else: pixel moves off grid - do nothing based on examples

    return output_grid
```

Previous Code:
```python
import numpy as np
from typing import List, Tuple, Dict, Optional

"""
Moves a blue (1) object relative to a red (2) line.
If the red line is vertical, the blue object moves 1 step horizontally away from the line.
If the red line is horizontal, the blue object moves 2 steps vertically away from the line.
The red line and white (0) background remain unchanged.
"""

def find_object_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    """Finds all coordinates of pixels with the specified color."""
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def determine_line_orientation_and_position(pixels: List[Tuple[int, int]]) -> Optional[Tuple[str, int]]:
    """
    Determines if the pixels form a vertical or horizontal line.
    Returns the orientation ('vertical' or 'horizontal') and the fixed coordinate (column or row index).
    Returns None if the pixels don't form a straight line or are empty.
    """
    if not pixels:
        return None

    rows = {r for r, c in pixels}
    cols = {c for r, c in pixels}

    if len(cols) == 1:
        # All pixels share the same column -> vertical line
        return 'vertical', list(cols)[0]
    elif len(rows) == 1:
        # All pixels share the same row -> horizontal line
        return 'horizontal', list(rows)[0]
    else:
        # Not a straight line
        return None

def calculate_average_position(pixels: List[Tuple[int, int]]) -> Optional[Tuple[float, float]]:
    """Calculates the average row and column index for a set of pixels."""
    if not pixels:
        return None
    
    avg_row = sum(r for r, c in pixels) / len(pixels)
    avg_col = sum(c for r, c in pixels) / len(pixels)
    return avg_row, avg_col

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by moving the blue object away from the red line.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Find blue and red pixels
    blue_pixels = find_object_pixels(input_grid, 1)
    red_pixels = find_object_pixels(input_grid, 2)

    # If no blue object or no red line, return the original grid
    if not blue_pixels or not red_pixels:
        return input_grid.copy() # Return a copy to avoid modifying original

    # Determine red line orientation and position
    line_info = determine_line_orientation_and_position(red_pixels)
    if line_info is None:
         # Red pixels don't form a line, return original
        return input_grid.copy()
    orientation, line_pos = line_info

    # Calculate average position of the blue object
    avg_blue_pos = calculate_average_position(blue_pixels)
    if avg_blue_pos is None: # Should not happen if blue_pixels is not empty
        return input_grid.copy()
    blue_avg_row, blue_avg_col = avg_blue_pos

    # Determine the shift vector (dx, dy)
    dx = 0
    dy = 0
    if orientation == 'vertical':
        red_col = line_pos
        # If blue object is to the left (smaller avg col), move right (dx=1)
        # If blue object is to the right (larger avg col), move left (dx=-1)
        dx = 1 if blue_avg_col < red_col else -1
        dy = 0
    elif orientation == 'horizontal':
        red_row = line_pos
        # If blue object is above (smaller avg row), move down (dy=2)
        # If blue object is below (larger avg row), move up (dy=-2)
        dy = 2 if blue_avg_row < red_row else -2
        dx = 0

    # Initialize the output grid with the background color (white, 0)
    output_grid = np.zeros_like(input_grid)

    # Copy the red line from the input to the output
    for r, c in red_pixels:
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
             output_grid[r, c] = 2

    # Apply the shift to the blue pixels and place them in the output grid
    for r, c in blue_pixels:
        new_r, new_c = r + dy, c + dx
        # Check bounds before placing the pixel
        if 0 <= new_r < output_grid.shape[0] and 0 <= new_c < output_grid.shape[1]:
            output_grid[new_r, new_c] = 1
        # else: pixel moves off grid - do nothing based on examples

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 2 0
0 0 0 0 0 2 0
0 1 1 0 0 2 0
0 1 1 0 0 2 0
0 0 0 0 0 2 0
0 0 0 0 0 2 0
0 0 0 0 0 2 0
```
Expected Output:
```
0 0 0 0 0 2 0
0 0 0 0 0 2 0
0 0 0 1 1 2 0
0 0 0 1 1 2 0
0 0 0 0 0 2 0
0 0 0 0 0 2 0
0 0 0 0 0 2 0
```
Transformed Output:
```
0 0 0 0 0 2 0
0 0 0 0 0 2 0
0 0 1 1 0 2 0
0 0 1 1 0 2 0
0 0 0 0 0 2 0
0 0 0 0 0 2 0
0 0 0 0 0 2 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 8.16326530612244

## Example 2:
Input:
```
0 0 0 0 2 0
0 1 0 0 2 0
0 1 1 0 2 0
0 1 0 0 2 0
0 0 0 0 2 0
0 0 0 0 2 0
```
Expected Output:
```
0 0 0 0 2 0
0 0 1 0 2 0
0 0 1 1 2 0
0 0 1 0 2 0
0 0 0 0 2 0
0 0 0 0 2 0
```
Transformed Output:
```
0 0 0 0 2 0
0 0 1 0 2 0
0 0 1 1 2 0
0 0 1 0 2 0
0 0 0 0 2 0
0 0 0 0 2 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 3:
Input:
```
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
0 0 0 1 1 0 2 0
0 0 1 1 0 0 2 0
0 0 0 1 1 0 2 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
```
Expected Output:
```
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
0 0 0 0 1 1 2 0
0 0 0 1 1 0 2 0
0 0 0 0 1 1 2 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
```
Transformed Output:
```
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
0 0 0 0 1 1 2 0
0 0 0 1 1 0 2 0
0 0 0 0 1 1 2 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
0 0 0 0 0 0 2 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 4:
Input:
```
0 0 0 0 0 0
0 1 1 1 1 1
0 1 0 0 0 1
0 0 0 0 0 0
2 2 2 2 2 2
0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0
0 0 0 0 0 0
0 1 1 1 1 1
0 1 0 0 0 1
2 2 2 2 2 2
0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 1 1 1 1 1
2 1 2 2 2 1
0 0 0 0 0 0
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 55.55555555555557
**General Assessment:**

The initial analysis correctly identified the core components (blue object, red line, background) and the general action (moving the blue object relative to the red line). However, the specific rule for calculating the *distance* of the move was incorrect. The first code attempt assumed fixed distances (1 horizontally, 2 vertically) based on an incomplete perception, leading to failures in examples 1 and 4.

Example 1 failed because the expected horizontal shift was 2, but the code shifted by 1.
Example 4 failed because the expected vertical shift was 1, but the code shifted by 2, causing the blue object to move too far and overwrite parts of the red line in the erroneous output.

The new evidence suggests the shift distance is not fixed but depends on the size of the empty space (gap) between the blue object and the red line.

**Strategy:**

1.  Recalculate the required shift distance based on the gap between the blue object's bounding box and the red line.
2.  Update the YAML facts and Natural Language Program to reflect this gap-based calculation.
3.  Ensure the code correctly determines the bounding box, line orientation, relative position, gap width, and applies the corresponding shift away from the line.

**Metrics:**



*code_execution:*
```python
import numpy as np
from typing import List, Tuple, Dict, Optional

def find_object_pixels(grid: np.ndarray, color: int) -> List[Tuple[int, int]]:
    rows, cols = np.where(grid == color)
    return list(zip(rows, cols))

def get_bounding_box(pixels: List[Tuple[int, int]]) -> Optional[Tuple[int, int, int, int]]:
    """Calculates the bounding box (min_row, min_col, max_row, max_col) for a set of pixels."""
    if not pixels:
        return None
    min_row = min(r for r, c in pixels)
    min_col = min(c for r, c in pixels)
    max_row = max(r for r, c in pixels)
    max_col = max(c for r, c in pixels)
    return min_row, min_col, max_row, max_col

def determine_line_orientation_and_position(pixels: List[Tuple[int, int]]) -> Optional[Tuple[str, int]]:
    """Determines if the pixels form a vertical or horizontal line."""
    if not pixels: return None
    rows = {r for r, c in pixels}
    cols = {c for r, c in pixels}
    if len(cols) == 1: return 'vertical', list(cols)[0]
    elif len(rows) == 1: return 'horizontal', list(rows)[0]
    else: return None

def calculate_gap_width(blue_pixels: List[Tuple[int, int]], red_pixels: List[Tuple[int, int]]) -> Optional[int]:
    """Calculates the gap width (number of background cells) between the blue object's bounding box and the red line."""
    blue_bbox = get_bounding_box(blue_pixels)
    line_info = determine_line_orientation_and_position(red_pixels)

    if not blue_bbox or not line_info:
        return None

    min_r, min_c, max_r, max_c = blue_bbox
    orientation, line_pos = line_info

    gap = -1 # Default invalid gap
    if orientation == 'vertical':
        red_col = line_pos
        if red_col < min_c: # Line is left of object
            gap = min_c - red_col - 1
        elif red_col > max_c: # Line is right of object
            gap = red_col - max_c - 1
        # Implicitly handles case where object touches or overlaps line (gap=0 or negative)
        # But based on examples, they are always separated by at least one background cell.

    elif orientation == 'horizontal':
        red_row = line_pos
        if red_row < min_r: # Line is above object
            gap = min_r - red_row - 1
        elif red_row > max_r: # Line is below object
            gap = red_row - max_r - 1
        # Implicitly handles case where object touches or overlaps line (gap=0 or negative)

    # Return gap only if it's non-negative (>= 0)
    # Based on examples, gap is always >= 1, but we check >= 0 for robustness.
    return gap if gap >= 0 else None

# Input grids for all training examples
grids = [
    # Train 1
    np.array([
        [0,0,0,0,0,2,0], [0,0,0,0,0,2,0], [0,1,1,0,0,2,0], [0,1,1,0,0,2,0],
        [0,0,0,0,0,2,0], [0,0,0,0,0,2,0], [0,0,0,0,0,2,0]
    ]),
    # Train 2
    np.array([
        [0,0,0,0,2,0], [0,1,0,0,2,0], [0,1,1,0,2,0], [0,1,0,0,2,0],
        [0,0,0,0,2,0], [0,0,0,0,2,0]
    ]),
    # Train 3
    np.array([
        [0,0,0,0,0,0,2,0], [0,0,0,0,0,0,2,0], [0,0,0,1,1,0,2,0], [0,0,1,1,0,0,2,0],
        [0,0,0,1,1,0,2,0], [0,0,0,0,0,0,2,0], [0,0,0,0,0,0,2,0], [0,0,0,0,0,0,2,0]
    ]),
    # Train 4
    np.array([
        [0,0,0,0,0,0], [0,1,1,1,1,1], [0,1,0,0,0,1], [0,0,0,0,0,0],
        [2,2,2,2,2,2], [0,0,0,0,0,0]
    ])
]

# Corresponding expected shift amounts based on visual inspection of input/output pairs
# (dx, dy)
expected_shifts = [
    (2, 0), # Example 1: dx=2
    (1, 0), # Example 2: dx=1
    (1, 0), # Example 3: dx=1
    (0, 1)  # Example 4: dy=1
]

results = []
for i, grid in enumerate(grids):
    blue_pixels = find_object_pixels(grid, 1)
    red_pixels = find_object_pixels(grid, 2)
    line_info = determine_line_orientation_and_position(red_pixels)
    blue_bbox = get_bounding_box(blue_pixels)
    gap = calculate_gap_width(blue_pixels, red_pixels)
    
    # Determine shift direction
    shift_dx = 0
    shift_dy = 0
    if line_info and blue_bbox:
        orientation, line_pos = line_info
        min_r, min_c, max_r, max_c = blue_bbox
        gap_width = gap if gap is not None else 0 # Use calculated gap
        
        if orientation == 'vertical':
            shift_dy = 0
            # Determine direction based on relative position
            if line_pos > max_c: # Line is right, move right
                shift_dx = gap_width
            elif line_pos < min_c: # Line is left, move left
                shift_dx = -gap_width # Correction: move AWAY from line
                # If line is at col 5 (line_pos) and blue is at max_c=2, need to move RIGHT (positive dx)
                # If line is at col 1 (line_pos) and blue is at min_c=3, need to move LEFT (negative dx)
                # Check average position? Or bbox edge? Use BBox edge.
                
                # Let's refine direction logic: Move AWAY from line
                blue_center_col = (min_c + max_c) / 2.0
                if blue_center_col < line_pos: # Blue is left of line
                     shift_dx = gap_width # Move right
                else: # Blue is right of line
                     shift_dx = -gap_width # Move left
                     
        elif orientation == 'horizontal':
            shift_dx = 0
            # Determine direction based on relative position
            blue_center_row = (min_r + max_r) / 2.0
            if blue_center_row < line_pos: # Blue is above line
                 shift_dy = gap_width # Move down
            else: # Blue is below line
                 shift_dy = -gap_width # Move up

    results.append({
        "Example": i + 1,
        "Line Info": line_info,
        "Blue BBox": blue_bbox,
        "Calculated Gap Width": gap,
        "Expected Shift (dx, dy)": expected_shifts[i],
        "Calculated Shift (dx, dy)": (shift_dx, shift_dy)
    })

print(results)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
[{'Example': 1, 'Line Info': ('vertical', np.int64(5)), 'Blue BBox': (np.int64(2), np.int64(1), np.int64(3), np.int64(2)), 'Calculated Gap Width': np.int64(2), 'Expected Shift (dx, dy)': (2, 0), 'Calculated Shift (dx, dy)': (np.int64(2), 0)}, {'Example': 2, 'Line Info': ('vertical', np.int64(4)), 'Blue BBox': (np.int64(1), np.int64(1), np.int64(3), np.int64(2)), 'Calculated Gap Width': np.int64(1), 'Expected Shift (dx, dy)': (1, 0), 'Calculated Shift (dx, dy)': (np.int64(1), 0)}, {'Example': 3, 'Line Info': ('vertical', np.int64(6)), 'Blue BBox': (np.int64(2), np.int64(2), np.int64(4), np.int64(4)), 'Calculated Gap Width': np.int64(1), 'Expected Shift (dx, dy)': (1, 0), 'Calculated Shift (dx, dy)': (np.int64(1), 0)}, {'Example': 4, 'Line Info': ('horizontal', np.int64(4)), 'Blue BBox': (np.int64(1), np.int64(1), np.int64(2), np.int64(5)), 'Calculated Gap Width': np.int64(1), 'Expected Shift (dx, dy)': (0, 1), 'Calculated Shift (dx, dy)': (0, np.int64(1))}]

```
The metrics calculation confirms that the "gap width" hypothesis correctly predicts the required shift distance and direction for all training examples. The calculated shifts match the expected shifts.

**YAML Facts:**


```yaml
task_description: Move a blue object away from a red line. The distance moved is equal to the number of background cells separating the blue object's bounding box from the red line.
elements:
  - object: background
    color: white (0)
    role: static_canvas
  - object: primary_shape
    color: blue (1)
    role: movable_object
    properties:
      - shape: variable
      - contiguity: contiguous block of blue pixels
  - object: constraint_line
    color: red (2)
    role: static_constraint
    properties:
      - shape: straight line (vertical or horizontal)
      - contiguity: contiguous block of red pixels
relationships:
  - type: spatial
    description: The blue object is positioned relative to the red line (left/right or above/below), separated by a gap of background cells.
  - type: interaction
    description: The red line dictates the movement (direction and distance) of the blue object.
actions:
  - action: identify_objects
    inputs: [input_grid]
    outputs: [blue_object_pixels, red_object_pixels]
  - action: determine_line_properties
    inputs: [red_object_pixels]
    outputs: [orientation (vertical/horizontal), line_coordinate (col index or row index)]
  - action: determine_object_bounding_box
    inputs: [blue_object_pixels]
    outputs: [min_row, min_col, max_row, max_col]
  - action: calculate_gap_width
    inputs: [blue_object_bounding_box, line_orientation, line_coordinate]
    outputs: [gap_width]
    logic:
      - if line is vertical (at red_col):
        - if red_col > max_col (line right of object): gap = red_col - max_col - 1
        - if red_col < min_col (line left of object): gap = min_col - red_col - 1
      - if line is horizontal (at red_row):
        - if red_row > max_row (line below object): gap = red_row - max_row - 1
        - if red_row < min_r (line above object): gap = min_row - red_row - 1
  - action: calculate_shift_vector
    inputs: [blue_object_bounding_box, line_orientation, line_coordinate, gap_width]
    outputs: [shift_vector (dx, dy)]
    logic:
      - if line is vertical (at red_col):
        - determine relative position (e.g., using blue bounding box center vs red_col)
        - if blue is left of line: dx = gap_width, dy = 0
        - if blue is right of line: dx = -gap_width, dy = 0
      - if line is horizontal (at red_row):
        - determine relative position (e.g., using blue bounding box center vs red_row)
        - if blue is above line: dx = 0, dy = gap_width
        - if blue is below line: dx = 0, dy = -gap_width
  - action: apply_shift
    inputs: [input_grid, blue_object_pixels, red_object_pixels, shift_vector]
    outputs: [output_grid]
    logic:
      - Create a new grid, identical in size to the input grid and initially filled with the background color (white, 0).
      - For each blue pixel at coordinate `(row, col)` in the input grid, calculate the new coordinate `(new_row, new_col) = (row + dy, col + dx)`. If `(new_row, new_col)` is within grid bounds, place a blue pixel there in the output grid.
      - Copy the red line from the input grid to the output grid at its original position (overwriting any blue pixels that might have landed there, although this shouldn't happen based on task logic).

```


**Natural Language Program:**

1.  Identify the coordinates of the blue pixels (color 1) forming the blue object and the red pixels (color 2) forming the red line.
2.  Determine the bounding box of the blue object (minimum row, minimum column, maximum row, maximum column).
3.  Determine the orientation (vertical or horizontal) and the fixed coordinate (column index or row index) of the red line.
4.  Calculate the gap width: the number of background (white, 0) cells strictly between the edge of the blue object's bounding box and the red line.
    *   If the line is vertical at `red_col`:
        *   If the line is to the right of the object (`red_col > max_col`), the gap is `red_col - max_col - 1`.
        *   If the line is to the left of the object (`red_col < min_col`), the gap is `min_col - red_col - 1`.
    *   If the line is horizontal at `red_row`:
        *   If the line is below the object (`red_row > max_row`), the gap is `red_row - max_row - 1`.
        *   If the line is above the object (`red_row < min_row`), the gap is `min_row - red_row - 1`.
5.  Determine the shift vector (`dx`, `dy`) based on the line orientation, gap width, and relative position:
    *   If the line is vertical: `dy = 0`.
        *   If the blue object is to the left of the line, `dx = gap_width` (move right).
        *   If the blue object is to the right of the line, `dx = -gap_width` (move left).
    *   If the line is horizontal: `dx = 0`.
        *   If the blue object is above the line, `dy = gap_width` (move down).
        *   If the blue object is below the line, `dy = -gap_width` (move up).
6.  Create the output grid, same size as the input, filled with the background color (white, 0).
7.  Translate each blue pixel from the input grid by the shift vector (`dx`, `dy`) and draw it onto the output grid, checking boundary conditions.
8.  Copy the red line pixels from their original positions in the input grid onto the output grid.
