"""
Transforms a 3x2 input grid into a 9x4 output grid based on the following steps:
1. Row Expansion: Each row [A, B] in the input is transformed into a new row [B, A, A, B].
2. Intermediate Grid Formation: The three transformed rows are stacked vertically, maintaining their original order, to form a 3x4 intermediate grid.
3. Pattern Grid (P) Creation: The intermediate grid is flipped vertically (rows reversed) to create the primary 3x4 Pattern Grid (P).
4. Flipped Pattern Grid (P_flipped) Creation: The Pattern Grid (P) is flipped vertically to create the Flipped Pattern Grid (P_flipped).
5. Final Assembly: The output grid is constructed by vertically stacking the Pattern Grid (P), the Flipped Pattern Grid (P_flipped), and the Pattern Grid (P) again, in that order.
"""

import numpy as np

def transform(input_grid):
    """
    Applies the described transformation to the input grid.

    Args:
        input_grid (list of lists): A 3x2 grid represented as a list of lists.

    Returns:
        list of lists: The transformed 9x4 grid.
    """

    # Convert input to numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Initialize a list to hold the rows of the intermediate grid
    intermediate_rows = []

    # Step 1 & 2: Iterate through input rows, transform them, and create the intermediate grid
    for row in input_array:
        pixel_a = row[0]
        pixel_b = row[1]
        # Create the new row [Pixel_B, Pixel_A, Pixel_A, Pixel_B]
        new_row = [pixel_b, pixel_a, pixel_a, pixel_b]
        intermediate_rows.append(new_row)

    # Convert intermediate rows list to a numpy array
    intermediate_grid = np.array(intermediate_rows, dtype=int)

    # Step 3: Create the Pattern Grid (P) by vertically flipping the intermediate grid
    # Slicing [::-1] reverses the rows (vertical flip)
    pattern_grid = intermediate_grid[::-1, :]

    # Step 4: Create the Flipped Pattern Grid (P_flipped) by vertically flipping the Pattern Grid (P)
    flipped_pattern_grid = pattern_grid[::-1, :]

    # Step 5: Assemble the final output grid by vertically stacking P, P_flipped, and P
    # np.vstack concatenates arrays vertically
    output_grid = np.vstack((pattern_grid, flipped_pattern_grid, pattern_grid))

    # Return the final grid as a list of lists
    return output_grid.tolist()