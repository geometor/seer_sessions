"""
Identifies all 3x3 subgrids within the input grid where none of the four corner cells (top-left, top-right, bottom-left, bottom-right) match the background color orange (7). For each identified 3x3 subgrid, applies a specific mixed rotation: the four corner pixels and the center pixel are rotated 90 degrees counter-clockwise, while the four edge pixels are rotated 90 degrees clockwise. These transformed 3x3 blocks replace the original blocks in the output grid. Pixels outside these transformed blocks remain unchanged.
"""

import numpy as np

def apply_mixed_rotation(subgrid):
    """
    Applies a mixed rotation to a 3x3 subgrid.
    Corners and center rotate counter-clockwise.
    Edges rotate clockwise.

    Args:
        subgrid (np.ndarray): A 3x3 numpy array.

    Returns:
        np.ndarray: The transformed 3x3 numpy array.
    """
    # Ensure the input is a 3x3 array
    if subgrid.shape != (3, 3):
        raise ValueError("Input subgrid must be 3x3")

    # Create a new 3x3 array to store the result
    output_block = np.zeros_like(subgrid)

    # Apply 90-degree counter-clockwise rotation for corners and center
    output_block[0, 0] = subgrid[0, 2]  # Top-right corner moves to top-left
    output_block[0, 2] = subgrid[2, 2]  # Bottom-right corner moves to top-right
    output_block[2, 0] = subgrid[0, 0]  # Top-left corner moves to bottom-left
    output_block[2, 2] = subgrid[2, 0]  # Bottom-left corner moves to bottom-right
    output_block[1, 1] = subgrid[1, 1]  # Center stays in place (or rotates onto itself)

    # Apply 90-degree clockwise rotation for edges
    output_block[0, 1] = subgrid[1, 0]  # Left edge moves to top edge
    output_block[1, 0] = subgrid[2, 1]  # Bottom edge moves to left edge
    output_block[1, 2] = subgrid[0, 1]  # Top edge moves to right edge
    output_block[2, 1] = subgrid[1, 2]  # Right edge moves to bottom edge

    return output_block

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    
    height, width = input_np.shape
    background_color = 7
    subgrid_size = 3

    # Iterate through all possible top-left corners (r, c) for a 3x3 subgrid
    # The range ensures that the 3x3 subgrid fits entirely within the grid boundaries
    for r in range(height - subgrid_size + 1):
        for c in range(width - subgrid_size + 1):
            
            # Define the coordinates of the four corners of the current 3x3 subgrid
            top_left_coord = (r, c)
            top_right_coord = (r, c + subgrid_size - 1)
            bottom_left_coord = (r + subgrid_size - 1, c)
            bottom_right_coord = (r + subgrid_size - 1, c + subgrid_size - 1)

            # Check if none of the four corner pixels have the background color (7)
            if (input_np[top_left_coord] != background_color and
                input_np[top_right_coord] != background_color and
                input_np[bottom_left_coord] != background_color and
                input_np[bottom_right_coord] != background_color):

                # Extract the 3x3 subgrid from the input grid
                subgrid_to_transform = input_np[r:r + subgrid_size, c:c + subgrid_size]
                
                # Perform the specific mixed rotation
                transformed_subgrid = apply_mixed_rotation(subgrid_to_transform)
                
                # Place the transformed 3x3 block into the output grid at the same position
                output_grid[r:r + subgrid_size, c:c + subgrid_size] = transformed_subgrid

    # Return the modified output grid as a list of lists
    return output_grid.tolist()
