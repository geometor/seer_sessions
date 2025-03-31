import numpy as np
from typing import List, Set, Tuple, FrozenSet

"""
Transforms an input grid based on the following rules:
1. Identifies a central cross shape made of orange (7) pixels (middle row and middle column). This cross remains unchanged.
2. Identifies all other pixels. If a pixel is not orange (7), it remains unchanged.
3. If a pixel is orange (7) but NOT part of the central cross, its color might change based on its neighbors.
4. To determine the new color for such an orange pixel:
    a. Find all 8 neighbors (cardinal and diagonal).
    b. Collect the colors of these neighbors.
    c. Filter out any orange (7) neighbors.
    d. Create a unique set of the remaining non-orange neighbor colors.
    e. Apply a specific mapping rule based on this set to determine the new color. If no rule matches, the pixel remains orange (7) (though this case doesn't seem to occur in the examples).
5. The output grid is constructed with these changes applied.

Specific Mappings Observed:
- {white(0), blue(1), azure(8)} -> gray(5)
- {blue(1), gray(5), azure(8)} -> white(0)
- {green(3), azure(8), maroon(9)} -> red(2)
- {red(2), azure(8), maroon(9)} -> green(3)
- {green(3), yellow(4)} -> gray(5)
- {green(3), yellow(4), gray(5)} -> yellow(4)
- {green(3), gray(5)} -> yellow(4)
"""

def get_neighbors(r: int, c: int, height: int, width: int) -> List[Tuple[int, int]]:
    """Gets coordinates of 8 neighbors for a given cell (r, c)."""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            nr, nc = r + dr, c + dc
            # Check boundaries
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append((nr, nc))
    return neighbors

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape

    # Determine center row and column indices
    center_row = height // 2
    center_col = width // 2

    # Define the color mapping based on the frozenset of unique non-orange neighbors
    # Using frozenset because sets are mutable and cannot be dictionary keys
    color_map: Dict[FrozenSet[int], int] = {
        frozenset({0, 1, 8}): 5, # white, blue, azure -> gray
        frozenset({1, 5, 8}): 0, # blue, gray, azure -> white
        frozenset({3, 8, 9}): 2, # green, azure, maroon -> red
        frozenset({2, 8, 9}): 3, # red, azure, maroon -> green
        frozenset({3, 4}): 5,    # green, yellow -> gray
        frozenset({3, 4, 5}): 4, # green, yellow, gray -> yellow
        frozenset({3, 5}): 4     # green, gray -> yellow
    }

    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the pixel is orange (7)
            if grid[r, c] == 7:
                # Check if the pixel is part of the central cross
                is_on_cross = (r == center_row) or (c == center_col)

                # If it's an orange pixel *not* on the central cross, apply transformation logic
                if not is_on_cross:
                    # Get neighbors' coordinates
                    neighbor_coords = get_neighbors(r, c, height, width)

                    # Get neighbors' colors from the original input grid
                    neighbor_colors = [grid[nr, nc] for nr, nc in neighbor_coords]

                    # Filter out orange (7) neighbors
                    non_orange_neighbors = [color for color in neighbor_colors if color != 7]

                    # Create a unique set of non-orange neighbor colors
                    unique_non_orange_set = frozenset(non_orange_neighbors)

                    # Determine the new color using the map
                    # If the set is found in the map, change the color in the output grid
                    if unique_non_orange_set in color_map:
                        output_grid[r, c] = color_map[unique_non_orange_set]
                    # If the set is empty or not in the map, it implicitly stays orange (7)
                    # because we copied the grid initially. No action needed here for that case.

            # If pixel is not orange (7), or if it's on the central cross,
            # it remains unchanged (already handled by copying the grid).

    # Convert back to list of lists format if necessary, though numpy array is often fine
    return output_grid.tolist()
