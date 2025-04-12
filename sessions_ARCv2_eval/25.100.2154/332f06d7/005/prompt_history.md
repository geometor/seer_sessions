
## train_1

**input:**
```
3 2 2 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3
3 1 1 3 3 3 3 3 3 3 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 3 1 1 3 3
3 1 1 1 3 3 3 3 0 0 3 3
3 3 3 3 3 3 3 3 0 0 3 3
3 3 3 3 3 3 3 3 3 3 3 3
```


**output:**
```
3 0 0 3 3 3 3 3 3 3 3 3
3 0 0 3 3 3 3 3 3 3 3 3
3 1 1 3 3 3 3 3 3 3 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 1 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 3 3
3 1 1 3 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 1 1 1 1 3
3 1 1 1 1 1 3 3 1 1 3 3
3 1 1 1 3 3 3 3 1 1 3 3
3 3 3 3 3 3 3 3 1 1 3 3
3 3 3 3 3 3 3 3 3 3 3 3
```

## Initial Perception

The input and output are grids of the same dimensions (12x12). The grids contain numerical digits (0, 1, 2, 3 in the input; 0, 1, 3 in the output). A border composed of the digit '3' surrounds both grids and remains unchanged. The core transformation seems to involve swapping specific digits within the grid's interior. Specifically, the digit '2' in the input is replaced by '0' in the output, and the digit '0' in the input is replaced by '1' in the output. The digit '1' appears to remain '1', and the digit '3' remains '3'.

## Observed Facts

```yaml
task_elements:
  - grid:
      type: object
      description: A 2D array of digits.
      properties:
        - dimensions: [12, 12]
        - unique_values_input: [0, 1, 2, 3]
        - unique_values_output: [0, 1, 3]
  - border:
      type: object
      description: A frame composed of a single digit ('3') surrounding the grid's content.
      properties:
        - value: 3
        - thickness: 1 cell
      relationships:
        - unchanged: between input and output
  - digits:
      type: object
      description: Individual numerical values within the grid cells.
      properties:
        - value_map:
            input_2: output_0
            input_0: output_1
            input_1: output_1
            input_3: output_3
      actions:
        - substitution: based on the value_map
relationships:
  - identity: The grid dimensions remain constant.
  - identity: The border ('3') remains constant.
  - transformation: Internal grid values are substituted based on a specific mapping rule (2->0, 0->1, 1->1, 3->3).
```

## Natural Language Program

1.  Iterate through each cell of the input grid.
2.  For each cell, check the digit value:
    *   If the value is '2', change it to '0' in the corresponding output cell.
    *   If the value is '0', change it to '1' in the corresponding output cell.
    *   If the value is '1', keep it as '1' in the corresponding output cell.
    *   If the value is '3', keep it as '3' in the corresponding output cell.
3.  Construct the output grid with these modified cell values.

## train_2

**input:**
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 1 1 0 0 3 3
3 3 3 3 3 1 1 1 1 1 0 0 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 1 1 3 3 3 3
3 3 3 3 3 1 1 1 1 1 3 3 3 3
3 3 3 3 3 3 3 3 3 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
```


**output:**
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 1 1 1 1 3 3
3 3 3 3 3 1 1 1 1 1 1 1 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 3 3 3 3 3 3 3
3 3 3 3 3 1 1 1 0 0 3 3 3 3
3 3 3 3 3 1 1 1 0 0 3 3 3 3
3 3 3 3 3 3 3 3 3 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 1 1 1 1 1 1 1 1 1 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
3 2 2 3 3 3 3 3 3 3 3 3 3 3
```

## Refined Perception

The core transformation involves mapping input digits to output digits, primarily focused on '0' and '2'. However, the specific mapping rules are conditional, depending on the presence and potentially the configuration (specifically, forming 2x2 blocks) of these digits within the input grid.

Observing both examples reveals two distinct modes of operation:

1.  **Mode 1 (Seen in `train_1`):** When a 2x2 block of '0's is present, but *no* 2x2 block of '2's exists:
    *   The '0's (in the 2x2 block) are changed to '1's.
    *   *All* instances of '2' (regardless of their configuration) are changed to '0's.
    *   '1's and '3's remain unchanged.

2.  **Mode 2 (Seen in `train_2`):** When *both* a 2x2 block of '0's *and* a 2x2 block of '2's are present:
    *   The '0's (in the 2x2 block) are changed to '1's.
    *   The '2's (in the 2x2 block) *remain* '2's.
    *   A *specific* 2x2 block of '1's is changed to '0's. (In `train_2`, this was the block at (7,9)-(8,10)).
    *   Other '1's and '3's remain unchanged.

The key differentiator between the examples is the presence of a 2x2 block of '2's in `train_2`, which triggers the preservation of those '2's and the transformation of a specific '1' block, contrasting with `train_1` where the absence of a '2' block led to all '2's becoming '0's. The transformation `0 -> 1` (for 2x2 blocks of 0s) appears consistent across both modes where such blocks exist. The identification criteria for the "specific" 2x2 block of '1's in Mode 2 needs further clarification if more examples were provided, but based on `train_2`, it was a distinct 2x2 block separate from the 0s and 2s blocks.

## Updated Observed Facts

```yaml
task_elements:
  - grid:
      type: object
      description: A 2D array of digits.
      properties:
        - dimensions: variable (e.g., [12, 12] or [14, 14])
        - unique_values_input: [0, 1, 2, 3]
        - unique_values_output: [0, 1, 2, 3] # Updated based on train_2 output
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
        - value_map: conditional based on 2x2 blocks
  - two_by_two_block:
      type: object
      description: A 2x2 square of identical digits (0, 1, or 2).
      properties:
        - digit_value: The digit composing the block (0, 1, or 2).
        - top_left_coord: The (row, col) of the top-left cell of the block.
relationships:
  - identity: Grid dimensions remain constant between input and output for a given example.
  - identity: The border ('3') remains constant.
  - conditional_transformation:
      condition: Input contains a 2x2 block of '0's (L0_block) AND input does NOT contain a 2x2 block of '2's.
      actions:
        - change_value: at L0_block, input '0' -> output '1'.
        - change_value: for ALL input '2's (L2_any), input '2' -> output '0'.
        - identity: all input '1's -> output '1'.
  - conditional_transformation:
      condition: Input contains a 2x2 block of '0's (L0_block) AND input contains a 2x2 block of '2's (L2_block).
      actions:
        - change_value: at L0_block, input '0' -> output '1'.
        - identity: at L2_block, input '2' -> output '2'.
        - find_specific: identify ONE specific 2x2 block of '1's (L1_special). # Specific identification rule TBD (e.g., most central? first found?)
        - change_value: at L1_special, input '1' -> output '0'.
        - identity: all other input '1's -> output '1'.
```

## Updated Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Search the input grid (excluding borders) for a 2x2 block composed entirely of '0's. Record its location(s) if found (L0_block).
3.  Search the input grid (excluding borders) for a 2x2 block composed entirely of '2's. Record its location(s) if found (L2_block).
4.  **Check Condition 1:** If an L0_block was found AND an L2_block was *not* found:
    *   For each cell within the found L0_block(s), change the corresponding output cell value to '1'.
    *   Find *all* cells in the input grid containing '2' (L2_any).
    *   For each cell location in L2_any, change the corresponding output cell value to '0'.
5.  **Check Condition 2:** If *both* an L0_block was found AND an L2_block was found:
    *   For each cell within the found L0_block(s), change the corresponding output cell value to '1'.
    *   (The '2's in the L2_block remain '2' as per the initial copy).
    *   Search the input grid for *all* 2x2 blocks composed entirely of '1's (L1_blocks).
    *   Identify *one specific* block from L1_blocks (L1_special). (Rule for choosing needs confirmation, e.g., based on position like centrality or index).
    *   For each cell within L1_special, change the corresponding output cell value to '0'.
6.  (Implicit) All other cells ('3's, and '1's not covered by the rules above) retain their original values from the initial copy.
7.  Return the final output grid.

## train_3

**input:**
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 3
2 2 2 1 1 1 1 3 3 1 1 1 1 1 1 3
2 2 2 1 1 3 3 3 3 3 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 1 1 1 1 3 1 1 1 3 3 3 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 3 3 1 1 3 3 3 1 1 1 3
3 0 0 0 1 3 3 1 1 1 1 1 1 1 1 3
3 0 0 0 1 3 3 1 1 1 1 1 1 1 1 3
3 0 0 0 1 3 3 1 1 1 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```


**output:**
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
2 2 2 1 1 1 1 1 1 1 1 1 1 1 1 3
2 2 2 1 1 1 1 3 3 1 1 1 1 1 1 3
2 2 2 1 1 3 3 3 3 3 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 1 1 3
3 3 3 1 1 1 1 1 1 1 3 3 3 1 1 3
3 3 3 1 1 1 1 0 0 0 3 3 3 1 1 3
3 3 3 1 1 1 1 0 0 0 3 3 3 1 1 3
3 3 1 1 1 1 3 0 0 0 3 3 3 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 1 3 1 1 3 3 3 1 1 1 3
3 3 1 1 1 3 3 1 1 3 3 3 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 1 1 1 1 3 3 1 1 1 1 1 1 1 1 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```

## Refined Perception

The core task involves identifying the largest monochromatic square blocks (MSBs) of digits '0' and '2' within the input grid (excluding the border). The transformation applied depends on the presence and relative sizes of these blocks.

Based on all three examples:
1.  The transformation hinges on finding the largest square block of '0's (0-MSB) and the largest square block of '2's (2-MSB). Let their side lengths be N0 and N2, respectively.
2.  **Scenario 1 (Only 0-MSB exists):** If a 0-MSB is found (N0 > 0) but no 2-MSB exists (N2 = 0), the 0-MSB is converted to a block of '1's of the same size, and *all* individual '2's *anywhere* in the grid are converted to '0's. (Seen in `train_1` where N0=2, N2=0).
3.  **Scenario 2 (Both 0-MSB and 2-MSB exist):** If both a 0-MSB (N0 > 0) and a 2-MSB (N2 > 0) are found, and crucially, *if they have the same size* (N0 = N2 = N), then:
    *   The 0-MSB is converted to a block of '1's of size N.
    *   The 2-MSB remains unchanged (block of '2's of size N).
    *   A *specific* MSB of '1's, also of size N, is identified and converted to a block of '0's. (Seen in `train_2` where N=2, and `train_3` where N=3).
4.  **Selection of the 1-MSB:** In Scenario 2, the 1-MSB that gets converted to '0's appears to be the *first* block of '1's with side length N encountered when scanning the grid top-to-bottom, left-to-right.
5.  Digits '3' (primarily the border) and any '1's not part of the selected 1-MSB in Scenario 2 remain unchanged.

The concept of 2x2 blocks from the initial hypothesis was too specific; the relevant feature is the largest monochromatic square block for '0's and '2's, and matching-sized blocks for '1's under certain conditions.

## Updated Observed Facts

```yaml
task_elements:
  - grid:
      type: object
      description: A 2D array of digits.
      properties:
        - dimensions: variable (e.g., [12, 12], [14, 14], [16, 16])
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
        - value_map: conditional based on monochromatic square blocks
  - monochromatic_square_block:
      type: object
      description: An NxN square (N>=2) of identical digits (0, 1, or 2).
      properties:
        - digit_value: The digit composing the block (0, 1, or 2).
        - size: The side length N of the square block.
        - top_left_coord: The (row, col) of the top-left cell of the block.
      relationships:
        - maximality: We are primarily interested in the largest such block for '0' and '2'.

relationships:
  - identity: Grid dimensions remain constant between input and output for a given example.
  - identity: The border ('3') remains constant.
  - conditional_transformation:
      condition_check: Find the largest MSB of '0's (L0_MSB, size N0) and the largest MSB of '2's (L2_MSB, size N2).
      branch_1: # Corresponds to Scenario 1
        condition: N0 > 0 AND N2 == 0
        actions:
          - find_block: Locate the first largest 0-MSB (top_left_coord_0).
          - change_value: At L0_MSB, input '0' -> output '1'.
          - change_value: For ALL input '2's (L2_any), input '2' -> output '0'.
          - identity: All input '1's -> output '1'.
      branch_2: # Corresponds to Scenario 2
        condition: N0 > 0 AND N2 > 0 AND N0 == N2 # Let N = N0 = N2
        actions:
          - find_block: Locate the first largest 0-MSB (top_left_coord_0).
          - find_block: Locate the first largest 2-MSB (top_left_coord_2).
          - change_value: At L0_MSB, input '0' -> output '1'.
          - identity: At L2_MSB, input '2' -> output '2'.
          - find_block: Locate the *first* (in reading order) MSB of '1's with size N (L1_special).
          - change_value: At L1_special, input '1' -> output '0'.
          - identity: All other input '1's -> output '1'.
      branch_3: # Default/Fallback (implied)
        condition: Other cases (e.g., N0=0, N2>0; or N0>0, N2>0, N0!=N2)
        actions:
          - identity: Input grid is copied to output grid. # Assumption based on lack of examples

```

## Updated Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Define a function `find_largest_msb(grid, digit)` that searches the input grid (excluding borders) for monochromatic square blocks of the specified `digit`. It should return the top-left coordinate and the size (N) of the largest such block found. If multiple largest blocks exist, return the one whose top-left coordinate comes first in reading order (top-to-bottom, left-to-right). If no block (N>=2) is found, return size N=0.
3.  Call `find_largest_msb` for digit '0' to get `(coord0, N0)`.
4.  Call `find_largest_msb` for digit '2' to get `(coord2, N2)`.
5.  **Check Scenario 1:** If `N0 > 0` AND `N2 == 0`:
    *   Iterate through the cells forming the N0xN0 block starting at `coord0`. For each cell in this block, set the corresponding output grid cell value to '1'.
    *   Iterate through all cells of the input grid (excluding borders). If an input cell contains '2', set the corresponding output grid cell value to '0'.
6.  **Check Scenario 2:** If `N0 > 0` AND `N2 > 0` AND `N0 == N2`:
    *   Let N = N0.
    *   Iterate through the cells forming the NxN block starting at `coord0`. For each cell in this block, set the corresponding output grid cell value to '1'.
    *   (The NxN block of '2's starting at `coord2` remains '2' because the output was initialized as a copy).
    *   Define a function `find_first_msb_of_size(grid, digit, size)` that finds the first MSB (in reading order) of the specified `digit` having the exact side length `size`. Return its top-left coordinate (`coord1_special`). If none is found, return a special value (e.g., None).
    *   Call `find_first_msb_of_size` for digit '1' and size N to get `coord1_special`.
    *   If `coord1_special` is found (not None):
        *   Iterate through the cells forming the NxN block starting at `coord1_special`. For each cell in this block, set the corresponding output grid cell value to '0'.
7.  **Fallback:** If neither Scenario 1 nor Scenario 2 conditions are met, the output grid remains the initial copy of the input grid.
8.  Return the final output grid.

## train_4

**input:**
```
3 3 3 3 3 3 3 3 3 3
3 0 1 1 3 3 3 3 3 3
3 3 3 1 3 1 1 1 3 3
3 3 3 1 3 1 3 1 3 3
3 3 3 1 1 1 3 1 3 3
3 3 3 3 3 3 3 1 3 3
3 3 3 3 1 1 1 1 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 2 3 3 3 3 3
```


**output:**
```
3 3 3 3 3 3 3 3 3 3
3 1 1 1 3 3 3 3 3 3
3 3 3 1 3 1 1 1 3 3
3 3 3 1 3 1 3 1 3 3
3 3 3 1 1 1 3 1 3 3
3 3 3 3 3 3 3 1 3 3
3 3 3 3 1 1 1 1 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 1 3 3 3 3 3
3 3 3 3 0 3 3 3 3 3
```

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
```python
import copy

def find_largest_msb(grid: list[list[int]], digit: int) -> tuple[tuple[int, int] | None, int]:
    """
    Finds the largest monochromatic square block (MSB) of a given digit.

    Args:
        grid: The input grid (list of lists of integers).
        digit: The digit to search for (0, 1, or 2).

    Returns:
        A tuple containing:
        - The top-left coordinate (row, col) of the first largest MSB found
          (in reading order), or None if no MSB of size >= 2x2 exists.
        - The size (side length N) of the largest MSB found, or 0 if none exists.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0
    max_size = 0
    best_coord = None

    # Iterate possible sizes from largest possible down to 2
    for size in range(min(rows, cols), 1, -1):
        found_at_this_size = False
        # Iterate through possible top-left corners
        for r in range(rows - size + 1):
            for c in range(cols - size + 1):
                is_msb = True
                # Check if the square block is monochromatic
                for i in range(r, r + size):
                    for j in range(c, c + size):
                        if grid[i][j] != digit:
                            is_msb = False
                            break
                    if not is_msb:
                        break
                
                if is_msb:
                    # Found an MSB of the current size
                    if size > max_size:
                        # This is the largest size found so far
                        max_size = size
                        best_coord = (r, c)
                        found_at_this_size = True
                    elif size == max_size and best_coord is None:
                        # This is the first block of the current max size found
                         best_coord = (r,c)
                         found_at_this_size = True
                    # Only need the first one for a given size if it's the max size found so far
                    # For subsequent blocks of the *same* max size, we keep the first coordinate found
        # If we found the largest possible size, no need to check smaller sizes
        if found_at_this_size and size == max_size:
             break # optimization: we found the largest size

    return best_coord, max_size


def find_first_msb_of_size(grid: list[list[int]], digit: int, size: int) -> tuple[int, int] | None:
    """
    Finds the first monochromatic square block (MSB) of a given digit and exact size.

    Args:
        grid: The input grid.
        digit: The digit to search for.
        size: The exact side length N of the square block to find.

    Returns:
        The top-left coordinate (row, col) of the first MSB found
        (in reading order), or None if no such block exists.
    """
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    if size < 2 or size > min(rows, cols):
        return None

    # Iterate through possible top-left corners in reading order
    for r in range(rows - size + 1):
        for c in range(cols - size + 1):
            is_msb = True
            # Check if the square block is monochromatic and of the target size
            for i in range(r, r + size):
                for j in range(c, c + size):
                    if grid[i][j] != digit:
                        is_msb = False
                        break
                if not is_msb:
                    break
            
            if is_msb:
                # Found the first MSB of the required size
                return (r, c)
                
    return None # No MSB of the specified size found

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the following rules:

    Default Rule:
    - Change all '0's to '1's.
    - Change all '2's to '0's.
    - '1's and '3's remain unchanged.

    Exception Condition:
    - If the largest monochromatic square block (MSB) of '0's (size N0 >= 2)
      and the largest MSB of '2's (size N2 >= 2) both exist AND have the
      exact same size (N0 = N2 = N), then the following overrides apply:
        1. The '0's within the N x N 0-MSB change to '1's (as per default).
        2. The '2's within the N x N 2-MSB remain '2's (overriding default).
        3. The first N x N MSB of '1's found (in reading order) changes
           to a block of '0's (overriding default).
        4. All other digits outside these specific blocks follow the default rule.
    """
    
    # Find the largest MSBs for 0 and 2
    coord0, N0 = find_largest_msb(input_grid, 0)
    coord2, N2 = find_largest_msb(input_grid, 2)

    # Initialize output grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    rows = len(output_grid)
    cols = len(output_grid[0]) if rows > 0 else 0

    # Check if the exception condition is met
    exception_applies = (N0 >= 2 and N2 >= 2 and N0 == N2)
    
    if exception_applies:
        N = N0 # The common size
        # Find the first MSB of '1's with size N
        coord1_special = find_first_msb_of_size(input_grid, 1, N)

        # Apply transformations considering the exception
        for r in range(rows):
            for c in range(cols):
                # Check if cell is within the 2-MSB
                is_in_L2_MSB = (coord2 is not None and 
                                r >= coord2[0] and r < coord2[0] + N and 
                                c >= coord2[1] and c < coord2[1] + N)
                
                # Check if cell is within the special 1-MSB
                is_in_L1_special = (coord1_special is not None and 
                                      r >= coord1_special[0] and r < coord1_special[0] + N and 
                                      c >= coord1_special[1] and c < coord1_special[1] + N)

                if is_in_L2_MSB:
                    # Rule 2: 2s in the 2-MSB remain 2
                    output_grid[r][c] = 2 
                elif is_in_L1_special:
                     # Rule 3: 1s in the special 1-MSB become 0
                    output_grid[r][c] = 0
                else:
                    # Apply default rules for cells outside the exception blocks
                    if input_grid[r][c] == 0:
                        output_grid[r][c] = 1
                    elif input_grid[r][c] == 2:
                        output_grid[r][c] = 0
                    # else: 1s and 3s remain as copied initially
                        
    else:
        # Apply default transformations globally
        for r in range(rows):
            for c in range(cols):
                if input_grid[r][c] == 0:
                    output_grid[r][c] = 1
                elif input_grid[r][c] == 2:
                    output_grid[r][c] = 0
                # else: 1s and 3s remain as copied initially

    return output_grid
```
