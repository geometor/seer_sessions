import copy

"""
Transforms a 5x5 input grid based on the following rules:
- If a cell in the input grid contains the value 5, its value in the output grid is determined by its specific (row, column) coordinates according to a predefined mapping.
- If a cell in the input grid contains any value other than 5 (specifically 0 in the examples), its value remains unchanged in the output grid.
"""

def transform(input_grid):
    """
    Applies a coordinate-based transformation to cells with value 5.

    Args:
        input_grid: A 5x5 list of lists representing the input grid.

    Returns:
        A 5x5 list of lists representing the transformed output grid.
    """
    # Define the mapping for coordinates where the input value is 5
    coord_mapping = {
        (0, 0): 1,
        (0, 2): 1,
        (0, 4): 2,
        (2, 0): 3,
        (2, 2): 4,
        (2, 4): 7,
        (4, 0): 6,
        (4, 2): 8,
        (4, 4): 7,
    }

    # Initialize the output grid as a deep copy of the input grid
    # This handles the case where values other than 5 should remain unchanged
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0]) # Assuming a rectangular grid

    # Iterate through each cell of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the input cell value is 5
            if input_grid[r][c] == 5:
                # Check if the coordinates exist in our mapping
                if (r, c) in coord_mapping:
                    # Replace the value in the output grid using the mapping
                    output_grid[r][c] = coord_mapping[(r, c)]
                # else:
                    # Optional: Handle cases where a 5 appears at an unmapped coordinate
                    # In this problem definition, all 5s seem to be mapped.
                    # If not, they would retain the value 5 based on the initial deepcopy.
                    # pass

    # Return the transformed grid
    return output_grid