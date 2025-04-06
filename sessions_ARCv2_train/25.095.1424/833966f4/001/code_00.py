import copy

"""
Reorders a list of five single-element lists (representing rows with one integer each).
The reordering involves swapping the first two rows, keeping the third row in place, 
and swapping the last two rows.
"""

# No external libraries needed beyond standard list operations.

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by swapping specific rows.

    Args:
        input_grid: A list of lists, where each inner list contains a single integer. 
                      Expected to have exactly 5 rows.

    Returns:
        A new list of lists with rows reordered according to the rule:
        - Row 0 swapped with Row 1
        - Row 2 remains in place
        - Row 3 swapped with Row 4
    """
    # Create a copy of the input grid to avoid modifying the original list.
    # Since we are swapping entire sublists (rows), a shallow copy of the outer list is sufficient.
    output_grid = input_grid[:] 

    # Check if the input has the expected length (5 rows) for the transformation logic.
    # While not explicitly requested, this makes the function more robust.
    if len(output_grid) != 5:
        # Handle unexpected input length, e.g., return copy or raise error.
        # For now, we'll proceed assuming the length is always 5 based on examples.
        # Consider adding error handling if needed in a real application.
        pass # Or raise ValueError("Input grid must have exactly 5 rows.")

    # Perform transformations based on row index:

    # 1. Swap the element (row) at the first position (index 0) 
    #    with the element (row) at the second position (index 1).
    output_grid[0], output_grid[1] = output_grid[1], output_grid[0]

    # 2. Keep the element (row) at the third position (index 2) unchanged.
    #    No action needed for index 2.

    # 3. Swap the element (row) at the fourth position (index 3) 
    #    with the element (row) at the fifth position (index 4).
    output_grid[3], output_grid[4] = output_grid[4], output_grid[3]

    # 4. Return the modified list (grid).
    return output_grid
