
## train_1

**input:**
```
0 0 0 3 0 0 0 3 3 3 3 3 3 3 3 3 3 0 0 0 3 0 0 3 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 1 0 0 0 1 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 1 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 3 0 0 3 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0 0
```

## Perception

The input and output are both single rows (1D grids) of pixels.
The input contains segments of non-white pixels (color 3/green or 1/blue) separated by white pixels (color 0). Some segments are short (length 1), while one segment is significantly longer than the others.
The output retains only the single longest contiguous segment of non-white pixels found in the input. All other pixels, including those that were part of shorter non-white segments in the input, are turned white (color 0). The position of the longest segment is preserved.

## Facts


```yaml
task_type: filtering
grid_dimensionality: 1D (row)
input_elements:
  - type: background
    color: white (0)
  - type: segment
    description: contiguous sequence of non-white pixels
    properties:
      - color: non-white (e.g., green/3, blue/1)
      - length: number of pixels in the sequence
      - position: start and end index within the row
output_elements:
  - type: background
    color: white (0)
  - type: segment
    description: the single longest segment from the input
    properties:
      - color: same as the longest input segment
      - length: same as the longest input segment
      - position: same as the longest input segment
transformation:
  action: identify_segments
  description: Find all contiguous segments of non-white pixels in the input row.
  input: input row
  output: list of segments with their color, length, and position
  action: find_longest_segment
  description: Determine the segment with the maximum length. If multiple segments share the maximum length, the examples suggest only one is kept (implicitly, perhaps the first one encountered, although the examples don't explicitly test this ambiguity).
  input: list of segments
  output: the single longest segment
  action: generate_output
  description: Create a new row of the same dimensions as the input, filled with the background color (white). Place the identified longest segment into this new row at its original position.
  input: input dimensions, background color, longest segment
  output: final output row
relationship:
  - The output row has the same length as the input row.
  - Only the pixels belonging to the longest contiguous non-white segment from the input are preserved in the output.
  - All other pixels in the output are set to the background color (white).
```


## Natural Language Program

1.  Scan the input row to identify all contiguous segments of non-white pixels. Record the color, starting position, and length of each segment.
2.  Compare the lengths of all identified segments and find the segment with the greatest length. (Assume there is only one such segment based on the examples).
3.  Create a new output row with the same length as the input row, initially filled entirely with white pixels (0).
4.  Copy the pixels corresponding to the single longest segment identified in step 2 from the input row to the same positions in the new output row.
5.  The resulting row is the final output.
```python
import numpy as np
from typing import List, Tuple, Dict

"""
Identify all contiguous segments of non-white pixels in the input row. 
Find the segment with the maximum length. 
Create an output row of the same length as the input, filled with white pixels.
Copy the pixels corresponding to the single longest segment from the input row 
to the same positions in the output row.
"""

def find_segments(row: List[int]) -> List[Dict]:
    """
    Finds all contiguous segments of non-white pixels in a 1D list (row).

    Args:
        row: A list of integers representing pixel colors.

    Returns:
        A list of dictionaries, where each dictionary represents a segment
        and contains 'color', 'start_index', and 'length'.
    """
    segments = []
    current_segment = None
    for i, pixel in enumerate(row):
        if pixel != 0:  # Non-white pixel
            if current_segment is None:
                # Start a new segment
                current_segment = {'color': pixel, 'start_index': i, 'length': 1}
            else:
                # Continue the current segment
                current_segment['length'] += 1
        else:  # White pixel
            if current_segment is not None:
                # End the current segment
                segments.append(current_segment)
                current_segment = None
    
    # Add the last segment if the row ends with non-white pixels
    if current_segment is not None:
        segments.append(current_segment)
        
    return segments

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by keeping only the longest contiguous segment 
    of non-white pixels in the row.

    Args:
        input_grid: A list containing a single list (the row) of integers.

    Returns:
        A list containing a single list (the transformed row) of integers.
    """
    # Input is expected to be a single row
    if not input_grid or len(input_grid) != 1:
        # Handle empty or multi-row input if necessary, though examples are 1D
        # For now, assume valid 1xN input based on examples.
        # If input is truly empty, return empty. If malformed, maybe error or default.
        return [] if not input_grid else [[]] * len(input_grid) # or raise ValueError

    input_row = input_grid[0]
    row_length = len(input_row)

    # Initialize output row with white pixels
    output_row = [0] * row_length

    # Find all non-white segments
    segments = find_segments(input_row)

    # If no non-white segments are found, return the all-white row
    if not segments:
        return [output_row]

    # Find the longest segment
    # If there's a tie in length, the first one encountered by find_segments will be chosen.
    longest_segment = max(segments, key=lambda s: s['length'])

    # Copy the longest segment to the output row
    start = longest_segment['start_index']
    length = longest_segment['length']
    for i in range(length):
        output_row[start + i] = input_row[start + i] # Use original color

    # Return the output row wrapped in a list
    return [output_row]
```
