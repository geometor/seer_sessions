"""
Scales the input grid by 2x. 
Non-white input pixels are expanded into 2x2 blocks of the same color.
White input pixels are expanded based on their cardinal neighbours:
- If all existing cardinal neighbours are white, the 2x2 output block becomes a diagonal blue (1) pattern: [[1, 0], [0, 1]].
- If any existing cardinal neighbour is non-white, the 2x2 output block remains entirely white (0).
"""

import numpy as np

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described scaling and pattern replacement transformation.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    input_height, input_width = input_np.shape

    # Initialize output grid with white (0)
    output_height = 2 * input_height
    output_width = 2 * input_width
    output_np = np.zeros((output_height, output_width), dtype=int)

    # Iterate through each cell of the input grid
    for r in range(input_height):
        for c in range(input_width):
            input_color = input_np[r, c]
            
            # Determine the top-left coordinates of the corresponding 2x2 block in the output grid
            out_r = 2 * r
            out_c = 2 * c

            # If the input pixel is not white
            if input_color > 0:
                # Fill the 2x2 output block with the input color
                output_np[out_r:out_r+2, out_c:out_c+2] = input_color
            
            # If the input pixel is white
            else: # input_color == 0
                # Check cardinal neighbours in the input grid
                all_neighbours_white = True
                neighbours = []
                # Check up
                if r > 0:
                    neighbours.append(input_np[r-1, c])
                # Check down
                if r < input_height - 1:
                    neighbours.append(input_np[r+1, c])
                # Check left
                if c > 0:
                    neighbours.append(input_np[r, c-1])
                # Check right
                if c < input_width - 1:
                     neighbours.append(input_np[r, c+1])

                # See if any existing neighbour is non-white
                for neighbour_color in neighbours:
                    if neighbour_color > 0:
                        all_neighbours_white = False
                        break
                
                # If all existing neighbours were white (or there were no neighbours)
                if all_neighbours_white:
                    # Set the diagonal blue pattern
                    output_np[out_r, out_c] = 1  # Top-left blue
                    output_np[out_r + 1, out_c + 1] = 1 # Bottom-right blue
                # Else (if any neighbour was non-white), the block remains white (0) - already initialized

    # Convert the NumPy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid