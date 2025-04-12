```python
"""
Transforms an 11x11 input grid based on the content of a central 3x3 pattern
and its immediate border neighbors.

1. Initialize the output grid as a copy of the input grid.
2. Identify the 3x3 subgrid region corresponding to input grid indices rows 4-6
   and columns 4-6. Check if this region matches the pattern
   P = [[3,3,3],[3,2,3],[3,3,3]].
3. If the pattern P is found at the specified location:
    a. Examine the 12 'border neighbor' cells surrounding this 3x3 region
       (cells at (3,4), (3,5), (3,6), (4,3), (5,3), (6,3), (7,4), (7,5),
       (7,6), (4,7), (5,7), (6,7)).
    b. Count the number of cells with value 6 (count6) among these 12
       border neighbors.
    c. Apply a transformation to the 3x3 region in the output grid based on
       the count6:
        i.   If count6 is 0: Update the 3x3 region in the output grid to
             [[9,9,9],[9,2,3],[3,3,3]].
        ii.  Else if count6 is greater than 8: Update the 3x3 region in the
             output grid to [[9,9,3],[3,2,3],[3,3,3]].
        iii. Else if count6 is greater than 0 and less than or equal to 8:
             Update the 3x3 region in the output grid to
             [[9,9,9],[9,9,9],[9,9,9]].
4. Return the final output grid. Any cells not part of the transformed 3x3
   region remain unchanged from the input.
"""

import copy

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a transformation to a central 3x3 pattern in the grid based on
    the values of its 12 immediate border neighbors.

    Args:
        input_grid: An 11x11 grid represented as a list of lists of integers.

    Returns:
        A new 11x11 grid with the transformation applied.
    """
    # initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    rows = len(input_grid)
    cols = len(input_grid[0]) if rows > 0 else 0

    # Define the target pattern and its location
    pattern_rows = (4, 7) # Slice indices: start row 4, end before row 7
    pattern_cols = (4, 7) # Slice indices: start col 4, end before col 7
    target_pattern = [
        [3, 3, 3],
        [3, 2, 3],
        [3, 3, 3]
    ]

    # Extract the actual subgrid from the input
    actual_subgrid = [row[pattern_cols[0]:pattern_cols[1]] for row in input_grid[pattern_rows[0]:pattern_rows[1]]]

    # Check if the pattern matches at the specified location
    if actual_subgrid == target_pattern:
        # Define coordinates of the 12 border neighbors
        neighbor_coords = [
            (3, 4), (3, 5), (3, 6),  # Top neighbors
            (7, 4), (7, 5), (7, 6),  # Bottom neighbors
            (4, 3), (5, 3), (6, 3),  # Left neighbors
            (4, 7), (5, 7), (6, 7)   # Right neighbors
        ]

        # Get the values of the border neighbors
        neighbor_values = []
        for r, c in neighbor_coords:
            # Basic boundary check although grid is fixed size 11x11
            if 0 <= r < rows and 0 <= c < cols:
                neighbor_values.append(input_grid[r][c])

        # Count the number of 6s among the neighbors
        count6 = neighbor_values.count(6)

        # Determine the transformation based on count6
        transformed_pattern = None
        if count6 == 0:
            # Condition i: No 6s found (implies all 7s based on examples)
             transformed_pattern = [
                 [9, 9, 9],
                 [9, 2, 3],
                 [3, 3, 3]
             ]
        elif count6 > 8:
             # Condition ii: More than 8 6s found
             transformed_pattern = [
                 [9, 9, 3],
                 [3, 2, 3],
                 [3, 3, 3]
             ]
        elif 0 < count6 <= 8:
             # Condition iii: Between 1 and 8 (inclusive) 6s found
             transformed_pattern = [
                 [9, 9, 9],
                 [9, 9, 9],
                 [9, 9, 9]
             ]

        # Apply the transformation to the output grid if a pattern was determined
        if transformed_pattern:
            for r_idx, row_val in enumerate(transformed_pattern):
                for c_idx, cell_val in enumerate(row_val):
                    output_grid[pattern_rows[0] + r_idx][pattern_cols[0] + c_idx] = cell_val

    # Return the potentially modified grid
    return output_grid
```