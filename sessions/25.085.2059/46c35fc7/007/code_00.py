# -*- coding: utf-8 -*-
"""
Transforms the input grid by identifying specific 3x3 subgrids and applying one 
of two possible permutations based on the colors in the subgrid's bottom corners.

1.  Initialize the output grid as a copy of the input grid.
2.  Define the background color as orange (7).
3.  Iterate through all possible 3x3 subgrids in the input grid by considering 
    their top-left corner coordinates (r, c).
4.  For each 3x3 subgrid:
    a.  Check if the non-orange pixels within the subgrid span a 3x3 
        bounding box relative to the subgrid itself (the criterion).
    b.  If the criterion is met:
        i.  Examine the colors of the pixels at relative coordinates (2,0) 
            (bottom-left) and (2,2) (bottom-right) within the 3x3 subgrid.
        ii. If Input[2,0] == Input[2,2], apply Permutation P1.
        iii. If Input[2,0] != Input[2,2], apply Permutation P2.
        iv. Apply the selected permutation to rearrange the pixels from the 
            input 3x3 subgrid into a new 3x3 subgrid.
        v.  Place the resulting permuted 3x3 subgrid into the output grid at 
            the corresponding location (r, c).
5.  Return the final output grid.
"""

import numpy as np

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
    # Find coordinates of non-background pixels relative to the 3x3 subgrid
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

def _apply_conditional_permutation(subgrid_3x3):
    """
    Applies one of two pixel rearrangements to a 3x3 subgrid based on its
    bottom corner pixels.

    Args:
        subgrid_3x3 (np.array): A 3x3 numpy array.

    Returns:
        np.array: The rearranged 3x3 numpy array.
    """
    # Create a new 3x3 array to store the result, preserving dtype
    permuted_subgrid = np.zeros_like(subgrid_3x3)

    # Apply the common mappings (Input Row, Input Col) -> (Output Row, Output Col)
    permuted_subgrid[2, 0] = subgrid_3x3[0, 0]
    permuted_subgrid[1, 2] = subgrid_3x3[0, 1]
    permuted_subgrid[0, 0] = subgrid_3x3[0, 2]
    permuted_subgrid[0, 1] = subgrid_3x3[1, 0]
    permuted_subgrid[1, 1] = subgrid_3x3[1, 1] # Center pixel remains
    permuted_subgrid[2, 1] = subgrid_3x3[1, 2]
    permuted_subgrid[1, 0] = subgrid_3x3[2, 1]

    # Apply conditional mappings based on bottom corners
    if subgrid_3x3[2, 0] == subgrid_3x3[2, 2]:
        # Permutation P1 (bottom corners are same)
        permuted_subgrid[0, 2] = subgrid_3x3[2, 0]
        permuted_subgrid[2, 2] = subgrid_3x3[2, 2]
    else:
        # Permutation P2 (bottom corners are different)
        permuted_subgrid[2, 2] = subgrid_3x3[2, 0]
        permuted_subgrid[0, 2] = subgrid_3x3[2, 2]

    return permuted_subgrid

def transform(input_grid):
    """
    Applies a conditional permutation to 3x3 subgrids based on the spatial 
    extent of their non-orange pixels and the colors of their bottom corners.
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

            # Check if this subgrid meets the spatial criterion
            if _check_criterion(subgrid, bg_color):
                # If criterion met, apply the conditional permutation
                permuted_subgrid = _apply_conditional_permutation(subgrid)

                # Place the permuted subgrid into the *output* grid
                output_np[r : r + 3, c : c + 3] = permuted_subgrid

    # Convert the final numpy array back to a list of lists
    return output_np.tolist()