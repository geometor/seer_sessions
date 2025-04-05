*   **Perception of Task Elements:**
    *   The input and output are sequences of single-digit integers.
    *   The length of the input sequence is preserved in the output sequence.
    *   The transformation involves reversing a specific portion of the input sequence.
    *   Leading and trailing zeros in the input sequence appear to remain in their original positions in the output.
    *   The core operation targets the sub-sequence of digits located between the first non-zero digit and the last non-zero digit (inclusive). If the sequence contains no non-zero digits, or only one, it remains unchanged (although this case isn't explicitly shown, it's a logical consequence). If the sequence contains no zeros at the start or end, the entire sequence is reversed.

*   **Facts:**
    
```yaml
    task_elements:
      - object: sequence
        properties:
          - type: list_of_integers
          - length: variable
      - object: digit
        properties:
          - value: integer (0-9)
          - position: index_in_sequence
          - attribute: is_zero (boolean)
          - attribute: is_non_zero (boolean)
      - object: sub_sequence
        properties:
          - type: list_of_integers
          - location: delimited by first and last non-zero digits
          - relationship: part_of the main sequence
        actions:
          - extract
          - reverse
      - object: padding_zeros
        properties:
          - value: 0
          - location: leading or trailing the non-zero sub_sequence
        actions:
          - identify
          - preserve_position
    transformation:
      - action: identify_boundaries
        inputs: input_sequence
        outputs: start_index (first non-zero), end_index (last non-zero)
        description: Find the index of the first non-zero digit and the last non-zero digit. Handle cases with no non-zero digits.
      - action: extract_subsequence
        inputs: input_sequence, start_index, end_index
        outputs: target_subsequence
        description: Get the part of the sequence from start_index to end_index (inclusive).
      - action: reverse_subsequence
        inputs: target_subsequence
        outputs: reversed_subsequence
        description: Reverse the order of elements in the target_subsequence.
      - action: construct_output
        inputs: leading_zeros, reversed_subsequence, trailing_zeros
        outputs: output_sequence
        description: Combine the leading zeros (elements before start_index), the reversed_subsequence, and the trailing zeros (elements after end_index) to form the final output sequence.
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of digits.
    2.  Identify the index of the first non-zero digit in the sequence. If no non-zero digit exists, the sequence remains unchanged; return the original input sequence.
    3.  Identify the index of the last non-zero digit in the sequence.
    4.  Define the sub-sequence as the elements from the first non-zero digit's index to the last non-zero digit's index (inclusive).
    5.  Reverse the order of the digits within this identified sub-sequence.
    6.  Construct the output sequence by concatenating:
        *   The sequence of digits before the first non-zero digit (leading zeros, if any).
        *   The reversed sub-sequence.
        *   The sequence of digits after the last non-zero digit (trailing zeros, if any).
    7.  Return the constructed output sequence.