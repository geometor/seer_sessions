
## train_1

**input:**
```
1 1 1 1 1 1
0 0 0 0 0 0
1 1 1 1 1 1
0 0 0 0 0 0
1 1 1 1 1 1
0 0 0 0 0 0
```


**output:**
```
5 5 5 5 5 5
0 0 0 0 0 0
1 1 1 1 1 1
0 0 0 0 0 0
1 1 1 1 1 1
0 0 0 0 0 0
```


## train_2

**input:**
```
2 0 0 2 0 0
0 2 0 0 2 0
0 0 2 0 0 2
2 0 0 2 0 0
0 2 0 0 2 0
0 0 2 0 0 2
```


**output:**
```
2 0 0 5 0 0
0 2 0 0 5 0
0 0 2 0 0 5
2 0 0 2 0 0
0 2 0 0 2 0
0 0 2 0 0 2
```


## train_3

**input:**
```
0 4 0 4 0 4
4 4 0 4 0 4
0 0 0 4 0 4
4 4 4 4 0 4
0 0 0 0 0 4
4 4 4 4 4 4
```


**output:**
```
0 5 0 4 0 4
5 5 0 4 0 4
0 0 0 4 0 4
4 4 4 4 0 4
0 0 0 0 0 4
4 4 4 4 4 4
```


## train_4

**input:**
```
0 8 8 8 0 0
8 8 0 0 0 8
0 0 0 8 8 8
0 8 8 8 0 0
8 8 0 0 0 8
0 0 0 8 8 8
```


**output:**
```
0 5 5 5 0 0
5 5 0 0 0 8
0 0 0 8 8 8
0 8 8 8 0 0
8 8 0 0 0 8
0 0 0 8 8 8
```

**Perception of Elements:**

The task involves transforming a 6x6 input grid of digits into a 6x6 output grid. The transformation specifically targets a single connected region (block) of identical non-zero digits within the input grid and changes the digits within that selected block to the value 5. The selection of which block to modify follows specific criteria based on block size and position. Connectivity between cells includes horizontal, vertical, and diagonal adjacency. Cells with the value 0 are treated as background and do not form blocks, nor do they participate in the connectivity of non-zero blocks.

**Facts:**


```yaml
objects:
  - name: Grid
    properties:
      - type: 2D array of integers
      - dimensions: 6x6
      - contains: Cells
  - name: Cell
    properties:
      - row_index: integer (0-5)
      - column_index: integer (0-5)
      - value: integer (0-9)
  - name: Block
    properties:
      - type: connected component of Cells
      - connection_rule: adjacent horizontally, vertically, or diagonally
      - cell_value: common non-zero integer for all cells in the block
      - size: count of cells in the block
      - top_left_anchor: coordinates (row, col) of the highest, then leftmost cell in the block

relationships:
  - type: spatial
    description: Cells are positioned within the Grid.
  - type: connectivity
    description: Cells with the same non-zero value can be connected to form a Block.
  - type: selection
    description: Blocks are compared based on size (>1) and the position of their top_left_anchor to select one target Block for modification.

actions:
  - name: identify_blocks
    description: Scan the input Grid to find all distinct Blocks of connected non-zero cells.
    inputs: Grid
    outputs: list of Blocks
  - name: filter_blocks
    description: Remove Blocks with size less than or equal to 1.
    inputs: list of Blocks
    outputs: filtered list of Blocks
  - name: find_top_left_anchors
    description: For each Block, determine its top_left_anchor coordinates.
    inputs: list of Blocks
    outputs: list of Blocks with anchors identified
  - name: select_target_block
    description: >
      From the filtered list of Blocks, select the one whose top_left_anchor
      has the minimum row index, breaking ties by selecting the minimum column index.
    inputs: filtered list of Blocks with anchors
    outputs: target Block (or none if list is empty)
  - name: modify_grid
    description: >
      Create a copy of the input Grid. If a target Block was selected,
      change the value of all cells corresponding to the target Block to 5 in the copied grid.
    inputs: input Grid, target Block (optional)
    outputs: output Grid
```


**Natural Language Program:**

1.  Identify all distinct groups of connected cells in the input grid that share the same non-zero digit value. Connectivity includes cells touching horizontally, vertically, or diagonally.
2.  Discard any identified groups that consist of only one cell.
3.  If no groups remain after discarding single-cell groups, the output grid is identical to the input grid.
4.  If groups remain, determine the top-most, left-most cell coordinate (anchor) for each group.
5.  Select the group whose anchor cell has the smallest row index. If multiple groups share the same smallest row index, select the one among them whose anchor cell has the smallest column index. This is the target group.
6.  Create the output grid by copying the input grid.
7.  Modify the output grid by changing the value of every cell belonging to the target group to 5.
8.  Return the modified grid.
```python
import numpy as np
from collections import deque

"""
1. Identify all distinct groups of connected cells (horizontally, vertically, or diagonally) 
   in the input grid that share the same non-zero digit value.
2. Discard any identified groups that consist of only one cell.
3. If no groups remain after discarding single-cell groups, the output grid is identical to the input grid.
4. If groups remain, determine the top-most, left-most cell coordinate (anchor) for each group.
5. Select the group whose anchor cell has the smallest row index. If multiple groups share the same 
   smallest row index, select the one among them whose anchor cell has the smallest column index. 
   This is the target group.
6. Create the output grid by copying the input grid.
7. Modify the output grid by changing the value of every cell belonging to the target group to 5.
8. Return the modified grid.
"""

def find_blocks(grid):
    """
    Identifies all connected blocks of non-zero cells in the grid.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents a block
        and contains:
        - 'value': The common digit value of the block's cells.
        - 'cells': A list of (row, col) tuples for cells in the block.
        - 'size': The number of cells in the block.
        - 'anchor': A tuple (min_row, min_col) representing the top-left anchor.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    blocks = []
    
    # Define 8 directions for connectivity (horizontal, vertical, diagonal)
    directions = [(-1, -1), (-1, 0), (-1, 1), 
                  (0, -1),           (0, 1), 
                  (1, -1), (1, 0), (1, 1)]

    for r in range(rows):
        for c in range(cols):
            # If cell is non-zero and not visited, start BFS to find a block
            if grid[r, c] != 0 and not visited[r, c]:
                block_value = grid[r, c]
                current_block_cells = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c # Initialize anchor candidates

                while q:
                    row, col = q.popleft()
                    current_block_cells.append((row, col))
                    
                    # Update potential anchor
                    if row < min_r:
                        min_r, min_c = row, col
                    elif row == min_r and col < min_c:
                        min_c = col

                    # Explore neighbors
                    for dr, dc in directions:
                        nr, nc = row + dr, col + dc
                        # Check bounds, matching value, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == block_value and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Store the found block
                blocks.append({
                    'value': block_value,
                    'cells': current_block_cells,
                    'size': len(current_block_cells),
                    'anchor': (min_r, min_c)
                })
                
    return blocks

def transform(input_grid):
    """
    Transforms the input grid based on identifying and modifying a specific block.

    Args:
        input_grid: A list of lists or numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = grid_np.copy()

    # 1. Identify all connected blocks of non-zero cells
    all_blocks = find_blocks(grid_np)

    # 2. Filter out blocks with size 1 or less
    valid_blocks = [block for block in all_blocks if block['size'] > 1]

    # 3. If no valid blocks, return the original grid
    if not valid_blocks:
        return output_grid

    # 4. & 5. Select the target block based on anchor position (min row, then min col)
    # Sort blocks first by anchor row, then by anchor column
    valid_blocks.sort(key=lambda b: (b['anchor'][0], b['anchor'][1]))
    target_block = valid_blocks[0]

    # 6. & 7. Modify the output grid by changing the target block's cells to 5
    for r, c in target_block['cells']:
        output_grid[r, c] = 5

    # 8. Return the modified grid
    return output_grid.tolist() # Return as list of lists if needed, or keep as numpy array

```
