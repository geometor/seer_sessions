"""
Transforms the input grid by iterating through all possible 3x3 subgrids.
For each 3x3 subgrid, it checks if the non-orange (7) pixels within that 
subgrid span a 3x3 bounding box (relative to the subgrid itself).
If this criterion is met, a specific fixed permutation is applied to the 
pixels of that 3x3 subgrid, and the result is placed in the corresponding 
location in the output grid. Pixels in the output grid that do not belong 
to any such transformed 3x3 subgrid remain identical to the input grid.
The output grid is initialized as a copy of the input grid.
"""

import numpy as np

def _apply_permutation(subgrid_3x3):
    """
    Applies the specific pixel rearrangement to a 3x3 subgrid.

    Args:
        subgrid_3x3 (np.array): A 3x3 numpy array.

    Returns:
        np.array: The rearranged 3x3 numpy array.
    """
    # Create a new 3x3 array to store the result, preserving dtype
    permuted_subgrid = np.zeros_like(subgrid_3x3)

    # Apply the specific mapping
    # (Input Row, Input Col) -> (Output Row, Output Col)
    permuted_subgrid[2, 0] = subgrid_3x3[0, 0]
    permuted_subgrid[1, 2] = subgrid_3x3[0, 1]
    permuted_subgrid[0, 0] = subgrid_3x3[0, 2]
    permuted_subgrid[0, 1] = subgrid_3x3[1, 0]
    permuted_subgrid[1, 1] = subgrid_3x3[1, 1] # Center pixel remains
    permuted_subgrid[2, 1] = subgrid_3x3[1, 2]
    permuted_subgrid[0, 2] = subgrid_3x3[2, 0] # Correction from previous attempt based on NL description
    permuted_subgrid[1, 0] = subgrid_3x3[2, 1]
    permuted_subgrid[2, 2] = subgrid_3x3[2, 2] # Correction from previous attempt based on NL description
    
    return permuted_subgrid

def _check_criterion(subgrid_3x3, bg_color):
    """
    Checks if the non-background pixels within the 3x3 subgrid
    span a 3x3 bounding box relative to the subgrid.

    Args:
        subgrid_3x3 (np.array): The 3x3 subgrid.
        bg_color (int): The background color to ignore.

    Returns:
        bool: True if the criterion is met, False otherwise.
    """
    non_bg_coords = []
    for r in range(3):
        for c in range(3):
            if subgrid_3x3[r, c] != bg_color:
                non_bg_coords.append((r, c))

    # If there are no non-background pixels, criterion is not met
    if not non_bg_coords:
        return False

    # Calculate bounding box relative to the 3x3 subgrid
    min_r = min(r for r, c in non_bg_coords)
    max_r = max(r for r, c in non_bg_coords)
    min_c = min(c for r, c in non_bg_coords)
    max_c = max(c for r, c in non_bg_coords)

    # Calculate height and width of the bounding box
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Check if the bounding box is exactly 3x3
    return height == 3 and width == 3

def transform(input_grid):
    """
    Applies a permutation to 3x3 subgrids based on the spatial extent 
    of their non-orange pixels.
    """
    # Convert input list of lists to a numpy array
    input_np = np.array(input_grid, dtype=int)
    # Initialize output grid as a copy of the input
    output_np = np.copy(input_np)
    rows, cols = input_np.shape
    
    # Define the background color (orange)
    bg_color = 7

    # Iterate through all possible top-left corners (r, c) of 3x3 subgrids
    for r in range(rows - 2):
        for c in range(cols - 2):
            # Extract the 3x3 subgrid from the *input* grid
            subgrid = input_np[r : r + 3, c : c + 3]
            
            # Check if this subgrid meets the criterion
            if _check_criterion(subgrid, bg_color):
                # If criterion met, apply the permutation
                permuted_subgrid = _apply_permutation(subgrid)
                
                # Place the permuted subgrid into the *output* grid
                output_np[r : r + 3, c : c + 3] = permuted_subgrid
                
    # Convert the final numpy array back to a list of lists
    return output_np.tolist()