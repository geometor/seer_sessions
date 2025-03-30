import numpy as np
from collections import Counter

"""
Replace instances of a 'noise' color (magenta=6) based on a pattern
determined by the two most frequent non-noise colors and the parity of the
pixel's coordinates.

1. Identify the noise color (magenta=6).
2. Find the two most frequent colors in the input grid, excluding the noise color.
   Let the most frequent be C1 and the second most frequent be C2.
   If only one non-noise color exists, C1 = C2 = that color.
   If no non-noise colors exist (e.g., grid is all magenta or empty), default C1 = C2 = white (0).
3. Create an output grid initialized from the input grid.
4. Iterate through each cell (r, c) of the grid.
5. If the input cell `input_grid[r][c]` is the noise color (6):
   a. Determine the replacement color based on coordinate parity:
      - If the row index 'r' is even, the replacement color is C1.
      - If 'r' is odd and the column index 'c' is even, the replacement color is C1.
      - If 'r' is odd and 'c' is odd, the replacement color is C2.
   b. Update the corresponding cell `output_grid[r][c]` with this replacement color.
6. Pixels that were not the noise color remain unchanged.
7. Return the modified output grid.
"""

def find_pattern_colors(grid, noise_color):
    """
    Finds the two most frequent colors in the grid, excluding the noise_color.

    Args:
        grid (np.array): The input grid.
        noise_color (int): The color value to exclude from frequency counting.

    Returns:
        tuple: (C1, C2) where C1 is the most frequent and C2 is the second
               most frequent non-noise color. Handles cases where fewer than
               two non-noise colors are present. Defaults to (0, 0) if no
               non-noise colors are found.
    """
    # Flatten the grid to easily count all pixel values
    pixels = grid.flatten()

    # Count the frequency of each color
    color_counts = Counter(pixels)

    # Remove the noise color from the counts if it exists
    if noise_color in color_counts:
        del color_counts[noise_color]

    # Get the colors sorted by frequency (most common first)
    most_common = color_counts.most_common(2)

    # Determine C1 and C2 based on the number of non-noise colors found
    if len(most_common) == 0:
        # No non-noise colors were found
        c1, c2 = 0, 0  # Default to white
    elif len(most_common) == 1:
        # Only one non-noise color was found
        c1 = most_common[0][0]
        c2 = c1  # Use the same color for C2
    else:
        # Two or more non-noise colors were found
        c1 = most_common[0][0]
        c2 = most_common[1][0]

    return (c1, c2)

def transform(input_grid):
    """
    Transforms the input grid by replacing noise pixels (magenta=6) based on
    a pattern determined by coordinate parity and the two most frequent
    non-noise colors (C1 and C2).

    Args:
        input_grid (list of lists): The input grid represented as a list of lists.

    Returns:
        list of lists: The transformed grid with noise pixels replaced.
    """
    # Convert input list of lists to a NumPy array for efficient operations
    grid_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original non-noise pixels
    output_grid_np = grid_np.copy()
    rows, cols = grid_np.shape

    # Define the noise color to be identified and replaced
    noise_color = 6

    # Determine the primary (C1) and secondary (C2) pattern colors globally
    c1, c2 = find_pattern_colors(grid_np, noise_color)

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel in the original grid is the noise color
            if grid_np[r, c] == noise_color:
                # Apply the parity-based replacement rule
                if r % 2 == 0:
                    # Rule for even rows
                    replacement_color = c1
                else:
                    # Rules for odd rows
                    if c % 2 == 0:
                        # Rule for odd row, even column
                        replacement_color = c1
                    else:
                        # Rule for odd row, odd column
                        replacement_color = c2
                
                # Update the pixel in the output grid
                output_grid_np[r, c] = replacement_color

    # Convert the NumPy array back to a list of lists for the final output format
    output_grid = output_grid_np.tolist()

    return output_grid