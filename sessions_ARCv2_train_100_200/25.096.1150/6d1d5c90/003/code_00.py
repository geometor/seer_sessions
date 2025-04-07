import copy

"""
Transforms an input grid of numbers based on the values of the first elements
of the first two rows.

1.  For each row in the input grid, remove the first element to create a
    'transformed row'.
2.  Determine the sorting/ordering method based on the first elements of the
    first and second input rows:
    a.  If the first element of the first row is 2, the transformed rows
        maintain their original relative order in the output.
    b.  If the first element of the first row is 6:
        i.  If the grid has at least two rows AND the first element of the
            second row is also 6, the transformed rows are sorted based on
            their respective last elements in descending order. The sort is
            stable, preserving the original relative order of rows with the
            same last element.
        ii. Otherwise (first element of the second row is not 6, or the grid
            has only one row), the transformed rows are sorted
            lexicographically in ascending order.
3.  The final output grid consists of the ordered/sorted transformed rows.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a conditional sorting transformation to a grid of integers.

    Args:
        input_grid: A list of lists representing the input grid of integers.

    Returns:
        A list of lists representing the transformed grid.
    """

    # Handle empty input grid
    if not input_grid:
        return []

    # --- Step 1: Create transformed rows (removing first element) ---
    # Store transformed rows along with their original index for potential stable sort
    indexed_transformed_rows = []
    for i, row in enumerate(input_grid):
        if len(row) > 0: # Ensure row is not empty
             transformed_row = row[1:]
             # Handle potential empty row after transformation for sort key later
             last_element = transformed_row[-1] if transformed_row else float('-inf')
             indexed_transformed_rows.append({
                 'index': i,
                 'row': transformed_row,
                 'last': last_element
             })
        else:
             # Handle case of an initially empty row in input
             indexed_transformed_rows.append({
                 'index': i,
                 'row': [],
                 'last': float('-inf') # Assign lowest value for sorting
             })


    # --- Step 2: Determine sorting method based on control values ---
    top_left = input_grid[0][0] if len(input_grid[0]) > 0 else None
    second_row_start = input_grid[1][0] if len(input_grid) > 1 and len(input_grid[1]) > 0 else None

    output_rows = []

    # Case 1: Top-left element is 2 -> Preserve original order
    if top_left == 2:
        output_rows = [item['row'] for item in indexed_transformed_rows] # Already in original order

    # Case 2: Top-left element is 6 -> Conditional sorting
    elif top_left == 6:
        # Sub-case 2a: Second row starts with 6 -> Sort by last element desc (stable)
        if second_row_start == 6:
             # Python's sort is stable. Sorting by the key is sufficient.
            sorted_items = sorted(indexed_transformed_rows, key=lambda x: x['last'], reverse=True)
            output_rows = [item['row'] for item in sorted_items]
        # Sub-case 2b: Second row doesn't start with 6 or only one row -> Sort lexicographically
        else:
            sorted_items = sorted(indexed_transformed_rows, key=lambda x: x['row'])
            output_rows = [item['row'] for item in sorted_items]

    # Fallback/Default case (if top_left is neither 2 nor 6, though not seen in examples)
    # Let's default to lexicographical sort as a sensible default if needed.
    else:
        sorted_items = sorted(indexed_transformed_rows, key=lambda x: x['row'])
        output_rows = [item['row'] for item in sorted_items]


    # --- Step 3: Return the final ordered/sorted grid ---
    return output_rows