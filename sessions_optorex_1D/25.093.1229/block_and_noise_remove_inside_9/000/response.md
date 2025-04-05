*   **Perception:** The task involves transforming a sequence of single-digit integers. The core transformation seems to focus on a contiguous sub-sequence defined by the first and last non-zero elements. Within this sub-sequence, all elements are replaced by the single most frequent digit found within that original sub-sequence. Elements outside this sub-sequence (leading and trailing zeros) remain unchanged.

*   **Facts:**
    
```yaml
    task_elements:
      - object: input_sequence
        properties:
          - type: list of integers
          - contains_zeros: boolean (can have leading/trailing zeros)
          - contains_non_zeros: boolean (defines the active segment)
      - object: output_sequence
        properties:
          - type: list of integers
          - derived_from: input_sequence
      - object: active_segment
        properties:
          - type: sub-sequence of input_sequence
          - definition: starts at the first non-zero element, ends at the last non-zero element (inclusive)
          - relation: If no non-zero elements exist, this segment is empty.
      - object: dominant_digit
        properties:
          - type: integer
          - definition: The most frequently occurring digit within the active_segment of the input_sequence.
          - relation: Used to replace all digits within the active_segment bounds in the output_sequence. (Note: Tie-breaking rule is not explicitly defined by examples, but seems consistent with using the most frequent).
    actions:
      - identify_active_segment:
          input: input_sequence
          output: start_index, end_index
          description: Find the indices of the first and last non-zero elements. Handle the case where no non-zero elements exist.
      - find_dominant_digit:
          input: active_segment (sub-sequence from start_index to end_index)
          output: dominant_digit
          description: Calculate the frequency of each digit in the segment and return the digit with the highest frequency.
      - construct_output:
          input: input_sequence, start_index, end_index, dominant_digit
          output: output_sequence
          description: Create the output by concatenating the portion of the input before start_index, followed by dominant_digit repeated (end_index - start_index + 1) times, followed by the portion of the input after end_index. If start_index/end_index are invalid (all zeros input), return the original input sequence.
    ```


*   **Natural Language Program:**
    1.  Read the input sequence of digits.
    2.  Identify the portion of the sequence between the first non-zero digit and the last non-zero digit (inclusive). Call this the "active segment". If there are no non-zero digits, the output is identical to the input; proceed to step 6.
    3.  Analyze the digits within the original active segment (from step 2) to find the digit that appears most frequently. Call this the "dominant digit".
    4.  Create a new sequence, starting with the same digits as the input sequence that appear *before* the active segment.
    5.  Append the dominant digit to the new sequence, repeated as many times as the length of the active segment.
    6.  Append the digits from the input sequence that appear *after* the active segment to the new sequence.
    7.  Return the newly constructed sequence.