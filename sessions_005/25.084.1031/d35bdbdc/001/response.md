```python
"""
Transforms an input grid based on rules applied to specific 3x3 patterns and preserves gray elements.

1. Create a new empty grid (filled with background color 0) of the same dimensions as the input grid.
2. Define a transformation map for specific 3x3 patterns: (Frame Color, Center Color) -> New Center Color.
3. Search the input grid for 3x3 "target objects" (8 uniform frame pixels F, 1 different center pixel C, F!=0, C!=0).
4. If a target object's (F, C) pair is in the map, copy its frame pixels (F) to the output grid and set the center pixel to the mapped New Center Color.
5. Copy all gray pixels (color 5) from the input grid to their corresponding positions in the output grid.
6. Return the resulting output grid.
"""

import numpy as np

def _is_target_object(grid, r, c, height, width):
    """
    Checks if the 3x3 area starting at (r, c) is a target object.
    Returns (is_target, frame_color, center_color)
    """
    # Check bounds
    if r + 2 >= height or c + 2 >= width:
        return False, None, None

    center_color = grid[r + 1, c + 1]
    frame_color = grid[r, c]

    # Basic checks: non-background colors and different frame/center
    if frame_color == 0 or center_color == 0 or frame_color == center_color:
        return False, None, None

    # Check if all 8 frame pixels match frame_color
    for i in range(3):
        for j in range(3):
            # Skip center pixel check
            if i == 1 and j == 1:
                continue
            # Check boundary pixels
            if grid[r + i, c + j] != frame_color:
                return False, None, None

    return True, frame_color, center_color

def transform(input_grid):
    """
    Applies the transformation rules to the input grid.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Initialize output_grid with background color (0)
    output_grid = np.zeros_like(input_grid_np)

    # Define the transformation map: (Frame Color, Center Color) -> New Center Color
    transformation_map = {
        (3, 4): 2,  # Green frame, Yellow center -> Red center
        (6, 1): 3,  # Magenta frame, Blue center -> Green center
        (1, 4): 8,  # Blue frame, Yellow center -> Azure center
        (8, 3): 2,  # Azure frame, Green center -> Red center
        (1, 2): 9,  # Blue frame, Red center -> Maroon center
        (7, 4): 3,  # Orange frame, Yellow center -> Green center
    }

    # Iterate through the input grid to find and process target objects
    for r in range(height - 2):
        for c in range(width - 2):
            is_target, frame_color, center_color = _is_target_object(input_grid_np, r, c, height, width)

            if is_target:
                # Check if the (Frame Color, Center Color) pair is in the map
                if (frame_color, center_color) in transformation_map:
                    new_center_color = transformation_map[(frame_color, center_color)]

                    # Apply the transformation to the output grid
                    # Copy frame pixels
                    for i in range(3):
                        for j in range(3):
                            if i != 1 or j != 1: # if it's a frame pixel
                                output_grid[r + i, c + j] = frame_color
                    # Set new center pixel
                    output_grid[r + 1, c + 1] = new_center_color

    # Iterate through the input grid again to preserve all gray pixels
    for r in range(height):
        for c in range(width):
            if input_grid_np[r, c] == 5:  # Gray color
                output_grid[r, c] = 5

    return output_grid.tolist()
```