"""
Transforms an input grid by scaling each pixel into a square block in the output grid.
The size of the square block (scaling factor) is determined by the total count of non-white (non-zero) pixels in the input grid.

1. Count the number of non-zero pixels in the input grid. This count is the scaling factor, F.
2. Determine the input grid dimensions (H, W).
3. Calculate the output grid dimensions: (H * F, W * F).
4. Create an output grid of the calculated dimensions, initialized with white (0).
5. Iterate through each pixel (r, c) of the input grid.
6. Get the color C of the input pixel at (r, c).
7. Determine the top-left corner (output_row, output_col) of the corresponding block in the output grid: output_row = r * F, output_col = c * F.
8. Fill an F x F block in the output grid starting at (output_row, output_col) with the color C.
9. Return the completed output grid.
"""

import numpy as np

def _count_non_zero_pixels(grid):
  """Counts the number of non-zero pixels in a grid."""
  return np.count_nonzero(grid)

def transform(input_grid):
    """
    Scales an input grid based on the count of its non-zero pixels.

    Args:
        input_grid (list of lists or numpy array): The input grid.

    Returns:
        numpy array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)

    # 1. Determine Scaling Factor (F)
    scaling_factor = _count_non_zero_pixels(input_np)

    # Handle edge case where scaling factor is 0 (all white input)
    if scaling_factor == 0:
        # Decide on behavior: return empty grid, original grid, or error?
        # Based on examples, it seems unlikely, but let's return an empty grid of size 0x0
        # Or perhaps return a grid of the same size but all white?
        # Let's assume the factor is at least 1 if there's input. If truly 0,
        # output dimensions would be 0x0. Let's stick to the derived logic.
        # An F=0 implies output_H=0, output_W=0.
        return np.array([[]], dtype=int) # Or just np.zeros((0,0), dtype=int) ?
                                        # The latter seems more correct dimensionally.
                                        # Let's refine: if input is 1x1 and 0, F=0, output is 0x0.
                                        # If input is 2x2 and all 0, F=0, output is 0x0.
        # Check if input is empty first
    if input_np.size == 0:
        return np.array([[]], dtype=int) # Return empty if input is empty

    if scaling_factor == 0 and input_np.size > 0:
         # If input is not empty but all zeros, F=0. Output size H*0 x W*0 = 0x0.
         return np.zeros((0,0), dtype=int)


    # 2. Get Input Dimensions (H, W)
    input_height, input_width = input_np.shape

    # 3. Calculate Output Size
    output_height = input_height * scaling_factor
    output_width = input_width * scaling_factor

    # 4. Create Output Grid (initialize with white/0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 5. Scale and Place Pixels
    for r in range(input_height):
        for c in range(input_width):
            # 6. Get input color
            color = input_np[r, c]

            # Only need to fill if the color is non-zero, otherwise it's already 0
            if color != 0:
                 # 7. Calculate output block top-left corner
                 output_row_start = r * scaling_factor
                 output_col_start = c * scaling_factor

                 # 8. Fill the F x F block in the output grid
                 output_row_end = output_row_start + scaling_factor
                 output_col_end = output_col_start + scaling_factor
                 output_grid[output_row_start:output_row_end, output_col_start:output_col_end] = color

    # Return the result as a numpy array (common in ARC)
    return output_grid