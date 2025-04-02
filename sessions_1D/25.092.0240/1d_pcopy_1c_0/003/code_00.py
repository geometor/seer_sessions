"""
Transforms a 1xN input grid by expanding isolated non-white pixels into 3-pixel horizontal lines.

Specifically:
1. Takes a 2D grid (list of lists) with shape 1xN as input.
2. Initializes an output grid as a copy of the input grid.
3. Identifies the primary non-white color present in the input grid. If none exists, returns the copy.
4. Iterates through each column index `c` of the input grid's single row (row 0).
5. If a pixel at location (0, c) has the non-white color and both its left neighbor (if `c > 0`) and right neighbor (if `c < width-1`) are white (color 0), it is considered "isolated". Pixels at the edges are considered isolated if their single existing neighbor is white.
6. For each isolated pixel found at location (0, c), the corresponding pixels at locations (0, c-1), (0, c), and (0, c+1) in the output grid are set to the non-white color (respecting grid boundaries).
7. Pixels that are not part of an expansion or were already part of a non-white sequence retain their original color from the initial copy.
8. Returns the modified output grid as a list of lists.
"""

import numpy as np

def find_non_white_color(grid_array):
  """Finds the first non-white color in the grid array."""
  # Find unique non-zero elements
  unique_colors = np.unique(grid_array)
  non_white_colors = unique_colors[unique_colors != 0]
  if non_white_colors.size > 0:
    return non_white_colors[0]
  return None # Return None if grid is all white or empty

def transform(input_grid):
    """
    Applies the transformation rule to the 1xN input grid.

    Args:
      input_grid: A list of lists representing the 1xN input grid.

    Returns:
      A list of lists representing the transformed 1xN output grid.
    """
    # Convert list of lists to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    
    # Handle empty input case (e.g., [[], []] or [])
    if input_array.size == 0:
        # Need to return structure consistent with input (list of lists)
        # If input was [], return []. If input was [[]], return [[]].
        if isinstance(input_grid, list) and len(input_grid) == 1 and isinstance(input_grid[0], list) and len(input_grid[0]) == 0:
             return [[]]
        return [] # Should ideally match input structure more robustly if needed
        
    # Get dimensions (should be 1xN)
    height, width = input_array.shape
    
    # Ensure input is indeed 1xN, although ARC constraints usually handle this
    if height != 1:
        # Or raise an error, depending on desired behavior for invalid input
        print(f"Warning: Expected input height 1, got {height}. Processing first row only.") 
        # Alternatively return input_grid unchanged if strict 1xN required

    # Initialize output_grid as a copy of the input_grid
    output_array = np.copy(input_array)

    # Determine the primary non-white color
    object_color = find_non_white_color(input_array)

    # If there's no non-white color, return the copy converted back to list of lists
    if object_color is None:
        return output_array.tolist()

    # Iterate through each column of the input grid's first (only) row
    for c in range(width):
        # Check if the current pixel is the object color
        if input_array[0, c] == object_color:
            # Check if it's isolated
            # Check left neighbor (handle boundary c=0)
            is_left_white = (c == 0) or (input_array[0, c - 1] == 0)
            # Check right neighbor (handle boundary c=width-1)
            is_right_white = (c == width - 1) or (input_array[0, c + 1] == 0)

            # If both neighbors are white (or non-existent due to boundary), it's isolated
            if is_left_white and is_right_white:
                # Modify the output grid: expand the pixel
                
                # Set the center pixel (0, c) - already correct from copy, but explicit is fine
                output_array[0, c] = object_color 
                
                # Change left neighbor if it exists (c > 0)
                if c > 0:
                    output_array[0, c - 1] = object_color
                    
                # Change right neighbor if it exists (c < width - 1)
                if c < width - 1:
                    output_array[0, c + 1] = object_color

    # Convert the final numpy array back to a list of lists before returning
    return output_array.tolist()