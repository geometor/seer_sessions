import copy

"""
Transforms an input grid by stacking its rows in reverse order on top of its original rows.
1. Take the input grid.
2. Create a list of the rows from the input grid.
3. Create a new list containing the rows from the input grid in reverse order (last row becomes first, first row becomes last).
4. Concatenate the reversed list of rows with the original list of rows vertically.
5. The resulting combined list of rows forms the output grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """

    # 1. Take the input grid (passed as argument)
    # 2. Create a list of the rows from the input grid.
    original_rows = input_grid

    # 3. Create a new list containing the rows from the input grid in reverse order.
    # Use list slicing [::-1] for a concise way to reverse the list of rows.
    # Use copy.deepcopy to ensure modifications to reversed_rows don't affect original_rows if rows were mutable objects (though lists of ints are okay here)
    # However, simply reversing the order of rows doesn't require deepcopy. A shallow copy via slicing is sufficient.
    reversed_rows = original_rows[::-1]

    # 4. Concatenate the reversed list of rows with the original list of rows vertically.
    # The '+' operator concatenates lists in Python.
    output_grid = reversed_rows + original_rows

    # 5. The resulting combined list of rows forms the output grid.
    return output_grid
