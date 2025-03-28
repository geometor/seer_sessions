"""
Transforms a 5x5 input grid into a 3x3 output grid by selecting pixels from specific fixed locations in the input and placing them into corresponding fixed locations in the output.

1. Identify 9 key pixels in the 5x5 input grid based on fixed positions:
   - Corners: (0,0), (0,4), (4,0), (4,4)
   - Center: (2,2)
   - Inner Edges (adjacent to center along diagonals): (1,1), (1,3), (3,1), (3,3)
2. Create a new 3x3 output grid.
3. Place the identified pixels into the output grid according to the mapping:
   (0,0) -> (0,0), (0,4) -> (0,2), (1,1) -> (0,1), (1,3) -> (1,2),
   (2,2) -> (1,1), (3,1) -> (1,0), (3,3) -> (2,1), (4,0) -> (2,0),
   (4,4) -> (2,2)
"""

import numpy as np

def transform(input_grid):
    """
    Applies the described transformation rule to the input grid.

    Args:
        input_grid (list of lists): A 5x5 grid represented as a list of lists.

    Returns:
        list of lists: A 3x3 grid representing the transformed output.
    """
    # Convert input list of lists to a numpy array for easier access
    input_np = np.array(input_grid, dtype=int)

    # Define the size of the output grid
    output_height = 3
    output_width = 3

    # Initialize the output grid with zeros (or any placeholder)
    # Using numpy makes initialization and assignment easier
    output_np = np.zeros((output_height, output_width), dtype=int)

    # Define the mapping from input coordinates to output coordinates
    # Format: (input_row, input_col): (output_row, output_col)
    coord_mapping = {
        (0, 0): (0, 0),  # Top-left corner
        (0, 4): (0, 2),  # Top-right corner
        (1, 1): (0, 1),  # Top edge (from inner)
        (1, 3): (1, 2),  # Right edge (from inner)
        (2, 2): (1, 1),  # Center
        (3, 1): (1, 0),  # Left edge (from inner)
        (3, 3): (2, 1),  # Bottom edge (from inner)
        (4, 0): (2, 0),  # Bottom-left corner
        (4, 4): (2, 2)   # Bottom-right corner
    }

    # Iterate through the defined mapping
    for (input_r, input_c), (output_r, output_c) in coord_mapping.items():
        # Get the pixel value from the input grid at the specified input coordinates
        pixel_value = input_np[input_r, input_c]

        # Place the pixel value into the output grid at the corresponding output coordinates
        output_np[output_r, output_c] = pixel_value

    # Convert the numpy output grid back to a list of lists for the return value
    output_grid = output_np.tolist()

    return output_grid