"""
1. Initialize the output grid as a copy of the input grid, filled entirely with the background color (white, 0).
2. Locate the single maroon pixel (9) in the input grid and note its index (`pivot_index`). Place this maroon pixel at the `pivot_index` in the output grid.
3. Identify the contiguous segment of pixels that are not white (0) and not maroon (9). Note the color (`object_color`) and the indices (`object_indices`) of these pixels in the input grid.
4. For each index `i` in the `object_indices`:
   a. Calculate the reflected index `reflected_index = (2 * pivot_index) - i`.
   b. Place the `object_color` at the `reflected_index` in the output grid.
5. Return the completed output grid.
"""

import numpy as np

def find_pivot_index(grid_1d):
    """Finds the index of the pivot pixel (maroon, 9)."""
    for i, pixel in enumerate(grid_1d):
        if pixel == 9:
            return i
    raise ValueError("Pivot pixel (9) not found in the input grid.")

def find_object_pixels(grid_1d, pivot_index):
    """Finds the color and indices of the non-background, non-pivot object."""
    object_color = None
    object_indices = []
    for i, pixel in enumerate(grid_1d):
        # Skip background (0) and pivot (9)
        if pixel != 0 and i != pivot_index:
            if object_color is None:
                # Found the first pixel of the object
                object_color = pixel
                object_indices.append(i)
            elif pixel == object_color:
                # Found another pixel of the same object
                object_indices.append(i)
            else:
                # Found a different color - unexpected based on examples
                # For simplicity, assume only one object color as per examples
                pass 
                
    if object_color is None:
         raise ValueError("Movable object not found in the input grid.")
         
    return object_color, object_indices

def transform(input_grid):
    """
    Transforms the input grid by reflecting the colored object (non-white, non-maroon)
    across the position of the stationary maroon pixel (9).
    
    Args:
        input_grid (list): A 1D list representing the input grid row.

    Returns:
        list: A 1D list representing the transformed output grid row.
    """
    # Convert to numpy array for easier handling if needed, though list is fine for 1D
    grid_1d = np.array(input_grid)
    grid_width = len(grid_1d)

    # --- Find key elements ---
    
    # Find the index of the stationary maroon pivot pixel (9)
    pivot_index = find_pivot_index(grid_1d)

    # Find the color and indices of the movable object
    # The object consists of contiguous pixels that are not background (0) and not the pivot (9)
    object_color, object_indices = find_object_pixels(grid_1d, pivot_index)

    # --- Construct the output grid ---

    # Initialize the output grid with the background color (0)
    output_grid = np.zeros(grid_width, dtype=int)

    # Place the pivot pixel (9) at its original position
    output_grid[pivot_index] = 9

    # Calculate the reflected positions for the object pixels and place the object
    for i in object_indices:
        # Calculate the reflection: distance from pivot is (i - pivot_index)
        # Reflected position is pivot_index - (i - pivot_index) = 2 * pivot_index - i
        reflected_index = 2 * pivot_index - i
        
        # Check bounds (although reflection should stay within bounds given input structure)
        if 0 <= reflected_index < grid_width:
            output_grid[reflected_index] = object_color
        else:
            # This case shouldn't happen based on observed examples where the grid seems large enough.
             print(f"Warning: Reflected index {reflected_index} for original index {i} is out of bounds.")


    # Return the output grid as a standard Python list
    return output_grid.tolist()