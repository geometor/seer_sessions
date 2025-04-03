
## train_1

**input:**
```
0 0 1 1 1 1 0 0 1 1 1 0 0 1 1 0 0 0 0 0
```


**output:**
```
0 0 4 4 4 4 0 0 1 1 1 0 0 1 1 0 0 0 0 0
```


## train_2

**input:**
```
0 1 1 1 1 0 1 1 1 1 1 1 1 0 1 1 0 0 0 0
```


**output:**
```
0 1 1 1 1 0 4 4 4 4 4 4 4 0 1 1 0 0 0 0
```


## train_3

**input:**
```
0 0 0 1 1 1 1 1 0 0 0 1 0 0 1 1 1 0 0 0
```


**output:**
```
0 0 0 4 4 4 4 4 0 0 0 1 0 0 1 1 1 0 0 0
```

*   **Perception:**
    *   The input and output are sequences of integers representing colors.
    *   The primary colors involved are white (0), blue (1), and yellow (4).
    *   The transformation focuses on contiguous segments (blocks) of blue pixels (value 1).
    *   In each example, one specific block of blue pixels is changed to yellow (value 4), while other blue blocks remain unchanged.
    *   By comparing the lengths of the blue blocks in each example, it appears the *longest* contiguous block of blue pixels is the one selected for modification.
    *   If multiple blocks share the maximum length (which doesn't occur in these examples, but is a possibility), the rule likely selects the first one encountered when reading the sequence from left to right.

*   **Facts:**
    
```yaml
    elements:
      - element: sequence
        properties:
          - represents: colors
          - values: [0, 1, 4] # white, blue, yellow
      - element: segment
        properties:
          - type: contiguous block of identical color
          - relevant_color: blue (1)
          - attributes:
              - start_index: position where the segment begins
              - end_index: position where the segment ends
              - length: number of pixels in the segment
    transformation:
      - action: identify_segments
        parameters:
          - color: blue (1)
        output: list of blue segments with their properties (start_index, end_index, length)
      - action: find_longest_segment
        input: list of blue segments
        criteria: maximum length
        tie_breaking: select the segment with the smallest start_index
        output: the target segment to be modified
      - action: modify_segment
        input: target segment
        change: color of pixels within the segment
        from_color: blue (1)
        to_color: yellow (4)
    relationships:
      - The modification applies only to the segment identified as the longest (and earliest, in case of ties).
      - Other segments, even if blue, remain unchanged.
      - The overall length and structure of the sequence remain the same, only pixel values within the target segment are altered.
    ```


*   **Natural Language Program:**
    1.  Scan the input sequence from left to right to identify all contiguous segments (blocks) composed entirely of blue pixels (value 1).
    2.  For each identified blue segment, record its starting position and its length.
    3.  Determine the maximum length among all identified blue segments.
    4.  Identify the blue segment(s) that have this maximum length.
    5.  If there is only one segment with the maximum length, select it as the target segment.
    6.  If there are multiple segments with the same maximum length, select the one that appears earliest in the sequence (i.e., the one with the smallest starting position) as the target segment.
    7.  Create the output sequence by copying the input sequence.
    8.  Change the color of all pixels within the selected target segment from blue (1) to yellow (4) in the output sequence.
```python
import copy

"""
Identifies all contiguous segments of blue pixels (value 1) in the input sequence.
Finds the longest blue segment. If multiple segments share the maximum length, selects the one that starts earliest (smallest index).
Changes the color of the pixels within this selected segment from blue (1) to yellow (4) in the output sequence.
Other pixels remain unchanged.
"""

def find_segments(sequence, target_color):
    """
    Finds all contiguous segments of a target color in a sequence.

    Args:
        sequence (list): The input sequence of colors (integers).
        target_color (int): The color value to find segments of.

    Returns:
        list: A list of dictionaries, where each dictionary represents a segment
              and contains 'start' (index), 'end' (index), and 'length'.
              Returns an empty list if no segments are found.
    """
    segments = []
    start_index = -1
    for i, color in enumerate(sequence):
        if color == target_color:
            if start_index == -1:
                # Start of a new segment
                start_index = i
        elif start_index != -1:
            # End of the current segment
            segments.append({
                'start': start_index,
                'end': i - 1,
                'length': i - start_index
            })
            start_index = -1 # Reset for the next potential segment

    # Check if the sequence ends with a target segment
    if start_index != -1:
        segments.append({
            'start': start_index,
            'end': len(sequence) - 1,
            'length': len(sequence) - start_index
        })

    return segments

def transform(input_grid):
    """
    Transforms the input sequence by changing the longest contiguous block
    of blue (1) pixels to yellow (4). If there's a tie in length,
    the earliest block is chosen.

    Args:
        input_grid (list): A 1D list representing the input sequence of colors.
                           Although named 'grid', this specific task uses a 1D list.

    Returns:
        list: The transformed 1D list.
    """
    # Ensure input is treated as a 1D sequence for this task
    input_sequence = input_grid[0] if isinstance(input_grid[0], list) else input_grid

    # Initialize output_sequence as a copy of the input
    output_sequence = list(input_sequence) # Use list() for shallow copy if input is already a list

    # 1. & 2. Find all blue segments and record their properties
    blue_segments = find_segments(input_sequence, target_color=1)

    # 3. & 4. & 5. & 6. Find the longest segment (earliest in case of tie)
    longest_segment = None
    max_length = 0

    if not blue_segments:
        # No blue segments found, return the original sequence
        return output_sequence

    for segment in blue_segments:
        if segment['length'] > max_length:
            max_length = segment['length']
            longest_segment = segment
        # Tie-breaking is implicitly handled because we iterate from left to right;
        # the first segment encountered with max_length will be stored and
        # subsequent segments of the same max_length won't overwrite it.

    # 7. & 8. Modify the output sequence
    if longest_segment:
        start = longest_segment['start']
        end = longest_segment['end']
        for i in range(start, end + 1):
            # Change blue (1) to yellow (4)
            if output_sequence[i] == 1: # Double check it's blue before changing
                 output_sequence[i] = 4

    return output_sequence

```
