```python
"""
Transforms an input 1D grid based on the following rules:
1. Identifies a single 'marker' pixel (maroon, 9) and its index (`marker_index`).
2. Identifies the first contiguous block of pixels (the 'object') whose color is neither background (white, 0) nor the marker color. Notes the object's pixel sequence (`object_pixels`), start index (`original_start_index`), and end index (`original_end_index`).
3. Calculates a new starting index for the object using the formula: `new_start_index = 2 * marker_index - original_end_index`.
4. Creates a new grid of the same size, filled with the background color.
5. Places the marker pixel at its original index (`marker_index`) in the new grid.
6. Places the object's pixels (`object_pixels`) into the new grid, starting at the calculated `new_start_index`.
"""

import numpy as np
from typing import List, Tuple, Optional

# Define constants for colors
BACKGROUND_COLOR = 0
MARKER_COLOR = 9

def find_marker_index(grid: List[int], marker_color: int) -> Optional[int]:
    """Finds the index of the first occurrence of the marker color."""
    for i, pixel in enumerate(grid):
        if pixel == marker_color:
            return i
    return None # Marker not found

def find_object(grid: List[int], exclude_colors: List[int]) -> Optional[Tuple[List[int], int, int]]:
    """
    Finds the first contiguous block of pixels whose color is not in exclude_colors.
    Returns: (object_pixels, start_index, end_index) or None if not found.
    """
    object_pixels = []
    start_index = -1
    end_index = -1
    current_object_color = -1

    for i, pixel in enumerate(grid):
        if pixel not in exclude_colors:
            if start_index == -1: # Start of a potential object
                start_index = i
                current_object_color = pixel
                object_pixels.append(pixel)
            elif pixel == current_object_color: # Continuing the object
                object_pixels.append(pixel)
            else: # Found a different non-excluded color, object ended at i-1
                end_index = i - 1
                return object_pixels, start_index, end_index
        elif start_index != -1: # End of the object block (encountered excluded color)
            end_index = i - 1
            return object_pixels, start_index, end_index

    # Check if object runs until the end of the grid
    if start_index != -1:
        end_index = len(grid) - 1
        return object_pixels, start_index, end_index

    return None # No object found

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to the input grid.
    """
    grid_size = len(input_grid)
    exclude_colors = [BACKGROUND_COLOR, MARKER_COLOR]

    # 1. Find the marker index
    marker_index = find_marker_index(input_grid, MARKER_COLOR)
    if marker_index is None:
        print("Error: Marker pixel not found.")
        return input_grid # Return original grid or raise error

    # 2. Find the object pixels and its original indices
    object_info = find_object(input_grid, exclude_colors)
    if object_info is None:
        print("Error: Movable object not found.")
        return input_grid # Return original grid or raise error
    
    object_pixels, _original_start_index, original_end_index = object_info
    object_length = len(object_pixels)

    # 3. Calculate the new starting index for the object
    # Formula derived from examples: new_start = 2 * marker_pos - original_end
    new_start_index = (2 * marker_index) - original_end_index
    new_end_index = new_start_index + object_length # Calculate expected end index

    # 4. Create a new grid filled with the background color
    output_grid = [BACKGROUND_COLOR] * grid_size

    # 5. Place the marker in the new grid
    if 0 <= marker_index < grid_size:
         output_grid[marker_index] = MARKER_COLOR
    else:
         # This case should ideally not happen if marker is found
         print(f"Warning: Marker index {marker_index} out of bounds for grid size {grid_size}.")


    # 6. Place the object pixels into the new grid at the calculated position
    # Check if the calculated placement is valid within grid bounds
    if 0 <= new_start_index < grid_size and new_end_index <= grid_size:
        for i in range(object_length):
            output_grid[new_start_index + i] = object_pixels[i]
    else:
        # Handle cases where the calculated position might be invalid/out of bounds
        # Based on the examples, this calculation seems robust, but good practice to check.
        print(f"Warning: Calculated object placement [{new_start_index}:{new_end_index}] might be out of bounds for grid size {grid_size}.")
        # Potentially adjust behavior here if needed, e.g., clamp indices or return an error state.
        # For now, attempt placement even if partially out of bounds, relying on list slicing behavior.
        # Note: Python slicing handles out-of-bounds gracefully for assignment length mismatch, 
        # but direct index assignment needs care. The loop above is safer.
        # A slice assignment alternative (less safe if indices are wrong):
        # output_grid[new_start_index:new_end_index] = object_pixels 
        # --> Let's stick to the loop for explicit index checking.
        pass # Continue, potentially placing partial object if start is valid but end goes over

    return output_grid
```