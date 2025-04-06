
## train_1

**input:**
```
7 7 7 7 7 7 7
7 8 7 7 7 7 7
7 8 7 2 7 7 7
7 8 7 2 7 7 7
7 8 7 2 7 7 7
7 8 7 2 7 7 7
```


**output:**
```
7 7 7 7 7 7 7
7 8 7 7 7 7 7
7 8 7 2 7 7 7
7 8 7 2 7 7 7
7 8 7 2 7 7 7
7 8 7 2 7 5 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7
7 7 7 7 7 7 7
7 7 7 7 7 7 7
7 7 7 8 7 7 7
7 8 7 8 7 7 7
7 8 7 8 7 7 7
```


**output:**
```
7 7 7 7 7 7 7
7 7 7 7 7 5 7
7 7 7 7 7 5 7
7 7 7 8 7 5 7
7 8 7 8 7 5 7
7 8 7 8 7 5 7
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 2 7 7 7 7 7
7 7 7 8 7 2 7 7 7 7 7
7 7 7 8 7 2 7 7 7 7 7
7 7 7 8 7 2 7 8 7 7 7
7 8 7 8 7 2 7 8 7 7 7
7 8 7 8 7 2 7 8 7 7 7
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 2 7 7 7 7 7
7 7 7 8 7 2 7 7 7 7 7
7 7 7 8 7 2 7 7 7 5 7
7 7 7 8 7 2 7 8 7 5 7
7 8 7 8 7 2 7 8 7 5 7
7 8 7 8 7 2 7 8 7 5 7
```

Okay, let's break down the transformation logic for these grid examples.

**Perception of the Elements:**

1.  **Input/Output Format:** Both input and output are grids (matrices) of single digits. The grids are represented as text, with digits separated by spaces within a row, and rows separated by newlines.
2.  **Grid Content:** The grids primarily consist of the digit '7'. Digits '8' and '2' appear in specific locations in the input. The digit '5' appears in the output, replacing existing digits ('7' in the examples).
3.  **Transformation Nature:** The transformation selectively changes certain cells to '5' based on the presence and location of '8's or '2's in the input grid. The rest of the grid remains unchanged. The rules for placing '5' seem to depend on whether '8' is present.

**Facts:**


```yaml
Objects:
  - Grid: A 2D array of digits.
    Properties:
      - rows: Number of rows.
      - columns: Number of columns.
  - Cell: An element within the Grid.
    Properties:
      - row_index: The 0-based row number.
      - column_index: The 0-based column number.
      - value: The digit ('2', '5', '7', '8') stored in the cell.

Relationships:
  - Location: Cells have specific (row, column) coordinates.
  - Rightmost '8': The '8' with the largest column index in the entire grid.
  - First Row with '8': The lowest row index containing any '8'.
  - First Row with Rightmost '8': The lowest row index containing an '8' at the column of the Rightmost '8'.
  - Last Row with '2': The highest row index containing a '2'.
  - Column Offset: A target column is often determined by adding 2 to the column index of a key digit ('8' or '2').

Actions:
  - Scan Grid: Iterate through cells to find specific digits ('8', '2').
  - Identify Key Locations: Determine the column of the rightmost '8', the row/column of relevant '2's, and first/last rows containing key digits.
  - Conditional Modification: Change cell values to '5' based on the identified key locations and specific row ranges.
```


**Natural Language Program:**

1.  Initialize the output grid as an identical copy of the input grid.
2.  Scan the entire input grid to determine if the digit '8' is present.
3.  **If the digit '8' is present:**
    a.  Find the maximum column index (`C_max8`) where an '8' appears in any row of the input grid.
    b.  Calculate the target column index for modification: `C_target = C_max8 + 2`.
    c.  Find the minimum row index (`R_first_any8`) containing any '8'.
    d.  Find the minimum row index (`R_first_max8`) containing an '8' specifically in column `C_max8`.
    e.  Determine the starting row index (`R_start`) for modification:
        i.  If `R_first_any8` is equal to `R_first_max8`, set `R_start = 1`.
        ii. Otherwise (if they are different), set `R_start = R_first_max8 - 1`.
    f.  Iterate through all rows from `R_start` down to the last row index of the grid. For each row `R` in this range, change the value of the cell at `(R, C_target)` in the output grid to '5'.
4.  **If the digit '8' is NOT present:**
    a.  Scan the entire input grid to determine if the digit '2' is present.
    b.  **If the digit '2' is present:**
        i.  Find the maximum row index (`R_last2`) where a '2' appears in the input grid.
        ii. Find the column index (`C_2`) of the '2' located in row `R_last2`. (Assuming a consistent column for '2' if multiple '2's exist in that row, or take the first one encountered).
        iii. Calculate the target column index for modification: `C_target = C_2 + 2`.
        iv. Change the value of the single cell at `(R_last2, C_target)` in the output grid to '5'.
5.  **(Implicit) If neither '8' nor '2' is present:** The output grid remains unchanged from the initial copy.
6.  Return the final output grid.
```python
"""
Transforms an input grid of digits based on the presence and location of '8's and '2's.

1.  Initialize the output grid as a copy of the input grid.
2.  Check if the digit '8' exists in the input grid.
3.  If '8' is present:
    a.  Find the maximum column index (C_max8) where an '8' appears.
    b.  Calculate the target column (C_target = C_max8 + 2).
    c.  Find the minimum row index (R_first_any8) containing any '8'.
    d.  Find the minimum row index (R_first_max8) containing an '8' specifically in column C_max8.
    e.  Determine the starting row (R_start):
        i.  If R_first_any8 equals R_first_max8, R_start = 1.
        ii. Otherwise, R_start = R_first_max8 - 1.
    f.  Modify the output grid: For each row R from R_start down to the last row, change the digit at column C_target to '5', if the target cell is within grid bounds.
4.  If '8' is NOT present:
    a.  Check if the digit '2' exists in the input grid.
    b.  If '2' is present:
        i.  Find the maximum row index (R_last2) where a '2' appears.
        ii. Find the column index (C_2) of the '2' in row R_last2 (assuming one '2' per row or taking the first).
        iii. Calculate the target column (C_target = C_2 + 2).
        iv. Modify the output grid: Change the digit at (R_last2, C_target) to '5', if the target cell is within grid bounds.
5.  If neither '8' nor '2' is present, the output grid remains unchanged.
6.  Return the modified output grid.
"""

import copy

def _find_digit_locations(grid: list[list[int]], digit: int) -> list[tuple[int, int]]:
    """Finds all (row, col) coordinates of a given digit in the grid."""
    locations = []
    for r, row in enumerate(grid):
        for c, cell_value in enumerate(row):
            if cell_value == digit:
                locations.append((r, c))
    return locations

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.
    """
    # initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)
    if not input_grid:
        return output_grid
        
    num_rows = len(input_grid)
    if num_rows == 0:
        return output_grid
    num_cols = len(input_grid[0])
    if num_cols == 0:
        return output_grid

    # Find locations of '8'
    locations_8 = _find_digit_locations(input_grid, 8)

    # perform transformations based on '8' or '2'
    if locations_8:
        # Case 1: '8' is present
        
        # Find C_max8: maximum column index of any '8'
        C_max8 = -1
        for r, c in locations_8:
            if c > C_max8:
                C_max8 = c
        
        # Calculate C_target
        C_target = C_max8 + 2

        # Check if C_target is within grid bounds
        if C_target < num_cols:
            # Find R_first_any8: minimum row index of any '8'
            R_first_any8 = num_rows 
            for r, c in locations_8:
                if r < R_first_any8:
                    R_first_any8 = r
            
            # Find R_first_max8: minimum row index of '8' in column C_max8
            R_first_max8 = num_rows
            for r, c in locations_8:
                if c == C_max8 and r < R_first_max8:
                    R_first_max8 = r

            # Determine R_start
            R_start = 0 # Default value, should be updated
            if R_first_any8 == R_first_max8:
                R_start = 1
            else:
                R_start = R_first_max8 - 1 # Ensure this doesn't go negative if R_first_max8 is 0? The rule implies R_start=1 if they match, and R_start=R_first_max8-1 otherwise. If R_first_max8 is 0, and they don't match, R_first_any8 must be > 0, which is impossible. So R_first_max8 > 0 if they don't match. Let's clamp R_start just in case, though the logic suggests it might not be needed.
                R_start = max(0, R_start) # Clamp to 0 if R_first_max8 was 0 (though this case seems impossible based on logic)

            # Modify output grid from R_start downwards in C_target
            for r in range(R_start, num_rows):
                 # Check row bounds just in case, though range handles upper bound
                 if 0 <= r < num_rows:
                     output_grid[r][C_target] = 5
                     
    else:
        # Case 2: '8' is NOT present, check for '2'
        locations_2 = _find_digit_locations(input_grid, 2)
        
        if locations_2:
            # Find R_last2: maximum row index of any '2'
            R_last2 = -1
            for r, c in locations_2:
                if r > R_last2:
                    R_last2 = r
            
            # Find C_2: column index of '2' in row R_last2 
            # (assuming only one '2' in that row, or taking the first one found)
            C_2 = -1
            for r, c in locations_2:
                if r == R_last2:
                    C_2 = c
                    break # Take the first one found in that row
            
            if R_last2 != -1 and C_2 != -1:
                # Calculate C_target
                C_target = C_2 + 2
                
                # Modify the single cell if C_target is within bounds
                if 0 <= R_last2 < num_rows and 0 <= C_target < num_cols:
                    output_grid[R_last2][C_target] = 5

    # If neither '8' nor '2' was found, output_grid remains the initial copy
    return output_grid
```
```python
import copy

"""
Transforms an input grid of digits based on the presence and location of '8's and '2's.

The rules are applied hierarchically:

1.  If the digit '8' is present:
    a.  Find the maximum column index (C_max8) where an '8' appears.
    b.  Calculate the target column (C_target = C_max8 + 2).
    c.  Find the minimum row index (R_first_any8) containing any '8'.
    d.  Find the minimum row index (R_first_max8) containing an '8' specifically in column C_max8.
    e.  If R_first_any8 equals R_first_max8:
        i.  If the digit '2' is also present:
            - Find the maximum row index (R_last2) containing a '2'.
            - Change only the cell at (R_last2, C_target) to '5'.
        ii. If the digit '2' is NOT present:
            - Set the starting row R_start = 1.
            - Change all cells in column C_target from row R_start downwards to '5'.
    f.  If R_first_any8 is NOT equal to R_first_max8:
        i.  Set the starting row R_start = R_first_max8 - 1 (clamped at 0).
        ii. Change all cells in column C_target from row R_start downwards to '5'.
2.  If the digit '8' is NOT present, but the digit '2' is present:
    a.  Find the maximum row index (R_last2) where a '2' appears.
    b.  Find the column index (C_last2) of the first '2' found in row R_last2.
    c.  Calculate the target column (C_target = C_last2 + 2).
    d.  Change only the cell at (R_last2, C_target) to '5'.
3.  If neither '8' nor '2' is present, the grid remains unchanged.

Boundary checks are performed to ensure modifications only happen within the grid dimensions.
"""


def _find_digit_locations(grid: list[list[int]], digit: int) -> list[tuple[int, int]]:
    """Finds all (row, col) coordinates of a given digit in the grid."""
    locations = []
    for r, row in enumerate(grid):
        for c, cell_value in enumerate(row):
            if cell_value == digit:
                locations.append((r, c))
    return locations

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rules to the input grid.
    """
    # Handle empty or invalid input
    if not input_grid or not input_grid[0]:
        return copy.deepcopy(input_grid) # Return copy or empty list? Returning copy.

    num_rows = len(input_grid)
    num_cols = len(input_grid[0])
    
    # Initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)

    # Find locations of '8' and '2'
    locations_8 = _find_digit_locations(input_grid, 8)
    locations_2 = _find_digit_locations(input_grid, 2)
    has_8 = bool(locations_8)
    has_2 = bool(locations_2)

    # Rule 1: '8' is present
    if has_8:
        # Calculate C_max8: maximum column index of any '8'
        C_max8 = -1
        for r, c in locations_8:
            if c > C_max8:
                C_max8 = c
        
        # Calculate C_target from '8'
        C_target = C_max8 + 2

        # Check if C_target is within grid bounds
        if C_target < num_cols:
            # Calculate R_first_any8: minimum row index of any '8'
            R_first_any8 = num_rows # Initialize higher than possible index
            for r, c in locations_8:
                if r < R_first_any8:
                    R_first_any8 = r
            
            # Calculate R_first_max8: minimum row index of '8' in column C_max8
            R_first_max8 = num_rows # Initialize higher than possible index
            for r, c in locations_8:
                if c == C_max8 and r < R_first_max8:
                    R_first_max8 = r

            # Rule 1.e: R_first_any8 == R_first_max8
            if R_first_any8 == R_first_max8:
                # Rule 1.e.i: '2' is also present
                if has_2:
                    # Find R_last2: maximum row index of any '2'
                    R_last2 = -1
                    for r, c in locations_2:
                        if r > R_last2:
                            R_last2 = r
                    # Modify the single cell at (R_last2, C_target) if R_last2 is valid
                    if R_last2 != -1 and 0 <= R_last2 < num_rows:
                         output_grid[R_last2][C_target] = 5
                # Rule 1.e.ii: '2' is NOT present
                else:
                    R_start = 1 # Start modifying from row 1
                    # Modify column C_target from R_start downwards
                    for r in range(R_start, num_rows):
                        output_grid[r][C_target] = 5
            # Rule 1.f: R_first_any8 != R_first_max8
            else:
                # Ensure R_first_max8 is valid before calculating R_start
                if R_first_max8 < num_rows: 
                   R_start = max(0, R_first_max8 - 1) # Start modifying from R_first_max8 - 1 (clamped at 0)
                   # Modify column C_target from R_start downwards
                   for r in range(R_start, num_rows):
                       output_grid[r][C_target] = 5

    # Rule 2: '8' is NOT present, but '2' IS present
    elif has_2:
        # Find R_last2: maximum row index of any '2'
        R_last2 = -1
        for r, c in locations_2:
            if r > R_last2:
                R_last2 = r
        
        # Find C_last2: column index of the first '2' in row R_last2 
        C_last2 = -1
        if R_last2 != -1:
            for r, c in locations_2:
                if r == R_last2:
                    C_last2 = c
                    break # Take the first one found in that row
        
        # Proceed if both R_last2 and C_last2 were found
        if R_last2 != -1 and C_last2 != -1:
            # Calculate C_target from '2'
            C_target = C_last2 + 2
            
            # Modify the single cell if C_target is within bounds
            if 0 <= R_last2 < num_rows and 0 <= C_target < num_cols:
                output_grid[R_last2][C_target] = 5

    # Rule 3: Neither '8' nor '2' is present - No changes needed, output_grid is already a copy

    return output_grid
```
