import numpy as np
from collections import Counter

"""
Identifies an 8x8 repeating pattern tile underlying the input grid.
Some pixels in the input grid are replaced with white (0), obscuring the pattern.
The transformation reconstructs the most likely 8x8 pattern tile by analyzing the non-white pixels across the entire input grid.
It then fills in the white pixels in the input grid using the reconstructed pattern based on their position relative to the 8x8 tile structure.

Workflow:
1. Define the pattern tile dimensions (H=8, W=8).
2. Create a data structure to store potential colors for each position within the 8x8 tile.
3. Iterate through the input grid. For each non-white pixel, record its color at the corresponding position within the 8x8 tile structure (using modulo H and W).
4. Reconstruct the definitive 8x8 pattern tile by finding the most frequent non-white color recorded for each tile position.
5. Create the output grid by copying the input grid.
6. Iterate through the output grid. If a pixel is white (0), replace it with the color from the reconstructed pattern tile corresponding to its position (using modulo H and W).
7. Return the repaired output grid.
"""

def find_most_common_color(colors):
    """Finds the most common color in a list, ignoring potential errors."""
    if not colors:
        # Should not happen if input always contains non-white examples for each pattern cell
        # If it did, we might return 0 or raise an error. Assuming it won't happen based on examples.
        return 0 
    count = Counter(colors)
    # Find the color with the maximum count
    most_common = count.most_common(1)[0][0]
    return most_common

def transform(input_grid):
    """
    Repairs white pixels in an input grid based on an underlying repeating 8x8 pattern.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    pattern_h, pattern_w = 8, 8

    # Data structure to hold lists of observed colors for each pattern cell
    # Uses nested lists: pattern_colors[tile_row][tile_col] = [color1, color2, ...]
    pattern_colors = [[[] for _ in range(pattern_w)] for _ in range(pattern_h)]

    # Step 1 & 2: Iterate through input grid and collect colors for each pattern cell position
    for r in range(rows):
        for c in range(cols):
            color = input_np[r, c]
            if color != 0:  # Ignore white pixels when building the pattern
                tile_r = r % pattern_h
                tile_c = c % pattern_w
                pattern_colors[tile_r][tile_c].append(color)

    # Step 3: Reconstruct the definitive 8x8 pattern tile
    reconstructed_pattern = np.zeros((pattern_h, pattern_w), dtype=int)
    for tr in range(pattern_h):
        for tc in range(pattern_w):
            # Find the most frequent non-white color for this pattern cell
            reconstructed_pattern[tr, tc] = find_most_common_color(pattern_colors[tr][tc])

    # Step 4: Create the output grid as a copy of the input
    output_grid = np.copy(input_np)

    # Step 5 & 6: Fill white pixels in the output grid using the reconstructed pattern
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == 0:  # If the pixel is white
                tile_r = r % pattern_h
                tile_c = c % pattern_w
                # Replace with the color from the reconstructed pattern
                output_grid[r, c] = reconstructed_pattern[tile_r, tile_c]

    # Step 7: Return the repaired grid
    return output_grid.tolist()