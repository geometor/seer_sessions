"""
Transforms a 2D grid of integers based on neighborhood interactions.
A non-zero cell's value is reset to zero if it has at least one neighbor 
(in the 8-cell Moore neighborhood) with a different, non-zero value that is
strictly smaller than the cell's own value. Otherwise, the cell retains 
its original value. Zero-valued cells (background) remain unchanged.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the 2D input grid.

    Returns:
        A list of lists representing the transformed 2D output grid.
    """
    
    # Get grid dimensions
    if not input_grid:
        return []
    height = len(input_grid)
    if height == 0:
        return [[]]
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize output_grid as a deep copy of the input_grid
    # This ensures we check neighbors based on the original state
    output_grid = copy.deepcopy(input_grid)

    # Define the 8 neighbor offsets (Moore neighborhood)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1)
    ]

    # Iterate through each cell in the input grid
    for r in range(height):
        for c in range(width):
            cell_value = input_grid[r][c]

            # Skip background cells
            if cell_value == 0:
                continue

            # Flag to determine if the cell should be reset to 0
            reset_cell = False

            # Check all 8 neighbors
            for dr, dc in neighbor_offsets:
                nr, nc = r + dr, c + dc

                # Check if the neighbor coordinates are within the grid bounds
                if 0 <= nr < height and 0 <= nc < width:
                    neighbor_value = input_grid[nr][nc]

                    # Check the conditions for resetting the cell
                    # 1. Neighbor is not background (non-zero)
                    # 2. Neighbor value is different from the current cell value
                    # 3. Neighbor value is smaller than the current cell value
                    if neighbor_value != 0 and neighbor_value != cell_value and neighbor_value < cell_value:
                        reset_cell = True
                        break # Found a neighbor that triggers the reset, no need to check others

            # If the reset flag is true, update the cell in the output grid to 0
            if reset_cell:
                output_grid[r][c] = 0
            # Otherwise, the output_grid already holds the original correct value due to the initial deep copy

    # Return the modified grid
    return output_grid