
## train_1

**input:**
```
4 4 4 4 1
4 4 4 4 0
4 4 4 4 0
4 4 4 4 0
```


**output:**
```
4 4 4 4 0 4 4 4 4
4 4 4 4 0 4 4 4 4
4 4 4 4 0 4 4 4 4
4 4 4 4 0 4 4 4 4
```


## train_2

**input:**
```
3 3 3 1 1
3 3 3 0 0
3 3 3 0 0
```


**output:**
```
3 3 3 0 3 3 3 0 3 3 3
3 3 3 0 3 3 3 0 3 3 3
3 3 3 0 3 3 3 0 3 3 3
```


## train_3

**input:**
```
6 6 6 6
6 4 4 6
6 6 6 6
1 0 0 0
1 0 0 0
1 0 0 0
```


**output:**
```
6 6 6 6
6 4 4 6
6 6 6 6
0 0 0 0
6 6 6 6
6 4 4 6
6 6 6 6
0 0 0 0
6 6 6 6
6 4 4 6
6 6 6 6
0 0 0 0
6 6 6 6
6 4 4 6
6 6 6 6
```

Okay, let's break down the transformation logic for these examples.

**Perception of Task Elements:**

1.  **Input/Output Format:** Both inputs and outputs are 2D grids (matrices) of single-digit integers.
2.  **Key Element:** The number '1' seems to play a crucial role as a marker or separator within the input grid. Its position and distribution dictate the transformation type.
3.  **Transformation Types:** Two distinct transformation patterns emerge based on the arrangement of '1's:
    *   **Horizontal Expansion (train\_1, train\_2):** When '1' appears in a single column, the grid is expanded horizontally. The process involves identifying parts of the grid relative to the '1' column, modifying the '1' column, and repeating/concatenating these parts.
    *   **Vertical Expansion (train\_3):** When '1' appears in a block of rows (specifically, these rows start with '1' and are grouped together in the example), the grid is expanded vertically. The process involves identifying blocks of rows relative to the '1'-containing rows, creating a zero-filled row, and repeating/stacking these parts.
4.  **Core Operations:** The transformations involve partitioning the input grid, replacing '1' with '0', repetition, and concatenation (horizontal or vertical stacking).

**Facts (YAML):**


```yaml
Task: Grid Transformation based on '1' marker

Input:
  Type: 2D Grid (List of Lists of Integers)
  Objects:
    - Grid: The entire input matrix.
    - Marker_Cell: Cell(s) containing the value '1'.
    - Partition_A: Subgrid identified based on Marker_Cell location.
    - Partition_B: Subgrid/Column/Row containing the Marker_Cell.
    - Partition_C: (Optional) Subgrid identified based on Marker_Cell location (relevant for horizontal case).
  Properties:
    - Dimensions: rows, columns
    - Marker_Location: Coordinates or defining axis (column index or row indices) of '1'.
    - Marker_Distribution: Pattern of '1's (single column vs. block of rows).

Output:
  Type: 2D Grid (List of Lists of Integers)
  Construction: Based on repeating and assembling parts derived from the input.

Actions:
  - Locate_Marker: Find the position(s) of '1'.
  - Determine_Axis: Identify if the transformation is primarily horizontal or vertical based on '1' distribution.
  - Partition_Grid: Divide the input grid into relevant parts (A, B, C or A, B) based on the marker and axis.
  - Modify_Marker_Region: Create a new element (Column 0 or Row 0) by replacing '1's with '0's in the marker's region (Partition B).
  - Calculate_Repetitions: Determine the number of repetitions based on the size of a specific partition (Partition C for horizontal, Partition B for vertical).
  - Assemble_Output: Construct the output grid by repeating and concatenating/stacking the derived parts according to the determined axis and repetition count.

Relationships:
  - Output grid's structure and content are derived from the input grid's partitions.
  - The location and pattern of '1's dictate the partitioning strategy and assembly method (horizontal vs. vertical).
  - The size of certain input partitions determines the number of repetitions in the output.
```


**Natural Language Program:**

1.  **Analyze Marker:** Examine the input grid to locate all cells containing the value '1'. Determine the distribution pattern of these '1's.
2.  **Branch by Pattern:**
    *   **If '1's are confined to a single column:**
        a.  Identify this column as `Column B`.
        b.  Identify the block of columns to the left of `Column B` as `Matrix A`.
        c.  Identify the block of columns to the right of `Column B` as `Matrix C`. If no columns are to the right, `Matrix C` is empty.
        d.  Create `Column 0` by copying `Column B` and changing the cell(s) containing '1' to '0'.
        e.  Count the number of columns in `Matrix C` (call this `N_right`).
        f.  Define a repeating block as the horizontal concatenation `[Matrix A | Column 0]`.
        g.  Construct the output by horizontally concatenating the repeating block `(N_right + 1)` times, followed by `Matrix A`.
    *   **If '1's are found in a contiguous block of rows (specifically, rows where '1' appears, potentially at the start):**
        a.  Identify these rows as `Subgrid B`.
        b.  Identify the contiguous block of rows above `Subgrid B` (which do not contain '1') as `Subgrid A`. Assume `Subgrid B` is below `Subgrid A`.
        c.  Create `Row 0`, a single row filled entirely with '0's, having the same width as the input grid.
        d.  Count the number of rows in `Subgrid B` (call this `N_rows_B`).
        e.  Define a repeating block as the vertical stacking `[Subgrid A / Row 0]` (where `/` denotes stacking rows).
        f.  Construct the output by vertically stacking the repeating block `N_rows_B` times, followed by `Subgrid A`.
3.  **Return:** Output the final constructed grid.
```python
import numpy as np
from typing import List, Tuple

"""
Transforms an input grid based on the location and pattern of the number '1'.

The transformation follows one of two rules:

1.  **Horizontal Expansion:** If all '1's are located within a single column:
    a.  The grid is partitioned into three parts: `Matrix A` (columns left of the '1' column), `Column B` (the '1' column), and `Matrix C` (columns right of the '1' column).
    b.  A new `Column 0` is created by replacing the '1'(s) in `Column B` with '0'.
    c.  The output is constructed by repeating the concatenation `[Matrix A | Column 0]` horizontally `N+1` times (where `N` is the number of columns in `Matrix C`), followed by a final `Matrix A`.

2.  **Vertical Expansion:** If all '1's are located within a contiguous block of rows:
    a.  The grid is partitioned into two parts: `Subgrid A` (rows above the '1' block) and `Subgrid B` (the contiguous rows containing all the '1's).
    b.  A new `Row 0` is created, consisting entirely of '0's with the same width as the input grid.
    c.  The output is constructed by repeating the vertical stack `[Subgrid A / Row 0]` `M` times (where `M` is the number of rows in `Subgrid B`), followed by a final `Subgrid A`.

If the '1' pattern doesn't match either of these specific cases, the behavior is undefined by the examples.
"""

def find_marker_positions(grid: np.ndarray, marker: int = 1) -> List[Tuple[int, int]]:
    """Finds all occurrences of the marker value in the grid."""
    rows, cols = np.where(grid == marker)
    return list(zip(rows, cols))

def determine_pattern(marker_positions: List[Tuple[int, int]], grid_shape: Tuple[int, int]) -> Tuple[str, int | Tuple[int, int]]:
    """
    Determines the pattern of marker positions ('column' or 'rows').

    Returns:
        A tuple: (pattern_type, relevant_indices)
        - If 'column': ('column', column_index)
        - If 'rows': ('rows', (start_row_index, end_row_index))
        - If 'unknown': ('unknown', -1)
    """
    if not marker_positions:
        return 'unknown', -1 # No marker found

    rows, cols = zip(*marker_positions)
    unique_cols = set(cols)
    unique_rows = set(rows)

    # Check for single column pattern
    if len(unique_cols) == 1:
        return 'column', unique_cols.pop()

    # Check for contiguous block of rows pattern
    min_row, max_row = min(unique_rows), max(unique_rows)
    if max_row - min_row + 1 == len(unique_rows):
         # Check if ALL markers are within this contiguous block
         # (This check is implicitly true if we reached here after failing the column check)
        return 'rows', (min_row, max_row)

    return 'unknown', -1


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid based on '1' marker patterns.
    """
    if not input_grid or not input_grid[0]:
        return [] # Handle empty input

    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    grid_shape = grid.shape

    # 1. Analyze Marker: Find '1's and determine the pattern
    marker_positions = find_marker_positions(grid, 1)

    if not marker_positions:
        # If no '1' is found, maybe return the input unchanged or handle as error?
        # Based on examples, '1' is always present. Assuming valid input.
        # For robustness, let's return input as is if no marker.
         return input_grid


    pattern_type, indices = determine_pattern(marker_positions, grid_shape)

    # 2. Branch by Pattern
    output_grid_np = None

    if pattern_type == 'column':
        # Horizontal Expansion Logic
        marker_col = indices
        num_cols = grid_shape[1]

        # a. Identify partitions
        matrix_a = grid[:, :marker_col] if marker_col > 0 else None
        column_b = grid[:, marker_col:marker_col+1] # Keep as 2D column
        matrix_c = grid[:, marker_col+1:] if marker_col < num_cols - 1 else None

        # b. Create Column 0
        column_0 = np.where(column_b == 1, 0, column_b)

        # c. Calculate Repetitions
        n_right = matrix_c.shape[1] if matrix_c is not None else 0
        repetitions = n_right + 1

        # d. Define repeating block
        # Handle cases where matrix_a is None (marker is in the first column)
        if matrix_a is not None:
             repeating_block = np.hstack((matrix_a, column_0))
        else:
             repeating_block = column_0 # If marker is col 0, block is just Column 0


        # e. Assemble Output
        output_parts = []
        for _ in range(repetitions):
             output_parts.append(repeating_block)

        # Add the final Matrix A if it exists
        if matrix_a is not None:
            output_parts.append(matrix_a)

        # Concatenate all parts horizontally
        if output_parts:
             output_grid_np = np.hstack(output_parts)
        else: # Should not happen with valid inputs, but handle gracefully
             output_grid_np = np.array([[]] * grid_shape[0]) # Empty grid with correct rows


    elif pattern_type == 'rows':
        # Vertical Expansion Logic
        start_row, end_row = indices
        num_rows, num_cols = grid_shape

        # a. Identify partitions
        subgrid_a = grid[:start_row, :] if start_row > 0 else None
        # Subgrid B is defined by the rows containing '1's, its size is used for reps
        subgrid_b_row_count = end_row - start_row + 1

        # b. Create Row 0
        row_0 = np.zeros((1, num_cols), dtype=int)

        # c. Calculate Repetitions
        repetitions = subgrid_b_row_count

        # d. Define repeating block part (Subgrid A / Row 0)
        # Handle cases where subgrid_a is None (marker rows start at row 0)
        if subgrid_a is not None:
            repeating_block_part = np.vstack((subgrid_a, row_0))
        else:
            repeating_block_part = row_0 # If marker rows start at 0, block is just Row 0


        # e. Assemble Output
        output_parts = []
        for _ in range(repetitions):
            output_parts.append(repeating_block_part)

        # Add the final Subgrid A if it exists
        if subgrid_a is not None:
            output_parts.append(subgrid_a)

        # Stack all parts vertically
        if output_parts:
            output_grid_np = np.vstack(output_parts)
        else: # Should not happen if repetitions > 0
            output_grid_np = np.array([[]]) # Empty grid


    else: # pattern_type == 'unknown'
        # Handle unknown patterns - perhaps return input or raise error
        # For now, return input grid as per robustness comment earlier
        return input_grid


    # Convert numpy array back to list of lists for the final output
    return output_grid_np.tolist()

```
