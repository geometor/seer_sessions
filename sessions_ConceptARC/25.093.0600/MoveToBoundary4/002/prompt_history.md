
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 6 0 0
0 0 6 0 0 0 0 6 0 0
0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 6 0
0 0 0 0 0 0 6 0 6 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
6 6 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 6 6 6 0 0 0 0 0 0
6 0 0 6 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 6 6 6 0 0
0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 6 6 6 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The input and output are 2D grids (10x10) containing integers.
    *   The grids primarily consist of the value 0 (background).
    *   The value 6 appears as distinct elements within the grid.
    *   The transformation involves repositioning the '6' values within each row.
    *   The '6' values in the output grid appear shifted towards the left compared to the input grid.
    *   The transformation seems to operate independently on each row.
    *   Contiguous horizontal sequences (blocks) of '6's in the input seem to be treated as units.
    *   These blocks are moved to the leftmost available positions in the output row, maintaining their original length and relative order.

*   **Facts:**
    
```yaml
    task_elements:
      - element: grid
        properties:
          - type: 2D array
          - dimensions: 10x10
          - cell_values: [0, 6]
          - background_value: 0
          - foreground_value: 6
      - element: row
        properties:
          - structure: 1D array (slice of the grid)
          - processing_scope: Transformation is applied independently to each row.
      - element: block
        properties:
          - type: contiguous horizontal sequence of foreground_values (6) within a row
          - preservation: length and value (6) are preserved during transformation
          - relative_order: the left-to-right order of blocks within a row is preserved
      - action: shift_left
        properties:
          - target: blocks
          - direction: horizontal, towards column 0
          - constraint: blocks are placed starting from the leftmost available column (column 0), packed together without overlap, maintaining relative order.
      - relationship: input_output
        properties:
          - rule: For each row, identify all contiguous blocks of '6'. Create a new row initialized with '0's. Place the identified blocks into the new row starting from column 0, preserving their relative order and packing them consecutively.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid, filled with the background value (0).
    2.  Iterate through each row of the input grid independently.
    3.  For the current row, identify all contiguous horizontal blocks of the non-zero value (6). Store these blocks (including their length) in the order they appear from left to right.
    4.  Initialize a variable `current_output_column` to 0.
    5.  Iterate through the identified blocks for the current row in their stored order.
    6.  For each block, place its sequence of '6's into the corresponding output row, starting at the `current_output_column`.
    7.  Update the `current_output_column` by adding the length of the block just placed.
    8.  After processing all blocks for the row, the remaining cells in the output row (from `current_output_column` to the end) remain 0.
    9.  Repeat steps 3-8 for all rows.
    10. The final modified grid is the task output.
```python
import math
import copy

"""
For each row in the input grid independently:
1. Identify all contiguous horizontal blocks of the value 6.
2. Create a new output row initialized with the background value 0.
3. Place the identified blocks into the new output row, starting from the leftmost column (column 0).
4. Preserve the relative order of the blocks as they appeared in the input row.
5. Pack the blocks consecutively without any gaps between them in the output row.
6. The final output grid is composed of these newly generated rows.
"""

def find_blocks_in_row(row, target_value=6):
    """
    Identifies contiguous blocks of a target value in a row.

    Args:
        row (list): A list representing a row of the grid.
        target_value (int): The value to search for blocks of.

    Returns:
        list: A list containing the lengths of the identified contiguous blocks,
              in the order they appear from left to right.
    """
    blocks = []
    in_block = False
    block_start = -1
    for i, cell in enumerate(row):
        # Entering a block
        if cell == target_value and not in_block:
            in_block = True
            block_start = i
        # Exiting a block
        elif cell != target_value and in_block:
            in_block = False
            block_length = i - block_start
            blocks.append(block_length)
            block_start = -1 # Reset start index
    # Handle case where a block extends to the end of the row
    if in_block:
        block_length = len(row) - block_start
        blocks.append(block_length)
    return blocks

def transform(input_grid):
    """
    Transforms the input grid by shifting all contiguous blocks of '6'
    in each row to the left, preserving their relative order and lengths.

    Args:
        input_grid (list of list of int): The input 2D grid.

    Returns:
        list of list of int: The transformed 2D grid.
    """
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize output_grid with background value (0)
    output_grid = [[0 for _ in range(width)] for _ in range(height)]

    # Process each row independently
    for r in range(height):
        input_row = input_grid[r]
        
        # Find all contiguous blocks of '6' in the current row
        block_lengths = find_blocks_in_row(input_row, target_value=6)

        # Place the blocks into the output row, shifted left
        current_output_col = 0
        for length in block_lengths:
            # Fill the block with '6's in the output row
            for c in range(length):
                # Check bounds just in case, though logic should prevent overflow
                if current_output_col + c < width: 
                    output_grid[r][current_output_col + c] = 6
            # Update the starting column for the next block
            current_output_col += length

    return output_grid
```
