import numpy as np

"""
Iterate through each pixel of the input grid. If a pixel's color is neither white (0) nor red (2), check its 8 neighbors (including diagonals) in the input grid. If any neighbor is red (2), change the pixel's color to yellow (4) in the output grid. Otherwise, the pixel retains its original color. White (0) and red (2) pixels remain unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on adjacency to red pixels.

    Args:
        input_grid (list of lists or np.array): The input grid representing pixel colors.

    Returns:
        np.array: The transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)
    rows, cols = input_np.shape

    # Iterate through each cell (pixel) of the input grid
    for r in range(rows):
        for c in range(cols):
            current_color = input_np[r, c]

            # If the current pixel is white (0) or red (2), skip it
            if current_color == 0 or current_color == 2:
                continue

            # Check neighbors for red pixels
            found_red_neighbor = False
            # Define relative coordinates for the 8 neighbors
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    # Skip the center cell itself (dr=0, dc=0)
                    if dr == 0 and dc == 0:
                        continue

                    nr, nc = r + dr, c + dc

                    # Check if the neighbor is within grid boundaries
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if the neighbor in the *input* grid is red (2)
                        if input_np[nr, nc] == 2:
                            found_red_neighbor = True
                            break  # Stop checking neighbors once a red one is found
                if found_red_neighbor:
                    break # Stop checking neighbor rows

            # If a red neighbor was found, change the color in the output grid
            if found_red_neighbor:
                output_grid[r, c] = 4 # Change to yellow

    return output_grid.tolist() # Return as list of lists if required by ARC format