
## train_1

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 6 6 6 0
6 1 1 1 6
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
1 0 0 0 1
0 6 6 6 0
6 1 1 1 6
```


## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 8 0 0
8 8 3 8 8
```


**output:**
```
0 0 0 0 0
3 0 0 0 3
0 3 0 3 0
0 0 8 0 0
8 8 3 8 8
```


## train_3

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
4 0 0 0 0 0 4
0 4 0 0 0 4 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```


## train_4

**input:**
```
0 0 0
0 2 0
2 4 2
```


**output:**
```
4 0 4
0 2 0
2 4 2
```

**Perception of Elements:**

1.  **Input/Output Structure:** Both input and output are 2D grids of integers, representing colors (0 typically being the background). The grid dimensions vary between examples.
2.  **Core Transformation:** The output grid is largely identical to the input grid, with some specific cells changing color from 0 to a non-zero color. The transformation adds new colored points based on a pattern derived from the input.
3.  **Key Feature - Bottom Row:** The bottom row of the input grid seems critical. It contains patterns of non-zero colors that determine the transformation.
4.  **Source Identification:** Within the bottom row, there appears to be a "source" element. This source is characterized by its color and its central position within a contiguous block of non-zero colors in that row.
    *   In `train_1`, the source is the central '1' from the `1 1 1` block.
    *   In `train_2`, the source is the central '3' from the `3` block.
    *   In `train_3`, the source is the central '4' from the `4 4 4` block.
    *   In `train_4`, the source is the central '4' from the `4` block.
5.  **Projection Pattern:** New points are added in the rows *above* the source cell. These points use the *source color*. They form a symmetrical pattern expanding upwards and outwards from the source cell's column.
6.  **Projection Rule Dependency:** The exact pattern (the "slope" of the diagonal projection) depends on the *length* of the contiguous block containing the source color in the bottom row.
    *   If the block length is 1 (e.g., `train_2`, `train_4`), the projection seems to follow one rule (`abs(horizontal_offset) = vertical_offset - 1`).
    *   If the block length is greater than 1 (e.g., `train_1`, `train_3`, which have length 3), the projection follows another rule (`abs(horizontal_offset) = vertical_offset`).
7.  **No Overwriting:** The added points only change cells that were originally 0 (background color). Existing non-zero cells from the input are preserved.

**YAML Facts:**


```yaml
task_description: Projecting a pattern upwards from a source element in the bottom row.

elements:
  - object: grid
    properties:
      - type: 2D array of integers (colors)
      - size: variable rows and columns
  - object: cell
    properties:
      - coordinates: (row, column)
      - color: integer (0 is background)
  - object: bottom_row
    properties:
      - location: last row of the grid
      - contains: patterns of non-zero colors
  - object: source_block
    properties:
      - location: within the bottom row
      - type: contiguous horizontal sequence of non-zero cells
      - centrality: typically the single centrally located block
      - length: number of cells in the block
  - object: source_cell
    properties:
      - location: central cell within the source_block
      - coordinates: (R, C) where R is the last row index
      - color: X (the color value of the cell)
  - object: projected_points
    properties:
      - location: cells above the source_cell (row < R)
      - color: same as source_color X
      - condition: only added if the target cell is initially background color (0)
      - pattern: symmetrical around the source_cell's column C

relationships:
  - type: dependency
    from: projected_points.location
    to: source_cell.location
    details: Points (r, c) are generated based on (R, C).
  - type: dependency
    from: projected_points.color
    to: source_cell.color
    details: Projected points take the color X.
  - type: dependency
    from: projected_points.pattern
    to: source_block.length (L)
    details: |
      The relationship between vertical distance (k = R - r) and horizontal distance (d = abs(c - C)) depends on L.
      If L == 1, then d = k - 1.
      If L > 1, then d = k.
  - type: constraint
    on: projected_points
    details: Projection starts from k=2 (i.e., r = R - 2), not the row immediately above (k=1). Projection occurs only within grid boundaries.

actions:
  - action: identify_source
    steps:
      - locate bottom row R
      - find contiguous non-zero blocks in row R
      - select the central block
      - find the central cell (R, C) and its color X within that block
      - determine block length L
  - action: project_pattern
    steps:
      - copy input grid to output grid
      - determine projection rule based on L (d = k-1 or d = k)
      - iterate k from 2 up to R
      - calculate target row r = R - k
      - calculate target columns c1 = C - d, c2 = C + d
      - for each target (r, c):
        - check if (r, c) is within grid bounds
        - check if output[r][c] is 0
        - if both true, set output[r][c] = X
```


**Natural Language Program:**

1.  Initialize the `output_grid` as a copy of the `input_grid`.
2.  Identify the index of the bottom row, `R`.
3.  Analyze the bottom row (`input_grid[R]`) to find the centrally located contiguous block of non-zero colored cells.
4.  Determine the column index `C` and color `X` of the central cell within this central block.
5.  Measure the length `L` of
```python
import numpy as np
import copy

"""
Identifies a 'source' element within a contiguous block of non-zero colors in the bottom row of the input grid. 
The source element is the central cell of the block closest to the horizontal center of the grid.
A pattern is then projected upwards from this source cell. The pattern consists of points having the same color as the source cell.
These projected points form symmetrical diagonal lines originating conceptually from the row below the source cell.
The slope of these diagonal lines depends on the length (L) of the source block identified in the bottom row:
- If L == 1, the horizontal distance (d) from the source column equals the vertical distance (k) minus 1 (d = k - 1).
- If L > 1, the horizontal distance (d) equals the vertical distance (k) (d = k).
The projection starts from k=2 (two rows above the source row).
Projected points are only placed if the target cell in the output grid is currently background color (0).
The rest of the input grid remains unchanged in the output.
"""

def find_source_block(bottom_row: list[int], grid_width: int) -> tuple[int | None, int | None, int | None]:
    """
    Finds the centrally located contiguous block of non-zero cells in the bottom row.

    Args:
        bottom_row: A list of integers representing the bottom row of the grid.
        grid_width: The width of the grid.

    Returns:
        A tuple (length, center_col_index, center_color) for the identified source block,
        or (None, None, None) if no suitable block is found.
    """
    width = len(bottom_row)
    blocks = []
    in_block = False
    start_col = -1

    # Iterate through the row to find all contiguous non-zero blocks
    for c in range(width):
        if bottom_row[c] != 0 and not in_block:
            # Start of a new block
            in_block = True
            start_col = c
        elif (bottom_row[c] == 0 or c == width - 1) and in_block:
             # End of the current block
            in_block = False
            end_col = c - 1 if bottom_row[c] == 0 else c # Adjust end if ended by zero or grid edge
            length = end_col - start_col + 1
            # Calculate the index of the central cell within the block
            center_col_idx = start_col + (length - 1) // 2
            center_color = bottom_row[center_col_idx]
             # Calculate the geometric center coordinate of the block
            block_geometric_center = (start_col + end_col) / 2.0
            
            blocks.append({
                'start': start_col,
                'end': end_col,
                'length': length,
                'center_col_index': center_col_idx,
                'center_color': center_color,
                'geometric_center': block_geometric_center
            })
            # Reset start_col for the next potential block
            start_col = -1

    if not blocks:
        return None, None, None # No non-zero blocks found

    # Calculate the horizontal center coordinate of the entire grid
    grid_center_coord = (grid_width - 1) / 2.0

    # Find the block whose geometric center is closest to the grid's center
    # If there's a tie in distance, min() usually picks the first one encountered,
    # which corresponds to the leftmost block in case of a tie.
    closest_block = min(blocks, key=lambda b: abs(b['geometric_center'] - grid_center_coord))

    return closest_block['length'], closest_block['center_col_index'], closest_block['center_color']


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Check if the grid is too small to have a bottom row or rows above it
    if height < 2:
        return output_np.tolist() # Return copy of input if grid is too small

    # Identify the bottom row
    bottom_row_index = height - 1
    bottom_row = input_np[bottom_row_index, :].tolist()

    # Find the source block properties
    source_length, source_col, source_color = find_source_block(bottom_row, width)

    # If no source block is found, return the initial copy
    if source_length is None:
        return output_np.tolist()

    # Perform the projection
    # Iterate through vertical distances (k) upwards from the source row
    # k=1 is the row directly above source, k=2 is two rows above, etc.
    # Projection starts from k=2 as per analysis.
    for k in range(2, height): # Iterate up to k = height-1 (top row)
        target_row = bottom_row_index - k
        
        # Ensure target_row is valid (it will be >= 0 based on loop range)
        #if target_row < 0: # This check is implicitly handled by range limit
        #    continue 

        # Determine horizontal distance (d) based on source block length (L)
        if source_length == 1:
            d = k - 1
        else: # source_length > 1
            d = k

        # Calculate target columns
        target_col_left = source_col - d
        target_col_right = source_col + d

        # Project point to the left
        if 0 <= target_col_left < width: # Check column bounds
            # Only color if the cell is currently background (0)
            if output_np[target_row, target_col_left] == 0:
                output_np[target_row, target_col_left] = source_color

        # Project point to the right (avoid double-painting if d=0)
        if d != 0 and 0 <= target_col_right < width: # Check column bounds
             # Only color if the cell is currently background (0)
            if output_np[target_row, target_col_right] == 0:
                output_np[target_row, target_col_right] = source_color

    # Convert back to list of lists and return
    return output_np.tolist()
```
```python
import numpy as np
import copy

"""
Projects a symmetrical pattern upwards from a source element identified in the 
bottom row, coloring background cells (0). The source element is the central 
cell of the contiguous horizontal block of non-zero cells in the bottom row 
that is closest to the grid's horizontal center. The projection pattern's shape 
depends on the length (L) of this source block: if L=1, the horizontal distance 
(d) from the source column equals the vertical distance (k) minus 1 (d = k - 1); 
if L>1, d equals k (d = k). The projection starts two rows above the source row 
(k=2) and continues upwards. Only background cells (color 0) are modified.
"""


def find_source_block(bottom_row: list[int], grid_width: int) -> tuple[int | None, int | None, int | None]:
    """
    Finds the centrally located contiguous block of non-zero cells in the bottom row.

    Args:
        bottom_row: A list of integers representing the bottom row of the grid.
        grid_width: The width of the grid.

    Returns:
        A tuple (length, center_col_index, center_color) for the identified source block,
        or (None, None, None) if no suitable block is found.
    """
    width = len(bottom_row)
    blocks = []
    in_block = False
    start_col = -1

    # Iterate through the row to find all contiguous non-zero blocks
    for c in range(width):
        is_non_zero = bottom_row[c] != 0
        is_last_col = c == width - 1

        if is_non_zero and not in_block:
            # Start of a new block
            in_block = True
            start_col = c
        
        # End condition: (current cell is zero OR it's the last column) AND we are inside a block
        if (not is_non_zero or is_last_col) and in_block:
            in_block = False
            # Determine the correct end column index
            end_col = c - 1 if not is_non_zero else c 
            length = end_col - start_col + 1
            
            # Calculate the index of the central cell within the block
            center_col_idx = start_col + (length - 1) // 2
            center_color = bottom_row[center_col_idx]
            
            # Calculate the geometric center coordinate of the block for comparison
            block_geometric_center = (start_col + end_col) / 2.0
            
            blocks.append({
                'start': start_col,
                'end': end_col,
                'length': length,
                'center_col_index': center_col_idx,
                'center_color': center_color,
                'geometric_center': block_geometric_center
            })
            # Reset start_col shouldn't be needed here as loop continues

    if not blocks:
        return None, None, None # No non-zero blocks found

    # Calculate the horizontal center coordinate of the entire grid
    grid_center_coord = (grid_width - 1) / 2.0

    # Find the block whose geometric center is closest to the grid's center
    # min() with a key function finds the minimum based on the key's return value
    closest_block = min(blocks, key=lambda b: abs(b['geometric_center'] - grid_center_coord))

    return closest_block['length'], closest_block['center_col_index'], closest_block['center_color']


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to a numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Handle edge case: grid height must be at least 2 for a bottom row and a row above
    if height < 2:
        return output_np.tolist() # Return copy of input if grid is too small

    # Identify the bottom row and its index
    bottom_row_index = height - 1
    bottom_row_list = input_np[bottom_row_index, :].tolist()

    # Find the source block properties (length L, center column C, color X)
    source_length, source_col, source_color = find_source_block(bottom_row_list, width)

    # If no source block is found, return the initial copy
    if source_length is None:
        return output_np.tolist()

    # Determine the projection rule based on source block length L
    # d = horizontal distance, k = vertical distance
    if source_length == 1:
        # Rule: d = k - 1
        get_d = lambda k: k - 1
    else: # source_length > 1
        # Rule: d = k
        get_d = lambda k: k
        
    # Perform the projection upwards from the source row
    # Iterate through vertical distances (k) starting from k=2 (two rows above source)
    # up to k=height-1 (which corresponds to the top row, index 0)
    # Note: k = bottom_row_index - target_row
    for k in range(2, height): 
        # Calculate target row index
        target_row = bottom_row_index - k
        
        # Ensure target_row is valid (this check is technically redundant due to loop range)
        # if target_row < 0:
        #     continue 

        # Calculate horizontal distance 'd' based on 'k' and the rule
        d = get_d(k)
        
        # If d becomes negative (only possible if k=0 or k=1 for d=k-1, but k starts at 2), skip
        if d < 0:
            continue

        # Calculate target column indices
        target_col_left = source_col - d
        target_col_right = source_col + d

        # Project point to the left, checking bounds and background color
        if 0 <= target_col_left < width: # Check column bounds
            # Check if the target cell is currently background color (0)
            if output_np[target_row, target_col_left] == 0:
                output_np[target_row, target_col_left] = source_color

        # Project point to the right, checking bounds and background color
        # Avoid double-painting if d=0 (source_col == target_col_left == target_col_right)
        if d != 0 and 0 <= target_col_right < width: # Check column bounds
             # Check if the target cell is currently background color (0)
            if output_np[target_row, target_col_right] == 0:
                output_np[target_row, target_col_right] = source_color

    # Convert the final numpy array back to a list of lists
    return output_np.tolist()
```
