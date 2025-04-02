
## train_1

**input:**
```
0 0 0 0 0 0 0 1 1 1 0 0 0 9 0 0
```


**output:**
```
0 0 0 0 0 0 0 1 1 1 1 1 1 9 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 1 1 1 0 0 0 9
```


**output:**
```
0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 9
```


## train_3

**input:**
```
0 6 6 6 6 6 6 6 6 6 6 0 0 0 9 0
```


**output:**
```
0 6 6 6 6 6 6 6 6 6 6 6 6 6 9 0
```

*   **Perception of the elements:**
    *   The inputs and outputs are 1D arrays (or grids of height 1).
    *   Each example features a sequence of three white pixels (`0 0 0`) followed immediately by a maroon pixel (`9`).
    *   Immediately preceding the `0 0 0` sequence is a contiguous block of pixels of a single non-white color (e.g., blue `1` or magenta `6`).
    *   The transformation modifies the three white pixels (`0 0 0`) located between the colored block and the maroon pixel (`9`).
    *   The three white pixels are replaced by three pixels of the same color as the block preceding them.
    *   All other pixels in the grid remain unchanged.
    *   The overall length/dimensions of the grid remain the same.

*   **Facts:**
    
```yaml
    elements:
      - object: grid
        description: A 1D array of pixels with color values 0-9.
      - object: pixel
        properties:
          - color: (white: 0, blue: 1, red: 2, green: 3, yellow: 4, gray: 5, magenta: 6, orange: 7, azure: 8, maroon: 9)
          - position: index within the 1D array.
      - object: block
        description: A contiguous sequence of pixels of the same non-white color.
      - object: gap
        description: A specific contiguous sequence of three white pixels (0 0 0).
      - object: marker
        description: A single maroon pixel (9).
    relationships:
      - type: spatial_sequence
        description: A block of non-white pixels is immediately followed by the gap (0 0 0), which is immediately followed by the marker (9). Let the color of the block be C.
        example_train_1: "Block [1 1 1] followed by Gap [0 0 0] followed by Marker [9]" (C=1)
        example_train_3: "Block [6 6 ... 6] followed by Gap [0 0 0] followed by Marker [9]" (C=6)
    action:
      - type: replacement
        description: The gap sequence (0 0 0) is replaced by a sequence of three pixels, all having the color C derived from the preceding block.
        input_pattern: "... [Block C] [0 0 0] [9] ..."
        output_pattern: "... [Block C] [C C C] [9] ..."
    invariants:
      - Grid dimensions remain constant.
      - Pixels outside the identified [Gap] sequence remain unchanged.
      - The marker pixel [9] and the block preceding the gap remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Scan the input grid from left to right to find the last occurrence of the sequence `[0, 0, 0, 9]` (three white pixels followed by a maroon pixel).
    2.  If this sequence is found:
        a.  Identify the pixel immediately preceding the `[0, 0, 0]` sequence. Let its color be `C`. Assume `C` is not white (0).
        b.  Replace the `[0, 0, 0]` sequence with `[C, C, C]`.
    3.  If the sequence `[0, 0, 0, 9]` is not found, or if the pixel preceding it is white (0), leave the grid unchanged.
    4.  Return the modified grid.
```python
import numpy as np

"""
Identifies the last occurrence of the sequence [0, 0, 0, 9] (three white pixels followed by a maroon pixel) in a 1D input grid. 
If found, it checks the color 'C' of the pixel immediately preceding this sequence. 
If this preceding pixel exists and its color 'C' is not white (0), it replaces the three white pixels [0, 0, 0] with three pixels of color 'C' ([C, C, C]). 
Otherwise, the grid remains unchanged.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the rule described above.

    Args:
        input_grid (list or np.array): A 1D list or numpy array representing the input grid.

    Returns:
        np.array: The transformed 1D numpy array.
    """
    # Convert input to numpy array for easier slicing and manipulation
    grid = np.array(input_grid, dtype=int)
    # Create a copy to modify, ensuring the original is untouched if no change is needed
    output_grid = grid.copy()
    n = len(grid)
    
    # Target sequence to find
    target_sequence = np.array([0, 0, 0, 9], dtype=int)
    sequence_len = len(target_sequence)
    
    # Variable to store the index of the last found match
    last_match_index = -1
    
    # Scan the grid from left to right to find the sequence
    # We store the index of the *last* occurrence found
    for i in range(n - sequence_len + 1):
        if np.array_equal(grid[i : i + sequence_len], target_sequence):
            last_match_index = i
            
    # If a match was found (last_match_index is not -1)
    if last_match_index != -1:
        # Check if there is a preceding pixel (index > 0)
        if last_match_index > 0:
            # Get the color of the preceding pixel
            preceding_color = grid[last_match_index - 1]
            
            # Check if the preceding color is not white (0)
            if preceding_color != 0:
                # Replace the [0, 0, 0] sequence with [C, C, C]
                # The sequence starts at last_match_index
                output_grid[last_match_index : last_match_index + 3] = preceding_color

    # Return the modified grid (or the original copy if no modification occurred)
    return output_grid.tolist() # Return as list, consistent with input format if needed
```
