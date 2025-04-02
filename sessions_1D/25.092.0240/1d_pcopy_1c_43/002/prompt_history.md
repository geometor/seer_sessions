
## train_1

**input:**
```
0 2 2 2 0 0 0 0 2 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2 0 0 0 2 2 2 0 0 0 2 2 2 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 5 5 5 0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 5 5 5 0 0 5 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 9 9 9 0 0 9 0 0 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 9 9 9 0 9 9 9 0 0 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception of task elements:**
    *   The input and output are 1D arrays or single-row grids of pixels.
    *   The primary elements are horizontal sequences (contiguous blocks) of identical non-white pixels, separated by white pixels (0).
    *   Each example contains at least one sequence longer than one pixel and one or more sequences of exactly one pixel.
    *   The transformation involves identifying a "pattern" sequence (the first encountered sequence longer than one pixel) and replacing single-pixel sequences of the *same color* with a copy of this pattern sequence.
    *   The replacement starts at the position of the single pixel and extends to the right, overwriting any existing pixels in that range.
    *   Pixels not part of a single-pixel sequence being replaced are copied directly from the input to the output.

*   **YAML Facts:**
    
```yaml
    task_type: pattern_replacement
    grid_dimensionality: 1D (or single row 2D)
    objects:
      - type: sequence
        description: Contiguous horizontal block of identical non-white pixels.
        properties:
          - color: The color (1-9) of the pixels in the sequence.
          - length: The number of pixels in the sequence.
          - position: The starting index (column) of the sequence.
    pattern_object:
      description: The first identified sequence with length > 1.
      identified_by: Scanning left-to-right.
      properties:
        - pattern_color: The color of the pattern object.
        - pattern_length: The length of the pattern object.
    target_objects:
      description: Sequences with length = 1.
      identified_by: Scanning the entire input.
    action:
      type: replace
      condition: A target object's color matches the pattern_color.
      mechanism: Replace the target object (single pixel) with a sequence identical to the pattern object (same color, same length), starting at the target object's position and extending rightwards.
    background:
      color: white (0)
      behavior: Generally preserved, unless overwritten by a replacement action.
    output_generation:
      - Initialize output as a copy of the input.
      - Identify the pattern object (color C, length L).
      - Iterate through the input grid.
      - If a single pixel of color C is found at index i:
          - Replace pixels in the output grid from index i to i + L - 1 with color C.
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the initial output grid.
    2.  Scan the input grid from left to right to find the first contiguous horizontal sequence of identical non-white pixels with a length greater than 1. Store the color (C) and length (L) of this sequence as the "pattern". If no such sequence exists, the output is identical to the input.
    3.  Iterate through each pixel position (index `i`) in the input grid.
    4.  Check if the pixel at index `i` in the input grid meets the following criteria:
        *   It is a non-white pixel.
        *   Its color matches the pattern color C.
        *   It forms a sequence of length 1 (i.e., the pixel to its left, if it exists, is different, and the pixel to its right, if it exists, is different or the grid ends).
    5.  If all criteria are met, modify the output grid by placing the pattern sequence (color C, length L) starting at index `i` and extending to index `i + L - 1`. These pixels in the output grid are set to color C, overwriting their previous values.
    6.  After checking all pixel positions, the modified output grid is the final result.
```python
import numpy as np

"""
Transforms a 1D input grid based on a pattern replacement rule.

1.  Identify the "pattern": Find the first contiguous horizontal sequence of 
    identical non-white pixels (color C) with a length (L) greater than 1, 
    scanning from left to right.
2.  If no such pattern exists, return the input grid unchanged.
3.  Identify "target" pixels: Locate all single pixels in the input grid 
    that have the same color (C) as the pattern. A pixel is considered single 
    if it's not adjacent (horizontally) to another pixel of the same color.
4.  Replace targets: For each target pixel found at index 'i', replace the 
    segment of the grid from index 'i' up to 'i + L - 1' (or the end of the 
    grid, whichever comes first) with the pattern color (C). This replacement 
    happens on a copy of the input grid.
5.  Return the modified grid.
"""

def find_pattern_sequence(grid_1d):
    """
    Finds the first sequence longer than 1 pixel.
    Returns its color and length, or (None, None) if not found.
    """
    n = len(grid_1d)
    i = 0
    while i < n:
        color = grid_1d[i]
        if color == 0:  # Skip white background
            i += 1
            continue
        
        # Found a non-white pixel, start counting sequence length
        start_index = i
        j = i + 1
        while j < n and grid_1d[j] == color:
            j += 1
        
        length = j - start_index
        
        if length > 1:
            return color, length # Found the pattern
            
        i = j # Move to the pixel after the sequence
        
    return None, None # No sequence longer than 1 found

def transform(input_grid):
    """
    Applies the pattern replacement transformation to the input grid.
    """
    # Ensure input is treated as a 1D numpy array
    input_np = np.array(input_grid, dtype=int)
    # Store original shape if it was 2D (like [[...]])
    original_shape = input_np.shape 
    if input_np.ndim > 1:
        if input_np.shape[0] == 1: # Check if it's a single row 2D array
             grid_1d = input_np.flatten()
        else:
             # This function expects a 1D array or single row 2D array
             # For multi-row inputs, the logic is undefined by the examples.
             # Returning input unchanged for now. Consider raising an error?
             # print(f"Warning: Input grid has multiple rows ({original_shape}), expected 1 row. Returning input unchanged.")
             return input_grid # Or raise ValueError("Input must be 1D or a single row.")
    else:
        grid_1d = input_np

    width = len(grid_1d)
    
    # Initialize output_grid as a copy of the 1D input
    output_grid_1d = grid_1d.copy()

    # 1. Find the pattern sequence (color C, length L)
    pattern_color, pattern_length = find_pattern_sequence(grid_1d)

    # 2. If no pattern found, return the original input
    if pattern_color is None:
        # Return in the original shape
        return output_grid_1d.reshape(original_shape)

    # 3. & 4. Find single target pixels and replace them in the output grid
    i = 0
    while i < width:
        # Check if current pixel is a potential target (matches pattern color)
        if grid_1d[i] == pattern_color:
            # Check if it's a single pixel sequence
            is_single = True
            # Check left neighbor (if exists)
            if i > 0 and grid_1d[i-1] == pattern_color:
                is_single = False
            # Check right neighbor (if exists)
            if i < width - 1 and grid_1d[i+1] == pattern_color:
                is_single = False
            
            # 5. If it's a single target pixel, perform replacement
            if is_single:
                # Determine the end index for replacement, capped by grid width
                end_index = min(i + pattern_length, width)
                # Replace the segment in the output grid
                output_grid_1d[i:end_index] = pattern_color
                # Important: Advance 'i' past the newly placed pattern to avoid re-evaluating replaced pixels
                # or creating overlapping patterns immediately. Although the logic checks original grid, 
                # skipping prevents redundant checks if we were modifying in place or checking output.
                # However, since we check the *original* grid_1d for targets, we just need to advance i by 1.
                # If we placed a pattern of length L, the next potential *start* of a single pixel
                # cannot be within the replaced section based on the original grid.
                # Let's just advance by 1.
                i += 1 
            else:
                # It's part of a longer sequence, just move to the next pixel
                i += 1
        else:
            # Not the pattern color, move to the next pixel
            i += 1

    # Reshape the output to match the original input shape before returning
    return output_grid_1d.reshape(original_shape)

```
