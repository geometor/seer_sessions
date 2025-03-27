import numpy as np

"""
1. Create a new output grid with the same dimensions as the input grid.
2. Fill the entire output grid with the gray color (5).
3. Iterate through each pixel of the input grid at coordinates (row, column).
4. If the color of the input pixel is not white (0) and its column index is greater than 0 (i.e., column > 0):
   a. Determine the target position in the output grid by shifting one column to the left: (row, column - 1).
   b. Set the color of the pixel at the target position (row, column - 1) in the output grid to the color of the input pixel at (row, column).
5. The resulting grid is the final output.
"""

def transform(input_grid):
    """
    Transforms the input grid by shifting all non-white pixels one column to the left,
    placing them onto a gray background. Pixels shifted off the left edge are discarded.
    """
    # Convert input to numpy array for easier handling
    input_np = np.array(input_grid)
    height, width = input_np.shape

    # 1. Create a new output grid with the same dimensions as the input grid.
    # 2. Fill the entire output grid with the gray color (5).
    output_grid = np.full((height, width), 5, dtype=int)

    # 3. Iterate through each pixel of the input grid at coordinates (row, column).
    for r in range(height):
        for c in range(width):
            input_color = input_np[r, c]

            # 4. If the color of the input pixel is not white (0) and its column index is greater than 0:
            if input_color != 0 and c > 0:
                # a. Determine the target position: (row, column - 1).
                target_c = c - 1
                # b. Set the color of the pixel at the target position in the output grid.
                output_grid[r, target_c] = input_color

    # 5. The resulting grid is the final output.
    # Convert back to list of lists if necessary, though numpy array is often preferred
    return output_grid.tolist()