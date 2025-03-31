"""
Identify the background color (most frequent color) in the input grid.
Scan the input grid to find all 3x3 subgrid patterns where:
1. The central pixel has color 'A'.
2. All 8 surrounding pixels (neighbors, including diagonals) have the same color 'B'.
3. Color 'A' is different from color 'B'.
4. Color 'A' is different from the background color.
5. Color 'B' is different from the background color.
If multiple such patterns are found, select the one whose center pixel is located at the highest row index (bottom-most). If there is a tie in row index, select the one with the highest column index (right-most).
Extract and return this selected 3x3 subgrid.
"""

import numpy as np
from collections import Counter

def _find_background_color(grid_np):
    """Finds the most frequent color in the grid."""
    # Handle empty grid case if necessary, though ARC grids are >= 1x1
    if grid_np.size == 0:
        return 0 # Default to white or handle as error
    colors, counts = np.unique(grid_np, return_counts=True)
    background_color = colors[np.argmax(counts)]
    return background_color

def transform(input_grid):
    """
    Identifies and extracts a specific 3x3 pattern from the input grid,
    selecting the bottom-most, right-most one if multiple exist.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The extracted 3x3 pattern, or an empty list if none found.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # Handle grids too small to contain a 3x3 pattern
    if height < 3 or width < 3:
        return [] # Cannot find a 3x3 pattern

    # 1. Identify Background Color
    background_color = _find_background_color(input_grid_np)

    # 2. Scan for Target Pattern and store candidates
    candidates = [] # Store tuples of (row, col, pattern_grid)
    # Iterate through possible center points (r, c) of a 3x3 subgrid
    for r in range(1, height - 1):
        for c in range(1, width - 1):
            # 3. Analyze Subgrid centered at (r, c)
            center_color = input_grid_np[r, c]

            # Get the 8 neighbors
            neighbors = [
                input_grid_np[r-1, c-1], input_grid_np[r-1, c], input_grid_np[r-1, c+1],
                input_grid_np[r,   c-1],                     input_grid_np[r,   c+1],
                input_grid_np[r+1, c-1], input_grid_np[r+1, c], input_grid_np[r+1, c+1]
            ]

            # Check if all neighbors are the same color
            first_neighbor_color = neighbors[0]
            all_neighbors_same = all(n == first_neighbor_color for n in neighbors)

            if all_neighbors_same:
                border_color = first_neighbor_color

                # Check conditions:
                # a. Center color != border color
                # b. Center color != background color
                # c. Border color != background color
                if (center_color != border_color and
                    center_color != background_color and
                    border_color != background_color):

                    # Extract the 3x3 subgrid
                    pattern_grid = input_grid_np[r-1:r+2, c-1:c+2]
                    # Store the candidate along with its center coordinates
                    candidates.append({'row': r, 'col': c, 'grid': pattern_grid})

    # 4. Select the correct candidate if any were found
    if not candidates:
        # No pattern found matching the criteria
        print("Warning: Target pattern not found.")
        return [] 
    elif len(candidates) == 1:
        # Only one candidate, return it
        selected_candidate = candidates[0]
    else:
        # Multiple candidates, select based on position (max row, then max col)
        # Sort by row (descending), then by column (descending)
        candidates.sort(key=lambda x: (x['row'], x['col']), reverse=True)
        selected_candidate = candidates[0] # The first one after sorting is the desired one

    # 5. Return the selected 3x3 subgrid
    # Convert back to list of lists format
    return selected_candidate['grid'].tolist()