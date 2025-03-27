```python
import numpy as np
from collections import deque

"""
Identify connected components (objects) of non-background (non-blue/1) pixels.
For each object, check if it contains both azure (8) pixels and at least one yellow (4) pixel.
If an object meets this criteria (is a "target object"):
  Find the location (column index) of a yellow (4) pixel within it (the "anchor pixel").
  Determine the grid's vertical midpoint column index (width // 2).
  If the anchor pixel's column index is less than the midpoint, the object is shifted 3 columns to the right.
  If the anchor pixel's column index is greater than or equal to the midpoint, the object is shifted 3 columns to the left.
All other objects (those not containing both azure and yellow) and the background pixels remain in their original positions.
The output grid is constructed by placing the shifted target objects and the unchanged elements onto a background grid.
"""

def find_objects(grid_np, background_color):
    """
    Finds connected objects of non-background pixels using BFS.

    Args:
        grid_np (np.array): The input grid.
        background_color (int): The color considered as background.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'pixels' (list of (r, c, color)), 'has_azure',
              'has_yellow', and 'yellow_loc' (first found).
    """
    height, width = grid_np.shape
    visited = set()
    all_objects = []

    for r in range(height):
        for c in range(width):
            # If this pixel is background or already visited, skip
            if grid_np[r, c] == background_color or (r, c) in visited:
                continue

            # Start BFS for a new object
            current_object_pixels = []
            q = deque([(r, c)])
            visited.add((r, c))
            has_azure = False
            has_yellow = False
            yellow_pixel_loc = None # Store the first yellow pixel found

            while q:
                row, col = q.popleft()
                color = grid_np[row, col]
                current_object_pixels.append((row, col, color))

                # Check object properties
                if color == 8:
                    has_azure = True
                if color == 4:
                    has_yellow = True
                    if yellow_pixel_loc is None: # Store only the first one encountered
                         yellow_pixel_loc = (row, col)

                # Explore neighbors (8-connectivity: includes diagonals)
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row + dr, col + dc

                        # Check bounds and if neighbor is part of the object
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid_np[nr, nc] != background_color and \
                           (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))

            # Store the found object and its properties
            all_objects.append({
                "pixels": current_object_pixels,
                "has_azure": has_azure,
                "has_yellow": has_yellow,
                "yellow_loc": yellow_pixel_loc
            })

    return all_objects


def transform(input_grid):
    """
    Transforms the input grid based on shifting rules applied to specific objects.
    Objects containing both azure (8) and yellow (4) pixels are shifted horizontally.
    The shift direction depends on the column of the yellow pixel relative to the grid's midpoint.
    Shift is +3 columns (right) if yellow_col < midpoint, -3 columns (left) if yellow_col >= midpoint.
    Other objects and the background remain unchanged.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Assuming the most frequent color is background if not specified.
    # For train_1, background is blue (1). Let's hardcode for now based on analysis.
    background_color = 1 
    
    # Determine midpoint and shift amount
    midpoint_col = width // 2
    shift_amount = 3

    # Initialize output grid with the background color
    output_np = np.full_like(input_np, background_color)

    # Find all connected objects of non-background colors
    objects = find_objects(input_np, background_color)

    # Process each object
    for obj_data in objects:
        obj_pixels = obj_data["pixels"]
        is_target_object = obj_data["has_azure"] and obj_data["has_yellow"]

        if is_target_object:
            # This is a target object, determine shift based on yellow pixel location
            _ , anchor_col = obj_data["yellow_loc"] # Get column of the yellow pixel
            
            if anchor_col < midpoint_col:
                # Shift right
                shift = shift_amount
            else:
                # Shift left
                shift = -shift_amount

            # Apply shift and draw the object in the new location
            for r, c, color in obj_pixels:
                new_c = c + shift
                # Draw the pixel if the new column is within grid bounds
                if 0 <= new_c < width:
                    output_np[r, new_c] = color
        else:
            # This is not a target object, draw it in its original position
            for r, c, color in obj_pixels:
                 # Basic bounds check (shouldn't be needed for original positions)
                 if 0 <= r < height and 0 <= c < width:
                    output_np[r, c] = color

    # Convert the result back to a list of lists
    return output_np.tolist()
```