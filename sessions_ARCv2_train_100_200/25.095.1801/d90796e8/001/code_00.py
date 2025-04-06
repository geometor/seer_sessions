"""
Transforms an input grid based on the adjacency of cells with value 2 and 3.
If a cell containing '2' is adjacent (up, down, left, or right) to a cell containing '3' in the input grid,
the cell originally containing '2' is changed to '0' in the output grid,
and the cell originally containing '3' is changed to '8' in the output grid.
All changes are based on the initial adjacencies found in the input grid.
Cells not involved in such a '2'-'3' adjacency retain their original value.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the 2D integer grid.

    Returns:
        A new list of lists representing the transformed 2D grid.
    """
    # Get grid dimensions
    if not input_grid:
        return []
    rows = len(input_grid)
    if rows == 0 or not input_grid[0]:
         return [[] for _ in range(rows)] # Handle empty rows or empty grid
    cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid
    # This ensures cells not involved in the transformation retain their value
    output_grid = copy.deepcopy(input_grid)

    # Sets to store coordinates of cells that need to be changed
    # Using sets automatically handles duplicates if a cell is adjacent to multiple partners
    twos_to_zero = set()
    threes_to_eight = set()

    # Define relative coordinates for adjacent neighbors (Von Neumann neighborhood)
    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)] # right, left, down, up

    # First pass: Identify all pairs of adjacent '2's and '3's based *only* on the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell is a '2'
            if input_grid[r][c] == 2:
                # Check its neighbors
                for dr, dc in neighbors:
                    nr, nc = r + dr, c + dc
                    # Check if neighbor coordinates are within grid bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if the neighbor is a '3' in the original input grid
                        if input_grid[nr][nc] == 3:
                            # Mark this '2' cell to be changed to '0'
                            twos_to_zero.add((r, c))
                            # Mark the adjacent '3' cell to be changed to '8'
                            threes_to_eight.add((nr, nc))
                            # Note: We don't need to break here, as sets handle duplicates.
                            # If a '2' is next to multiple '3's, it's still just one change to 0.
                            # If a '3' is next to multiple '2's, it's still just one change to 8.

    # Second pass: Apply the identified changes to the output grid
    for r, c in twos_to_zero:
        output_grid[r][c] = 0

    for r, c in threes_to_eight:
        output_grid[r][c] = 8

    # Return the modified grid
    return output_grid