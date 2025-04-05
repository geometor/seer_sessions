*   **Perception of Elements:**
    *   The inputs and outputs are sequences of single-digit integers, represented as space-separated strings.
    *   All sequences (input and output) have the same length (12 elements).
    *   The core content consists of a contiguous block of digits that starts with the first non-zero digit and ends with the last non-zero digit in the input sequence. This block may contain internal zeros.
    *   The remaining elements are zeros, appearing before (leading) and after (trailing) the core block.
    *   The transformation involves repositioning the core block within the sequence.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - item: sequence
        properties:
          - type: list of integers
          - length: 12
          - representation: space-separated string
      - item: core_block
        properties:
          - type: sub-sequence
          - definition: contiguous elements from the first non-zero digit to the last non-zero digit (inclusive)
          - contains: digits (can include internal zeros)
      - item: surrounding_zeros
        properties:
          - type: sequence elements
          - value: 0
          - position: before (leading) and after (trailing) the core_block
    transformation:
      action: shift_left
      target: core_block
      details:
        - identify the start index (first_nz) of the core_block in the input
        - calculate the new start index (new_start) for the core_block in the output: new_start = max(0, first_nz - 4)
        - place the core_block at the new_start index in an output sequence of the same length, initialized with zeros
        - the remaining positions in the output sequence are filled with zeros, effectively redistributing the original leading and trailing zeros.
    edge_case:
      - condition: input sequence contains only zeros
        output: return the input sequence unchanged
    ```


*   **Natural Language Program:**
    1.  Read the input sequence of 12 digits.
    2.  Find the index of the first non-zero digit (`first_nz`).
    3.  If no non-zero digit is found (the sequence is all zeros), return the original sequence.
    4.  Find the index of the last non-zero digit (`last_nz`).
    5.  Extract the sub-sequence (the "core block") from `first_nz` to `last_nz` (inclusive).
    6.  Calculate the target starting index for the core block in the output sequence: `new_start = max(0, first_nz - 4)`.
    7.  Create a new sequence of 12 zeros.
    8.  Place the extracted core block into the new sequence, starting at the calculated `new_start` index.
    9.  Return the resulting sequence.