## Refined Perception

The core transformation rule appears to be a simple digit substitution: '0' becomes '1', and '2' becomes '0'. Digits '1' and '3' remain unchanged by default.

However, there is a significant exception condition: This simple substitution rule is overridden *if and only if* the input grid contains *both* a largest monochromatic square block (MSB) of '0's (with side length N0 >= 2) *and* a largest MSB of '2's (with side length N2 >= 2), *and* these blocks have the *exact same size* (N0 = N2 = N).

When this specific exception condition is met:
1.  The '0's *within* the identified largest 0-MSB change to '1's.
2.  The '2's *within* the identified largest 2-MSB *remain* '2's (overriding the default 2->0 rule for these specific cells).
3.  A specific MSB of '1's, which must also have the same size N, is identified (the first one found in reading order) and changed to a block of '0's.
4.  Any '0's or '2's *outside* these specific MSBs still follow the default substitution rule (0->1, 2->0). (Though the provided examples for this exception case did not contain such stray digits).

If the exception condition is *not* met (either because there isn't an MSB >= 2x2 for '0' or '2', or because their largest MSBs have different sizes), then the simple default substitution (0->1, 2->0 everywhere) applies to the entire grid.

Example `train_4` confirms the default behaviour: no 0-MSB or 2-MSB of size N>=2 exists, so the single '0' becomes '1' and the single '2' becomes '0'. This clarifies that the MSB logic is an *exception* rather than the primary rule.

## Updated Observed Facts

```yaml
task_elements:
  - grid:
      type: object
      description: A 2D array of digits.
      properties:
        - dimensions: variable
        - unique_values_input: [0, 1, 2, 3]
        - unique_values_output: [0, 1, 2, 3]
  - border:
      type: object
      description: A frame composed of a single digit ('3') surrounding the grid's content.
      properties:
        - value: 3
        - thickness: 1 cell (observed)
      relationships:
        - unchanged: between input and output
  - digits:
      type: object
      description: Individual numerical values within the grid cells, excluding the border.
      properties:
        - default_value_map:
            input_0: output_1
            input_2: output_0
            input_1: output_1
            input_3: output_3
        - transformation_mode: Defaults to applying 'default_value_map' cell-wise, unless the exception condition is met.
  - monochromatic_square_block:
      type: object
      description: An NxN square (N>=2) of identical digits (0, 1, or 2). Relevant for the exception condition.
      properties:
        - digit_value: The digit composing the block (0, 1, or 2).
        - size: The side length N of the square block.
        - top_left_coord: The (row, col) of the top-left cell of the block.
      relationships:
        - maximality: The exception condition compares the *largest* MSB for '0' and '2'.

relationships:
  - identity: Grid dimensions remain constant between input and output for a given example.
  - identity: The border ('3') remains constant.
  - conditional_transformation:
      condition_check: Find the largest MSB of '0's (L0_MSB, size N0 >= 2) and the largest MSB of '2's (L2_MSB, size N2 >= 2). If multiple largest exist, use the first in reading order.
      exception_condition: (N0 >= 2) AND (N2 >= 2) AND (N0 == N2)
      actions_if_exception:
          - let N = N0 = N2.
          - find_block: Locate the largest 0-MSB (L0_MSB) and largest 2-MSB (L2_MSB).
          - find_block: Locate the *first* (in reading order) MSB of '1's with size N (L1_special).
          - apply_map_selectively:
              - Apply 'default_value_map' to all cells *except* those within L2_MSB and L1_special.
              - For cells within L2_MSB: input '2' -> output '2'.
              - For cells within L1_special: input '1' -> output '0'.
      actions_if_no_exception:
          - apply_map_globally: Apply 'default_value_map' to all cells (excluding border).

```

## Updated Natural Language Program

1.  Define a function `find_largest_msb(grid, digit)` that searches the input grid (excluding borders) for monochromatic square blocks (size N>=2) of the specified `digit`. It returns the top-left coordinate and the size (N) of the largest such block. If multiple largest blocks exist, return the one whose top-left coordinate comes first in reading order. If no block (N>=2) is found, return size N=0 and a null coordinate.
2.  Call `find_largest_msb` for digit '0' to get `(coord0, N0)`.
3.  Call `find_largest_msb` for digit '2' to get `(coord2, N2)`.
4.  Initialize the output grid as a copy of the input grid.
5.  **Check Exception Condition:** If `N0 >= 2` AND `N2 >= 2` AND `N0 == N2`:
    *   Let N = N0.
    *   Define a function `find_first_msb_of_size(grid, digit, size)` that finds the first MSB (in reading order) of the specified `digit` having the exact side length `size`. Return its top-left coordinate (`coord_special`). If none is found, return a null coordinate.
    *   Call `find_first_msb_of_size` for digit '1' and size N to get `coord1_special`.
    *   **Apply Transformations (Exception Case):**
        *   Iterate through all cells `(r, c)` of the input grid (excluding border):
            *   If cell `(r, c)` is within the N x N block starting at `coord0` (the 0-MSB): Set `output[r][c] = 1`.
            *   Else if cell `(r, c)` is within the N x N block starting at `coord2` (the 2-MSB): Set `output[r][c] = 2`.
            *   Else if `coord1_special` is not null AND cell `(r, c)` is within the N x N block starting at `coord1_special` (the special 1-MSB): Set `output[r][c] = 0`.
            *   Else if `input[r][c] == 0`: Set `output[r][c] = 1`. # Handles potential stray 0s
            *   Else if `input[r][c] == 2`: Set `output[r][c] = 0`. # Handles potential stray 2s
            *   Else: `output[r][c]` remains the copied `input[r][c]` ('1' or '3').
6.  **Default Behaviour:** If the exception condition in step 5 is *not* met:
    *   Iterate through all cells `(r, c)` of the input grid (excluding border):
        *   If `input[r][c] == 0`: Set `output[r][c] = 1`.
        *   Else if `input[r][c] == 2`: Set `output[r][c] = 0`.
        *   Else: `output[r][c]` remains the copied `input[r][c]` ('1' or '3').
7.  Return the final output grid.