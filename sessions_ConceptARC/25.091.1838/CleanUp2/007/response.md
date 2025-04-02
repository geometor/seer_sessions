```python
"""
Transforms an input grid based on the presence and location of white (0) pixels.

If white pixels (color 0) exist, touch the grid's perimeter, and non-white pixels also exist, 
then the transformation preserves the white pixels and replaces all non-white pixels with the 
single most frequent non-white color found in the input grid.

Otherwise (if white pixels are absent, don't touch the perimeter, or no non-white pixels exist), 
the transformation replaces the entire grid with the single most frequent color found in the 
overall input grid.
"""

import numpy as np
from collections import Counter

def _check_perimeter_touch(grid_array, color_value):
    """
    Checks if any pixel of the specified color touches the outer perimeter of the grid.

    Args:
        grid_array (np.array): The input grid as a NumPy array.
        color_value (int): The color value to check for.

    Returns:
        bool: True if the color touches the perimeter, False otherwise.
    """
    height, width = grid_array.shape
    if height == 0 or width == 0:
        return False
    
    # Check top row
    if height > 0 and np.any(grid_array[0, :] == color_value):
        return True
    # Check bottom row (only check if height > 1 to avoid double-checking single row)
    if height > 1 and np.any(grid_array[-1, :] == color_value):
        return True
    # Check left column
    if width > 0 and np.any(grid_array[:, 0] == color_value):
        return True
    # Check right column (only check if width > 1 to avoid double-checking single column)
    if width > 1 and np.any(grid_array[:, -1] == color_value):
        return True
        
    return False

def transform(input_grid):
    """
    Applies the conditional homogenization transformation to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed output grid.
    """
    # Convert input to NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape

    # Handle empty grid case
    if height == 0 or width == 0:
        return []

    # --- Analysis Step ---
    
    # Flatten the grid to easily count all pixels
    all_pixels = input_array.flatten()
    if all_pixels.size == 0: 
        return [] # Safety check for edge cases like 1x0 grid

    # 1. Count all pixel colors
    color_counts = Counter(all_pixels)
    
    # 2. Check the three conditions for the special 'white frame' logic
    # Condition 1: Does white (0) exist?
    has_white_pixels = 0 in color_counts
    
    # Condition 2: Does white touch the perimeter?
    white_touches_perimeter = False
    if has_white_pixels:
        # Use helper function to check perimeter
        white_touches_perimeter = _check_perimeter_touch(input_array, 0)
        
    # Condition 3: Do non-white pixels exist?
    has_non_white_pixels = any(color != 0 for color in color_counts)
    
    # Determine if the special white frame logic applies based on the three conditions
    apply_white_frame_logic = has_white_pixels and white_touches_perimeter and has_non_white_pixels

    # --- Transformation Step ---
    
    # Initialize output array (content will be overwritten)
    # Using zeros_like ensures the same shape and type
    output_array = np.zeros_like(input_array) 

    if apply_white_frame_logic:
        # Branch 1: Preserve white, fill rest with dominant non-white color
        
        # Find all non-white pixels
        non_white_pixels = all_pixels[all_pixels != 0]
        # We know non_white_pixels is not empty because has_non_white_pixels is True
        
        # Count frequencies of non-white pixels
        interior_counts = Counter(non_white_pixels)
        
        # Find the most frequent non-white color
        dominant_interior_color = interior_counts.most_common(1)[0][0]
        
        # Create output grid: Start by filling everything with the dominant non-white color
        output_array = np.full_like(input_array, dominant_interior_color) 
        
        # Identify the locations of the original white pixels
        white_mask = (input_array == 0)
        
        # Put the white pixels (0) back into the output grid at their original locations
        output_array[white_mask] = 0 

    else:
        # Branch 2: Fill entire grid with the overall dominant color
        
        # Find the most frequent color among ALL pixels (calculated earlier in color_counts)
        dominant_overall_color = color_counts.most_common(1)[0][0]
        
        # Create output grid filled entirely with the overall dominant color
        output_array = np.full_like(input_array, dominant_overall_color)

    # Convert the final NumPy array back to the required list of lists format
    output_grid = output_array.tolist()
    
    return output_grid
```