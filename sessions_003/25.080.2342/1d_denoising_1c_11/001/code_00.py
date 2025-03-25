"""
Iterate through the input. Remove any digit that has zero as both neighbors,
forming a new, modified list.
"""

def transform(input_grid):
    """
    Transforms the input grid by removing digits surrounded by zeros.
    """
    output_grid = []
    n = len(input_grid)

    # Iterate through the input grid
    for i in range(n):
        # Check boundary conditions and neighbors
        if i > 0 and i < n - 1:  # Ensure we're not at the edges
            if input_grid[i-1] == 0 and input_grid[i+1] == 0:
                # Skip adding the digit to output if surrounded by zeros
                continue
        output_grid.append(input_grid[i])

    return output_grid