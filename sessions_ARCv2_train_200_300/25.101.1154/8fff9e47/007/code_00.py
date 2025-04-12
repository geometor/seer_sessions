import numpy as np
import math

"""
Transforms an input grid to a fixed 12x12 output grid by scaling and sampling neighbors 
based on empirically derived mappings specific to the scaling factor.

1.  The input grid (H_in x W_in) must have dimensions that are positive integer divisors of 12.
2.  Integer scaling factors are calculated: scale_h = 12 // H_in, scale_w = 12 // W_in.
3.  A specific neighbor offset map is chosen based on the block shape (scale_h, scale_w). 
    These maps define, for each relative position (rel_r, rel_c) within a scaled block, 
    which neighbor offset (dr, dc) relative to the source input pixel (i, j) should be sampled.
    - Map for 2x3 blocks (scale_h=2, scale_w=3):
        (0,0)->(1,1), (0,1)->(-1,0), (0,2)->(1,-1)
        (1,0)->(-1,1), (1,1)->(0,-1), (1,2)->(0,1)
    - Map for 3x2 blocks (scale_h=3, scale_w=2):
        (0,0)->(-1,1), (0,1)->(1,-1)
        (1,0)->(-1,-1), (1,1)->(1,1)
        (2,0)->(0,-1), (2,1)->(0,1)
4.  The output grid (12x12) is generated pixel by pixel. For each output pixel Output[r, c]:
    a.  The corresponding source input pixel (i, j) and relative position (rel_r, rel_c) are calculated.
    b.  The neighbor offset (dr, dc) is retrieved from the chosen map using (rel_r, rel_c).
    c.  The target neighbor coordinate (ni, nj) = (i+dr, j+dc) is calculated.
    d.  If (ni, nj) is within the bounds of the input grid, its color Input[ni, nj] is used.
    e.  If (ni, nj) is out of bounds, the color of the central source pixel Input[i, j] is used instead.
    f.  This color is assigned to Output[r, c].
5.  The completed 12x12 grid is returned.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the scaling and mapped neighbor sampling transformation.

    Args:
        input_grid: The input grid as a list of lists.

    Returns:
        The transformed 12x12 grid as a list of lists.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    H_in, W_in = input_np.shape
    
    # Define fixed output dimensions
    H_out, W_out = 12, 12
    
    # Define the empirically derived neighbor offset maps
    offset_map_2x3 = {
        (0,0): (1,1), (0,1): (-1,0), (0,2): (1,-1),
        (1,0): (-1,1), (1,1): (0,-1), (1,2): (0,1)
    }
    offset_map_3x2 = {
        (0,0): (-1,1), (0,1): (1,-1),
        (1,0): (-1,-1), (1,1): (1,1),
        (2,0): (0,-1), (2,1): (0,1)
    }

    # Validate input dimensions: must be non-zero and divisors of 12
    if H_in <= 0 or W_in <= 0 or H_out % H_in != 0 or W_out % W_in != 0:
        # Return a default 12x12 black grid if dimensions are invalid
        return [[0 for _ in range(W_out)] for _ in range(H_out)]

    # Calculate integer scaling factors
    scale_h = H_out // H_in
    scale_w = W_out // W_in

    # Select the appropriate offset map based on the calculated block shape
    if scale_h == 2 and scale_w == 3:
        offset_map = offset_map_2x3
    elif scale_h == 3 and scale_w == 2:
        offset_map = offset_map_3x2
    else:
        # Handle unexpected block shapes (e.g., return default grid)
        # This case shouldn't occur based on the training examples.
        print(f"Warning: Unsupported block shape ({scale_h}x{scale_w}). Returning default grid.")
        return [[0 for _ in range(W_out)] for _ in range(H_out)]

    # Initialize the output grid with zeros (black)
    output_np = np.zeros((H_out, W_out), dtype=int)

    # Iterate through each pixel coordinate (r, c) of the output grid
    for r in range(H_out):
        for c in range(W_out):
            # Calculate the corresponding source pixel coordinates (i, j) in the input grid
            i = r // scale_h
            j = c // scale_w

            # Calculate the relative coordinates (rel_r, rel_c) within the scaled block
            rel_r = r % scale_h
            rel_c = c % scale_w

            # Look up the neighbor offset (dr, dc) from the selected map
            dr, dc = offset_map.get((rel_r, rel_c), (0, 0)) # Default to (0,0) if key missing, though shouldn't happen

            # Calculate the target neighbor coordinates
            ni = i + dr
            nj = j + dc

            # Determine the color based on boundary checks
            if 0 <= ni < H_in and 0 <= nj < W_in:
                # Neighbor is within bounds: use neighbor's color
                color = input_np[ni, nj]
            else:
                # Neighbor is out of bounds: use the central source pixel's color
                color = input_np[i, j]

            # Assign the determined color to the current output grid pixel
            output_np[r, c] = color

    # Convert the resulting numpy array back to a list of lists and return
    return output_np.tolist()