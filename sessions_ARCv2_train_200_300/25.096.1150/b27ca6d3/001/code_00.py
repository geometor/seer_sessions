"""
Transforms an input grid based on the proximity of cells with value 0 to cells with value 2.

1. Cells with value 2 in the input grid remain 2 in the output grid.
2. Cells with value 0 in the input grid become 3 in the output grid if they have at least one neighbor (horizontally, vertically, or diagonally) with value 2 in the input grid.
3. Cells with value 0 in the input grid that do not have any neighbors with value 2 remain 0 in the output grid.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D list of integers representing the input state.

    Returns:
        A 2D list of integers representing the transformed output state.
    """
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize output_grid as a deep copy of the input_grid
    # This handles rule 1 (2s stay 2s) and the default case for rule 3 (0s stay 0s unless changed)
    output_grid = copy.deepcopy(input_grid)

    # Define the relative coordinates for the 8 neighbors (Moore neighborhood)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        ( 0, -1),          ( 0, 1),
        ( 1, -1), ( 1, 0), ( 1, 1),
    ]

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current cell in the input grid is 0 (Rule 2 & 3)
            if input_grid[r][c] == 0:
                # Check its neighbors in the input grid
                found_neighbor_2 = False
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc

                    # Check if the neighbor coordinates are within the grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor cell has a value of 2
                        if input_grid[nr][nc] == 2:
                            found_neighbor_2 = True
                            break # Found a neighbor 2, no need to check others

                # If at least one neighbor was 2, update the output grid cell to 3 (Rule 2)
                if found_neighbor_2:
                    output_grid[r][c] = 3
            # If input_grid[r][c] was 2, it remains 2 in the output_grid (handled by initial copy)
            # If input_grid[r][c] was 0 and no neighbor was 2, it remains 0 (handled by initial copy)


    return output_grid