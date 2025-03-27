"""
Construct a larger grid (3 times the height and width of the input) by selectively 
tiling copies of the input grid based on the locations of its most frequent 
non-background (non-zero) color.

1. Identify the non-zero color that appears most frequently in the input grid. 
   If there's a tie, choose the smallest color value among the tied ones.
2. Create a 'pattern' grid of the same dimensions as the input. Mark cells 'True' 
   where the most frequent color appears in the input, 'False' otherwise.
3. Create an output grid 3 times the height and 3 times the width of the input, 
   filled with the background color (0).
4. Iterate through the 'pattern' grid. If a cell (r, c) is 'True', copy the 
   entire input grid into the corresponding (r, c) block of the output grid. 
   The top-left corner of the block in the output grid is at (r * H, c * W), 
   where H and W are the height and width of the input grid.
"""

import numpy as np
from collections import Counter

def find_most_frequent_nonzero_color(grid):
    """Finds the most frequent non-zero color in the grid. Handles ties by choosing the smallest value."""
    # Flatten the grid and filter out zeros
    non_zeros = [pixel for row in grid for pixel in row if pixel != 0]

    if not non_zeros:
        # Handle case where grid is all zeros or empty
        return None 

    # Count frequencies
    counts = Counter(non_zeros)
    
    # Find the maximum frequency
    max_freq = 0
    for color in counts:
        if counts[color] > max_freq:
            max_freq = counts[color]

    # Find all colors with the maximum frequency
    most_frequent_colors = []
    for color in counts:
        if counts[color] == max_freq:
            most_frequent_colors.append(color)

    # Return the smallest color value among those tied for most frequent
    return min(most_frequent_colors) if most_frequent_colors else None

def transform(input_grid):
    """
    Transforms the input grid based on the tiling rule described above.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Step 1: Find the most frequent non-zero color
    most_frequent_color = find_most_frequent_nonzero_color(input_grid)
    
    # Handle edge case where no non-zero color exists
    if most_frequent_color is None:
         # If no non-zero colors, the pattern grid would be all False,
         # resulting in an all-zero output grid of the target size.
         output_H, output_W = 3 * H, 3 * W
         output_np = np.zeros((output_H, output_W), dtype=int)
         return output_np.tolist()


    # Step 2: Create the boolean pattern grid
    pattern_grid = (input_np == most_frequent_color)

    # Step 3: Initialize the output grid
    output_H, output_W = 3 * H, 3 * W
    output_np = np.zeros((output_H, output_W), dtype=int)

    # Step 4: Populate the output grid based on the pattern grid
    for r in range(H):
        for c in range(W):
            if pattern_grid[r, c]:  # If the pattern is True at (r, c)
                # Calculate the top-left corner for the block in the output grid
                start_row = r * H
                start_col = c * W
                # Calculate the bottom-right corner (exclusive)
                end_row = start_row + H
                end_col = start_col + W
                # Copy the input grid into the corresponding block
                output_np[start_row:end_row, start_col:end_col] = input_np

    # Convert the final numpy array back to a list of lists
    return output_np.tolist()