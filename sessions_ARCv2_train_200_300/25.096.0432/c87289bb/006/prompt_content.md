
Previous Code:
```python
import copy

"""
Transforms the input grid by identifying a top block of identical rows and using 
patterns within this block and the locations of '2's below it to determine 
which columns should be filled vertically with '8's below the block.

1. Identify the initial block of identical rows at the top ('Header Block').
2. Find columns containing '8' within this Header Block ('Header8Cols').
3. Find columns containing '2' anywhere in the grid ('TwoCols').
4. Find columns immediately adjacent to any column in 'TwoCols' ('NeighboursOfTwoCols').
5. Determine neighbour columns that don't contain '2's themselves ('NeighboursToFill').
6. Combine 'Header8Cols' and 'NeighboursToFill' to get the final set of columns 
   to modify ('TargetFillCols').
7. Below the Header Block, iterate through the 'TargetFillCols' and change any '0's 
   to '8's, preserving existing non-zero values like '2'.
"""

# === Helper Functions ===

def find_last_top_row(grid: list[list[int]]) -> int:
    """
    Finds the index of the last row belonging to the initial block of identical top rows.
    """
    if not grid:
        return -1
    if len(grid) == 1:
        return 0

    first_row = grid[0]
    last_top_row = 0
    for r in range(1, len(grid)):
        # Check for row length consistency before comparing content
        if len(grid[r]) == len(first_row) and grid[r] == first_row:
            last_top_row = r
        else:
            break
    return last_top_row

def get_cols_with_value_in_rows(grid: list[list[int]], value: int, start_row: int, end_row_inclusive: int) -> set[int]:
    """
    Finds the indices of columns containing the specified value within the specified row range.
    """
    cols = set()
    if not grid or not grid[0]: return cols
    num_cols = len(grid[0]) # Assume rectangular grid for simplicity based on examples
    
    # Adjust end_row_inclusive to be within grid bounds
    actual_end_row = min(end_row_inclusive, len(grid) - 1)
    
    for c in range(num_cols):
        for r in range(start_row, actual_end_row + 1):
             # Check column index is valid for the current row
            if c < len(grid[r]) and grid[r][c] == value:
                cols.add(c)
                break # Found in this column, move to next column
    return cols

def get_cols_with_value_anywhere(grid: list[list[int]], value: int) -> set[int]:
    """
    Finds the indices of columns containing the specified value anywhere in the grid.
    """
    cols = set()
    if not grid: return cols
    num_rows = len(grid)
    if num_rows == 0 or not grid[0]: return cols
    num_cols = len(grid[0]) # Assume rectangular

    for r in range(num_rows):
         for c in range(num_cols):
             # Check column index is valid for the current row
             if c < len(grid[r]) and grid[r][c] == value:
                 cols.add(c)
                 # Optimization: If we only care if the column *ever* contains the value,
                 # we could potentially break to the next column earlier, but checking
                 # all rows is safer if we later need counts or positions.
                 # For just identifying columns, we can make this faster:
                 # Add c to cols and break the inner loop 'for c in range(num_cols):'
                 # This requires restructuring the loops (iterate rows first).

    # Alternative (potentially faster if value is sparse)
    # for c in range(num_cols):
    #     for r in range(num_rows):
    #         if c < len(grid[r]) and grid[r][c] == value:
    #             cols.add(c)
    #             break # Move to next column

    return cols

def get_neighbours(cols: set[int], num_total_cols: int) -> set[int]:
    """
    Finds the set of unique column indices adjacent to the indices in the input set.
    Handles boundary conditions (column 0 and last column).
    """
    neighbours = set()
    if num_total_cols <= 0: return neighbours
    
    for c in cols:
        # Add left neighbour if not the first column
        if c > 0:
            neighbours.add(c - 1)
        # Add right neighbour if not the last column
        if c < num_total_cols - 1:
            neighbours.add(c + 1)
    return neighbours

# === Main Transform Function ===

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        return []

    # Initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)
    num_rows = len(input_grid)
    num_cols = len(input_grid[0]) # Assume rectangular

    # --- Workflow ---

    # 1. Find the extent of the identical top block
    last_top_row = find_last_top_row(input_grid)

    # 2. Identify columns with '8' in the header block
    header_8_cols = get_cols_with_value_in_rows(input_grid, 8, 0, last_top_row)

    # 3. Identify columns with '2' anywhere in the grid
    two_cols = get_cols_with_value_anywhere(input_grid, 2)

    # 4. Find immediate neighbours of the '2' columns
    neighbours_of_two = get_neighbours(two_cols, num_cols)

    # 5. Filter neighbours: keep only those that DON'T contain '2's themselves
    neighbours_to_fill = neighbours_of_two - two_cols

    # 6. Determine the final set of columns to fill below the header
    # Combine columns from header and qualified neighbours
    target_fill_cols = header_8_cols.union(neighbours_to_fill)

    # 7. Fill downwards in the target columns below the header block
    start_fill_row = last_top_row + 1
    for r in range(start_fill_row, num_rows):
        for c in target_fill_cols:
            # Ensure column index is valid (safety check)
            if c < len(output_grid[r]):
                # Only change the cell if it's currently '0'
                if output_grid[r][c] == 0:
                    output_grid[r][c] = 8

    # Return the modified grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 8 0 0 0 8 0 8 0 0 8 0
0 8 0 0 0 8 0 8 0 0 8 0
0 8 0 0 0 8 0 8 0 0 8 0
0 8 0 0 0 8 0 8 0 0 8 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 8 0 0 0 8 0 8 0 0 8 0
0 8 0 0 0 8 0 8 0 0 8 0
0 8 0 0 0 8 0 8 0 0 8 0
0 8 0 0 0 8 0 8 0 0 8 0
8 8 0 0 8 8 0 8 8 0 8 0
8 2 2 0 8 2 2 2 8 0 8 0
8 0 0 0 8 0 0 0 8 0 8 0
8 0 0 0 8 0 0 0 8 0 8 0
8 0 0 0 8 0 0 0 8 0 8 0
8 0 0 0 8 0 0 0 8 0 8 0
```
Transformed Output:
```
0 8 0 0 0 8 0 8 0 0 8 0
0 8 0 0 0 8 0 8 0 0 8 0
0 8 0 0 0 8 0 8 0 0 8 0
0 8 0 0 0 8 0 8 0 0 8 0
8 8 0 8 8 8 0 8 8 0 8 0
8 2 2 8 8 2 2 2 8 0 8 0
8 8 0 8 8 8 0 8 8 0 8 0
8 8 0 8 8 8 0 8 8 0 8 0
8 8 0 8 8 8 0 8 8 0 8 0
8 8 0 8 8 8 0 8 8 0 8 0
```
Match: False
Pixels Off: 18
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 30.0

## Example 2:
Input:
```
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8 0 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 8 8 0 8 8 8 0 8
0 8 0 8 8 2 2 2 8 8 0 8
0 8 0 8 8 0 0 0 8 8 0 8
0 8 0 8 8 0 0 0 8 8 0 8
0 8 0 8 8 0 0 0 8 8 0 8
0 8 0 8 8 0 0 0 8 8 0 8
```
Transformed Output:
```
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8 0 8
0 8 0 8 8 8 0 8 8 8 0 8
0 8 0 8 8 2 2 2 8 8 0 8
0 8 0 8 8 8 0 8 8 8 0 8
0 8 0 8 8 8 0 8 8 8 0 8
0 8 0 8 8 8 0 8 8 8 0 8
0 8 0 8 8 8 0 8 8 8 0 8
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 13.333333333333343

## Example 3:
Input:
```
8 0 8 0 0 0 8 0 0 8 0 8
8 0 8 0 0 0 8 0 0 8 0 8
8 0 8 0 0 0 8 0 0 8 0 8
8 0 8 0 0 0 8 0 0 8 0 8
0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
8 0 8 0 0 0 8 0 0 8 0 8
8 0 8 0 0 0 8 0 0 8 0 8
8 0 8 0 0 0 8 0 0 8 0 8
8 0 8 0 0 0 8 0 0 8 0 8
8 8 8 0 0 0 8 8 8 8 0 8
8 8 2 2 0 2 2 2 8 8 0 8
8 8 0 0 0 0 0 0 8 8 0 8
8 8 0 0 0 0 0 0 8 8 0 8
8 8 0 0 0 0 0 0 8 8 0 8
8 8 0 0 0 0 0 0 8 8 0 8
```
Transformed Output:
```
8 0 8 0 0 0 8 0 0 8 0 8
8 0 8 0 0 0 8 0 0 8 0 8
8 0 8 0 0 0 8 0 0 8 0 8
8 0 8 0 0 0 8 0 0 8 0 8
8 8 8 0 8 0 8 0 8 8 0 8
8 8 2 2 8 2 2 2 8 8 0 8
8 8 8 0 8 0 8 0 8 8 0 8
8 8 8 0 8 0 8 0 8 8 0 8
8 8 8 0 8 0 8 0 8 8 0 8
8 8 8 0 8 0 8 0 8 8 0 8
```
Match: False
Pixels Off: 15
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 25.0

## Example 4:
Input:
```
0 8 0 0 0 8 0 0 0 8
0 8 0 0 0 8 0 0 0 8
0 8 0 0 0 8 0 0 0 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 8 0 0 0 8 0 0 0 8
0 8 0 0 0 8 0 0 0 8
0 8 0 0 0 8 0 0 0 8
0 8 0 0 0 8 8 8 0 8
0 8 0 0 2 2 2 8 0 8
0 8 0 0 0 0 0 8 0 8
0 8 0 0 0 0 0 8 0 8
0 8 0 0 0 0 0 8 0 8
0 8 0 0 0 0 0 8 0 8
```
Transformed Output:
```
0 8 0 0 0 8 0 0 0 8
0 8 0 0 0 8 0 0 0 8
0 8 0 0 0 8 0 0 0 8
0 8 0 8 0 8 0 8 0 8
0 8 0 8 2 2 2 8 0 8
0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8
0 8 0 8 0 8 0 8 0 8
```
Match: False
Pixels Off: 11
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 24.444444444444457
