import numpy as np
from scipy.ndimage import distance_transform_cdt

"""
Identifies objects composed of nested, concentric frames against a white (0) background.
For each object, determines the sequence of frame colors from outermost to innermost.
Reverses this sequence of colors.
Reconstructs the object in the output grid, preserving its shape and location, but applying the reversed color sequence to the frames.
The outermost frame layer receives the color of the original innermost frame layer, the second outermost receives the color of the second innermost, and so on.
"""

def transform(input_grid):
    """
    Transforms the input grid by reversing the color sequence of nested frames within objects.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input grid to a numpy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Create an output array initialized with background color (0)
    output_array = np.zeros_like(input_array)

    # Create a boolean mask where True indicates background pixels (color 0)
    is_background = (input_array == 0)

    # Calculate the Chebyshev distance (chessboard distance) from each pixel
    # to the nearest background pixel. For non-background pixels, this effectively
    # gives the layer depth of the frame, starting from 1 for the outermost frame.
    # Background pixels will have a distance of 0.
    depth_grid = distance_transform_cdt(is_background, metric='chessboard')

    # Find the maximum depth value across the entire grid. This represents
    # the number of layers in the "deepest" object structure.
    max_depth = np.max(depth_grid)

    # If max_depth is 0, it means the grid is all background or empty.
    if max_depth == 0:
        return input_grid # Return the original grid

    # Create a map to store the original color associated with each depth layer.
    # We assume that all pixels at a given depth within a single nested structure
    # share the same color, as per the examples.
    depth_to_color = {}
    for d in range(1, max_depth + 1):
        # Find coordinates where the depth grid equals the current depth d
        coords = np.argwhere(depth_grid == d)
        if len(coords) > 0:
            # Get the color from the input array at the first coordinate found for this depth
            r, c = coords[0]
            depth_to_color[d] = input_array[r, c]
        # else: # Should not happen if max_depth >= 1, but handle defensively if needed
            # Handle case where a depth layer might theoretically exist but has no pixels (unlikely with cdt)
            # pass or assign a default/error value

    # Iterate through each pixel of the grid to build the output
    for r in range(height):
        for c in range(width):
            # Get the depth of the current pixel
            current_depth = depth_grid[r, c]

            # If the current pixel is part of a frame (depth > 0)
            if current_depth > 0:
                # Calculate the target depth for the color swap
                # Outermost (depth 1) swaps with innermost (depth max_depth)
                # Second outermost (depth 2) swaps with second innermost (depth max_depth - 1)
                # etc.
                target_depth = max_depth - current_depth + 1
                
                # Get the color corresponding to the target depth
                # Handle potential missing keys defensively, though unlikely if map built correctly
                new_color = depth_to_color.get(target_depth, 0) # Default to background if something went wrong
                
                # Assign the new color to the output grid
                output_array[r, c] = new_color
            else:
                # If it's a background pixel, keep it as background (already initialized to 0)
                pass # output_array[r, c] is already 0

    # Convert the resulting numpy array back to a list of lists
    output_grid = output_array.tolist()

    return output_grid