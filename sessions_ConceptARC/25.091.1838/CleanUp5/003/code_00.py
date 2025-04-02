"""
Processes input grids based on the number and frequency of non-white colors.

1.  Analyze the input grid to identify all distinct non-white colors present and count them.
2.  If there is more than one distinct non-white color:
    a. Find the non-white color with the minimum count ('target color').
    b. Change all pixels with the 'target color' to white (0).
3.  If there is exactly one distinct non-white color ('the_color'):
    a. For each pixel with 'the_color', check its 8 neighbors (Moore neighborhood).
    b. If none of the neighbors also have 'the_color', change the pixel to white (0).
4.  If there are no non-white colors, the output is identical to the input.
White (0) pixels always remain unchanged unless they are the target of a change described above (which doesn't happen in this logic).
"""

import numpy as np
from collections import Counter

# Define relative coordinates for the 8 neighbors (Moore neighborhood)
_NEIGHBOR_OFFSETS = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1), (1, 0), (1, 1)
]

def _has_same_color_neighbor(grid, r, c):
    """
    Checks if the pixel at (r, c) in the grid has any neighbor
    (out of the 8 surrounding cells) with the same color.

    Args:
        grid (np.array): The input grid.
        r (int): Row index of the pixel.
        c (int): Column index of the pixel.

    Returns:
        bool: True if at least one neighbor has the same color, False otherwise.
    """
    rows, cols = grid.shape
    pixel_color = grid[r, c]

    # Iterate through all 8 neighbor positions
    for dr, dc in _NEIGHBOR_OFFSETS:
        nr, nc = r + dr, c + dc
        # Check if the neighbor coordinates are within the grid boundaries
        if 0 <= nr < rows and 0 <= nc < cols:
            # Check if the neighbor pixel has the same color
            if grid[nr, nc] == pixel_color:
                return True # Found a neighbor with the same color

    # If the loop completes without finding a same-colored neighbor
    return False

def transform(input_grid_list):
    """
    Transforms the input grid based on the rules derived from the examples.

    Args:
        input_grid_list (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape
    
    # Initialize the output grid as a copy of the input grid
    output_grid = np.copy(input_grid)

    # --- Analysis Phase ---
    # Find all non-white pixels
    non_white_pixels = input_grid[input_grid != 0]
    
    # Count the occurrences of each non-white color
    color_counts = Counter(non_white_pixels)
    
    # Get the number of distinct non-white colors
    num_distinct_colors = len(color_counts)

    # --- Transformation Logic ---
    
    # Case 1: More than one distinct non-white color
    if num_distinct_colors > 1:
        # Find the color with the minimum count
        # Initialize with a high count and placeholder color
        min_count = float('inf')
        target_color = -1 
        # Iterate through the counts to find the minimum
        # Note: If ties occur, the first color encountered with the minimum count is chosen.
        # Example 1 has counts {2: 19, 3: 9}, so 3 is correctly chosen.
        for color, count in color_counts.items():
            if count < min_count:
                min_count = count
                target_color = color
            # Optional: If counts are equal, could use color value as tie-breaker
            # elif count == min_count and color < target_color:
            #     target_color = color 
                
        # Change all pixels of the target color to white (0) in the output grid
        output_grid[output_grid == target_color] = 0
        
    # Case 2: Exactly one distinct non-white color
    elif num_distinct_colors == 1:
        # Get the single non-white color
        the_color = list(color_counts.keys())[0]
        
        # Iterate through each pixel of the input grid
        for r in range(rows):
            for c in range(cols):
                # Check if the current pixel has 'the_color'
                if input_grid[r, c] == the_color:
                    # Check if it's isolated (has no neighbors of the same color)
                    if not _has_same_color_neighbor(input_grid, r, c):
                        # If isolated, change this pixel to white (0) in the output grid
                        output_grid[r, c] = 0
                        
    # Case 3: No non-white colors (num_distinct_colors == 0)
    # No action needed, the output_grid is already a copy of the input.

    # Convert the final numpy array back to a list of lists format for the ARC standard
    return output_grid.tolist()