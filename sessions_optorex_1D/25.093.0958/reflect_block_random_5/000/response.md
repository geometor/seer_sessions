*   **Perception of Task Elements:**
    *   The input and output are sequences (lists) of single-digit integers.
    *   The length of the input sequence is preserved in the output sequence.
    *   The core transformation involves reversing a specific portion of the sequence.
    *   The digits '0' act as delimiters or padding around the segment that is reversed. Zeros outside this core segment remain in their original positions.
    *   The segment to be reversed is the contiguous block containing all non-zero digits, starting from the first non-zero digit and ending with the last non-zero digit in the original sequence.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: sequence
        properties:
          - type: list of integers
          - contains: digits (0-9)
          - length: variable, but consistent between input and output
      - object: non_zero_segment
        properties:
          - type: sub-sequence
          - location: within the main sequence
          - definition: the contiguous block from the first non-zero digit to the last non-zero digit (inclusive)
          - may_be_empty: false (implied by examples, although an all-zero input isn't shown)
        relationships:
          - contained_within: sequence
      - object: zero_padding
        properties:
          - type: sub-sequence(s)
          - value: consists only of the digit 0
          - location: before the first non-zero digit (leading zeros) and after the last non-zero digit (trailing zeros)
        relationships:
          - surrounds: non_zero_segment (potentially empty leading/trailing padding)
    actions:
      - name: identify_segment
        inputs: sequence
        outputs: start_index, end_index (of the non_zero_segment)
        description: Find the index of the first non-zero digit and the index of the last non-zero digit.
      - name: extract_subsequences
        inputs: sequence, start_index, end_index
        outputs: leading_zeros, non_zero_segment, trailing_zeros
        description: Separate the sequence into three parts based on the identified indices.
      - name: reverse_segment
        inputs: non_zero_segment
        outputs: reversed_segment
        description: Reverse the order of the elements within the non_zero_segment.
      - name: reconstruct_sequence
        inputs: leading_zeros, reversed_segment, trailing_zeros
        outputs: output_sequence
        description: Concatenate the leading zeros, the reversed segment, and the trailing zeros to form the final output.
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of digits.
    2.  Identify the index of the first non-zero digit in the sequence. If no non-zero digits exist, return the original sequence.
    3.  Identify the index of the last non-zero digit in the sequence.
    4.  Extract the sub-sequence containing the digits from the first non-zero index up to and including the last non-zero index (the "non-zero segment").
    5.  Extract the sub-sequence of leading zeros (all digits before the first non-zero index).
    6.  Extract the sub-sequence of trailing zeros (all digits after the last non-zero index).
    7.  Reverse the order of the digits within the extracted "non-zero segment".
    8.  Construct the output sequence by concatenating the leading zeros, the reversed non-zero segment, and the trailing zeros in that order.
    9.  Return the constructed output sequence.