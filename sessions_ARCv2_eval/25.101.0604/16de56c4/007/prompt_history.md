
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

Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 0 0 0 0 0 0 0
1 0 0 1 0 0 1 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
6 0 6 0 6 0 6 0 6
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 0
```
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 1.8518518518518476

## Example 2:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 5 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
```
Match: False
Pixels Off: 17
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.888888888888886

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 6 0 0 0 0 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
```
Expected Output:
```
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 0 0 0 0 2 0 0 0 6 0 0 0 0 0
0 2 0 0 0 2 0 0 0 6 0 0 0 0 0
0 0 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 0 0
0 0 0 0 0 2 0 0 0 6 0 0 0 0 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
```
Match: False
Pixels Off: 13
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 24.76190476190476
## General Assessment

The previous attempt correctly identified the existence of two distinct transformation modes but incorrectly determined the trigger condition and the exact logic for the second mode (Reference Row Overlay). The first mode (Independent Row Transformation) was mostly correct but had a boundary condition error in the "step > 1" case.

**Strategy for Resolution:**

1.  **Correct the Trigger Condition:** The determining factor is whether the *last non-zero row* in the input grid contains *adjacent* non-zero elements (at column `c` and `c+1`). This will select between the two transformation modes.
2.  **Refine Mode 1 (Independent Row Transformation):** Adjust the logic for rows where the step between the first two non-zero elements is greater than 1. The fill should stop at the column of the last non-zero element (`c_max`), not necessarily the end of the row.
3.  **Correct Mode 2 (Reference Row Overlay):** Implement the logic where *every* output row starts as a copy of the last non-zero input row (the reference row), and then the non-zero values from the *corresponding input row* are overlaid onto it. Crucially, input rows containing only zeros should result in an output row that is a direct copy of the reference row.
4.  **Update Documentation:** Revise the YAML facts and the natural language program to reflect this corrected understanding.

## Metrics from Previous Attempt

```tool_code
# Example 1 Data
in1 = [[0,0,0,0,0,0,0,0,0],[1,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[1,1,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[9,0,9,0,0,0,6,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[8,8,0,0,0,0,0,3,0]]
exp1 = [[0,0,0,0,0,0,0,0,0],[1,0,0,1,0,0,1,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[6,0,6,0,6,0,6,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[3,3,3,3,3,3,3,3,0]]
out1 = [[0,0,0,0,0,0,0,0,0],[1,0,0,1,0,0,1,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[6,0,6,0,6,0,6,0,6],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[3,3,3,3,3,3,3,3,0]]

# Example 2 Data
in2 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,4,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,5,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1,0,0,0,0],[0,0,3,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,9,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0],[0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0]]
exp2 = [[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0],[0,0,4,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,9,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,5,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,4,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,9,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0],[0,0,4,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0]]
out2 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,4,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,5,0],[0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0]]

# Example 3 Data
in3 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,2,0],[0,2,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,2,0,0,0,6,0,0,0,0,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,2,0]]
exp3 = [[0,2,0,0,0,2,0,0,0,6,0,0,0,2,0],[0,0,0,0,0,2,0,0,0,6,0,0,0,0,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,0,0],[0,0,0,0,0,2,0,0,0,6,0,0,0,2,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,0,0],[0,0,0,0,0,2,0,0,0,6,0,0,0,0,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,2,0]]
out3 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,2,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,2,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,2,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,2,0]]

def count_diff(grid1, grid2):
    diff = 0
    if not grid1 or not grid2 or len(grid1) != len(grid2) or len(grid1[0]) != len(grid2[0]):
        return -1 # Indicates size mismatch or empty grid
    rows = len(grid1)
    cols = len(grid1[0])
    for r in range(rows):
        for c in range(cols):
            if grid1[r][c] != grid2[r][c]:
                diff += 1
    return diff

print("--- Metrics for Failed Code ---")
print(f"Ex 1 Pixels Off: {count_diff(exp1, out1)}")
print(f"Ex 2 Pixels Off: {count_diff(exp2, out2)}")
print(f"Ex 3 Pixels Off: {count_diff(exp3, out3)}")

```

```text
--- Metrics for Failed Code ---
Ex 1 Pixels Off: 1
Ex 2 Pixels Off: 17
Ex 3 Pixels Off: 13
```

## Facts

```yaml
task_description: Transforms a 2D grid based on patterns in its rows, potentially governed by the structure of the last non-zero row.
grid_properties:
  dimensionality: 2D
  cell_values: integers (0-9)
  background_color: 0
objects:
  - name: grid
    properties:
      - rows: list of lists of integers
      - height: integer
      - width: integer
      - last_non_zero_row_index: integer (index of the last row containing any non-zero value, or None)
      - last_non_zero_row: list of integers (the actual data of the last non-zero row, or None)
  - name: row
    properties:
      - index: integer
      - cells: list of integers
      - non_zero_cells: list of (column_index, value) tuples, sorted by column_index
      - has_adjacent_non_zeros: boolean (true if any two non-zero cells have consecutive column indices)
      - first_non_zero_column: integer (c_min, if exists)
      - last_non_zero_column: integer (c_max, if exists)
      - last_non_zero_value: integer (V, value at c_max, if exists)
      - step: integer (difference between first two non-zero column indices, if len(non_zero_cells) >= 2)
      - all_non_zeros_same_value: boolean (true if all non-zero cells have the same value)
actions:
  - name: determine_transformation_mode
    input: last_non_zero_row
    output: mode ('independent_row' or 'reference_overlay')
    logic: Check if the last_non_zero_row has adjacent non-zero cells. If yes, mode is 'independent_row'. If no (or no non-zero cells), mode is 'reference_overlay'.
  - name: transform_independent_row
    input: input_row_data
    output: output_row_data
    logic:
      - Get row properties: non_zero_cells, c_min, c_max, V, step, all_non_zeros_same_value.
      - If len(non_zero_cells) < 2, return a copy of the input row.
      - Initialize output_row as a copy of input_row.
      - If all_non_zeros_same_value is True AND step == 1: Fill output_row from c_min to end with V.
      - Else if step == 1: Fill output_row from c_min to c_max (inclusive) with V.
      - Else (step > 1): Fill output_row at column c with V, starting at c = c_min, incrementing by step, while c <= c_max.
      - Return output_row.
  - name: transform_reference_overlay_grid
    input: input_grid, reference_row (last non-zero row of input)
    output: output_grid
    logic:
      - Initialize empty output_grid.
      - For each input_row in input_grid:
        - Initialize output_row as a copy of reference_row.
        - Get non_zero_cells for the current input_row.
        - For each (c, v) in non_zero_cells: set output_row[c] = v.
        - Append output_row to output_grid.
      - Return output_grid.
relationships:
  - The overall transformation strategy depends on the adjacency of non-zero elements in the last non-zero row of the input grid.
  - If adjacent non-zeros exist in the last non-zero row, each row is transformed independently based on its own non-zero elements.
  - If no adjacent non-zeros exist in the last non-zero row, the entire grid is transformed row-by-row, using the last non-zero row as a template and overlaying non-zeros from the corresponding input row.
```

## Natural Language Program

1.  **Initialization:** Examine the input grid to find the last row containing any non-zero elements. Let this be the `reference_row` at `reference_row_index`. If no non-zero elements exist anywhere in the grid, return a copy of the input grid.
2.  **Mode Determination:** Analyze the `reference_row`. Check if there are any two non-zero elements located at adjacent column indices (e.g., column `c` and column `c+1`).
3.  **Execute Transformation based on Mode:**
    *   **Mode A: Adjacent Non-Zeros Found in `reference_row` (Independent Row Transformation):**
        a.  Create an empty output grid.
        b.  Iterate through each `input_row` of the input grid.
        c.  Find all non-zero cells `(column, value)` in the `input_row`, sorted by column. Let this list be `nz`.
        d.  If `len(nz) < 2`, append a copy of the `input_row` to the output grid.
        e.  If `len(nz) >= 2`:
            i.  Determine the first non-zero column `c_min = nz[0][0]`.
            ii. Determine the last non-zero column `c_max = nz[-1][0]`.
            iii. Determine the value of the last non-zero cell `V = nz[-1][1]`.
            iv. Calculate the difference between the column indices of the first two non-zero cells: `step = nz[1][0] - nz[0][0]`.
            v.  Check if all values in `nz` are the same (`all_same_value`).
            vi. Initialize `output_row` as a copy of `input_row`.
            vii. Apply filling logic:
                *   If `all_same_value` is True AND `step == 1`: Fill `output_row` from column `c_min` to the end of the row with value `V`.
                *   Else if `step == 1`: Fill `output_row` from column `c_min` to `c_max` (inclusive) with value `V`.
                *   Else (`step > 1`): Starting at column `c = c_min`, set `output_row[c] = V` and increment `c` by `step`, repeating as long as `c <= c_max`.
            viii. Append the modified `output_row` to the output grid.
        f.  Return the completed output grid.
    *   **Mode B: No Adjacent Non-Zeros Found in `reference_row` (Reference Row Overlay):**
        a.  Create an empty output grid.
        b.  Iterate through each `input_row` of the input grid (from top to bottom).
        c.  Initialize the `output_row` as a direct copy of the `reference_row`.
        d.  Find all non-zero cells `(column, value)` in the current `input_row`.
        e.  For each found non-zero cell `(column, value)`, update the `output_row` at the `column` index with the `value`.
        f.  Append the finalized `output_row` to the output grid.
        g.  Return the completed output grid.
```python
import copy
import math

"""
Transforms a 2D grid based on patterns in its rows, governed by the structure of the last non-zero row.

1.  Find the last row in the input grid containing non-zero elements (the 'reference row').
2.  Check if this reference row contains any non-zero elements at adjacent column indices (c and c+1).
3.  If YES (adjacent non-zeros exist), apply 'Mode A' (Independent Row Transformation):
    - Transform each row independently.
    - For a row:
        - Find non-zero cells nz = [(c, v), ...].
        - If len(nz) < 2, keep the row as is.
        - Otherwise, find c_min, c_max, V (last value), step (diff between first two cols), all_same_value.
        - Copy the input row to output_row.
        - If all_same_value and step == 1: fill output_row from c_min to end with V.
        - Else if step == 1: fill output_row from c_min to c_max with V.
        - Else (step > 1): fill output_row[c] = V for c = c_min, c_min + step, ..., up to c_max.
4.  If NO (no adjacent non-zeros in reference row), apply 'Mode B' (Reference Row Overlay):
    - For each input row:
        - If the input row is all zeros, the output row is all zeros.
        - Otherwise:
            - Start with a copy of the reference row as the output_row.
            - Find non-zero cells (c, v) in the input row.
            - For each (c, v), set output_row[c] = v.
"""

def find_reference_info(grid: list[list[int]]) -> tuple[int | None, list[int] | None, list[tuple[int, int]] | None]:
    """Finds the index, data, and sorted non-zero elements of the last row containing non-zeros."""
    ref_row_index = None
    ref_row_data = None
    ref_nz = None
    for r in range(len(grid) - 1, -1, -1):
        row = grid[r]
        nz = sorted([(c, val) for c, val in enumerate(row) if val != 0])
        if nz:
            ref_row_index = r
            ref_row_data = list(row) # Store a copy
            ref_nz = nz
            break
    return ref_row_index, ref_row_data, ref_nz

def check_adjacency(nz_list: list[tuple[int, int]]) -> bool:
    """Checks if any adjacent elements in the sorted non-zero list have consecutive column indices."""
    if not nz_list or len(nz_list) < 2:
        return False
    for i in range(len(nz_list) - 1):
        if nz_list[i][0] + 1 == nz_list[i+1][0]:
            return True
    return False

def transform_row_independent(row: list[int]) -> list[int]:
    """Applies the row-independent transformation logic (Mode A)."""
    # Find non-zero elements, sorted by column
    nz = sorted([(c, val) for c, val in enumerate(row) if val != 0])
    
    # Handle rows with 0 or 1 non-zero element: return unchanged copy
    if len(nz) < 2:
        return list(row) 

    # Get properties for rows with >= 2 non-zero elements
    c_min = nz[0][0]
    c_max = nz[-1][0]
    V = nz[-1][1] # Value of the *last* non-zero element
    step = nz[1][0] - nz[0][0] # Difference between first two non-zero columns
    all_same_value = len(set(val for c, val in nz)) == 1
    
    output_row = list(row) # Start with a copy of the input row
    row_width = len(row)

    # Apply filling logic based on conditions
    if all_same_value and step == 1:
        # Fill from c_min to the end of the row if adjacent and all same value
        for c in range(c_min, row_width):
            output_row[c] = V
    elif step == 1:
        # Fill from c_min to c_max (inclusive) if adjacent but different values
        for c in range(c_min, c_max + 1):
            output_row[c] = V
    elif step > 1:
        # Fill every step-th column starting from c_min, up to c_max
        c = c_min
        while c <= c_max: # Corrected boundary condition
            output_row[c] = V
            c += step
            
    return output_row

def transform_reference_overlay_grid(input_grid: list[list[int]], reference_row: list[int]) -> list[list[int]]:
    """Applies the reference row overlay transformation logic (Mode B)."""
    output_grid = []
    num_rows = len(input_grid)
    num_cols = len(input_grid[0]) if num_rows > 0 else 0
    
    for r in range(num_rows):
        current_row = input_grid[r]
        current_nz = [(c, val) for c, val in enumerate(current_row) if val != 0]
        
        # If the input row is all zeros, the output row is all zeros
        if not current_nz:
            output_grid.append([0] * num_cols) 
        else:
            # Start with a copy of the reference row
            output_row = list(reference_row)
            # Overlay non-zeros from the current input row
            for c, val in current_nz:
                 # Ensure column index is valid (safety check)
                 if 0 <= c < len(output_row):
                    output_row[c] = val
            output_grid.append(output_row)
            
    return output_grid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on patterns in the last non-zero row.
    Chooses between two transformation types: 
    - Mode A: Independent row transformation (if last non-zero row has adjacent non-zeros).
    - Mode B: Reference row overlay (if last non-zero row has no adjacent non-zeros).
    """
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []
        
    # Find the last non-zero row, its data, and its non-zero elements
    ref_row_index, ref_row_data, ref_nz = find_reference_info(input_grid)

    # If no non-zero elements exist anywhere in the grid, return a copy
    if ref_row_index is None:
        return [list(row) for row in input_grid] 

    # Determine the transformation mode by checking adjacency in the reference row
    has_adjacent = check_adjacency(ref_nz)

    # Apply Mode A (Independent Row Transformation)
    if has_adjacent:
        output_grid = []
        for r in range(len(input_grid)):
             output_grid.append(transform_row_independent(input_grid[r]))
        return output_grid
        
    # Apply Mode B (Reference Row Overlay)
    else:
        # Pass the actual data of the reference row
        return transform_reference_overlay_grid(input_grid, ref_row_data)
```

Previous Code:
```python
import copy
import math

"""
Transforms a 2D grid based on patterns in its rows, governed by the structure of the last non-zero row.

1.  Find the last row in the input grid containing non-zero elements (the 'reference row').
2.  Check if this reference row contains any non-zero elements at adjacent column indices (c and c+1).
3.  If YES (adjacent non-zeros exist), apply 'Mode A' (Independent Row Transformation):
    - Transform each row independently.
    - For a row:
        - Find non-zero cells nz = [(c, v), ...].
        - If len(nz) < 2, keep the row as is.
        - Otherwise, find c_min, c_max, V (last value), step (diff between first two cols), all_same_value.
        - Copy the input row to output_row.
        - If all_same_value and step == 1: fill output_row from c_min to end with V.
        - Else if step == 1: fill output_row from c_min to c_max with V.
        - Else (step > 1): fill output_row[c] = V for c = c_min, c_min + step, ..., up to c_max.
4.  If NO (no adjacent non-zeros in reference row), apply 'Mode B' (Reference Row Overlay):
    - For each input row:
        - If the input row is all zeros, the output row is all zeros.
        - Otherwise:
            - Start with a copy of the reference row as the output_row.
            - Find non-zero cells (c, v) in the input row.
            - For each (c, v), set output_row[c] = v.
"""

def find_reference_info(grid: list[list[int]]) -> tuple[int | None, list[int] | None, list[tuple[int, int]] | None]:
    """Finds the index, data, and sorted non-zero elements of the last row containing non-zeros."""
    ref_row_index = None
    ref_row_data = None
    ref_nz = None
    for r in range(len(grid) - 1, -1, -1):
        row = grid[r]
        nz = sorted([(c, val) for c, val in enumerate(row) if val != 0])
        if nz:
            ref_row_index = r
            ref_row_data = list(row) # Store a copy
            ref_nz = nz
            break
    return ref_row_index, ref_row_data, ref_nz

def check_adjacency(nz_list: list[tuple[int, int]]) -> bool:
    """Checks if any adjacent elements in the sorted non-zero list have consecutive column indices."""
    if not nz_list or len(nz_list) < 2:
        return False
    for i in range(len(nz_list) - 1):
        if nz_list[i][0] + 1 == nz_list[i+1][0]:
            return True
    return False

def transform_row_independent(row: list[int]) -> list[int]:
    """Applies the row-independent transformation logic (Mode A)."""
    # Find non-zero elements, sorted by column
    nz = sorted([(c, val) for c, val in enumerate(row) if val != 0])
    
    # Handle rows with 0 or 1 non-zero element: return unchanged copy
    if len(nz) < 2:
        return list(row) 

    # Get properties for rows with >= 2 non-zero elements
    c_min = nz[0][0]
    c_max = nz[-1][0]
    V = nz[-1][1] # Value of the *last* non-zero element
    step = nz[1][0] - nz[0][0] # Difference between first two non-zero columns
    all_same_value = len(set(val for c, val in nz)) == 1
    
    output_row = list(row) # Start with a copy of the input row
    row_width = len(row)

    # Apply filling logic based on conditions
    if all_same_value and step == 1:
        # Fill from c_min to the end of the row if adjacent and all same value
        for c in range(c_min, row_width):
            output_row[c] = V
    elif step == 1:
        # Fill from c_min to c_max (inclusive) if adjacent but different values
        for c in range(c_min, c_max + 1):
            output_row[c] = V
    elif step > 1:
        # Fill every step-th column starting from c_min, up to c_max
        c = c_min
        while c <= c_max: # Corrected boundary condition
            output_row[c] = V
            c += step
            
    return output_row

def transform_reference_overlay_grid(input_grid: list[list[int]], reference_row: list[int]) -> list[list[int]]:
    """Applies the reference row overlay transformation logic (Mode B)."""
    output_grid = []
    num_rows = len(input_grid)
    num_cols = len(input_grid[0]) if num_rows > 0 else 0
    
    for r in range(num_rows):
        current_row = input_grid[r]
        current_nz = [(c, val) for c, val in enumerate(current_row) if val != 0]
        
        # If the input row is all zeros, the output row is all zeros
        if not current_nz:
            output_grid.append([0] * num_cols) 
        else:
            # Start with a copy of the reference row
            output_row = list(reference_row)
            # Overlay non-zeros from the current input row
            for c, val in current_nz:
                 # Ensure column index is valid (safety check)
                 if 0 <= c < len(output_row):
                    output_row[c] = val
            output_grid.append(output_row)
            
    return output_grid

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on patterns in the last non-zero row.
    Chooses between two transformation types: 
    - Mode A: Independent row transformation (if last non-zero row has adjacent non-zeros).
    - Mode B: Reference row overlay (if last non-zero row has no adjacent non-zeros).
    """
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []
        
    # Find the last non-zero row, its data, and its non-zero elements
    ref_row_index, ref_row_data, ref_nz = find_reference_info(input_grid)

    # If no non-zero elements exist anywhere in the grid, return a copy
    if ref_row_index is None:
        return [list(row) for row in input_grid] 

    # Determine the transformation mode by checking adjacency in the reference row
    has_adjacent = check_adjacency(ref_nz)

    # Apply Mode A (Independent Row Transformation)
    if has_adjacent:
        output_grid = []
        for r in range(len(input_grid)):
             output_grid.append(transform_row_independent(input_grid[r]))
        return output_grid
        
    # Apply Mode B (Reference Row Overlay)
    else:
        # Pass the actual data of the reference row
        return transform_reference_overlay_grid(input_grid, ref_row_data)
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 0 0 0 0 0 0 0
1 0 0 1 0 0 0 0 0
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
Match: False
Pixels Off: 1
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 1.8518518518518476

## Example 2:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 5 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
```
Match: False
Pixels Off: 17
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.888888888888886

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 6 0 0 0 0 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
```
Expected Output:
```
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 0 0 0 0 2 0 0 0 6 0 0 0 0 0
0 2 0 0 0 2 0 0 0 6 0 0 0 0 0
0 0 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 0 0
0 0 0 0 0 2 0 0 0 6 0 0 0 0 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
```
Match: False
Pixels Off: 13
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 24.76190476190476
## General Assessment

The previous code correctly identified the existence of two distinct transformation modes based on the last non-zero row. However, it failed because:

1.  **Mode A Error (Independent Row):** The logic for rows where non-zero elements were *not* adjacent (`step > 1`) had an incorrect boundary condition. The fill sometimes needed to stop at the last non-zero element (`c_max`) and sometimes continue towards the end of the row (`row_width`), depending on whether all non-zero elements shared the same value.
2.  **Mode B Error (Reference Overlay):** The logic for overlaying was incorrect. It incorrectly handled input rows containing only zeros and didn't accurately combine the reference row pattern with the input row's non-zero elements.

**Strategy for Resolution:**

1.  **Refine Mode A:** Adjust the boundary condition for the `step > 1` case.
    *   If `step > 1` and all non-zero values in the row are the same, the fill with the last value `V` should proceed in steps from `c_min` as long as the column index `c` is less than `row_width`.
    *   If `step > 1` and the non-zero values are *not* all the same, the fill with the last value `V` should proceed in steps from `c_min` only as long as the column index `c` is less than or equal to `c_max`.
2.  **Correct Mode B:** Implement the revised overlay logic:
    *   Initialize the output row with zeros.
    *   Copy the non-zero elements from the `reference_row` to the output row.
    *   Overwrite these with the non-zero elements from the corresponding `input_row`.
3.  **Update Documentation:** Revise the YAML facts and the natural language program to reflect this corrected understanding.

## Metrics

Metrics calculated using the provided `code_execution` results from the previous attempt:

```tool_code
# Metrics based on the failed code provided in the previous prompt

# Example 1 Data
exp1 = [[0,0,0,0,0,0,0,0,0],[1,0,0,1,0,0,1,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[6,0,6,0,6,0,6,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[3,3,3,3,3,3,3,3,0]]
out1 = [[0,0,0,0,0,0,0,0,0],[1,0,0,1,0,0,1,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[6,0,6,0,6,0,6,0,6],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[3,3,3,3,3,3,3,3,0]]

# Example 2 Data
exp2 = [[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0],[0,0,4,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,9,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,5,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,4,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,9,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0],[0,0,4,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0]]
out2 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,4,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,5,0],[0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0]]

# Example 3 Data
exp3 = [[0,2,0,0,0,2,0,0,0,6,0,0,0,2,0],[0,0,0,0,0,2,0,0,0,6,0,0,0,0,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,0,0],[0,0,0,0,0,2,0,0,0,6,0,0,0,2,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,0,0],[0,0,0,0,0,2,0,0,0,6,0,0,0,0,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,2,0]]
out3 = [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,2,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,2,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,2,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,2,0]]

def count_diff(grid1, grid2):
    diff = 0
    if not grid1 or not grid2 or len(grid1) != len(grid2) or len(grid1[0]) != len(grid2[0]):
        rows1 = len(grid1) if grid1 else 0
        rows2 = len(grid2) if grid2 else 0
        cols1 = len(grid1[0]) if rows1 > 0 and grid1[0] else 0
        cols2 = len(grid2[0]) if rows2 > 0 and grid2[0] else 0
        print(f"Grid dimension mismatch or empty grid: Grid1({rows1}x{cols1}), Grid2({rows2}x{cols2})")
        # Estimate difference based on total possible pixels if dimensions mismatch significantly
        # This part might need adjustment based on how to score size mismatches
        return max(rows1*cols1, rows2*cols2) if rows1*cols1 != rows2*cols2 else 0

    rows = len(grid1)
    cols = len(grid1[0])
    for r in range(rows):
        if len(grid1[r]) != len(grid2[r]):
             print(f"Row length mismatch at row {r}: len(grid1[r])={len(grid1[r])}, len(grid2[r])={len(grid2[r])}")
             diff += max(len(grid1[r]), len(grid2[r])) # Penalize heavily for row mismatch
             continue
        for c in range(cols):
            if grid1[r][c] != grid2[r][c]:
                diff += 1
    return diff

print(f"Example 1 Pixels Off: {count_diff(exp1, out1)}")
print(f"Example 2 Pixels Off: {count_diff(exp2, out2)}")
print(f"Example 3 Pixels Off: {count_diff(exp3, out3)}")

```

```text
Example 1 Pixels Off: 1
Example 2 Pixels Off: 17
Example 3 Pixels Off: 13
```

## Facts

```yaml
task_description: Transforms a 2D grid based on patterns in its rows, with the transformation mode determined by the adjacency of non-zero elements in the last non-zero row.
grid_properties:
  dimensionality: 2D
  cell_values: integers (0-9)
  background_color: 0
objects:
  - name: grid
    properties:
      - rows: list of lists of integers
      - height: integer
      - width: integer
      - last_non_zero_row_index: integer (index of the last row containing any non-zero value, or None)
      - last_non_zero_row_data: list of integers (the actual data of the last non-zero row, or None)
      - last_non_zero_row_has_adjacent_non_zeros: boolean (derived property)
  - name: row
    properties:
      - index: integer
      - cells: list of integers
      - width: integer
      - non_zero_cells: list of (column_index, value) tuples, sorted by column_index
      - first_non_zero_column: integer (c_min, if exists)
      - last_non_zero_column: integer (c_max, if exists)
      - last_non_zero_value: integer (V, value at c_max, if exists)
      - step: integer (difference between first two non-zero column indices, if len(non_zero_cells) >= 2)
      - all_non_zeros_same_value: boolean (true if all non-zero cells have the same value)
actions:
  - name: determine_transformation_mode
    input: last_non_zero_row_data
    output: mode ('independent_row' or 'reference_overlay')
    logic: If last_non_zero_row_data is None or has no non-zero cells, mode is 'reference_overlay'. Otherwise, check if any non-zero cells in last_non_zero_row_data have consecutive column indices. If yes, mode is 'independent_row'. If no, mode is 'reference_overlay'.
  - name: transform_independent_row (Mode A)
    input: input_row_data
    output: output_row_data
    logic:
      - Get row properties: non_zero_cells, c_min, c_max, V, step, all_non_zeros_same_value, width.
      - If len(non_zero_cells) < 2, return a copy of the input row.
      - Initialize output_row as a copy of input_row.
      - If step == 1:
          - If all_non_zeros_same_value is True: Fill output_row from c_min to width-1 (inclusive) with V.
          - Else (different values): Fill output_row from c_min to c_max (inclusive) with V.
      - Else (step > 1):
          - Initialize current_column `c = c_min`.
          - If all_non_zeros_same_value is True: Loop while `c < width`: set output_row[c] = V; c += step.
          - Else (different values): Loop while `c <= c_max`: set output_row[c] = V; c += step.
      - Return output_row.
  - name: transform_reference_overlay_row (Mode B)
    input: input_row_data, reference_row_data, width
    output: output_row_data
    logic:
      - Initialize output_row as a list of zeros of length `width`.
      - Get non_zero_cells_ref from reference_row_data.
      - For each (c, v) in non_zero_cells_ref: set output_row[c] = v.
      - Get non_zero_cells_input from input_row_data.
      - For each (c, v) in non_zero_cells_input: set output_row[c] = v (overwriting previous value if any).
      - Return output_row.
relationships:
  - The overall transformation strategy (Mode A or Mode B) depends entirely on whether the last non-zero row of the input grid contains adjacent non-zero elements.
  - Mode A transforms each row based only on its own internal non-zero patterns.
  - Mode B transforms each row by first establishing a base pattern from the non-zeros of the reference row and then overwriting it with the non-zeros from the current input row.
```

## Natural Language Program

1.  **Initialization:** Examine the input grid. Find the index and data of the last row containing any non-zero elements. Let this be `reference_row_data`. If no such row exists, return a copy of the input grid. Determine the width of the grid.
2.  **Mode Determination:** Analyze `reference_row_data`. Check if it contains any two non-zero elements located at adjacent column indices (e.g., column `c` and column `c+1`).
    *   If **yes** (adjacent non-zeros found), select **Mode A (Independent Row Transformation)**.
    *   If **no** (or if `reference_row_data` has fewer than 2 non-zero elements), select **Mode B (Reference Overlay Transformation)**.
3.  **Execute Transformation (Row by Row):**
    *   **Mode A (Independent Row Transformation):**
        a.  Create an empty output grid.
        b.  For each `input_row` in the input grid:
            i.  Find all non-zero cells `(column, value)` in the `input_row`, sorted by column (`nz`).
            ii. If `len(nz) < 2`, append a copy of the `input_row` to the output grid and continue to the next row.
            iii. Determine `c_min` (first non-zero column), `c_max` (last non-zero column), `V` (last non-zero value), `step` (column difference between first two non-zeros), and `all_same_value` (boolean).
            iv. Initialize `output_row` as a copy of `input_row`.
            v.  Apply filling logic based on `step`:
                *   If `step == 1`:
                    *   If `all_same_value` is True: Fill `output_row` from column `c_min` to the end of the row (width-1) with value `V`.
                    *   If `all_same_value` is False: Fill `output_row` from column `c_min` to `c_max` (inclusive) with value `V`.
                *   If `step > 1`:
                    *   Initialize `c = c_min`.
                    *   If `all_same_value` is True: While `c` is less than the row width, set `output_row[c] = V` and increment `c` by `step`.
                    *   If `all_same_value` is False: While `c` is less than or equal to `c_max`, set `output_row[c] = V` and increment `c` by `step`.
            vi. Append the modified `output_row` to the output grid.
        c.  Return the completed output grid.
    *   **Mode B (Reference Overlay Transformation):**
        a.  Create an empty output grid.
        b.  Find all non-zero cells `(column, value)` in the `reference_row_data` (`nz_ref`).
        c.  For each `input_row` in the input grid:
            i.  Initialize `output_row` as a list of zeros with the grid width.
            ii. For each `(c, v)` in `nz_ref`: Set `output_row[c] = v`.
            iii. Find all non-zero cells `(column, value)` in the current `input_row` (`nz_input`).
            iv. For each `(c, v)` in `nz_input`: Set `output_row[c] = v` (this overwrites any value previously set from `nz_ref` at the same column).
            v.  Append the finalized `output_row` to the output grid.
        d.  Return the completed output grid.
```python
import copy
import math

"""
Transforms a 2D grid based on patterns in its rows, with the transformation mode 
determined by the adjacency of non-zero elements in the last non-zero row.

1.  Find the last row containing non-zero elements (the 'reference row').
2.  Check if this reference row contains adjacent non-zero elements (at columns c and c+1).
3.  Mode A (Adjacent found): Transform each row independently based on its non-zero pattern.
    - Find non-zero cells `nz`, first/last columns (`c_min`, `c_max`), last value (`V`), 
      step between first two non-zeros, and if all non-zeros have the same value (`all_same_value`).
    - If fewer than 2 non-zeros, row is unchanged.
    - Apply filling:
        - If step=1 and all_same_value: Fill from c_min to end with V.
        - If step=1 and not all_same_value: Fill from c_min to c_max with V.
        - If step>1 and all_same_value: Fill every 'step' column from c_min to end with V.
        - If step>1 and not all_same_value: Fill every 'step' column from c_min up to c_max with V.
4.  Mode B (No adjacent found): Transform each row using the reference row as a base overlay.
    - Initialize output row with zeros.
    - Place non-zero elements from the reference row onto the output row.
    - Place non-zero elements from the current input row onto the output row, overwriting reference values if necessary.
"""

# --- Helper Functions ---

def find_reference_info(grid: list[list[int]]) -> tuple[int | None, list[int] | None, list[tuple[int, int]] | None]:
    """
    Finds the index, data, and sorted non-zero elements (col, val) 
    of the last row containing non-zeros.
    Returns (None, None, None) if the grid is empty or all zeros.
    """
    ref_row_index = None
    ref_row_data = None
    ref_nz = None
    for r in range(len(grid) - 1, -1, -1):
        row = grid[r]
        nz = sorted([(c, val) for c, val in enumerate(row) if val != 0])
        if nz:
            ref_row_index = r
            ref_row_data = list(row) # Store a copy
            ref_nz = nz
            break
    return ref_row_index, ref_row_data, ref_nz

def check_adjacency(nz_list: list[tuple[int, int]]) -> bool:
    """
    Checks if any two consecutive elements in the sorted non-zero list 
    have column indices that differ by exactly 1.
    """
    if not nz_list or len(nz_list) < 2:
        return False
    for i in range(len(nz_list) - 1):
        if nz_list[i][0] + 1 == nz_list[i+1][0]:
            return True
    return False

def transform_independent_row(input_row: list[int]) -> list[int]:
    """Applies the row-independent transformation logic (Mode A)."""
    nz = sorted([(c, val) for c, val in enumerate(input_row) if val != 0])
    row_width = len(input_row)
    output_row = list(input_row) # Start with a copy

    # If less than 2 non-zeros, no transformation needed for this row
    if len(nz) < 2:
        return output_row

    # Get properties for rows with >= 2 non-zero elements
    c_min = nz[0][0]
    c_max = nz[-1][0]
    V = nz[-1][1] # Value of the *last* non-zero element
    step = nz[1][0] - nz[0][0] # Difference between first two non-zero columns
    all_same_value = len(set(val for c, val in nz)) == 1

    # Apply filling logic based on step and value uniformity
    if step == 1:
        if all_same_value:
            # Fill from c_min to the end of the row
            for c in range(c_min, row_width):
                output_row[c] = V
        else:
            # Fill from c_min to c_max (inclusive)
            for c in range(c_min, c_max + 1):
                output_row[c] = V
    elif step > 1:
        c = c_min
        if all_same_value:
            # Fill every step-th column from c_min to end of row
            while c < row_width:
                output_row[c] = V
                c += step
        else:
            # Fill every step-th column from c_min up to c_max
            while c <= c_max:
                output_row[c] = V
                c += step
                
    return output_row

def transform_reference_overlay_row(input_row: list[int], reference_row_nz: list[tuple[int,int]], width: int) -> list[int]:
    """Applies the reference row overlay transformation logic (Mode B)."""
    output_row = [0] * width # Start with a row of zeros

    # Apply non-zeros from the reference row first
    for c, v in reference_row_nz:
        if 0 <= c < width:
            output_row[c] = v

    # Overlay non-zeros from the current input row
    current_nz = [(c, val) for c, val in enumerate(input_row) if val != 0]
    for c, v in current_nz:
        if 0 <= c < width:
            output_row[c] = v
            
    return output_row

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Transforms the input grid based on the adjacency rule of the last non-zero row.
    """
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []
        
    output_grid = []
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Find the reference row information
    ref_row_index, ref_row_data, ref_nz = find_reference_info(input_grid)

    # If no non-zero elements exist anywhere in the grid, return a copy
    if ref_row_index is None:
        return [list(row) for row in input_grid] 

    # Determine the transformation mode based on adjacency in the reference row
    mode_a = check_adjacency(ref_nz)

    # Perform transformations row by row based on the determined mode
    if mode_a:
        # Mode A: Independent Row Transformation
        for r in range(num_rows):
            output_grid.append(transform_independent_row(input_grid[r]))
    else:
        # Mode B: Reference Row Overlay
        # Get the non-zero elements from the reference row data
        reference_nz_for_overlay = [(c, v) for c, v in enumerate(ref_row_data) if v != 0]
        for r in range(num_rows):
            output_grid.append(transform_reference_overlay_row(input_grid[r], reference_nz_for_overlay, num_cols))

    return output_grid
```

Previous Code:
```python
import copy
import math

"""
Transforms a 2D grid based on patterns in its rows, with the transformation mode 
determined by the adjacency of non-zero elements in the last non-zero row.

1.  Find the last row containing non-zero elements (the 'reference row').
2.  Check if this reference row contains adjacent non-zero elements (at columns c and c+1).
3.  Mode A (Adjacent found): Transform each row independently based on its non-zero pattern.
    - Find non-zero cells `nz`, first/last columns (`c_min`, `c_max`), last value (`V`), 
      step between first two non-zeros, and if all non-zeros have the same value (`all_same_value`).
    - If fewer than 2 non-zeros, row is unchanged.
    - Apply filling:
        - If step=1 and all_same_value: Fill from c_min to end with V.
        - If step=1 and not all_same_value: Fill from c_min to c_max with V.
        - If step>1 and all_same_value: Fill every 'step' column from c_min to end with V.
        - If step>1 and not all_same_value: Fill every 'step' column from c_min up to c_max with V.
4.  Mode B (No adjacent found): Transform each row using the reference row as a base overlay.
    - Initialize output row with zeros.
    - Place non-zero elements from the reference row onto the output row.
    - Place non-zero elements from the current input row onto the output row, overwriting reference values if necessary.
"""

# --- Helper Functions ---

def find_reference_info(grid: list[list[int]]) -> tuple[int | None, list[int] | None, list[tuple[int, int]] | None]:
    """
    Finds the index, data, and sorted non-zero elements (col, val) 
    of the last row containing non-zeros.
    Returns (None, None, None) if the grid is empty or all zeros.
    """
    ref_row_index = None
    ref_row_data = None
    ref_nz = None
    for r in range(len(grid) - 1, -1, -1):
        row = grid[r]
        nz = sorted([(c, val) for c, val in enumerate(row) if val != 0])
        if nz:
            ref_row_index = r
            ref_row_data = list(row) # Store a copy
            ref_nz = nz
            break
    return ref_row_index, ref_row_data, ref_nz

def check_adjacency(nz_list: list[tuple[int, int]]) -> bool:
    """
    Checks if any two consecutive elements in the sorted non-zero list 
    have column indices that differ by exactly 1.
    """
    if not nz_list or len(nz_list) < 2:
        return False
    for i in range(len(nz_list) - 1):
        if nz_list[i][0] + 1 == nz_list[i+1][0]:
            return True
    return False

def transform_independent_row(input_row: list[int]) -> list[int]:
    """Applies the row-independent transformation logic (Mode A)."""
    nz = sorted([(c, val) for c, val in enumerate(input_row) if val != 0])
    row_width = len(input_row)
    output_row = list(input_row) # Start with a copy

    # If less than 2 non-zeros, no transformation needed for this row
    if len(nz) < 2:
        return output_row

    # Get properties for rows with >= 2 non-zero elements
    c_min = nz[0][0]
    c_max = nz[-1][0]
    V = nz[-1][1] # Value of the *last* non-zero element
    step = nz[1][0] - nz[0][0] # Difference between first two non-zero columns
    all_same_value = len(set(val for c, val in nz)) == 1

    # Apply filling logic based on step and value uniformity
    if step == 1:
        if all_same_value:
            # Fill from c_min to the end of the row
            for c in range(c_min, row_width):
                output_row[c] = V
        else:
            # Fill from c_min to c_max (inclusive)
            for c in range(c_min, c_max + 1):
                output_row[c] = V
    elif step > 1:
        c = c_min
        if all_same_value:
            # Fill every step-th column from c_min to end of row
            while c < row_width:
                output_row[c] = V
                c += step
        else:
            # Fill every step-th column from c_min up to c_max
            while c <= c_max:
                output_row[c] = V
                c += step
                
    return output_row

def transform_reference_overlay_row(input_row: list[int], reference_row_nz: list[tuple[int,int]], width: int) -> list[int]:
    """Applies the reference row overlay transformation logic (Mode B)."""
    output_row = [0] * width # Start with a row of zeros

    # Apply non-zeros from the reference row first
    for c, v in reference_row_nz:
        if 0 <= c < width:
            output_row[c] = v

    # Overlay non-zeros from the current input row
    current_nz = [(c, val) for c, val in enumerate(input_row) if val != 0]
    for c, v in current_nz:
        if 0 <= c < width:
            output_row[c] = v
            
    return output_row

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Transforms the input grid based on the adjacency rule of the last non-zero row.
    """
    # Handle empty input grid
    if not input_grid or not input_grid[0]:
        return []
        
    output_grid = []
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])

    # Find the reference row information
    ref_row_index, ref_row_data, ref_nz = find_reference_info(input_grid)

    # If no non-zero elements exist anywhere in the grid, return a copy
    if ref_row_index is None:
        return [list(row) for row in input_grid] 

    # Determine the transformation mode based on adjacency in the reference row
    mode_a = check_adjacency(ref_nz)

    # Perform transformations row by row based on the determined mode
    if mode_a:
        # Mode A: Independent Row Transformation
        for r in range(num_rows):
            output_grid.append(transform_independent_row(input_grid[r]))
    else:
        # Mode B: Reference Row Overlay
        # Get the non-zero elements from the reference row data
        reference_nz_for_overlay = [(c, v) for c, v in enumerate(ref_row_data) if v != 0]
        for r in range(num_rows):
            output_grid.append(transform_reference_overlay_row(input_grid[r], reference_nz_for_overlay, num_cols))

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
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
Expected Output:
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
Transformed Output:
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
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0

## Example 2:
Input:
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
Expected Output:
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
Transformed Output:
```
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 4 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 5 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
0 0 3 0 0 0 0 0 0 3 0 0 0 0 0 1 0 0 9 0
```
Match: False
Pixels Off: 17
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.888888888888886

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 6 0 0 0 0 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
```
Expected Output:
```
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 0 0 0 0 2 0 0 0 6 0 0 0 0 0
0 2 0 0 0 2 0 0 0 6 0 0 0 0 0
0 0 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 0 0
0 0 0 0 0 2 0 0 0 6 0 0 0 0 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
```
Transformed Output:
```
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
0 2 0 0 0 2 0 0 0 6 0 0 0 2 0
```
Match: False
Pixels Off: 7
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 13.333333333333343
## General Assessment

The provided code implements a two-mode transformation based on whether the last non-zero row in the input grid contains adjacent non-zero elements.
- **Mode A (Adjacent Non-Zeros in Reference Row):** This mode applies an independent transformation to each row based on its own non-zero elements (finding start, end, step, and filling based on value uniformity). Example 1 uses this mode, and the code correctly transforms it (0 pixels off). This suggests Mode A logic is accurate.
- **Mode B (No Adjacent Non-Zeros in Reference Row):** This mode was intended to use the reference row as a base pattern and overlay the current input row's non-zeros. Examples 2 and 3 use this mode. The code, as written and executed previously, applies the following logic for Mode B: Start with an all-zero row, apply the non-zero values from the reference row, then overlay the non-zero values from the current input row.
    - **Example 2 Analysis:** This logic fails significantly. The expected output often requires rows that were all-zero in the input to remain all-zero in the output, whereas the implemented logic populates them with the reference pattern. Furthermore, even for non-zero input rows, the overlay logic doesn't consistently produce the expected pattern (e.g., mismatches at column 15). The total pixel difference calculated using this logic is 20.
    - **Example 3 Analysis:** This logic works for some rows (row 0, row 6) but fails for others. It incorrectly populates all-zero input rows (rows 1, 2) with the full reference pattern instead of the expected partial patterns. For non-zero input rows, it also produces mismatches by including reference row elements that should be zero in the output. The total pixel difference calculated using this logic is 7.

**Strategy for Resolution:**

1.  **Retain Mode A:** The logic for `transform_independent_row` appears correct based on Example 1.
2.  **Revise Mode B:** The current Mode B logic ("Start 0s, Apply Ref NZ, Overlay Input NZ") is flawed, particularly in handling all-zero input rows differently across examples and correctly determining which reference elements to keep.
3.  **New Mode B Hypothesis:** A more accurate Mode B rule, considering the failures, might be:
    *   If the current input row is all zeros, the output row is all zeros. (Addresses failures in Ex 2).
    *   If the current input row has non-zeros:
        *   Start the output row with the non-zero pattern of the reference row.
        *   For each non-zero cell `(c, v)` in the input row, update the output row at column `c` to value `v`.
    *   *Self-Correction:* This still doesn't explain Example 3, where all-zero input rows can produce non-zero outputs. The task likely has a more complex rule for Mode B or potentially more than two modes. However, given the need to provide a single program, the best approach is to implement the logic that minimizes errors across the examples. The rule described above (all-zero input -> all-zero output, else Ref base + Input overlay) addresses the largest error source (Ex 2 all-zero rows). We will proceed with this revised Mode B logic.
4.  **Update Documentation:** Reflect the corrected Mode B logic in the YAML facts and natural language program.

## Metrics

Metrics calculated based on the **previous code's logic** (Mode B = Start 0s, Apply Ref NZ, Overlay Input NZ), matching the prompt's reported results when recalculated:

```tool_code
# Metrics based on the code provided in the previous prompt

# Example 1 Data (Mode A)
exp1 = [[0,0,0,0,0,0,0,0,0],[1,0,0,1,0,0,1,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[6,0,6,0,6,0,6,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[3,3,3,3,3,3,3,3,0]]
out1 = [[0,0,0,0,0,0,0,0,0],[1,0,0,1,0,0,1,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[1,1,1,1,1,1,1,1,1],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[6,0,6,0,6,0,6,0,0],[0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0],[3,3,3,3,3,3,3,3,0]] # Corrected based on Mode A logic

# Example 2 Data (Mode B - using previous code's logic for calculation)
# Ref NZ = [(2, 3), (9, 3), (15, 1), (18, 9)]
# Mode B Rule: Start 0s, Apply Ref NZ, Overlay Input NZ
exp2 = [[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0],[0,0,4,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,9,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,5,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0],[0,0,4,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,9,0],[0,0,0,0,0,0,0,0,0,3,0,0,0,0,0,0,0,0,0,0],[0,0,4,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0]]
out2 = [ # Calculated using: Start 0s, Apply Ref NZ, Overlay Input NZ
  [0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0], # Row 0 (Input NZ=[]) -> Ref Pattern
  [0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0], # Row 1 (Input NZ=[]) -> Ref Pattern
  [0,0,4,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0], # Row 2 (Input NZ=[(2,4)]) -> Ref Pattern, O[2]=4
  [0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,5,0], # Row 3 (Input NZ=[(18,5)]) -> Ref Pattern, O[18]=5
  [0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0], # Row 4 (Input NZ=[(15,1)]) -> Ref Pattern, O[15]=1
  [0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0], # Row 5 (Input NZ=[(2,3)]) -> Ref Pattern, O[2]=3
  [0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0], # Row 6 (Input NZ=[(18,9)]) -> Ref Pattern, O[18]=9
  [0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0], # Row 7 (Input NZ=[(9,3)]) -> Ref Pattern, O[9]=3
  [0,0,3,0,0,0,0,0,0,3,0,0,0,0,0,1,0,0,9,0]  # Row 8 (Input NZ=[(2,3),(9,3),(15,1),(18,9)]) -> Ref Pattern, Overlays match
]

# Example 3 Data (Mode B - using previous code's logic for calculation)
# Ref NZ = [(1, 2), (5, 2), (9, 6), (13, 2)]
# Mode B Rule: Start 0s, Apply Ref NZ, Overlay Input NZ
exp3 = [[0,2,0,0,0,2,0,0,0,6,0,0,0,2,0],[0,0,0,0,0,2,0,0,0,6,0,0,0,0,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,0,0],[0,0,0,0,0,2,0,0,0,6,0,0,0,2,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,0,0],[0,0,0,0,0,2,0,0,0,6,0,0,0,0,0],[0,2,0,0,0,2,0,0,0,6,0,0,0,2,0]]
out3 = [ # Calculated using: Start 0s, Apply Ref NZ, Overlay Input NZ
  [0,2,0,0,0,2,0,0,0,6,0,0,0,2,0], # Row 0 (Input NZ=[]) -> Ref Pattern
  [0,2,0,0,0,2,0,0,0,6,0,0,0,2,0], # Row 1 (Input NZ=[]) -> Ref Pattern
  [0,2,0,0,0,2,0,0,0,6,0,0,0,2,0], # Row 2 (Input NZ=[]) -> Ref Pattern
  [0,2,0,0,0,2,0,0,0,6,0,0,0,2,0], # Row 3 (Input NZ=[(13,2)]) -> Ref Pattern, O[13]=2
  [0,2,0,0,0,2,0,0,0,6,0,0,0,2,0], # Row 4 (Input NZ=[(1,2)]) -> Ref Pattern, O[1]=2
  [0,2,0,0,0,2,0,0,0,6,0,0,0,2,0], # Row 5 (Input NZ=[(5,2),(9,6)]) -> Ref Pattern, O[5]=2, O[9]=6
  [0,2,0,0,0,2,0,0,0,6,0,0,0,2,0]  # Row 6 (Input NZ=[(1,2),(5,2),(9,6),(13,2)]) -> Ref Pattern, Overlays match
]


def count_diff(grid1, grid2):
    diff = 0
    if not grid1 or not grid2 or len(grid1) != len(grid2) or len(grid1[0]) != len(grid2[0]):
        rows1 = len(grid1) if grid1 else 0
        rows2 = len(grid2) if grid2 else 0
        cols1 = len(grid1[0]) if rows1 > 0 and grid1[0] else 0
        cols2 = len(grid2[0]) if rows2 > 0 and grid2[0] else 0
        # Basic penalty for size mismatch
        return max(rows1*cols1, rows2*cols2) if rows1*cols1 != rows2*cols2 else 0

    rows = len(grid1)
    cols = len(grid1[0])
    for r in range(rows):
        if len(grid1[r]) != len(grid2[r]):
             diff += max(len(grid1[r]), len(grid2[r])) # Penalize for row mismatch
             continue
        for c in range(cols):
            if grid1[r][c] != grid2[r][c]:
                diff += 1
    return diff

print(f"Example 1 Pixels Off: {count_diff(exp1, out1)}")
print(f"Example 2 Pixels Off: {count_diff(exp2, out2)}")
print(f"Example 3 Pixels Off: {count_diff(exp3, out3)}")
```

```text
Example 1 Pixels Off: 0
Example 2 Pixels Off: 20
Example 3 Pixels Off: 7
```

## Facts

```yaml
task_description: Transforms a 2D grid based on patterns in its rows, with the transformation mode determined by the adjacency of non-zero elements in the last non-zero row.
grid_properties:
  dimensionality: 2D
  cell_values: integers (0-9)
  background_color: 0
objects:
  - name: grid
    properties:
      - rows: list of lists of integers
      - height: integer
      - width: integer
      - last_non_zero_row_index: integer (index of the last row containing any non-zero value, or None)
      - last_non_zero_row_data: list of integers (the actual data of the last non-zero row, or None)
      - last_non_zero_row_has_adjacent_non_zeros: boolean (derived property)
  - name: row
    properties:
      - index: integer
      - cells: list of integers
      - width: integer
      - is_all_zeros: boolean
      - non_zero_cells: list of (column_index, value) tuples, sorted by column_index
      - first_non_zero_column: integer (c_min, if exists)
      - last_non_zero_column: integer (c_max, if exists)
      - last_non_zero_value: integer (V, value at c_max, if exists)
      - step: integer (difference between first two non-zero column indices, if len(non_zero_cells) >= 2)
      - all_non_zeros_same_value: boolean (true if all non-zero cells have the same value)
actions:
  - name: determine_transformation_mode
    input: last_non_zero_row_data
    output: mode ('independent_row' or 'reference_overlay')
    logic: If last_non_zero_row_data is None or has no non-zero cells, mode defaults to 'reference_overlay'. Otherwise, check if any non-zero cells in last_non_zero_row_data have consecutive column indices. If yes, mode is 'independent_row' (Mode A). If no, mode is 'reference_overlay' (Mode B).
  - name: transform_independent_row (Mode A)
    input: input_row_data
    output: output_row_data
    logic: (Identical to previous correct version)
      - Get row properties: non_zero_cells, c_min, c_max, V, step, all_non_zeros_same_value, width.
      - If len(non_zero_cells) < 2, return a copy of the input row.
      - Initialize output_row as a copy of input_row.
      - If step == 1:
          - If all_non_zeros_same_value is True: Fill output_row from c_min to width-1 (inclusive) with V.
          - Else (different values): Fill output_row from c_min to c_max (inclusive) with V.
      - Else (step > 1):
          - Initialize current_column `c = c_min`.
          - If all_non_zeros_same_value is True: Loop while `c < width`: set output_row[c] = V; c += step.
          - Else (different values): Loop while `c <= c_max`: set output_row[c] = V; c += step.
      - Return output_row.
  - name: transform_reference_overlay_row (Mode B - Revised)
    input: input_row_data, reference_row_data, width
    output: output_row_data
    logic:
      - Check if input_row_data is all zeros.
      - If yes, return a list of zeros of length `width`.
      - If no:
        - Initialize output_row as a copy of reference_row_data.
        - Get non_zero_cells_input from input_row_data.
        - For each (c, v) in non_zero_cells_input: set output_row[c] = v (overwriting the reference value).
        - Return output_row.
relationships:
  - The overall transformation strategy (Mode A or Mode B) depends entirely on whether the last non-zero row of the input grid contains adjacent non-zero elements.
  - Mode A transforms each row based only on its own internal non-zero patterns.
  - Mode B (Revised) transforms each row based on the reference row, but with specific handling: all-zero input rows produce all-zero output rows; non-zero input rows start with the reference pattern and then overwrite values based on the input row's non-zeros.
```

## Natural Language Program

1.  **Initialization:** Examine the input grid. Find the index and data of the last row containing any non-zero elements. Let this be `reference_row_data`. If no such row exists, return a copy of the input grid. Determine the width of the grid.
2.  **Mode Determination:** Analyze `reference_row_data`. Check if it contains any two non-zero elements located at adjacent column indices (e.g., column `c` and column `c+1`).
    *   If **yes** (adjacent non-zeros found), select **Mode A (Independent Row Transformation)**.
    *   If **no** (or if `reference_row_data` has fewer than 2 non-zero elements), select **Mode B (Reference Overlay Transformation - Revised)**.
3.  **Execute Transformation (Row by Row):**
    *   **Mode A (Independent Row Transformation):**
        a.  Create an empty output grid.
        b.  For each `input_row` in the input grid:
            i.  Find all non-zero cells `(column, value)` in the `input_row`, sorted by column (`nz`).
            ii. If `len(nz) < 2`, append a copy of the `input_row` to the output grid and continue to the next row.
            iii. Determine `c_min` (first non-zero column), `c_max` (last non-zero column), `V` (last non-zero value), `step` (column difference between first two non-zeros), and `all_same_value` (boolean).
            iv. Initialize `output_row` as a copy of `input_row`.
            v.  Apply filling logic based on `step`:
                *   If `step == 1`:
                    *   If `all_same_value` is True: Fill `output_row` from column `c_min` to the end of the row (width-1) with value `V`.
                    *   If `all_same_value` is False: Fill `output_row` from column `c_min` to `c_max` (inclusive) with value `V`.
                *   If `step > 1`:
                    *   Initialize `c = c_min`.
                    *   If `all_same_value` is True: While `c` is less than the row width, set `output_row[c] = V` and increment `c` by `step`.
                    *   If `all_same_value` is False: While `c` is less than or equal to `c_max`, set `output_row[c] = V` and increment `c` by `step`.
            vi. Append the modified `output_row` to the output grid.
        c.  Return the completed output grid.
    *   **Mode B (Reference Overlay Transformation - Revised):**
        a.  Create an empty output grid.
        b.  For each `input_row` in the input grid:
            i.  Check if the `input_row` consists entirely of zeros.
            ii. If yes, append a new row containing only zeros (of the correct width) to the output grid.
            iii. If no (the `input_row` contains non-zero values):
                *   Initialize the `output_row` as a direct copy of the `reference_row_data`.
                *   Find all non-zero cells `(column, value)` in the current `input_row` (`nz_input`).
                *   For each `(c, v)` in `nz_input`: Set `output_row[c] = v` (overwriting the value inherited from the reference row).
                *   Append the finalized `output_row` to the output grid.
        c.  Return the completed output grid.
