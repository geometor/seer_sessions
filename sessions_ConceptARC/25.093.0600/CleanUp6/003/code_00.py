import numpy as np
from collections import Counter

"""
Transforms a 2D grid based on color frequency and connectivity.

1.  Identifies all non-zero colors and their frequencies in the input grid.
2.  Determines the maximum frequency among these colors.
3.  Identifies all colors ('dominant candidates') that occur with this maximum frequency.
4.  Applies a tie-breaking rule if multiple dominant candidates exist: A candidate color is disqualified if *all* of its occurrences in the input grid are 'isolated' (i.e., have no orthogonally adjacent neighbors of the same color). Otherwise, it remains a 'kept color'. If there was only one dominant candidate initially, it is automatically a 'kept color'.
5.  Creates an output grid initialized with zeros.
6.  Iterates through the input grid. For each cell containing a 'kept color', it checks if that cell has at least one orthogonally adjacent neighbor in the input grid that also contains the *same* kept color.
7.  If a cell contains a kept color and has at least one neighbor of the same color, its color is copied to the corresponding cell in the output grid.
8.  All other cells in the output grid (background, minority colors, disqualified dominant colors, and isolated kept colors) remain zero.
"""

def _get_color_frequencies(grid_np):
    """Counts frequencies of non-zero colors."""
    colors, counts = np.unique(grid_np[grid_np != 0], return_counts=True)
    return dict(zip(colors, counts))

def _has_neighbor_of_same_color(grid_np, r, c, color):
    """Checks if cell (r, c) has an orthogonal neighbor with the specified color."""
    rows, cols = grid_np.shape
    # Define orthogonal neighbor offsets
    neighbors_coords = [(r - 1, c), (r + 1, c), (r, c - 1), (r, c + 1)]

    for nr, nc in neighbors_coords:
        # Check bounds
        if 0 <= nr < rows and 0 <= nc < cols:
            # Check color
            if grid_np[nr, nc] == color:
                return True
    return False

def _is_color_entirely_isolated(grid_np, color):
    """Checks if ALL occurrences of a color are isolated."""
    rows, cols = grid_np.shape
    found_connected = False
    for r in range(rows):
        for c in range(cols):
            if grid_np[r, c] == color:
                if _has_neighbor_of_same_color(grid_np, r, c, color):
                    # Found at least one connected instance, so not entirely isolated
                    return False
    # If loop completes without finding a connected instance, it's entirely isolated
    return True


def transform(input_grid):
    """
    Applies the transformation rule based on frequency, tie-breaking, and connectivity.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    output_grid_np = np.zeros_like(input_np)

    # 1 & 2: Get color frequencies
    color_counts = _get_color_frequencies(input_np)

    if not color_counts: # Handle empty or all-zero grid
        return output_grid_np.tolist()

    # 3: Determine dominant candidates
    max_freq = max(color_counts.values())
    dominant_candidates = [color for color, count in color_counts.items() if count == max_freq]

    # 4: Apply tie-breaking rule
    kept_colors = set() # Use a set for efficient lookup
    if len(dominant_candidates) > 1:
        for color in dominant_candidates:
            # Keep the color if it's NOT entirely isolated
            if not _is_color_entirely_isolated(input_np, color):
                kept_colors.add(color)
    elif len(dominant_candidates) == 1:
         # If only one dominant color, it's automatically kept (no tie-breaking needed)
         # We still need to check isolation later cell-by-cell
         kept_colors.add(dominant_candidates[0])
    
    # If tie-breaking resulted in no kept colors (e.g., all candidates were purely isolated)
    if not kept_colors:
         return output_grid_np.tolist()

    # 5, 6, 7: Filter grid based on kept colors and connectivity
    for r in range(rows):
        for c in range(cols):
            current_color = input_np[r, c]
            # Check if it's one of the final kept colors
            if current_color in kept_colors:
                # Check if this specific instance is connected to a neighbor of the same color
                if _has_neighbor_of_same_color(input_np, r, c, current_color):
                    output_grid_np[r, c] = current_color
            # Otherwise, the output cell remains 0 (minority, disqualified, or isolated kept color)

    # 8: Return the final grid
    return output_grid_np.tolist()