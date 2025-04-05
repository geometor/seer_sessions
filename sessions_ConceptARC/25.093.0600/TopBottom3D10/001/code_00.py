"""
Transforms an input grid by changing the color of non-zero cells to the most frequent 
non-zero color (dominant color) if they are orthogonally adjacent to a cell 
that already has the dominant color in the original input grid. Background cells (0) 
and cells already having the dominant color remain unchanged.
"""

import numpy as np
from collections import Counter

def find_dominant_color(grid):
    """Finds the non-zero color with the highest frequency in the grid."""
    non_zeros = grid[grid != 0]
    if non_zeros.size == 0:
        return None # No non-zero colors found
    
    counts = Counter(non_zeros)
    dominant_color = counts.most_common(1)[0][0]
    return dominant_color

def transform(input_grid):
    """
    Applies the color spreading transformation based on the dominant color.

    Args:
        input_grid (list of lists): The input 2D grid of integers.

    Returns:
        list of lists: The transformed 2D grid.
    """
    # Convert input to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    
    # Initialize output_grid as a copy of the input
    output_np = np.copy(input_np)

    # Find the dominant non-zero color
    dominant_color = find_dominant_color(input_np)

    # If no dominant color exists (e.g., all zeros), return the original grid
    if dominant_color is None:
        return input_grid

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            current_color = input_np[r, c]

            # Skip background cells (0) and cells already having the dominant color
            if current_color == 0 or current_color == dominant_color:
                continue

            # Check orthogonal neighbors for the dominant color
            has_dominant_neighbor = False
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc

                # Check if neighbor is within grid boundaries
                if 0 <= nr < rows and 0 <= nc < cols:
                    # Check if the neighbor in the *original* input grid has the dominant color
                    if input_np[nr, nc] == dominant_color:
                        has_dominant_neighbor = True
                        break # Found a dominant neighbor, no need to check others

            # If an adjacent cell in the input grid had the dominant color, 
            # change the current cell's color in the output grid
            if has_dominant_neighbor:
                output_np[r, c] = dominant_color

    # Convert back to list of lists for the required output format
    return output_np.tolist()
