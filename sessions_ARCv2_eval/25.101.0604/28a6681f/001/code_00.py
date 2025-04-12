"""
Transforms a 2D grid by changing the value of certain cells from 0 to 1 based on their orthogonal neighbors.
A cell's value is changed from 0 to 1 if it is directly flanked either horizontally or vertically by two identical, non-zero neighboring cells in the input grid. Otherwise, the cell's value remains unchanged.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed output grid.
    """
    # Initialize output_grid as a deep copy of the input grid
    output_grid = copy.deepcopy(input_grid)
    
    # Get grid dimensions
    rows = len(input_grid)
    if rows == 0:
        return output_grid # Handle empty grid case
    cols = len(input_grid[0])
    if cols == 0:
        return output_grid # Handle empty row case

    # Iterate through each cell in the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current cell value in the input grid is 0
            if input_grid[r][c] == 0:
                # Check for horizontal flanking
                # Check if left neighbor exists (c > 0)
                has_left_neighbor = c > 0
                # Check if right neighbor exists (c < cols - 1)
                has_right_neighbor = c < cols - 1
                
                if has_left_neighbor and has_right_neighbor:
                    left_neighbor_val = input_grid[r][c-1]
                    right_neighbor_val = input_grid[r][c+1]
                    # Check if neighbors are identical and non-zero
                    if left_neighbor_val != 0 and left_neighbor_val == right_neighbor_val:
                        # Change the cell in the output grid to 1
                        output_grid[r][c] = 1
                        continue # Move to the next cell, no need to check vertical

                # Check for vertical flanking (only if horizontal condition was not met)
                # Check if top neighbor exists (r > 0)
                has_top_neighbor = r > 0
                # Check if bottom neighbor exists (r < rows - 1)
                has_bottom_neighbor = r < rows - 1

                if has_top_neighbor and has_bottom_neighbor:
                    top_neighbor_val = input_grid[r-1][c]
                    bottom_neighbor_val = input_grid[r+1][c]
                    # Check if neighbors are identical and non-zero
                    if top_neighbor_val != 0 and top_neighbor_val == bottom_neighbor_val:
                        # Change the cell in the output grid to 1
                        output_grid[r][c] = 1
                        
            # If the cell value is not 0, or if flanking conditions are not met,
            # the value in output_grid remains as copied from input_grid initially.

    # Return the final transformed grid
    return output_grid