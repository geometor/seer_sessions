import numpy as np

"""
Identify the background color (orange, 7).
Iterate through each pixel of the input grid. If the pixel is not the background color, examine its 8 neighbors. 
Find the maximum color value among neighbors that are neither the background color nor the same color as the current pixel.
If this maximum neighbor color value is greater than the current pixel's color value, change the current pixel's color in the output grid to this maximum neighbor color. 
Otherwise, keep the current pixel's original color. Background pixels remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on neighbor color precedence.
    A non-background pixel changes its color to the maximum color value found among its 
    8 neighbors, provided that neighbor color is not the background color, not its own color,
    and is greater than its own color value.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    rows, cols = input_array.shape
    background_color = 7 # Determined from examples

    # Iterate through each pixel in the grid
    for r in range(rows):
        for c in range(cols):
            current_color = input_array[r, c]

            # Skip background pixels
            if current_color == background_color:
                continue

            max_neighbor_color = -1 # Initialize lower than any possible color

            # Check all 8 neighbors (including diagonals)
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    # Skip the pixel itself
                    if dr == 0 and dc == 0:
                        continue

                    nr, nc = r + dr, c + dc

                    # Check grid boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        neighbor_color = input_array[nr, nc]

                        # Consider only non-background neighbors with different colors
                        if neighbor_color != background_color and neighbor_color != current_color:
                            max_neighbor_color = max(max_neighbor_color, neighbor_color)

            # If a higher-value relevant neighbor was found, update the output grid
            if max_neighbor_color > current_color:
                output_array[r, c] = max_neighbor_color
            # Otherwise, the pixel retains its original color (already set by np.copy)

    # Convert back to list of lists for standard output format
    return output_array.tolist()