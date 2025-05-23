import numpy as np

"""
The transformation identifies all 3x3 subgrids within the input grid that contain at least one pixel color different from orange (7). 
For each such 3x3 subgrid found, the 8 pixels forming its border are rotated 90 degrees counter-clockwise around the center pixel of the subgrid. 
The center pixel of the 3x3 subgrid remains unchanged. Pixels outside of any identified 3x3 subgrid also remain unchanged. The output grid has the same dimensions as the input grid.
"""

def rotate_3x3_border_ccw(subgrid):
    """
    Rotates the 8 border cells of a 3x3 numpy array 90 degrees counter-clockwise.
    
    Args:
        subgrid (np.ndarray): A 3x3 numpy array.
        
    Returns:
        np.ndarray: A new 3x3 numpy array with the border rotated.
    """
    # Coordinates of the border cells relative to the 3x3 subgrid, clockwise
    border_coords = [
        (0, 0), (0, 1), (0, 2), (1, 2), (2, 2), (2, 1), (2, 0), (1, 0)
    ]
    
    # Extract border values
    border_values = np.array([subgrid[r, c] for r, c in border_coords])
    
    # Rotate values 2 positions counter-clockwise (equivalent to a left shift of 2)
    # A 90-degree CCW rotation moves the value at index i to index (i - 2) % 8.
    # np.roll with a shift of -2 achieves this.
    rotated_values = np.roll(border_values, -2) 
    
    # Create the new 3x3 grid, starting with a copy
    new_subgrid = np.copy(subgrid)
    
    # Place rotated values back onto the border
    for i, (r, c) in enumerate(border_coords):
        new_subgrid[r, c] = rotated_values[i]
        
    # The center subgrid[1, 1] is already correct due to np.copy
    return new_subgrid

def transform(input_grid):
    """
    Applies the transformation rule: finds 3x3 subgrids with non-background colors
    and rotates their borders 90 degrees counter-clockwise.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed grid as a list of lists.
    """
    # Convert input to numpy array for easier slicing and manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_np = np.copy(input_np)
    # Get grid dimensions
    H, W = input_np.shape
    # Define the background color
    background_color = 7

    # Iterate through all possible top-left corners (r, c) for a 3x3 subgrid
    # The range ends at H-2 and W-2 to ensure a full 3x3 subgrid fits
    for r in range(H - 2):
        for c in range(W - 2):
            # Extract the 3x3 subgrid from the *original* input grid
            subgrid = input_np[r:r+3, c:c+3]

            # Check if the subgrid contains any cell value other than the background color
            if np.any(subgrid != background_color):
                # If it does, apply the 90-degree counter-clockwise rotation to its border
                rotated_subgrid = rotate_3x3_border_ccw(subgrid)
                # Place the resulting rotated subgrid into the corresponding location in the output grid
                # Modifications are made to the output_np array
                output_np[r:r+3, c:c+3] = rotated_subgrid

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_np.tolist()
