
## train_1

**input:**
```
0 0 0 1 1 1 0 0 9 0 0 0
```


**output:**
```
0 0 0 0 0 1 1 1 9 0 0 0
```


## train_2

**input:**
```
0 5 5 5 5 5 5 5 0 0 9 0
```


**output:**
```
0 0 0 5 5 5 5 5 5 5 9 0
```


## train_3

**input:**
```
4 4 4 4 4 4 4 0 0 9 0 0
```


**output:**
```
0 0 4 4 4 4 4 4 4 9 0 0
```

*   **Perception:**
    *   The input and output are single-row grids (1D arrays).
    *   Each input grid contains a contiguous block of pixels of a single color (e.g., blue, gray, yellow), distinct from white (0) and maroon (9).
    *   Each input grid also contains exactly one maroon (9) pixel.
    *   The remaining pixels are white (0).
    *   In the output grid, the contiguous block of colored pixels has shifted horizontally to the right.
    *   The final position of the block is such that its rightmost pixel is immediately adjacent to the left of the maroon (9) pixel.
    *   The original positions occupied by the colored block before the shift are replaced with white (0) pixels.
    *   The maroon pixel and all other white pixels remain in their original positions.

*   **Facts:**
    
```yaml
    task_type: object_manipulation
    grid_dimensionality: 1D
    objects:
      - type: block
        description: A contiguous sequence of pixels of the same color, not white (0) or maroon (9).
        properties:
          - color: Varies (blue, gray, yellow in examples)
          - length: Varies (3, 7, 7 in examples)
          - start_index: The index of the leftmost pixel of the block.
          - end_index: The index of the rightmost pixel of the block.
        count: 1 per grid
      - type: target_pixel
        description: A single pixel with the color maroon (9).
        properties:
          - color: maroon (9)
          - index: The position of the maroon pixel.
        count: 1 per grid
      - type: background
        description: Pixels with the color white (0).
    actions:
      - name: identify_block
        description: Locate the start index, end index, and color of the non-white, non-maroon contiguous block.
      - name: identify_target
        description: Locate the index of the maroon (9) pixel.
      - name: calculate_shift
        description: Determine the destination start index for the block so its end index is `target_index - 1`. The new start index is `target_index - block_length`.
      - name: move_block
        description: Create a new grid, initially filled with white (0). Copy the block pixels to their new positions based on the calculated shift.
      - name: preserve_target
        description: Copy the maroon (9) target pixel to its original position in the new grid.
      - name: preserve_background
        description: Ensure all other pixels in the new grid remain white (0), effectively replacing the original block position with white.
    relationships:
      - type: adjacency
        description: In the output, the rightmost pixel of the moved block is immediately to the left of the target pixel (index `target_index - 1`).
    state_changes:
      - The identified block changes its position (start and end indices).
      - The grid cells originally occupied by the block become white (0).
    constraints:
      - There is exactly one movable block.
      - There is exactly one target (maroon) pixel.
      - The block always moves rightwards.
      - The grid dimensions remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid, but fill it entirely with white (0) pixels.
    2.  Scan the input grid to identify the contiguous block of non-white (0) and non-maroon (9) pixels. Record its color, length, and start index.
    3.  Scan the input grid to find the index of the single maroon (9) pixel (the target index).
    4.  Calculate the new start index for the block in the output grid. This index is `target_index - block_length`.
    5.  Copy the pixels of the identified block (using its recorded color) into the output grid, starting at the calculated new start index and extending for the block's length.
    6.  Copy the maroon (9) pixel into the output grid at its original target index.
    7.  Return the modified output grid.
```python
import numpy as np

"""
Identify a contiguous block of a single color (not white 0 or maroon 9) and a single target pixel (maroon 9) in a 1D input grid. Shift the block horizontally to the right so its rightmost pixel is immediately to the left of the target pixel. Fill the original position of the block with white (0). Keep the target pixel and other white pixels in their original positions.
"""

def find_block(grid):
    """
    Finds the start index, end index, length, and color of the contiguous block.
    Assumes exactly one such block exists.
    """
    block_color = -1
    block_start = -1
    block_end = -1
    n = len(grid)
    
    for i in range(n):
        if grid[i] != 0 and grid[i] != 9:
            block_color = grid[i]
            block_start = i
            # Find the end of the block
            j = i
            while j < n and grid[j] == block_color:
                j += 1
            block_end = j - 1
            break # Found the block, stop searching
            
    if block_start != -1:
        block_length = block_end - block_start + 1
        return block_start, block_end, block_length, block_color
    else:
        return None # Should not happen based on problem description

def find_target(grid):
    """Finds the index of the target (maroon 9) pixel."""
    n = len(grid)
    for i in range(n):
        if grid[i] == 9:
            return i
    return -1 # Should not happen based on problem description

def transform(input_grid):
    """
    Transforms the input grid according to the described rule.
    """
    # Convert input to numpy array for easier slicing if it's not already
    grid_np = np.array(input_grid)
    n = len(grid_np)
    
    # 1. Initialize the output grid as a copy of the input grid, but fill it entirely with white (0) pixels.
    output_grid = np.zeros_like(grid_np) # Initialize with white (0)

    # 2. Scan the input grid to identify the contiguous block of non-white (0) and non-maroon (9) pixels.
    block_info = find_block(grid_np)
    if block_info is None:
        # Handle case where no block is found (though constraints say one exists)
        print("Warning: No movable block found.")
        return input_grid # Or return an empty/error state
    
    block_start, block_end, block_length, block_color = block_info

    # 3. Scan the input grid to find the index of the single maroon (9) pixel.
    target_index = find_target(grid_np)
    if target_index == -1:
        # Handle case where no target is found (though constraints say one exists)
        print("Warning: No target pixel (9) found.")
        return input_grid # Or return an empty/error state

    # 4. Calculate the new start index for the block in the output grid.
    new_start_index = target_index - block_length

    # 5. Copy the pixels of the identified block into the output grid at the new location.
    # Ensure indices are within bounds, though calculation should guarantee this if block fits
    if new_start_index >= 0 and new_start_index + block_length <= n:
         output_grid[new_start_index : new_start_index + block_length] = block_color
    else:
         # This case suggests the block wouldn't fit before the target.
         # Based on examples, this shouldn't occur. 
         # If it could, need clarification on handling.
         print(f"Warning: Calculated block position [{new_start_index}:{new_start_index + block_length}] is out of bounds for grid length {n}.")
         # Default behavior might be to not place the block or handle error.
         # For now, proceed but acknowledge potential issue.
         # Let's place what fits if it starts out of bound left? Or error out?
         # Let's assume it always fits based on task description.


    # 6. Copy the maroon (9) pixel into the output grid at its original target index.
    output_grid[target_index] = 9

    # 7. Return the modified output grid.
    # Convert back to list if the original input was a list
    if isinstance(input_grid, list):
        return output_grid.tolist()
    else:
        return output_grid
```
