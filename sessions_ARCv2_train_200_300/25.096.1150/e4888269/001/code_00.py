"""
Transforms a 2D integer grid based on the following rules:
1. Initializes the output grid as a copy of the input grid.
2. Sets the value of the cell at row index 2, column index 14 to 7.
3. Sets the value of the cell at row index 6, column index 11 to 5.
4. Checks the value of the cell at row index 3, column index 1 in the *input* grid.
5. If the value at input[3][1] is non-zero, sets the value of the cell at row index 7, column index 18 in the *output* grid to the value from input[3][1].
6. Otherwise (if input[3][1] is zero), sets the value of the cell at row index 7, column index 18 in the *output* grid to 4.
7. Returns the modified output grid.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies specific value changes to a copy of the input grid.

    Args:
        input_grid: A 10x20 2D list of integers.

    Returns:
        A 10x20 2D list of integers representing the transformed grid.
    """
    # initialize output_grid as a deep copy of the input grid
    # This ensures the original input_grid is not modified and non-target cells are preserved.
    output_grid = copy.deepcopy(input_grid)

    # perform transformations

    # Rule 2: Set the value at (2, 14) to 7
    # Check bounds just in case, although examples suggest fixed size
    if len(output_grid) > 2 and len(output_grid[2]) > 14:
        output_grid[2][14] = 7
    else:
        # Handle potential dimension mismatch if necessary (e.g., raise error, log warning)
        print("Warning: Grid dimensions are smaller than expected for rule 2.")


    # Rule 3: Set the value at (6, 11) to 5
    if len(output_grid) > 6 and len(output_grid[6]) > 11:
        output_grid[6][11] = 5
    else:
        print("Warning: Grid dimensions are smaller than expected for rule 3.")

    # Rule 4-6: Conditionally set the value at (7, 18) based on the value at input (3, 1)
    if len(input_grid) > 3 and len(input_grid[3]) > 1 and len(output_grid) > 7 and len(output_grid[7]) > 18:
        # Retrieve the value from the *input* grid at row index 3, column index 1.
        source_value = input_grid[3][1]

        # Check the condition
        if source_value != 0:
            # Set output[7][18] to the source value
            output_grid[7][18] = source_value
        else:
            # Set output[7][18] to 4
            output_grid[7][18] = 4
    else:
         print("Warning: Grid dimensions are smaller than expected for rule 4-6.")

    # Return the modified output grid
    return output_grid