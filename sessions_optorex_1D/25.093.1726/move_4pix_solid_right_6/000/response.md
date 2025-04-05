*   **Perception:** The task involves transforming a sequence of 12 numbers. The input sequence typically contains a contiguous block of identical non-zero digits, surrounded by zeros. The output sequence contains the same block of non-zero digits, but shifted 4 positions to the right. The remaining positions in the output sequence are filled with zeros. The length of the sequence remains constant at 12.

*   **Facts:**
    
```yaml
    objects:
      - input_sequence:
          type: list of integers
          length: 12
          properties:
            - contains a contiguous block of non-zero identical digits
            - remaining elements are zero
      - output_sequence:
          type: list of integers
          length: 12
          properties:
            - contains the same contiguous block of non-zero digits as the input
            - remaining elements are zero
      - non_zero_block:
          type: sub-sequence of integers
          properties:
            - consists of identical non-zero digits
            - extracted from input_sequence
      - zero:
          type: integer
          value: 0
    actions:
      - identify: locate non-zero elements in the input_sequence
      - shift: move elements to new positions
      - pad: fill positions with zeros
    relationships:
      - transformation: input_sequence is transformed into output_sequence
      - shifting_rule: each non-zero element at index `i` in the input_sequence is moved to index `i + 4` in the output_sequence
      - boundary_condition: if `i + 4` exceeds the sequence length (index 11), the element is discarded
      - padding_rule: positions in the output_sequence not filled by shifted non-zero elements are filled with zeros
    ```


*   **Natural Language Program:**
    1.  Create a new sequence of 12 elements, initialized with zeros.
    2.  Iterate through the input sequence from the first element (index 0) to the last element (index 11). Let the current index be `i`.
    3.  If the element at index `i` in the input sequence is not zero:
        a.  Calculate the target index `j` by adding 4 to the current index `i` (`j = i + 4`).
        b.  Check if the target index `j` is within the valid range of indices for the sequence (0 to 11).
        c.  If `j` is within the valid range, copy the non-zero element from the input sequence at index `i` to the new sequence at index `j`.
    4.  The final new sequence is the output.