import numpy as np

"""
Transforms a 1-row input grid by expanding isolated non-white pixels into 3-pixel horizontal blocks.

The transformation rule identifies single non-white pixels (color > 0) in the input grid that are horizontally surrounded by white pixels (color 0) or grid boundaries. 
Each such isolated pixel is expanded into a 3-pixel horizontal block of the same color in the output grid. This involves changing the color of the immediate left and right white neighbors (if they exist within the grid bounds) to the color of the isolated pixel. 
Non-white pixels that are already part of a horizontal block wider than one pixel, and all other white pixels, remain unchanged.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list): A list representing the single row of the input grid.
                           It's assumed to be a list of integers (colors).

    Returns:
        list: A list representing the single row of the transformed output grid.
    """
    # Convert input list to a NumPy array for easier manipulation
    # Assuming the input is fundamentally 1D for this task based on examples
    # Wrap it in a list to make it a 1xN 2D array for consistent indexing
    input_np = np.array([input_grid]) 
    
    # Get the dimensions (height will be 1, width is the length)
    height, width = input_np.shape

    # Initialize the output grid as a copy of the input grid
    # Changes will be made directly to this copy
    output_np = np.copy(input_np)

    # Iterate through each pixel of the input grid by its column index
    for c in range(width):
        # Get the color of the current pixel
        pixel_color = input_np[0, c]

        # Check if the pixel is non-white
        if pixel_color > 0:
            # Check horizontal neighbors, treating boundaries as white (0)
            
            # Check left neighbor
            left_neighbor_color = 0 # Assume white if at the left edge
            if c > 0:
                left_neighbor_color = input_np[0, c-1]

            # Check right neighbor
            right_neighbor_color = 0 # Assume white if at the right edge
            if c < width - 1:
                right_neighbor_color = input_np[0, c+1]

            # Determine if the current pixel is isolated (both neighbors are white)
            is_isolated = (left_neighbor_color == 0) and (right_neighbor_color == 0)

            # If the pixel is isolated, expand it in the output grid
            if is_isolated:
                # The pixel itself retains its color (already copied)
                # output_np[0, c] = pixel_color # No change needed due to copy

                # Change the left neighbor in the output grid if it exists
                if c > 0:
                    output_np[0, c-1] = pixel_color
                
                # Change the right neighbor in the output grid if it exists
                if c < width - 1:
                    output_np[0, c+1] = pixel_color

    # Convert the NumPy array back to a list (as per typical ARC format for 1D)
    output_grid = output_np[0].tolist()
    
    return output_grid
