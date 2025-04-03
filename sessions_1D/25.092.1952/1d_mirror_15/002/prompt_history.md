
## train_1

**input:**
```
0 0 0 0 0 0 1 1 1 1 1 1 0 9 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 9 0 1 1 1 1 1 1 0 0 0
```


## train_2

**input:**
```
0 0 0 3 3 3 3 3 3 3 0 0 9 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 9 0 0 3 3 3 3 3 3 3 0 0
```


## train_3

**input:**
```
0 2 2 2 2 2 2 2 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 9 0 0 2 2 2 2 2 2 2 0 0 0 0
```

*   **Perception:** The input is a 1D array of pixels (represented as integers). It contains a background of white pixels (0), a single maroon pixel (9) acting as a separator, and a contiguous block of pixels of another single color (blue, green, or red in the examples). The transformation involves moving the colored block from one side of the maroon separator to the other, filling the original location with white pixels. The maroon pixel remains in its original position.

*   **Facts YAML:**
    
```yaml
    task_type: array_manipulation
    components:
      - item: background
        color: 0 (white)
        role: fills empty space
      - item: separator
        color: 9 (maroon)
        count: 1
        role: pivot point, remains stationary
      - item: colored_block
        color: any color except 0 (white) and 9 (maroon)
        structure: contiguous block of identical pixels
        count: 1
        role: mobile element
    actions:
      - action: identify
        target: separator (maroon pixel)
        result: position (index) of the separator
      - action: identify
        target: colored_block
        result: color, length, and original position (relative to the separator)
      - action: move
        target: colored_block
        from: original side of the separator
        to: opposite side of the separator
        details: place the block adjacent to the separator on the new side
      - action: fill
        target: original position of the colored_block
        with: background color (white)
    constraints:
      - The input array always contains exactly one separator (maroon pixel).
      - The input array always contains exactly one contiguous colored_block (non-white, non-maroon).
      - The separator's position does not change.
    output_construction:
      - Initialize an output array of the same size as the input, filled with the background color (white).
      - Place the separator at its original position in the output array.
      - Place the colored_block in the output array on the side of the separator opposite to its original position, immediately adjacent to the separator.
    ```


*   **Natural Language Program:**
    1.  Find the index of the single maroon pixel (9) in the input array.
    2.  Identify the contiguous block of pixels that are neither white (0) nor maroon (9). Record its color and length.
    3.  Determine whether this colored block is positioned entirely to the left or entirely to the right of the maroon pixel.
    4.  Create a new array of the same size as the input, initially filled entirely with white pixels (0).
    5.  Place the maroon pixel (9) into the new array at the same index it occupied in the input array.
    6.  If the colored block was originally to the left of the maroon pixel, place the block into the new array immediately to the right of the maroon pixel, using its recorded color and length.
    7.  If the colored block was originally to the right of the maroon pixel, place the block into the new array immediately to the left of the maroon pixel, ensuring it ends just before the maroon pixel's index, using its recorded color and length.
    8.  The resulting array is the output.
```python
import numpy as np

"""
Finds a single maroon pixel (9) which acts as a separator.
Identifies a contiguous block of a single color (not white 0 or maroon 9).
Moves this colored block to the opposite side of the maroon separator, placing it adjacent to the separator.
Fills the original location of the colored block with white pixels (0).
The maroon separator remains in its original position.
"""

def find_maroon_index(grid):
    """Finds the index of the maroon pixel (9)."""
    for i, pixel in enumerate(grid):
        if pixel == 9:
            return i
    return -1 # Should not happen based on problem description

def find_colored_block(grid, maroon_index):
    """Finds the contiguous block of non-white, non-maroon color."""
    block_color = -1
    block_start = -1
    block_length = 0

    for i, pixel in enumerate(grid):
        if pixel != 0 and pixel != 9:
            if block_start == -1: # Start of a potential block
                block_color = pixel
                block_start = i
                block_length = 1
            elif pixel == block_color: # Continuing the block
                block_length += 1
            else: # Found a different color, stop (shouldn't happen with one block)
                break 
        elif block_start != -1: # End of the block (hit 0 or 9)
             break # Found the block, stop searching

    # Check if the block is valid (found and contiguous)
    if block_start != -1:
         # Verify contiguity if needed, but problem implies it
         pass 
            
    return block_color, block_start, block_length


def transform(input_grid):
    """
    Transforms the input grid by moving a colored block across a maroon separator.
    
    Args:
        input_grid (list or np.ndarray): A 1D array of integers representing pixel colors.

    Returns:
        np.ndarray: The transformed 1D array.
    """
    # Convert to numpy array for easier manipulation
    input_array = np.array(input_grid)
    grid_size = len(input_array)
    
    # 1. Find the index of the single maroon pixel (9).
    maroon_index = find_maroon_index(input_array)
    if maroon_index == -1:
        # Handle error: maroon pixel not found (though problem statement implies it exists)
        return input_array # Or raise an error

    # 2. Identify the contiguous block of pixels (not 0 or 9). Record color, length, start index.
    block_color, block_start, block_length = find_colored_block(input_array, maroon_index)
    if block_color == -1:
         # Handle error: colored block not found (though problem implies it exists)
         return input_array # Or raise an error

    # 3. Determine if the block is left or right of the maroon pixel.
    block_on_left = block_start < maroon_index

    # 4. Create a new array of the same size, filled with white pixels (0).
    output_array = np.zeros_like(input_array)

    # 5. Place the maroon pixel (9) in the output array at its original index.
    output_array[maroon_index] = 9

    # 6. & 7. Place the colored block on the opposite side of the maroon pixel.
    if block_on_left:
        # Place block immediately to the right of the maroon pixel
        new_block_start = maroon_index + 1
        # Ensure the block fits within the grid bounds
        if new_block_start + block_length <= grid_size:
            output_array[new_block_start : new_block_start + block_length] = block_color
        else:
            # Handle case where block doesn't fit (shouldn't happen based on examples)
             # Trim block if necessary? Or error? Based on ARC, likely won't happen.
             pass 
    else: # Block was on the right
        # Place block immediately to the left of the maroon pixel
        new_block_start = maroon_index - block_length
        # Ensure the block start index is valid
        if new_block_start >= 0:
             output_array[new_block_start : new_block_start + block_length] = block_color
        else:
            # Handle case where block doesn't fit (shouldn't happen based on examples)
             # Trim block if necessary? Or error? Based on ARC, likely won't happen.
             pass

    # 8. Return the resulting array.
    return output_array.tolist() # Return as list to match input/output format if necessary
```
