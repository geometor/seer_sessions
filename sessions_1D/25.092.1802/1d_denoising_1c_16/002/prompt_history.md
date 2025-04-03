
## train_1

**input:**
```
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 7 0 0 0 7 0 0 0 7 0 0 0 0 0 0
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 8 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 8 0 0 0 8 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 8 0 0 0 8 0 0 0 0 8 0 0
```


**output:**
```
0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output grids have the same dimensions in each example (5x7).
    *   The grids primarily consist of white pixels (0) and one other dominant color (orange - 7, or azure - 8).
    *   A key feature in the input grids is the presence of one or more rows completely filled with a single non-white color.
    *   In the output grids, only these solid-colored rows (or the largest contiguous block of them) are preserved from the input. All other rows are replaced entirely with white pixels (0).
    *   The transformation identifies the largest contiguous horizontal block of rows where each row consists of only one non-white color, preserves this block, and sets all other pixels in the grid to white.

*   **Facts:**
    
```yaml
    task_description: Identify the largest contiguous block of solid, non-white rows and preserve only that block, turning everything else white.
    grid_properties:
      - dimensions_match: Input and output grids have the same height and width.
      - colors_present_input: White (0) and one other non-white color (e.g., 7, 8).
      - colors_present_output: White (0) and the single non-white color identified in the input's solid rows.
    objects:
      - type: solid_row
        description: A row consisting entirely of a single non-white color.
        example_colors: [7, 8]
      - type: solid_block
        description: A contiguous vertical group of one or more solid_rows of the same non-white color.
        relation: This is the primary object to be preserved.
      - type: background
        description: Pixels not part of the identified solid_block.
        color_in_output: white (0)
    actions:
      - identify: Scan each row of the input grid.
      - filter: Keep rows that are composed of a single, non-white color.
      - group: Find contiguous vertical blocks of these solid rows sharing the same color.
      - select: Choose the largest contiguous block (by height/number of rows). If there's a tie, the specific examples don't show how to resolve it, but typically the first or last encountered might be chosen (the examples only show one such block).
      - construct_output: Create a new grid of the same dimensions as the input, filled with white (0).
      - copy: Transfer the selected largest solid block from the input grid to the corresponding position in the output grid.
    relationships:
      - contiguity: Rows must be vertically adjacent to form a block.
      - uniformity: Rows within a block must be solid and of the same non-white color.
      - preservation: Only the largest solid block is kept; everything else is discarded/replaced.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid with the same dimensions as the input grid, filling it entirely with white pixels (color 0).
    2.  Iterate through the rows of the input grid to identify all rows that consist of a single, non-white color. Record the row index and the color for each such solid row.
    3.  Group the identified solid rows based on vertical contiguity and having the same color. This identifies blocks of solid-colored rows.
    4.  Determine the largest block (the one with the most rows). If there is only one block, select that one. (The provided examples only show cases with one identifiable block).
    5.  If a largest solid block is found, copy the pixels corresponding to this block from the input grid to the same row and column positions in the output grid.
    6.  The output grid, now containing the copied solid block (if found) and white pixels elsewhere, is the result.
```python
import numpy as np

"""
Identify the largest contiguous block of solid, non-white rows in the input grid. 
Preserve only this block in the output grid, setting all other pixels to white (0).
A solid row consists entirely of a single non-white color.
A block is a vertically contiguous sequence of solid rows of the same color.
The largest block is the one with the greatest number of rows (height).
"""

def transform(input_grid):
    """
    Transforms the input grid by identifying the largest block of solid, 
    non-white rows and preserving only that block.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed grid.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    
    # Initialize output grid with white (0)
    output_grid = np.zeros_like(input_array)

    # --- Find solid rows ---
    solid_rows = []  # Store tuples: (row_index, color)
    for r in range(height):
        row = input_array[r, :]
        unique_colors = np.unique(row)
        # Check if the row has exactly one unique color and it's not white (0)
        if len(unique_colors) == 1 and unique_colors[0] != 0:
            solid_rows.append((r, unique_colors[0]))

    # If no solid rows found, return the all-white grid
    if not solid_rows:
        return output_grid.tolist()

    # --- Group solid rows into contiguous blocks of the same color ---
    blocks = []  # Store tuples: (start_row, end_row, color, height)
    if not solid_rows: # Should be redundant due to above check, but safe
         return output_grid.tolist()

    current_block_start_index = 0
    while current_block_start_index < len(solid_rows):
        start_row, color = solid_rows[current_block_start_index]
        current_height = 1
        
        # Look ahead to find contiguous rows of the same color
        next_row_in_block_index = current_block_start_index + 1
        while (next_row_in_block_index < len(solid_rows) and
               solid_rows[next_row_in_block_index][0] == start_row + current_height and # Check contiguity
               solid_rows[next_row_in_block_index][1] == color): # Check same color
            current_height += 1
            next_row_in_block_index += 1
            
        end_row = start_row + current_height - 1
        blocks.append((start_row, end_row, color, current_height))
        
        # Move to the start of the next potential block
        current_block_start_index = next_row_in_block_index

    # --- Select the largest block (by height) ---
    if not blocks: # If somehow no blocks were formed
        return output_grid.tolist()
        
    # Find the block with the maximum height
    # In case of ties in height, max() naturally takes the first one encountered in the list 'blocks'
    largest_block = max(blocks, key=lambda item: item[3])
    
    # --- Construct the output grid ---
    start_r, end_r, _, _ = largest_block
    
    # Copy the largest block from the input array to the output grid
    output_grid[start_r : end_r + 1, :] = input_array[start_r : end_r + 1, :]

    # Return the result as a list of lists
    return output_grid.tolist()

```
