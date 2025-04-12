
## train_1

**input:**
```
4 4 4 4 4 4 4 4 1 7 7 7 1
4 1 1 7 7 7 1 4 1 4 4 4 4
4 1 1 1 1 1 1 4 1 4 1 1 4
4 1 1 1 1 1 1 4 1 4 1 1 4
4 1 1 1 1 1 1 4 1 1 4 4 1
4 1 1 1 1 1 1 4 1 1 1 1 1
4 4 4 4 4 4 4 4 1 1 1 1 1
```


**output:**
```
4 4 4 4 4 4 4 4
4 1 1 4 4 4 4 4
4 1 1 4 1 1 4 4
4 1 1 4 1 1 4 4
4 1 1 1 4 4 1 4
4 1 1 1 1 1 1 4
4 4 4 4 4 4 4 4
```


## train_2

**input:**
```
4 1 1 1 1 1 1 1 1 1 7 1 4
4 4 4 4 4 4 1 1 1 1 4 4 4
1 1 1 4 1 4 1 1 1 1 1 1 1
1 4 4 4 4 4 1 1 1 1 1 1 1
1 4 1 1 1 1 1 1 1 1 1 1 1
1 4 1 1 1 1 1 1 1 1 1 1 1
1 7 1 1 1 1 1 1 1 1 1 1 1
```


**output:**
```
4 1 1 1 1 1
4 4 4 4 4 4
1 1 1 4 1 4
1 4 4 4 4 4
1 4 1 1 1 1
1 4 1 4 1 1
1 4 4 4 1 1
```


## train_3

**input:**
```
4 4 4
4 1 4
4 4 4
7 7 7
1 1 1
7 7 7
4 4 4
4 1 4
4 4 4
```


**output:**
```
4 4 4
4 1 4
4 4 4
4 4 4
4 1 4
4 4 4
```


## train_4

**input:**
```
4 4 4 4 1 1 1 1 1
4 1 1 4 1 1 1 1 1
4 4 4 4 4 4 1 1 1
1 1 1 1 1 4 1 1 1
1 1 1 1 1 7 1 4 4
1 1 7 1 1 1 1 4 1
1 1 4 4 4 4 4 4 1
```


**output:**
```
4 4 4 4 1 1 1 1 1 1 1 1
4 1 1 4 1 1 1 1 1 1 1 1
4 4 4 4 4 4 1 1 1 1 4 4
1 1 1 1 1 4 1 1 1 1 4 1
1 1 1 1 1 4 4 4 4 4 4 1
```

## Perception

1.  **Grid Structure:** The input and output are 2D grids of numbers (colors).
2.  **Color Palette:** The primary colors used are 1, 4, and 7. Color 4 often appears as a background or frame color. Color 1 appears as a foreground or fill color. Color 7 seems to be a special marker or signal, not part of the final output pattern.
3.  **Transformation Signal:** The presence and position of the number '7' heavily influence the transformation. The number '7' itself is consistently absent from the output grid.
4.  **Dimensional Changes:** The dimensions (height and width) of the grid often change between input and output.
    *   Height can decrease (train_3, train_4).
    *   Width can decrease (train_1, train_2).
    *   Width can increase (train_4).
5.  **Row Operations:** In some examples (train_3, train_4), rows containing the number '7' are removed from the input to produce the output. In train_3, a row containing only '1's situated between two rows containing '7's is also removed.
6.  **Column Operations:** In other examples (train_1, train_2), the output grid appears to be a horizontally cropped version of the input grid, possibly after some modification related to the '7's. The exact cropping logic is not immediately clear but might relate to the column index of the first '7'.
7.  **Element Replacement:** In the cases involving cropping (train_1, train_2), the '7's might be conceptually replaced (e.g., with '4') before or during the cropping, although simple replacement doesn't fully explain the output patterns.
8.  **Grid Extension:** In train_4, besides row removal, the width of the remaining rows increases, suggesting data is appended to the rows. The source of this appended data is unclear but might relate to the content of the removed rows or columns containing '7'.
9.  **Conditional Logic:** The transformation rule appears conditional, potentially branching based on the specific configuration or location of the '7's (e.g., whether they appear in the first/last row, whether they span multiple rows/columns in specific ways, or if entire rows consist only of '7's).

## Facts

```yaml
elements:
  - object: grid
    properties:
      - representation: 2D array of integers
      - colors: [1, 4, 7] (potentially others, but these are key)
      - dimensions: height (rows), width (columns)
  - object: color_7
    properties:
      - role: signal, marker, instruction
      - characteristic: transient (present in input, absent in output)
      - location: specific cell coordinates (row, column)

actions:
  - action: identify_signal_locations
    actor: transformation process
    input: input grid
    output: set of coordinates [(r1, c1), (r2, c2), ...] where the value is 7
  - action: determine_transformation_type
    actor: transformation process
    input: locations of color_7, grid properties (e.g., dimensions)
    output: type of operation (e.g., row_removal, column_crop_modify, row_removal_and_extension)
    logic_notes: The specific condition distinguishing the types is not fully clear. Possibilities include: presence of 7 in edge rows/columns, presence of rows solely consisting of 7s, etc.
  - action: remove_rows
    actor: transformation process
    input: input grid, rows_to_remove (identified based on color_7 presence, potentially including adjacent all-'1' rows)
    output: intermediate grid (reduced height)
  - action: modify_and_crop_columns
    actor: transformation process
    input: input grid (or modified version where 7s are replaced), target_width (potentially calculated based on first column containing 7)
    output: intermediate grid (reduced width, potentially modified content)
  - action: extend_rows
    actor: transformation process
    input: intermediate grid (after row removal), extension_data (source unclear, maybe from removed rows/columns)
    output: final grid (increased width)
  - action: replace_signal_color
    actor: transformation process
    input: grid, coordinates containing 7
    output: grid with 7 replaced by another color (e.g., 4) - this might be a sub-step within modify_and_crop_columns.

relationships:
  - relationship: controls
    subject: color_7 location(s)
    object: transformation_type selection
  - relationship: defines
    subject: color_7 location(s)
    object: rows_to_remove (in row_removal type)
  - relationship: defines
    subject: color_7 location(s) (e.g., first column index)
    object: target_width (in column_crop_modify type)
  - relationship: determines
    subject: transformation_type
    object: sequence of actions (e.g., remove_rows only vs. modify_and_crop_columns vs remove_rows then extend_rows)
```

## Natural Language Program

1.  **Analyze Signal:** Identify all cells in the input grid containing the number 7. Note their row and column indices.
2.  **Determine Operation Mode:** Based on the pattern and location of the 7s, determine the primary operation mode:
    *   **Mode A (Row Removal):** This mode seems active when 7s are present but potentially *not* in the first or last row (or perhaps triggered by other conditions like entire rows of 7s, observed in train_3, or just non-edge presence as in train_4).
    *   **Mode B (Column Crop/Modify):** This mode seems active when 7s *are* present in the first or last row (train_1, train_2).
    *   **Mode C (Row Removal + Extension):** This mode seems active in train_4, involving both row removal and subsequent width extension. (This might be a variation of Mode A).
3.  **Execute Operation:**
    *   **If Mode A (Row Removal):**
        a. Identify all rows `R_7` that contain at least one 7.
        b. Identify all rows `R_1_sandwiched` that consist entirely of 1s and are located vertically between two rows belonging to `R_7`.
        c. Create the output grid by taking all rows from the input grid *except* those in `R_7` and `R_1_sandwiched`, maintaining their original order.
    *   **If Mode B (Column Crop/Modify):**
        a. Find the minimum column index `min_c` where a 7 appears in any row.
        b. Calculate the target output width `W_out = min_c + 5`.
        c. Create a temporary copy of the input grid.
        d. In the temporary grid, replace all occurrences of 7 with 4.
        e. Create the output grid by taking only the first `W_out` columns from the modified temporary grid. (*Note: This step doesn't perfectly match outputs for train_1 and train_2, suggesting the modification/cropping logic might be more complex.*)
    *   **If Mode C (Row Removal + Extension):**
        a. Perform the row removal step as described in Mode A (remove rows with 7).
        b. Determine the necessary extension width and the data to append to each remaining row. (*Note: The logic for determining the appended data and width extension based on the input and removed rows/columns is not clear from the examples.*)
        c. Append the determined data to the right side of each remaining row to form the final output grid.
4.  **Final Output:** The grid resulting from the selected operation mode is the final output.
```python
import numpy as np
from typing import List, Tuple, Set

"""
The transformation rule distinguishes between two primary modes based on the location of the number 7 in the input grid.

1.  **Analyze Signal:** Identify all cells containing the number 7.
2.  **Determine Operation Mode:**
    *   **Mode A (Row Removal):** If no 7s are present in the first row (row 0) or the last row.
    *   **Mode B (Column Crop):** If any 7 is present in the first row or the last row.
3.  **Execute Operation:**
    *   **If Mode A:**
        a. Identify the set of row indices `R_7` that contain at least one 7.
        b. Identify the set of row indices `R_1_sandwiched` corresponding to rows that:
            i. Consist entirely of the number 1.
            ii. Are located strictly between two rows whose indices are in `R_7`. (e.g., row `r` is sandwiched if `r1 < r < r2` for some `r1, r2` in `R_7`, and row `r` contains only 1s).
        c. Construct the output grid by keeping all rows from the input grid whose indices are *not* in `R_7` and *not* in `R_1_sandwiched`, maintaining their original relative order.
        d. (Note: The extension observed in train_4 is not implemented in this version).
    *   **If Mode B:**
        a. Find the minimum column index `min_c` where a 7 appears in *any* row.
        b. Construct the output grid by taking only the first `min_c` columns from each row of the *original* input grid.
        c. (Note: This is a simplified interpretation for Mode B based on observations; it doesn't perfectly match train_1 and train_2 outputs and needs refinement).
4.  **Final Output:** The grid resulting from the selected operation mode.
"""

def find_value_coords(grid: np.ndarray, value: int) -> List[Tuple[int, int]]:
    """Finds all (row, col) coordinates of cells containing the specified value."""
    rows, cols = np.where(grid == value)
    return list(zip(rows, cols))

def get_rows_with_value(grid: np.ndarray, value: int) -> Set[int]:
    """Returns a set of row indices that contain the specified value."""
    coords = find_value_coords(grid, value)
    return set(r for r, c in coords)

def is_row_all_value(row: np.ndarray, value: int) -> bool:
    """Checks if a 1D numpy array (a row) contains only the specified value."""
    return np.all(row == value)

def find_sandwiched_rows(grid: np.ndarray, value_to_find: int, sandwiching_row_indices: Set[int]) -> Set[int]:
    """
    Finds indices of rows that contain only `value_to_find` and are
    vertically sandwiched between rows specified by `sandwiching_row_indices`.
    """
    sandwiched_indices = set()
    if not sandwiching_row_indices:
        return sandwiched_indices

    sorted_sandwich_indices = sorted(list(sandwiching_row_indices))
    
    for r_idx in range(grid.shape[0]):
        # Check if the row itself is one of the sandwiching rows
        if r_idx in sandwiching_row_indices:
            continue
            
        # Check if the row contains only the target value (e.g., 1)
        if is_row_all_value(grid[r_idx, :], value_to_find):
            # Check if there exists a sandwiching row above and below it
            has_above = any(sr < r_idx for sr in sorted_sandwich_indices)
            has_below = any(sr > r_idx for sr in sorted_sandwich_indices)
            
            if has_above and has_below:
                sandwiched_indices.add(r_idx)
                
    return sandwiched_indices

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on the presence and location of the number 7.
    """
    if not input_grid or not input_grid[0]:
        return []
        
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # 1. Analyze Signal
    coords_7 = find_value_coords(grid, 7)
    rows_with_7 = set(r for r, c in coords_7)

    # 2. Determine Operation Mode
    mode = 'A' # Default to Row Removal
    if height > 0:
        # Check first row (index 0) and last row (index height-1)
        if 0 in rows_with_7 or (height - 1) in rows_with_7:
            mode = 'B' # Column Crop mode if 7 is in boundary rows

    output_grid_np = None

    # 3. Execute Operation
    if mode == 'B':
        # Mode B: Column Crop (Simplified version)
        if not coords_7: # Should not happen if mode B is triggered, but handle defensively
             output_grid_np = grid # No 7s, return original? Or handle based on problem spec. Assume return original for now.
        else:
            min_c = min(c for r, c in coords_7)
            # Take the first 'min_c' columns
            output_grid_np = grid[:, :min_c]
            
    else: # mode == 'A'
        # Mode A: Row Removal
        
        # Identify rows consisting entirely of 1s sandwiched between rows containing 7s
        sandwiched_1_rows = find_sandwiched_rows(grid, 1, rows_with_7)
        
        # Rows to remove are those with 7s plus the sandwiched '1' rows
        rows_to_remove = rows_with_7.union(sandwiched_1_rows)
        
        # Keep rows whose indices are not in the removal set
        rows_to_keep = [r for r in range(height) if r not in rows_to_remove]
        
        if not rows_to_keep:
             output_grid_np = np.empty((0, width), dtype=int) # Return empty grid if all rows removed
        else:
             output_grid_np = grid[rows_to_keep, :]
             # Note: Extension logic for train_4 (Mode C) is not implemented here.

    # 4. Final Output
    # Convert numpy array back to list of lists
    if output_grid_np is None: # Should ideally not happen with current logic
        return []
        
    output_list = output_grid_np.tolist()
    
    # Handle case where output is empty (e.g., all rows removed or cropped to zero width)
    if output_grid_np.size == 0 and output_grid_np.shape[1] > 0: # Rows removed, keep original width structure for empty list
         return []
    elif output_grid_np.size == 0 and output_grid_np.shape[1] == 0: # Cropped to zero width
        # Return list of empty lists, one for each kept row
        return [[] for _ in range(output_grid_np.shape[0])]
        
    return output_list
```
