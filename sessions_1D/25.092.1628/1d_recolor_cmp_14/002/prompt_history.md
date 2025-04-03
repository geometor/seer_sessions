
## train_1

**input:**
```
0 0 9 0 0 9 9 9 9 9 0 0 0 9 9 9 9 0 0 0 9 9 9 9 0 0 0 9 9 0
```


**output:**
```
0 0 9 0 0 4 4 4 4 4 0 0 0 9 9 9 9 0 0 0 9 9 9 9 0 0 0 9 9 0
```


## train_2

**input:**
```
0 0 9 9 9 9 9 9 9 0 0 9 9 9 9 0 0 0 9 9 9 9 9 0 0 0 0 0 0 0
```


**output:**
```
0 0 4 4 4 4 4 4 4 0 0 9 9 9 9 0 0 0 9 9 9 9 9 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 9 9 9 0 0 9 9 9 9 0 0 0 9 9 9 9 0 0 0 9 9 0 0 9 9 0 9 9
```


**output:**
```
0 0 9 9 9 0 0 4 4 4 4 0 0 0 4 4 4 4 0 0 0 9 9 0 0 9 9 0 9 9
```

Okay, let's analyze the provided training example pair.

**Perception of Elements:**

*   **Input:** The input consists of a sequence of pixels, primarily white (0) and maroon (9). The maroon pixels form distinct horizontal segments separated by white pixels.
*   **Output:** The output is a sequence of the same length as the input. It contains white (0), maroon (9), and yellow (4) pixels.
*   **Transformation:** The core transformation involves changing the color of *some* of the maroon segments to yellow. Comparing the input and output sequences reveals that only specific maroon segments undergo this color change.

**Analysis of Changes:**

1.  **Identify Maroon Segments:** First, we locate all contiguous blocks (segments) of maroon (9) pixels in the input.
    *   `train_1`: `[9]` (len 1), `[9, 9, 9, 9, 9]` (len 5), `[9, 9, 9, 9]` (len 4), `[9, 9, 9, 9]` (len 4), `[9, 9]` (len 2)
    *   `train_2`: `[9, 9, 9, 9, 9, 9, 9]` (len 7), `[9, 9, 9, 9]` (len 4), `[9, 9, 9, 9, 9]` (len 5)
    *   `train_3`: `[9, 9, 9]` (len 3), `[9, 9, 9, 9]` (len 4), `[9, 9, 9, 9]` (len 4), `[9, 9]` (len 2), `[9, 9]` (len 2), `[9, 9]` (len 2)
2.  **Identify Changed Segments:** Next, we see which segments changed from maroon (9) to yellow (4) in the output.
    *   `train_1`: The segment of length 5 changed.
    *   `train_2`: The segment of length 7 changed.
    *   `train_3`: Both segments of length 4 changed.
3.  **Determine the Rule:** By observing the lengths of the segments that changed versus those that didn't, a pattern emerges:
    *   In `train_1`, the longest segment (length 5) changed.
    *   In `train_2`, the longest segment (length 7) changed.
    *   In `train_3`, the longest segments (both length 4) changed.
    *   The rule appears to be: identify the longest horizontal segment(s) of maroon pixels and change their color to yellow. If multiple segments share the maximum length, all of them are changed.

**YAML Facts:**


```yaml
task_description: Change the color of the longest horizontal maroon segment(s) to yellow.
elements:
  - type: pixel
    color: white (0)
    role: background
  - type: pixel
    color: maroon (9)
    role: input_object_component
  - type: pixel
    color: yellow (4)
    role: output_object_component
objects:
  - type: segment
    description: A contiguous horizontal sequence of pixels of the same color.
    relevant_color: maroon (9)
properties:
  - name: length
    applies_to: segment
    description: The number of pixels in the segment.
relationships:
  - type: comparison
    property: length
    comparison: maximum
    description: Identify the segment(s) with the greatest length among all maroon segments.
actions:
  - name: identify_segments
    input: input grid/sequence
    output: list of maroon segments with their properties (position, length)
  - name: find_max_length
    input: list of maroon segments
    output: the maximum length found
  - name: filter_longest_segments
    input: list of maroon segments, maximum length
    output: list of maroon segments with length equal to the maximum
  - name: recolor_segments
    target: segments identified in filter_longest_segments
    from_color: maroon (9)
    to_color: yellow (4)
    condition: segment length equals maximum length
grid_properties:
  - dimensionality: Assumed 1D or transformation applies row-wise independently in 2D.
  - preservation: Size and non-target pixels remain unchanged.
```


**Natural Language Program:**

1.  Scan the input sequence (or each row of the input grid) to identify all contiguous horizontal segments composed entirely of maroon (9) pixels. For each segment, record its starting position, ending position, and length.
2.  Determine the maximum length found among all identified maroon segments.
3.  Create a copy of the input sequence/grid to serve as the output.
4.  Iterate through the list of identified maroon segments.
5.  If a segment's length is equal to the maximum length determined in step 2, change the color of all pixels within that segment's start and end positions in the output copy to yellow (4).
6.  Leave all other pixels in the output copy unchanged from their corresponding input values.
7.  Return the modified output sequence/grid.
```python
import numpy as np
from typing import List, Tuple

"""
Change the color of the longest horizontal segment(s) of maroon (9) pixels 
in the input sequence to yellow (4). If multiple segments share the maximum 
length, change all of them. Treat the input as a 1D sequence.
"""

def find_maroon_segments(sequence: List[int]) -> List[Tuple[int, int, int]]:
    """
    Identifies contiguous segments of maroon (9) pixels in a 1D sequence.

    Args:
        sequence: A list of integers representing pixel colors.

    Returns:
        A list of tuples, where each tuple represents a maroon segment
        and contains (start_index, end_index, length).
    """
    segments = []
    start_index = -1
    current_length = 0
    maroon_color = 9

    for i, pixel in enumerate(sequence):
        if pixel == maroon_color:
            if start_index == -1:
                start_index = i
            current_length += 1
        else:
            if start_index != -1:
                # End of a segment
                segments.append((start_index, i - 1, current_length))
                start_index = -1
                current_length = 0

    # Handle segment ending at the very end of the sequence
    if start_index != -1:
        segments.append((start_index, len(sequence) - 1, current_length))

    return segments

def transform(input_grid: List[int]) -> List[int]:
    """
    Applies the transformation rule to a 1D input sequence.

    Args:
        input_grid: A list of integers representing the input pixel sequence.

    Returns:
        A list of integers representing the transformed pixel sequence.
    """
    # Treat the input as a 1D sequence
    sequence = input_grid

    # Initialize output_grid as a copy of the input
    output_grid = list(sequence)
    
    # --- Identify maroon segments ---
    maroon_segments = find_maroon_segments(sequence)

    # --- Handle case with no maroon segments ---
    if not maroon_segments:
        return output_grid # Return the original sequence if no maroon found

    # --- Find the maximum length among the segments ---
    max_length = 0
    for _, _, length in maroon_segments:
        if length > max_length:
            max_length = length

    # --- Recolor the longest segments ---
    yellow_color = 4
    for start, end, length in maroon_segments:
        if length == max_length:
            # Change the color of pixels in this segment to yellow in the output
            for i in range(start, end + 1):
                output_grid[i] = yellow_color

    return output_grid
```
