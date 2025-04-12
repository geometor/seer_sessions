
## train_1

**input:**
```
7 7 7 7 7 7 7 7 7 7 7
7 6 6 6 6 6 6 6 9 9 7
7 6 9 9 7 7 7 6 9 9 7
7 6 6 6 6 6 6 6 7 7 7
7 7 7 6 3 3 3 6 7 7 7
7 7 7 6 3 2 3 6 7 9 7
7 9 7 6 3 3 3 6 7 7 7
9 9 7 6 6 7 6 6 6 6 7
7 7 7 6 7 7 7 9 9 6 7
7 7 7 6 6 6 6 6 6 6 7
7 7 7 7 7 7 7 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 7
7 6 6 6 6 6 6 6 9 9 7
7 6 9 9 7 7 7 6 9 9 7
7 6 6 6 6 6 6 6 7 7 7
7 7 7 6 9 9 3 6 7 7 7
7 7 7 6 3 2 3 6 7 9 7
7 9 7 6 3 3 3 6 7 7 7
9 9 7 6 6 7 6 6 6 6 7
7 7 7 6 7 7 7 7 7 6 7
7 7 7 6 6 6 6 6 6 6 7
7 7 7 7 7 7 7 7 7 7 7
```


## train_2

**input:**
```
7 7 7 7 7 7 9 9 9 7 7
7 7 7 7 7 7 9 9 7 7 9
7 7 7 7 7 7 7 7 7 7 9
9 7 7 6 6 6 6 6 6 6 6
7 7 7 6 3 3 3 6 9 7 7
7 7 9 6 3 2 3 6 7 7 7
7 7 7 6 3 3 3 6 7 9 7
7 7 7 6 7 7 7 6 7 7 7
7 9 7 6 7 9 7 6 7 7 7
7 7 9 6 7 9 7 6 7 7 7
7 7 7 7 7 7 7 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 9 9 9 7 7
7 7 7 7 7 7 7 9 7 7 9
7 7 7 7 7 7 7 7 7 7 9
7 7 7 6 6 6 6 6 6 6 6
7 7 7 6 9 9 9 6 7 7 7
7 7 7 6 9 9 9 6 7 7 7
7 7 7 6 9 9 9 6 7 7 7
7 7 7 6 7 7 7 6 7 7 7
7 7 7 6 7 7 7 6 7 7 7
7 7 7 6 7 7 7 6 7 7 7
7 7 7 7 7 7 7 7 7 7 7
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 9 7
7 7 9 7 7 7 7 7 7 7 9
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 3 3 3 7 7 7 7
7 7 7 7 3 2 3 7 7 7 7
7 7 7 7 3 3 3 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 9 7 7
7 7 7 7 7 7 7 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 9 9 9 7 7 7 7
7 7 7 7 9 2 3 7 7 7 7
7 7 7 7 3 3 3 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
```

*   **perception**: The input and output are 11x11 grids of digits. The core transformation appears centered around a specific 3x3 pattern `[[3,3,3],[3,2,3],[3,3,3]]` which is consistently located at rows 4-6 and columns 4-6 (0-indexed) in the input grids. The transformation applied to this pattern depends on the values of the cells immediately surrounding this 3x3 block. A secondary transformation involving changing some `9`s to `7`s also occurs in some examples, but its rule is less clear and consistent across examples compared to the central pattern transformation. The digits likely represent different states or colors, with `7` often acting as a background or boundary color, `6` as another boundary/region color, and `2`/`3` forming the core pattern that gets transformed into `9`s under specific contextual conditions.

*   **facts**:
    ```yaml
    elements:
      - object: grid
        description: An 11x11 grid of single digits.
      - object: pattern_region
        description: A specific 3x3 subgrid pattern [[3,3,3],[3,2,3],[3,3,3]] located at input grid indices [4:7, 4:7].
        properties:
          - center_value: 2
          - surrounding_value: 3
          - location: Fixed at rows 4-6, columns 4-6.
      - object: border_neighbors
        description: The 12 cells immediately adjacent (N, S, E, W) to the boundary of the pattern_region.
        properties:
          - values: Vary across examples, primarily containing 6s and 7s.
      - object: digit_9
        description: Represents a state/color '9'.
      - object: digit_7
        description: Represents a state/color '7', often acting as a background or boundary.
      - object: digit_6
        description: Represents a state/color '6', often acting as a boundary near the pattern_region.

    actions:
      - action: locate_pattern
        description: Identify the 3x3 pattern_region in the input grid.
      - action: analyze_neighbors
        description: Examine the values of the border_neighbors surrounding the pattern_region.
      - action: count_border_values
        description: Count the occurrences of specific digits (e.g., '6', '7') within the border_neighbors.
      - action: transform_pattern
        description: Modify the values within the pattern_region based on the analysis of its border_neighbors. Three distinct transformation outcomes for the pattern_region are observed depending on the neighbor counts.
      - action: copy_grid
        description: Initialize the output grid as a copy of the input grid.
      - action: update_grid
        description: Apply the transformed pattern_region values to the corresponding location in the output grid.
      - action: modify_digit_9 # Secondary, less clear action
        description: In some cases, change cells with value 9 to 7 based on neighborhood conditions (rule unclear/inconsistent).

    relationships:
      - relationship: pattern_dependency
        description: The transformation applied to the pattern_region is dependent on the composition of its border_neighbors.
        properties:
          - condition_1: If all border_neighbors are 7, apply transformation type 1.
          - condition_2: If the count of 6s in border_neighbors is > 8, apply transformation type 2.
          - condition_3: If the count of 6s in border_neighbors is > 0 and <= 8, apply transformation type 3.
    ```

*   **natural language program**:
    1.  Initialize the output grid as a copy of the input grid.
    2.  Identify the 3x3 subgrid region corresponding to input grid indices rows 4-6 and columns 4-6. Check if this region matches the pattern `P = [[3,3,3],[3,2,3],[3,3,3]]`.
    3.  If the pattern `P` is found at the specified location:
        a.  Examine the 12 'border neighbor' cells surrounding this 3x3 region (cells at (3,4), (3,5), (3,6), (4,3), (5,3), (6,3), (7,4), (7,5), (7,6), (4,7), (5,7), (6,7)).
        b.  Count the number of cells with value `6` (`count6`) among these 12 border neighbors.
        c.  Count the number of cells with value `7` (`count7`) among these 12 border neighbors.
        d.  Apply a transformation to the 3x3 region in the output grid based on the counts:
            i.  If `count6` is 0 (and `count7` is 12): Update the 3x3 region in the output grid to `[[9,9,9],[9,2,3],[3,3,3]]`.
            ii. Else if `count6` is greater than 8: Update the 3x3 region in the output grid to `[[9,9,3],[3,2,3],[3,3,3]]`.
            iii. Else if `count6` is greater than 0 and less than or equal to 8: Update the 3x3 region in the output grid to `[[9,9,9],[9,9,9],[9,9,9]]`.
    4.  (Optional/Secondary) Iterate through the input grid. If a cell contains `9` and all of its 8 neighbors contain `7`, change the corresponding cell in the output grid to `7`. *[Note: This secondary rule only partially explains the 9->7 changes observed and might not be complete or correct.]*
    5.  Return the final output grid.
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
