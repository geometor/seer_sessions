import copy

"""
Takes an input list (represented as a list of lists, each containing one number) 
assumed to have 5 elements. Swaps the first two elements (at indices 0 and 1). 
Leaves the third element (at index 2) unchanged. Swaps the last two elements 
(at indices 3 and 4). Returns the rearranged list in the same format.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Rearranges a list of 5 elements by swapping the first pair and the last pair.

    Args:
        input_grid: A list of lists, where each inner list contains a single integer.
                     Expected to have 5 elements based on training examples.
                     Example: [[9], [0], [1], [6], [8]]

    Returns:
        A new list of lists with elements rearranged according to the rule.
        Example: [[0], [9], [1], [8], [6]]
    """

    # Ensure the input has the expected structure (at least 5 elements)
    # In a real scenario, more robust error handling might be needed.
    if len(input_grid) < 5:
        # Or raise an error, depending on desired behavior for invalid input
        return input_grid 

    # Create a copy of the input list to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)

    # Swap the first element (index 0) with the second element (index 1)
    # We are swapping the inner lists themselves.
    output_grid[0], output_grid[1] = output_grid[1], output_grid[0]

    # The third element (index 2) remains in its original position.

    # Swap the fourth element (index 3) with the fifth element (index 4)
    output_grid[3], output_grid[4] = output_grid[4], output_grid[3]

    # Return the rearranged list
    return output_grid
