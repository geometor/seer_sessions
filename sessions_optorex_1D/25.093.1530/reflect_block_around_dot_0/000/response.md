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