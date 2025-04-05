
## train_1

**input:**
```
0 0 0 0 2 0 4 0 0 0 0 0
```


**output:**
```
0 0 4 0 2 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 7 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 2 7 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 2 0 1 1 0 0
```


**output:**
```
0 0 0 1 1 0 2 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 4 4 0 2 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 0 4 4 0
```


## train_5

**input:**
```
0 0 0 0 0 0 2 0 0 0 0 9
```


**output:**
```
0 9 0 0 0 0 2 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 2 0 0 9 9 0 0 0
```


**output:**
```
9 9 0 0 2 0 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 8 0 0 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 2 0 0 8
```

*   **Perception of Task Elements:**
    *   The input and output are sequences of integers of fixed length (12).
    *   The sequences contain mostly zeros and a few non-zero integers.
    *   The number `2` appears exactly once in each input sequence and plays a special role.
    *   Other non-zero numbers can appear individually or in contiguous groups.
    *   The transformation involves rearranging the non-zero numbers based on their position relative to the number `2`. Zeros act as background/empty space.

*   **YAML Facts:**
    
```yaml
    task_type: sequence_transformation
    input_type: list_of_integers
    output_type: list_of_integers
    sequence_length: 12
    elements:
      - type: background
        value: 0
      - type: pivot_element
        value: 2
        behavior: remains in its original position
      - type: movable_elements
        value: non-zero integers other than 2
        behavior: position is reflected across the pivot element
    processing:
      - identify_pivot: find the index 'p2' of the element '2'
      - identify_segments: find contiguous sequences of movable_elements
      - reflect_segments:
          for each segment from index 'start' to 'end':
            calculate new start index 'start_out' = 2 * p2 - end
            place the segment's numbers starting at 'start_out' in the output
      - construct_output: start with a sequence of zeros, place the pivot element at 'p2', then place the reflected segments.
    constraints:
      - exactly one element with value 2 exists in the input.
      - output sequence has the same length as the input sequence.
      - reflection preserves the order of elements within a segment.
      - reflected segments might overlap if input segments are close to the pivot; the problem description doesn't explicitly state how overlaps are handled, but examples suggest later segments (in terms of original index) overwrite earlier ones if target indices conflict. However, no overlaps occur in the provided examples.
    ```


*   **Natural Language Program:**
    1.  Initialize an output sequence of the same length as the input, filled with zeros.
    2.  Find the index `p2` of the number `2` in the input sequence. Place the number `2` at index `p2` in the output sequence.
    3.  Iterate through the input sequence to identify contiguous segments of non-zero numbers *other than* the number `2`.
    4.  For each identified segment:
        a.  Note the numbers in the segment and their order.
        b.  Note the starting index (`start`) and ending index (`end`) of the segment in the input sequence.
        c.  Calculate the starting index (`start_out`) for this segment in the output sequence using the formula: `start_out = 2 * p2 - end`.
        d.  Place the noted numbers from the segment into the output sequence, starting at index `start_out`, preserving their original relative order.
    5.  Return the final output sequence.
```python
import collections

"""
Transforms a sequence of 12 integers based on a reflection rule centered around the number 2.

1. Initializes an output sequence of length 12 with all zeros.
2. Finds the index 'p2' of the number 2 in the input sequence.
3. Places the number 2 at index 'p2' in the output sequence.
4. Identifies contiguous segments of non-zero numbers (excluding 2) in the input sequence.
5. For each segment:
   a. Determines its numbers, start index ('start'), and end index ('end').
   b. Calculates the new starting index ('start_out') for the segment in the output sequence using the formula: start_out = 2 * p2 - end.
   c. Places the segment's numbers into the output sequence starting at 'start_out', preserving their original order.
6. Returns the resulting output sequence.
"""

def find_pivot_index(sequence, pivot_value=2):
    """Finds the index of the pivot element."""
    try:
        return sequence.index(pivot_value)
    except ValueError:
        raise ValueError(f"Pivot value {pivot_value} not found in the sequence.")

def find_segments(sequence, pivot_value=2, ignore_value=0):
    """Identifies contiguous segments of non-zero, non-pivot numbers."""
    segments = []
    current_segment = []
    start_index = -1

    for i, value in enumerate(sequence):
        if value != ignore_value and value != pivot_value:
            # Start or continue a segment
            if start_index == -1:
                start_index = i
            current_segment.append(value)
        else:
            # End of a segment (or non-segment element)
            if current_segment:
                end_index = i - 1
                segments.append({
                    "values": list(current_segment), # Make a copy
                    "start": start_index,
                    "end": end_index
                })
                current_segment = []
                start_index = -1

    # Handle segment extending to the end of the sequence
    if current_segment:
        end_index = len(sequence) - 1
        segments.append({
            "values": list(current_segment),
            "start": start_index,
            "end": end_index
        })

    return segments

def transform(input_sequence):
    """
    Applies the reflection transformation to the input sequence.
    """
    n = len(input_sequence)
    if n != 12:
        # Or handle dynamically if length isn't fixed
        print(f"Warning: Input sequence length is {n}, expected 12.")

    # Initialize output_sequence with zeros
    output_sequence = [0] * n

    # Find the index of the pivot element '2'
    try:
        pivot_index = find_pivot_index(input_sequence, 2)
    except ValueError as e:
        print(f"Error: {e}")
        return output_sequence # Or handle error differently

    # Place the pivot element '2' in the output
    if 0 <= pivot_index < n:
         output_sequence[pivot_index] = 2
    else:
        print(f"Warning: Pivot index {pivot_index} is out of bounds for length {n}.")


    # Find all non-zero, non-pivot segments
    segments = find_segments(input_sequence, 2, 0)

    # Reflect and place each segment
    for segment in segments:
        segment_values = segment["values"]
        segment_end = segment["end"]
        segment_len = len(segment_values)

        # Calculate the starting index for the reflected segment
        # The reflection point is the pivot index p2.
        # The end of the input segment (segment_end) maps to the start
        # of the output segment (start_out).
        # The distance from segment_end to p2 is (p2 - segment_end).
        # The output start should be the same distance on the other side:
        # start_out = p2 + (p2 - segment_end) = 2 * p2 - segment_end
        start_out = 2 * pivot_index - segment_end

        # Place the segment's values into the output sequence
        for i in range(segment_len):
            output_index = start_out + i
            # Ensure the output index is within the bounds
            if 0 <= output_index < n:
                output_sequence[output_index] = segment_values[i]
            else:
                 # This case doesn't occur in the examples, but good to acknowledge
                 print(f"Warning: Calculated output index {output_index} is out of bounds.")


    return output_sequence

```
