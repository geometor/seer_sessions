
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 4 4 4 4 4 4 4 4 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 3 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 7 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 5 5 5 5 7 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 1 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 4 4 4 1 0 0 0 0 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The input and output are 1D arrays (or single rows of a grid) of integers representing colors.
    *   Each array primarily consists of white (0) pixels.
    *   Within the white background, there is a single contiguous block of non-white pixels.
    *   This non-white block is composed of two distinct colors: one color appears only once (let's call it the "marker" color), and the other color fills the rest of the block (the "body" color).
    *   In all examples, the marker pixel is located at the leftmost position of the non-white block in the input.
    *   The transformation involves moving the marker pixel to the rightmost position of the non-white block in the output, while the body pixels shift accordingly to fill the space.
    *   The colors themselves, the length of the non-white block, and the position of the block within the overall array remain unchanged.

*   **YAML Facts:**
    
```yaml
    task: Move a unique 'marker' pixel from one end of a colored block to the other.
    elements:
      - type: background
        color: white (0)
        description: Fills the array outside the main object. Remains unchanged.
      - type: colored_block
        description: A contiguous sequence of non-white pixels.
        properties:
          - composition: Contains two distinct colors.
          - structure: One 'marker' pixel and multiple 'body' pixels.
          - invariant: Total length and constituent colors remain the same. Position within the array remains the same.
      - type: marker_pixel
        description: The single pixel within the colored_block with a unique color.
        properties:
          - color: variable (green, orange, blue in examples)
          - initial_position: Leftmost end of the colored_block in the input.
          - final_position: Rightmost end of the colored_block in the output.
      - type: body_pixels
        description: The pixels within the colored_block that share the same color, distinct from the marker.
        properties:
          - color: variable (yellow, gray, yellow in examples)
          - quantity: Fills the rest of the colored_block.
          - relative_position: Shifts to accommodate the marker's movement but maintain contiguity.
    transformation:
      action: Relocate the marker_pixel within the colored_block.
      details: Move the marker_pixel from the leftmost position to the rightmost position of the block.
      constraints: Preserve the colors, length, and overall position of the colored_block.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous sequence of non-white pixels (the "colored block") in the input array.
    2.  Within this colored block, distinguish the single "marker" pixel (which has a unique color within the block) from the "body" pixels (which all share a different, single color).
    3.  Determine the current position of the marker pixel within the block (it will be at one end - in the examples, the left end).
    4.  Create the output array by keeping all background (white) pixels the same.
    5.  Reconstruct the colored block in the output by placing the marker pixel at the opposite end of the block from where it was found in the input (e.g., if it was at the left end, move it to the right end).
    6.  Fill the remaining positions of the block with the body pixels, maintaining their color and count.
```python
import numpy as np
from collections import Counter

"""
Identify the contiguous sequence of non-white pixels (the 'colored block') in the input array.
Within this block, distinguish the single 'marker' pixel (unique color) from the 'body' pixels (shared color).
Move the marker pixel from its current end position (left in examples) to the opposite end (right in examples).
Fill the remaining positions of the block with the body pixels, maintaining their color and count.
The background pixels (white, 0) remain unchanged.
"""

def find_colored_block_indices(grid_1d):
    """Finds the start and end indices of the first contiguous block of non-zero pixels."""
    non_zero_indices = np.where(grid_1d != 0)[0]
    if len(non_zero_indices) == 0:
        return -1, -1  # No block found
    
    start_index = non_zero_indices[0]
    end_index = non_zero_indices[-1]
    
    # Verify contiguity (optional but good practice)
    if not np.all(grid_1d[start_index : end_index+1] != 0):
        # This handles cases with multiple separate blocks, 
        # but the problem description implies only one block.
        # For this specific problem, we might assume the first found contiguous segment is the target.
        # Let's refine based on the assumption of a single block:
        current_index = start_index
        while current_index + 1 < len(grid_1d) and grid_1d[current_index + 1] != 0:
            current_index += 1
        end_index = current_index
        
    return start_index, end_index

def transform(input_grid_list):
    """
    Transforms the input grid (represented as a 1D list) according to the rule:
    Move the unique 'marker' pixel within a colored block from one end to the other.
    """
    # Convert list to numpy array for easier manipulation
    input_grid = np.array(input_grid_list, dtype=int)
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)

    # 1. Identify the contiguous sequence of non-white pixels (the "colored block")
    start_index, end_index = find_colored_block_indices(input_grid)

    # If no block is found, return the original grid
    if start_index == -1:
        return output_grid.tolist() # Return as list

    # Extract the colored block
    colored_block = input_grid[start_index : end_index + 1]
    block_len = len(colored_block)

    # 2. Distinguish the marker pixel and body pixels
    if block_len <= 1:
        # Block is too small to have distinct marker/body, return original
        return output_grid.tolist()

    color_counts = Counter(colored_block)
    marker_color = -1
    body_color = -1
    
    for color, count in color_counts.items():
        if count == 1:
            marker_color = color
        elif count > 1:
            body_color = color
            
    # Check if marker and body colors were found as expected
    if marker_color == -1 or body_color == -1:
        # Unexpected block composition, return original
        # (e.g., all unique colors, or more than two colors)
        return output_grid.tolist()

    # 3. Determine the current position of the marker pixel
    # Based on examples, the marker is always at one end.
    marker_at_start = (colored_block[0] == marker_color)
    marker_at_end = (colored_block[-1] == marker_color)

    # 4. Create the new arrangement for the colored block
    new_block = np.full(block_len, body_color, dtype=int) # Fill with body color
    
    # 5. Place the marker pixel at the opposite end
    if marker_at_start:
        # Move marker to the end
        new_block[-1] = marker_color
    elif marker_at_end:
        # Move marker to the start
        new_block[0] = marker_color
    else:
        # Marker is not at an end - unexpected based on examples. Return original.
        # Or handle based on further clarification (e.g., swap with nearest end?)
        # For now, based strictly on observed examples, we assume it starts at left end.
        # Let's stick to the observed pattern: if marker is at start, move to end.
        if colored_block[0] == marker_color:
             new_block[-1] = marker_color
        else:
             # If it wasn't at the start, we might have misidentified or the pattern is different.
             # Safest is to return the original or log an error.
             # Given the examples always show start->end, let's assume this is the only case.
             # If the marker wasn't at the start, something is wrong with assumptions.
             # Re-evaluating the logic based ONLY on examples: marker is always at left, moves to right.
             if colored_block[0] == marker_color:
                 new_block[-1] = marker_color
             else:
                # This case shouldn't happen based on training data. Return original.
                return output_grid.tolist()


    # 6. Place the reconstructed block back into the output grid
    output_grid[start_index : end_index + 1] = new_block

    # Return the modified grid as a list
    return output_grid.tolist()

```
