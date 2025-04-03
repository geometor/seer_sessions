
## train_1

**input:**
```
0 0 0 7 7 7 0 0 7 7 0 7 7 0 7 7 7 0 0
```


**output:**
```
0 0 0 2 2 2 0 0 6 6 0 6 6 0 2 2 2 0 0
```


## train_2

**input:**
```
0 0 7 7 7 7 7 0 7 7 7 7 0 0 0 7 7 7 7
```


**output:**
```
0 0 2 2 2 2 2 0 6 6 6 6 0 0 0 6 6 6 6
```


## train_3

**input:**
```
0 0 7 7 7 7 7 7 0 0 0 7 7 7 7 7 0 0 7
```


**output:**
```
0 0 6 6 6 6 6 6 0 0 0 2 2 2 2 2 0 0 2
```

## Perception

The input and output are one-dimensional arrays (or single-row grids) of pixels.
The input contains white (0) and orange (7) pixels.
The output contains white (0), red (2), and magenta (6) pixels.
The white pixels remain unchanged in the output.
The orange pixels change color based on the length of the contiguous horizontal segment they belong to.
Specifically, contiguous segments of three orange pixels change to red, and contiguous segments of two orange pixels change to magenta.

## Facts


```yaml
task_context:
  grid_dimensionality: 1D (or single row)
  colors_present_input: [white, orange]
  colors_present_output: [white, red, magenta]

objects:
  - type: pixel_segment
    description: Contiguous horizontal sequence of pixels of the same color.
    properties:
      - color: The color of the pixels in the segment (e.g., white, orange).
      - length: The number of pixels in the segment.

transformation:
  description: Changes the color of orange pixel segments based on their length.
  rules:
    - condition: Input pixel is white (0).
      action: Output pixel remains white (0).
    - condition: Input pixel is orange (7) and belongs to a segment of length 3.
      action: Output pixel becomes red (2).
    - condition: Input pixel is orange (7) and belongs to a segment of length 2.
      action: Output pixel becomes magenta (6).
  unchanged_elements: White background pixels.

relationships:
  - type: color_mapping
    input_color: orange (7)
    output_color_conditions:
      - condition: segment length == 3
        output_color: red (2)
      - condition: segment length == 2
        output_color: magenta (6)
```


## Natural Language Program

1.  Iterate through the input array/row to identify contiguous horizontal segments of orange (7) pixels.
2.  For each identified orange segment:
    *   Determine the length of the segment.
    *   If the length is 3, replace all orange pixels in that segment with red (2) pixels in the output.
    *   If the length is 2, replace all orange pixels in that segment with magenta (6) pixels in the output.
3.  Keep all white (0) pixels unchanged in their original positions in the output.
4.  Construct the output array/row based on these replacements and unchanged pixels.
```python
"""
Iterate through the input array/row. If a pixel is white (0), keep it white in the output. 
If a pixel is orange (7), identify the contiguous horizontal segment of orange pixels it belongs to. 
Determine the length of this segment. If the length is 3, change all pixels in that segment to red (2) in the output. 
If the length is 2, change all pixels in that segment to magenta (6) in the output.
"""

import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the length of contiguous orange segments.

    Args:
        input_grid (list or np.array): A 1D list or array representing the input row.

    Returns:
        list: The transformed output row.
    """
    # Ensure input is a list for easier manipulation
    if isinstance(input_grid, np.ndarray):
        input_list = input_grid.tolist()
    else:
        input_list = list(input_grid) # Make a copy if it's already a list

    output_list = list(input_list) # Create a mutable copy for the output
    n = len(input_list)
    i = 0
    while i < n:
        # Check if the current pixel is orange
        if input_list[i] == 7:
            # Find the end of the contiguous orange segment
            start_index = i
            segment_length = 0
            while i < n and input_list[i] == 7:
                segment_length += 1
                i += 1
            end_index = i # i is now the index after the segment

            # Apply the transformation based on segment length
            if segment_length == 3:
                # Change segment to red (2)
                for j in range(start_index, end_index):
                    output_list[j] = 2
            elif segment_length == 2:
                # Change segment to magenta (6)
                for j in range(start_index, end_index):
                    output_list[j] = 6
            # If segment length is not 2 or 3, the original orange pixels remain 
            # (this shouldn't happen based on examples, but handles edge cases)
            # No need to increment i here, the inner loop already did

        else:
            # If the pixel is not orange (it's white 0), just move to the next pixel
            # White pixels are already correctly copied in output_list
            i += 1

    return output_list
```
