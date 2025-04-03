
## train_1

**input:**
```
0 0 0 0 0 3 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 1 1 1 1 1 1 1 1 3 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 8 2 2 2 2 2 2 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 8 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 8 2 2 2 2 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 8 0 0 0 0 0
```

*   **Perception:**
    *   The input consists of a 1D array (or a 1xN grid) containing mostly white pixels (0).
    *   There are two non-white elements present:
        1.  A single pixel of one color (the "marker"). In the examples, this is green (3) or azure (8).
        2.  A contiguous horizontal block of pixels of another color (the "block"). In the examples, this is blue (1) or red (2).
    *   The marker pixel is always located immediately to the left of the block.
    *   The transformation involves moving the marker pixel from its original position to the position immediately to the right of the block.
    *   The block itself remains unchanged in position and color.
    *   The pixel at the original marker position becomes white (0).

*   **Facts:**
    
```yaml
    task_type: object_manipulation
    grid_dimensionality: 1D # Effectively 1xN
    objects:
      - type: marker_pixel
        count: 1
        properties:
          - color: non-white (distinct from block color)
          - size: 1 pixel
          - initial_position: immediately precedes the block
      - type: color_block
        count: 1
        properties:
          - color: non-white (distinct from marker color)
          - shape: contiguous horizontal line
          - size: variable length (>= 1 pixel)
          - position: immediately follows the marker
    relationships:
      - type: adjacency
        object1: marker_pixel
        object2: color_block
        details: marker is immediately left-adjacent to the block in the input.
    actions:
      - action: move
        object: marker_pixel
        from: initial position (left of block)
        to: position immediately right of the block
      - action: recolor
        location: initial position of marker_pixel
        new_color: white (0)
    background: white (0)
    ```


*   **Natural Language Program:**
    1.  Scan the input array to find the non-white pixels.
    2.  Identify the single pixel that is immediately followed by a different non-white color; this is the "marker" pixel. Record its color and original index.
    3.  Identify the contiguous sequence of the *other* non-white color that follows the marker; this is the "block". Record the index of the last pixel in this block.
    4.  Create a copy of the input array to serve as the output.
    5.  Set the pixel at the marker's original index in the output array to white (0).
    6.  Set the pixel at the index immediately following the last pixel of the block in the output array to the marker's color.
    7.  Return the modified output array.
```python
import numpy as np

"""
Moves a single 'marker' pixel from the left side of a contiguous block of a different color to the right side of that block in a 1D array.
"""

def find_marker_and_block(grid_1d):
    """
    Finds the marker pixel and the block of pixels in the 1D grid.

    Args:
        grid_1d (np.array): The 1D input grid.

    Returns:
        tuple: (marker_color, marker_index, block_color, block_start_index, block_end_index)
               Returns (None, -1, None, -1, -1) if not found.
    """
    marker_color = None
    marker_index = -1
    block_color = None
    block_start_index = -1
    block_end_index = -1

    for i in range(len(grid_1d) - 1):
        # Potential marker found if current pixel is non-white and next is non-white but different color
        if grid_1d[i] != 0 and grid_1d[i+1] != 0 and grid_1d[i] != grid_1d[i+1]:
            # Check if this is the start of the pattern (no non-white before) or preceded by white
            if i == 0 or grid_1d[i-1] == 0:
                marker_color = grid_1d[i]
                marker_index = i
                block_color = grid_1d[i+1]
                block_start_index = i + 1
                
                # Find the end of the block
                block_end_index = block_start_index
                for j in range(block_start_index + 1, len(grid_1d)):
                    if grid_1d[j] == block_color:
                        block_end_index = j
                    else:
                        break # Block ended
                
                # Check if the pixel after the block is white, ensuring pattern integrity
                if block_end_index + 1 >= len(grid_1d) or grid_1d[block_end_index + 1] == 0:
                     return marker_color, marker_index, block_color, block_start_index, block_end_index
                else: # Invalid pattern, reset and keep searching
                     marker_color = None
                     marker_index = -1
                     block_color = None
                     block_start_index = -1
                     block_end_index = -1


    return marker_color, marker_index, block_color, block_start_index, block_end_index


def transform(input_grid):
    """
    Transforms the input grid by moving the marker pixel.

    Args:
        input_grid (list): A list representing the 1D input grid.

    Returns:
        list: The transformed list representing the 1D output grid.
    """
    # Convert input list to numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)

    # Find the marker and block details
    marker_color, marker_index, _, _, block_end_index = find_marker_and_block(input_array)

    # If the pattern wasn't found, return the original grid
    if marker_index == -1:
        return input_grid

    # Create a copy of the input array to modify for the output
    output_array = np.copy(input_array)

    # Set the original marker position to white (0)
    output_array[marker_index] = 0

    # Set the position immediately after the block to the marker color
    # Ensure we don't go out of bounds (though problem constraints might prevent this)
    new_marker_index = block_end_index + 1
    if new_marker_index < len(output_array):
         output_array[new_marker_index] = marker_color
    else:
        # Handle edge case if marker needs to be placed beyond the array boundary
        # Based on examples, this doesn't seem to happen, but good practice.
        # Option 1: Extend array (not typical for ARC)
        # Option 2: Return unmodified or error (safer)
        print(f"Warning: New marker position {new_marker_index} is out of bounds for array length {len(output_array)}. Returning original.")
        return input_grid


    # Convert the output numpy array back to a list
    output_grid = output_array.tolist()

    return output_grid
```
