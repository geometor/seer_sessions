
## train_1

**input:**
```
0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 4 4 4
0 2 2 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 1 1 0 0 0
0 0 0 0 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 2 2 2 1 1 1 4 4 4
0 2 2 2 1 1 1 4 4 4
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 2 2 0 0 0 0 0 0 0
0 2 2 0 0 0 0 1 1 0
0 0 0 0 4 4 0 1 1 0
0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 0 4 4 0 1 1 0
0 2 2 0 4 4 0 1 1 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0
0 1 0 2 0 0 0 0 0 0
0 1 0 0 0 0 4 0 0 0
0 0 0 0 0 0 4 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 2 0 0 4 0 0 0
0 1 0 2 0 0 4 0 0 0
0 0 0 0 0 0 0 0 0 0
```

## Perception of Task Elements

1.  **Input/Output Format:** Both input and output are 2D grids of single digits. The digit '0' represents the background. Non-zero digits represent distinct 'colors'.
2.  **Core Objects:** The key elements are contiguous rectangular blocks of identical non-zero digits ("color blocks"). In all examples, these blocks have a height of 2 rows. Their widths vary.
3.  **Transformation:** The task involves identifying these color blocks in the input, removing them from their original positions, and placing them adjacent to each other horizontally in a specific location in the output grid.
4.  **Horizontal Arrangement:** The blocks in the output are arranged horizontally without gaps. Their relative order corresponds to their left-to-right order in the input grid (based on the minimum column index of each block).
5.  **Horizontal Placement:** The combined horizontal strip of blocks in the output starts at the column corresponding to the minimum column index occupied by any non-zero cell in the input grid.
6.  **Vertical Placement:** The blocks are placed in two adjacent rows in the output grid. The determination of these two rows appears to depend on the input grid's height (`H`) and the vertical positions of the input blocks.
    *   Find the starting row index (top row) for each distinct color block in the input.
    *   If the grid height `H` is 10 or greater, the target top row (`r_target`) for the output strip seems to be `floor(H/2)`.
    *   If the grid height `H` is less than 10, find the median of the starting row indices of all blocks. The block corresponding to this median starting row index determines the target top row (`r_target`) for the output strip; `r_target` is the starting row index of this median block.
    *   The output strip occupies rows `r_target` and `r_target + 1`.
7.  **Output Grid:** The output grid has the same dimensions as the input grid. All locations not occupied by the rearranged blocks are filled with '0'.

## Documented Facts


```yaml
task_type: grid_transformation
input_features:
  grid_dimensions: [height, width]
  cell_values: digits 0-9
  background_value: 0
  objects:
    - type: contiguous_block
      properties:
        color: non-zero digit (constant within block)
        shape: rectangular (observed height is always 2)
        position: [top_row, left_col, height, width]
relationships:
  - type: spatial
    between: blocks
    attributes: [relative_position_horizontal, relative_position_vertical]
output_features:
  grid_dimensions: same as input
  cell_values: digits 0-9
  background_value: 0
  objects:
    - type: composite_block
      properties:
        constituent_blocks: ordered sequence of input blocks
        arrangement: horizontal adjacency
        position: [target_top_row, target_left_col]
        height: 2 (constant)
        width: sum of widths of constituent blocks
actions:
  - identify_blocks: find all distinct contiguous non-zero blocks in the input.
  - calculate_properties: determine color, position (top_row, left_col), width for each block.
  - determine_target_row:
      condition: grid_height >= 10
      action: target_top_row = floor(grid_height / 2)
      condition: grid_height < 10
      action:
        - find median starting row among all blocks
        - identify block corresponding to median starting row
        - target_top_row = starting row of the median block
  - determine_target_col: target_left_col = minimum left_col among all input blocks.
  - sort_blocks: order input blocks based on their left_col (ascending).
  - create_output_grid: initialize grid of same dimensions as input with background value.
  - place_blocks: copy sorted blocks sequentially into the output grid at the target row/column, updating the horizontal placement position after each block.
```


## Natural Language Program

1.  **Initialize:** Create an empty output grid with the same dimensions as the input grid, filled with the background color '0'.
2.  **Identify Blocks:** Scan the input grid to find all separate, contiguous rectangular blocks of identical non-zero digits. For each block, record its color (digit), its top row index (`r`), its leftmost column index (`c`), and its width (`w`). (Note: observed height `h` is always 2).
3.  **Determine Horizontal Order and Start:** Find the minimum column index (`c_min`) among all identified blocks. Sort the identified blocks based on their leftmost column index (`c`) in ascending order.
4.  **Determine Vertical Position:**
    a.  Let `H` be the height of the input grid.
    b.  Get the list of top
```python
import numpy as np
import math
import statistics
from collections import defaultdict

"""
Identifies contiguous rectangular blocks of height 2 with the same non-zero color in the input grid.
Determines the horizontal placement (minimum column index of any block) and vertical placement (based on grid height and median starting row of blocks) for the output.
Rearranges the identified blocks horizontally adjacent to each other in the output grid at the determined location, sorted by their original horizontal position (leftmost column).
The output grid has the same dimensions as the input grid, with all other cells set to 0.

Detailed Vertical Placement Logic:
1. Find the starting row index (top row) for each distinct color block (height 2) in the input.
2. Let H be the grid height.
3. If H >= 10, the target top row (r_target) for the output strip is floor(H/2).
4. If H < 10:
    a. Get the list of starting row indices of all blocks.
    b. Find the median value of these starting row indices. Use median_low (the lower of the two middle values if the count is even) to ensure the median corresponds to an actual starting row.
    c. The target top row (r_target) is this median starting row value.
5. The output strip occupies rows r_target and r_target + 1.
"""

def find_blocks(grid: np.ndarray) -> list[dict]:
    """
    Finds all contiguous rectangular blocks of height 2 with the same non-zero color.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        with keys: 'color', 'r', 'c', 'w', 'h'.
    """
    H, W = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    for r in range(H - 1): # Iterate rows up to H-2 (inclusive) for blocks of height 2
        for c in range(W): # Iterate columns
            # Check for the start of a potential block: non-zero, not visited, and cell below has same color
            if grid[r, c] > 0 and not visited[r, c] and grid[r + 1, c] == grid[r, c]:
                color = grid[r, c]
                
                # Found the top-left corner (r, c) of a block. Determine its width.
                width = 0
                for c_offset in range(W - c):
                    current_c = c + c_offset
                    # Check if the block continues horizontally in both rows
                    if (grid[r, current_c] == color and not visited[r, current_c] and
                        grid[r + 1, current_c] == color and not visited[r+1, current_c]):
                        width += 1
                        # Mark cells as visited
                        visited[r, current_c] = True
                        visited[r + 1, current_c] = True
                    else:
                        break # End of the block horizontally

                # If a valid block was found (width > 0), add it to the list
                if width > 0:
                    blocks.append({'color': color, 'r': r, 'c': c, 'w': width, 'h': 2})
            
            # Mark the cell as visited even if it wasn't the start of a 2-high block
            # This prevents recounting or partial block detection later
            # Note: This might mark cells that are part of a block found starting from a previous column,
            # but the visited check at the start of the loop handles this correctly.
            # We only need to ensure single non-zero cells not part of any block are eventually marked.
            elif grid[r,c] > 0 and not visited[r,c]:
                 visited[r, c] = True


    # Ensure any remaining unvisited non-zero cells in the last row are marked.
    # This is mostly for completeness, as valid blocks are height 2 and detected above.
    for c in range(W):
        if grid[H - 1, c] > 0 and not visited[H - 1, c]:
             visited[H - 1, c] = True

    return blocks

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding 2-row high blocks of color,
    and rearranging them horizontally in the middle of the grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Initialize output grid with zeros (background color)
    output_grid = np.zeros_like(input_np)

    # --- Identify Blocks ---
    # Find all the 2-row high blocks of color in the input grid
    blocks = find_blocks(input_np)

    # If no blocks are found, return the empty output grid
    if not blocks:
        return output_grid.tolist()

    # --- Determine Horizontal Order and Start Position ---
    # Sort the blocks based on their starting column index (left-to-right)
    blocks.sort(key=lambda b: b['c'])
    # The target starting column is the minimum column index of the first block
    c_min = blocks[0]['c']

    # --- Determine Vertical Position ---
    # Get the starting row indices of all found blocks
    start_rows = [b['r'] for b in blocks]

    # Determine the target top row (r_target) based on grid height
    if H >= 10:
        # For taller grids, place the combined block starting at the middle row (floor division)
        r_target = H // 2
    else:
        # For shorter grids, find the median starting row value among the blocks
        # Use median_low to handle cases with an even number of blocks correctly,
        # ensuring the result is one of the actual starting rows.
        sorted_start_rows = sorted(start_rows)
        median_row_value = statistics.median_low(sorted_start_rows)
        r_target = median_row_value

    # --- Place Blocks in Output Grid ---
    # Initialize the current column position for placing blocks
    current_c = c_min
    # Iterate through the sorted blocks
    for block in blocks:
        color = block['color']
        w = block['w']
        # Define the horizontal slice for the current block
        col_slice = slice(current_c, current_c + w)
        
        # Copy the block's color into the output grid at the target rows
        # The block height is always 2
        output_grid[r_target, col_slice] = color
        output_grid[r_target + 1, col_slice] = color
        
        # Update the current column position for the next block
        current_c += w

    # Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()
```
```python
import numpy as np
import statistics
import math

"""
Identifies contiguous rectangular blocks of height 2 with the same non-zero color in the input grid.
Determines a target top row (r_target) for placement in the output grid based on the input grid's height (H) and the median starting row of the identified blocks:
- If H >= 10, r_target = floor(H / 2).
- If H < 10, r_target = median_low of the starting rows of all blocks.
Rearranges the identified blocks into the output grid. Each block is placed in rows r_target and r_target + 1, maintaining its original horizontal column position (leftmost column index 'c' and width 'w').
The output grid has the same dimensions as the input grid, with all cells not covered by the placed blocks set to 0.
"""

def find_blocks_height2(grid: np.ndarray) -> list[dict]:
    """
    Finds all contiguous rectangular blocks of exactly height 2 with the same non-zero color.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        with keys: 'color', 'r' (top row), 'c' (left col), 'w' (width).
    """
    H, W = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []

    # Iterate rows up to H-2 (inclusive) to find blocks starting at row r and ending at r+1
    for r in range(H - 1):
        for c in range(W):
            # Check for the start of a potential block:
            # - Non-zero color
            # - Not yet visited
            # - Cell below has the same non-zero color
            if grid[r, c] > 0 and not visited[r, c] and grid[r + 1, c] == grid[r, c] and not visited[r+1,c]:
                color = grid[r, c]
                
                # Found a potential top-left corner (r, c) of a block. Determine its width.
                width = 0
                # Scan columns to the right starting from c
                for c_offset in range(W - c):
                    current_c = c + c_offset
                    # Check if the block continues horizontally in both rows r and r+1
                    if (grid[r, current_c] == color and not visited[r, current_c] and
                        grid[r + 1, current_c] == color and not visited[r+1, current_c]):
                        # Increment width and mark cells as visited
                        width += 1
                        visited[r, current_c] = True
                        visited[r + 1, current_c] = True
                    else:
                        # Stop scanning horizontally if the block ends or changes color
                        break 

                # If a valid block (width > 0) was found, add its properties to the list
                if width > 0:
                    blocks.append({
                        'color': int(color), # Store as standard int
                        'r': int(r),       # Store as standard int
                        'c': int(c),       # Store as standard int
                        'w': int(width)    # Store as standard int
                        # Height is implicitly 2
                    })
            
            # Important: Mark any unvisited non-zero cell as visited *after* checking for block start.
            # This prevents single non-zero cells or parts of already found blocks from being reconsidered.
            # It also handles cells that might be part of a block but weren't the top-left starting point
            # found in this specific (r, c) iteration.
            if grid[r, c] > 0 and not visited[r, c]:
                visited[r, c] = True
            if grid[r + 1, c] > 0 and not visited[r+1, c]: # Also mark the cell below if non-zero and unvisited
                 visited[r+1, c] = True


    return blocks


def determine_target_row(grid_height: int, block_start_rows: list[int]) -> int:
    """
    Determines the target top row for placing blocks in the output grid.

    Args:
        grid_height: The height (H) of the input grid.
        block_start_rows: A list of the starting row indices ('r') of all identified blocks.

    Returns:
        The calculated target top row index (r_target).
    """
    if grid_height >= 10:
        # For taller grids, target row is the middle row (floor division)
        r_target = grid_height // 2
    else:
        # For shorter grids, target row is the median_low of the block start rows
        # Ensure the list is sorted for median calculation
        sorted_start_rows = sorted(block_start_rows)
        r_target = statistics.median_low(sorted_start_rows)
        
    return r_target

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the specified rules.
    """
    # Convert input list of lists to a numpy array for efficient processing
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape

    # Initialize output grid with the background color (0)
    output_grid = np.zeros_like(input_np)

    # --- Step 1: Identify all 2-row high blocks ---
    blocks = find_blocks_height2(input_np)

    # If no blocks are found, return the empty (all zeros) output grid
    if not blocks:
        return output_grid.tolist()

    # --- Step 2: Determine the target row for placement ---
    # Collect the starting row ('r') of each identified block
    start_rows = [b['r'] for b in blocks]
    # Calculate the target top row based on grid height and median start row
    r_target = determine_target_row(H, start_rows)
    
    # Ensure target rows are within grid bounds (should be, but good practice)
    if r_target + 1 >= H: 
        # This case indicates an issue, maybe only 1 row grid or unexpected median.
        # Handle appropriately, e.g., adjust or log error. For now, cap it.
        print(f"Warning: Target rows {r_target}, {r_target+1} may exceed grid height {H}. Adjusting.")
        # If r_target is the last row, we can only write to r_target.
        # But the rule implies height 2, so this shouldn't happen with valid input/logic.
        # Let's proceed assuming r_target and r_target+1 are valid.
        pass # Or adjust r_target if needed, e.g. r_target = max(0, H-2) if len(blocks)>0

    # --- Step 3: Place blocks individually in the output grid ---
    # Iterate through the list of identified blocks (order doesn't matter for placement)
    for block in blocks:
        color = block['color']
        c = block['c']  # Original starting column
        w = block['w']  # Original width
        
        # Define the column slice for the block's original horizontal position
        # Ensure the slice does not exceed the grid width
        col_start = c
        col_end = min(c + w, W) # Prevent writing past the grid width
        col_slice = slice(col_start, col_end)
        
        # Copy the block's color into the output grid at the target rows (r_target, r_target+1)
        # and its original columns (col_slice)
        output_grid[r_target, col_slice] = color
        # Check if r_target+1 is still within bounds before writing
        if r_target + 1 < H:
            output_grid[r_target + 1, col_slice] = color
        # Else: block is height 2 but target is last row - only top half gets written if bounds strictly enforced.

    # Convert the final numpy array back to a list of lists before returning
    return output_grid.tolist()
```
