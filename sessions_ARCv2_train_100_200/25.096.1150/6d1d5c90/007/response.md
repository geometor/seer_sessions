```python
import functools

"""
Transforms an input grid of numbers based on the values of the first elements
of the first two rows.

1.  For each row in the input grid, remove the first element to create a
    'transformed row'.
2.  Determine the sorting/ordering method based on the first elements of the
    first and second input rows (`control_1` = input[0][0], `control_2` = input[1][0]):
    a.  If `control_1` is 2: The transformed rows maintain their original
        relative order in the output.
    b.  If `control_1` is 6:
        i.  If the grid has at least two rows AND `control_2` is also 6:
            - Sort transformed rows primarily by their last element in DESCENDING order.
            - Break ties based on the value of the tied last_element:
                - If last_element is EVEN: Use lexicographical ASCENDING order.
                - If last_element is ODD: Use lexicographical DESCENDING order.
        ii. Otherwise (`control_2` is not 6, or the grid has only one row):
            - Sort transformed rows lexicographically ASCENDING.
    c.  Default/Other cases (if `control_1` is not 2 or 6): Assume
        lexicographical ASCENDING sort.
3.  The final output grid consists of the ordered/sorted transformed rows.
"""

def _compare_complex(item1, item2):
    """
    Custom comparison function for the case where control_1 is 6 and control_2 is 6.
    Sorts primarily by last element descending.
    Breaks ties based on last element parity:
    - Even last element: Lexicographical ascending tie-break.
    - Odd last element: Lexicographical descending tie-break.

    Args:
        item1: First item dictionary {'row': list, 'last': int}.
        item2: Second item dictionary {'row': list, 'last': int}.

    Returns:
        -1 if item1 < item2, 0 if item1 == item2, 1 if item1 > item2 according to the rule.
    """
    row1, last1 = item1['row'], item1['last']
    row2, last2 = item2['row'], item2['last']

    # Primary sort: last element descending
    if last1 > last2:
        return -1  # item1 comes first (higher last element)
    if last1 < last2:
        return 1   # item2 comes first (lower last element)

    # Tie in last element: apply secondary sort based on parity
    if last1 == last2:
        # Check parity of the tied last element
        is_even = (last1 % 2 == 0)

        # Lexicographical comparison
        if row1 < row2:
            return -1 if is_even else 1 # Ascending for even, Descending for odd
        if row1 > row2:
            return 1 if is_even else -1 # Ascending for even, Descending for odd
        return 0 # Rows are identical

    # Should not be reached if last elements are numbers
    return 0


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a conditional sorting transformation to a grid of integers.
    """

    # Handle empty input grid
    if not input_grid:
        return []

    # --- Step 1: Extract control values ---
    control_1 = input_grid[0][0] if len(input_grid[0]) > 0 else None
    control_2 = input_grid[1][0] if len(input_grid) > 1 and len(input_grid[1]) > 0 else None

    # --- Step 2: Create transformed rows and store relevant info ---
    transformed_items = []
    for i, row in enumerate(input_grid):
        # Remove the first element
        transformed_row = row[1:]
        # Get the last element, handle empty transformed rows
        last_element = transformed_row[-1] if transformed_row else -float('inf') # Use -inf for empty rows
        transformed_items.append({
            'original_index': i, # Keep track if needed for stable sort simulation
            'row': transformed_row,
            'last': last_element
        })

    # --- Step 3: Apply conditional sorting logic ---
    output_rows = []

    # Case 1: control_1 is 2 -> Preserve original order
    if control_1 == 2:
        output_rows = [item['row'] for item in transformed_items] # Already ordered by creation

    # Case 2: control_1 is 6 -> Conditional sorting
    elif control_1 == 6:
        # Sub-case 2a: control_2 is also 6 -> Complex sort
        if control_2 == 6:
            # Use the custom comparison function with functools.cmp_to_key
            sorted_items = sorted(transformed_items, key=functools.cmp_to_key(_compare_complex))
            output_rows = [item['row'] for item in sorted_items]
        # Sub-case 2b: control_2 is not 6 or grid has only 1 row -> Lexicographical sort
        else:
            # Standard lexicographical sort applies directly to the rows
            sorted_items = sorted(transformed_items, key=lambda x: x['row'])
            output_rows = [item['row'] for item in sorted_items]

    # Case 3: Default/Other -> Lexicographical sort
    else:
        # Assume standard lexicographical sort for any other control_1 value
        sorted_items = sorted(transformed_items, key=lambda x: x['row'])
        output_rows = [item['row'] for item in sorted_items]

    # --- Step 4: Return the final grid ---
    return output_rows
```