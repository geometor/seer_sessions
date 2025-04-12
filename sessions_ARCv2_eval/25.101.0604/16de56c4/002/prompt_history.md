
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
1 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
9 0 9 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
8 8 0 0 0 0 0 3 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
1 0 0 1 0 0 1 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
6 0 6 0 6 0 6 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 4 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 9 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 6 0 0 0 0 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
```


**output:**
```
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 0 0 0 0 2 0 0 0 6 0 0 0 0 0
0 2 0 0 0 2 0 0 0 6 0 0 0 0 0
0 0 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 0 0
0 0 0 0 0 2 0 0 0 6 0 0 0 0 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
```

## Perception

The task involves transforming a 2D grid of numbers based on the patterns within each row. The transformation seems primarily horizontal, affecting cells within a row based on the positions and values of the non-zero elements in that row in the input grid.

Key observations across examples:

1.  **Row Independence:** The transformation appears to be applied independently to each row. The output of a row depends only on the input of that same row.
2.  **Non-Zero Elements Define Action:** The transformation is triggered and defined by the non-zero elements within a row. Rows containing only zeros remain unchanged.
3.  **Horizontal Span:** The transformation affects a horizontal segment of the row. This segment seems bounded by the leftmost and rightmost non-zero elements in the input row.
4.  **Dominant Color:** The color (value) used for filling the affected segment seems determined by the value of the *rightmost* non-zero element in the input row.
5.  **Filling Mechanism:**
    *   In some cases (e.g., `train_1`, row 11: `8 8 ... 3 0` -> `3 3 ... 3 0`), all cells between the leftmost and rightmost non-zero input cells (inclusive) are filled with the dominant color.
    *   In other cases (e.g., `train_1`, row 4: `1 1 0...` -> `1 1 1...`), the fill seems to extend beyond the rightmost non-zero cell, potentially to the end of the grid. This might occur when all non-zero elements in the input row share the same value.
    *   In yet other cases (e.g., `train_1`, row 8: `9 0 9 ... 6 0 0` -> `6 0 6 0 6 0 6 0 0`), the filling within the span is selective, not painting over all original zeros. This selective filling is the hardest part to generalize.

Given the variations, the most consistent core operation appears to be filling the horizontal span defined by the outermost non-zero elements with the color of the rightmost element. However, there are modifications or alternative rules based on the homogeneity of colors or specific patterns within the row.

## Facts

```yaml
task_description: Transform each row of a grid based on its non-zero elements.
grid_properties:
  dimensionality: 2D
  cell_values: integers (0-9)
  background_color: 0
objects:
  - name: row
    properties:
      - contains_non_zero_elements: boolean
      - non_zero_cells: list of (column_index, value) tuples
      - leftmost_non_zero_column: integer (c_min)
      - rightmost_non_zero_column: integer (c_max)
      - rightmost_non_zero_value: integer (V)
      - distinct_non_zero_values: set of integers
actions:
  - name: process_row
    input: input_row_data
    output: output_row_data
    logic:
      - If the row contains no non-zero elements, the output row is identical to the input row (all zeros).
      - Otherwise, identify the column indices of the leftmost (c_min) and rightmost (c_max) non-zero elements.
      - Identify the value of the rightmost non-zero element (V).
      - Determine the set of distinct non-zero values in the row.
      - **Hypothesized Rule (needs refinement):**
        - Initialize the output row as a copy of the input row.
        - Fill the cells in the output row from column `c_min` to `c_max` (inclusive) with the value `V`.
        - (Note: This rule does not perfectly explain all examples, especially train_1 row 4 and row 8, suggesting conditional logic or alternative rules might apply based on factors like color uniformity or specific spacing patterns).
relationships:
  - The transformation of a cell depends only on the data within its row in the input grid.
  - The output value of cells within the horizontal span [c_min, c_max] is primarily determined by the value V from the rightmost non-zero cell at c_max.
```

## Natural Language Program

1.  Iterate through each row of the input grid independently.
2.  For the current row:
    a.  Find all non-zero cells and their column indices.
    b.  If there are no non-zero cells, copy the input row (all zeros) to the output row and proceed to the next row.
    c.  If there are non-zero cells:
        i.  Determine the column index of the leftmost non-zero cell (`c_min`).
        ii. Determine the column index of the rightmost non-zero cell (`c_max`).
        iii. Determine the value of the rightmost non-zero cell (`V`).
        iv. Create the output row by copying the input row.
        v.  Fill the segment of the output row from column `c_min` to `c_max` (inclusive) with the value `V`.
        vi. (Self-correction/Refinement Needed: The simple span fill described in step `v` does not perfectly match all examples. Cases like `train_1` row 4, row 8, and row 1 suggest additional conditions: perhaps if all non-zero values are the same, the fill extends to the grid edge, or perhaps the fill within the span `[c_min, c_max]` sometimes preserves original zeros based on specific criteria not yet fully understood).
3.  Combine the processed output rows to form the final output grid.
```python
import copy
import math

"""
The transformation rule depends on the pattern of non-zero elements in the last non-zero row of the input grid.

1. Find the last row in the input grid that contains any non-zero elements. Call this the 'reference row'.
2. Examine the non-zero elements in this reference row.
3. Check if any two *adjacent* non-zero elements in the reference row (when sorted by column index) have *consecutive* column indices.

4. **If YES (adjacent non-zeros exist in the reference row):**
   - The transformation is applied *independently* to each row.
   - For a given row:
     - Find all non-zero cells, sorted by column index: nz = [(c1, v1), (c2, v2), ...].
     - If no non-zero cells exist (len(nz) == 0), the row remains unchanged.
     - If only one non-zero cell exists (len(nz) == 1), the row remains unchanged.
     - If multiple non-zero cells exist (len(nz) > 1):
       - Determine the column of the first non-zero cell (c_min).
       - Determine the value of the *last* non-zero cell (V).
       - Calculate the difference in column indices between the first two non-zero cells (step = nz[1][0] - nz[0][0]).
       - Check if all non-zero cells in this row have the same value (all_same_value).
       - Initialize the output row as a copy of the input row.
       - Apply filling logic based on conditions:
         - If `all_same_value` is True AND `step == 1`: Fill the output row from column `c_min` to the *end of the row* with value `V`.
         - Else if `step == 1`: Fill the output row from column `c_min` to the column of the *last* non-zero cell (`c_max`) (inclusive) with value `V`.
         - Else (`step > 1`): Starting from column `c_min`, fill every `step`-th column with value `V`, continuing as long as the column index is within the row bounds.

5. **If NO (no adjacent non-zeros exist in the reference row):**
   - The transformation uses the reference row as a base pattern.
   - For each row in the input grid:
     - If the input row contains no non-zero elements, the output row is identical (all zeros).
     - If the input row *does* contain non-zero elements:
       - Start with a copy of the reference row.
       - Overwrite the values in this copied reference row at the column indices corresponding to the non-zero elements of the *original input row*, using the values from the original input row. The resulting row is the output row.

"""

def find_reference_info(grid: list[list[int]]) -> tuple[int | None, list[tuple[int, int]] | None]:
    """Finds the index and sorted non-zero elements of the last row containing non-zeros."""
    ref_row_index = None
    ref_nz = None
    for r in range(len(grid) - 1, -1, -1):
        nz = sorted([(c, val) for c, val in enumerate(grid[r]) if val != 0])
        if nz:
            ref_row_index = r
            ref_nz = nz
            break
    return ref_row_index, ref_nz

def check_adjacency(nz_list: list[tuple[int, int]]) -> bool:
    """Checks if any adjacent elements in the sorted non-zero list have consecutive column indices."""
    if not nz_list or len(nz_list) < 2:
        return False
    for i in range(len(nz_list) - 1):
        if nz_list[i][0] + 1 == nz_list[i+1][0]:
            return True
    return False

def transform_row_independent(row: list[int]) -> list[int]:
    """Applies the row-independent transformation logic (Type 1)."""
    nz = sorted([(c, val) for c, val in enumerate(row) if val != 0])
    
    # Handle rows with 0 or 1 non-zero element
    if len(nz) < 2:
        return list(row) # Return a copy

    # Get properties for rows with >= 2 non-zero elements
    c_min = nz[0][0]
    c_max = nz[-1][0]
    V = nz[-1][1] # Value of the *last* non-zero element
    step = nz[1][0] - nz[0][0]
    all_same_value = len(set(val for c, val in nz)) == 1
    
    output_row = list(row) # Start with a copy
    row_width = len(row)

    # Apply filling logic based on conditions
    if all_same_value and step == 1:
        # Fill from c_min to the end of the row
        for c in range(c_min, row_width):
            output_row[c] = V
    elif step == 1:
        # Fill from c_min to c_max (inclusive)
        for c in range(c_min, c_max + 1):
            output_row[c] = V
    elif step > 1:
        # Fill every step-th column starting from c_min
        c = c_min
        while c < row_width:
            output_row[c] = V
            c += step
            
    return output_row

def transform_reference_overlay(input_grid: list[list[int]], ref_row_index: int) -> list[list[int]]:
    """Applies the reference row overlay transformation logic (Type 2)."""
    output_grid = []
    reference_row = input_grid[ref_row_index]
    num_rows = len(input_grid)
    
    for r in range(num_rows):
        current_row = input_grid[r]
        current_nz = [(c, val) for c, val in enumerate(current_row) if val != 0]
        
        if not current_nz:
            # If the input row is all zeros, the output is all zeros
            output_grid.append(list(current_row)) 
        else:
            # Start with reference row, overlay current non-zeros
            output_row = list(reference_row)
            for c, val in current_nz:
                output_row[c] = val
            output_grid.append(output_row)
            
    return output_grid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on patterns in the last non-zero row.
    Chooses between two transformation types: row-independent or reference-row-overlay.
    """
    # Find the last non-zero row and its non-zero elements
    ref_row_index, ref_nz = find_reference_info(input_grid)

    # If no non-zero elements exist anywhere in the grid, return a copy
    if ref_row_index is None:
        return [list(row) for row in input_grid] 

    # Check if the reference row has adjacent non-zero elements
    has_adjacent = check_adjacency(ref_nz)

    # Apply Transformation Type 1 (Row Independent)
    if has_adjacent:
        output_grid = []
        for r in range(len(input_grid)):
             output_grid.append(transform_row_independent(input_grid[r]))
        return output_grid
    # Apply Transformation Type 2 (Reference Row Overlay)
    else:
        return transform_reference_overlay(input_grid, ref_row_index)

```
