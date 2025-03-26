import numpy as np
from collections import Counter

"""
Identify the two most frequent colors in the input grid. These are designated as "stable colors".
Create an output grid, initially identical to the input grid.
Iterate through each pixel of the input grid.
If a pixel's color is NOT one of the two stable colors, examine its eight neighbors (orthogonal and diagonal).
If any neighbor's color IS one of the stable colors, change the corresponding pixel's color in the output grid to 7 (orange).
If a pixel's color IS one of the stable colors, or if it's not stable but has no stable neighbors, it retains its original color in the output grid.
Return the modified output grid.
"""

def get_neighbors(grid: np.ndarray, r: int, c: int) -> list:
    """
    Gets the colors of the 8 neighbors (Moore neighborhood) of cell (r, c).

    Args:
        grid: The numpy array representing the grid.
        r: The row index of the cell.
        c: The column index of the cell.

    Returns:
        A list containing the colors of the valid neighbors.
    """
    neighbors = []
    rows, cols = grid.shape
    # Iterate through the 3x3 area centered at (r, c)
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            # Skip the central cell itself
            if dr == 0 and dc == 0:
                continue
            # Calculate neighbor coordinates
            nr, nc = r + dr, c + dc
            # Check if the neighbor is within the grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append(grid[nr, nc])
    return neighbors

def transform(input_grid: list) -> list:
    """
    Transforms the input grid based on stable colors and neighbors.

    Identifies the two most frequent colors as 'stable'. Pixels with non-stable
    colors change to orange (7) if they have at least one neighbor with a
    stable color.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    rows, cols = grid_np.shape

    # --- Step 1: Identify Stable Colors ---
    # Calculate color frequencies in the input grid
    if grid_np.size == 0: # Handle empty grid case
        return []
    color_counts = Counter(grid_np.flatten())

    # Find the two most frequent colors.
    # Sort first by frequency (descending), then by color value (ascending) for consistent tie-breaking.
    sorted_colors = sorted(color_counts.items(), key=lambda item: (-item[1], item[0]))

    # Determine the set of stable colors (top 2)
    stable_colors = set()
    if len(sorted_colors) > 0:
        stable_colors.add(sorted_colors[0][0])
    if len(sorted_colors) > 1:
        stable_colors.add(sorted_colors[1][0])
    # Note: If there are fewer than 2 unique colors, stable_colors will contain only those available.

    # --- Step 2: Initialize Output Grid ---
    # Create a copy of the input grid to modify
    output_grid_np = np.copy(grid_np)

    # --- Step 3: Process Each Pixel ---
    # Iterate through each cell (pixel) in the grid
    for r in range(rows):
        for c in range(cols):
            current_color = grid_np[r, c]

            # --- Check if the current pixel's color is NOT stable ---
            if current_color not in stable_colors:
                # --- Examine Neighbors ---
                neighbors = get_neighbors(grid_np, r, c)

                # --- Check if any neighbor has a stable color ---
                has_stable_neighbor = False
                for neighbor_color in neighbors:
                    if neighbor_color in stable_colors:
                        has_stable_neighbor = True
                        break # Found a stable neighbor, no need to check further

                # --- Change color to orange (7) if a stable neighbor was found ---
                if has_stable_neighbor:
                    output_grid_np[r, c] = 7

            # --- If the current pixel's color IS stable ---
            # No action is needed; the output grid retains the original color from the copy.

    # --- Step 4: Return Output Grid ---
    # Convert the numpy array back to a list of lists format
    return output_grid_np.tolist()