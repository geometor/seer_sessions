*   **Perception of task elements:**
    *   The input is a sequence of single digits separated by spaces.
    *   The output is also a sequence of single digits separated by spaces, with the same length as the input.
    *   The core transformation involves inserting a '0' into the sequence.
    *   The position of the inserted '0' appears to be related to the position of the first non-zero digit in the input sequence.
    *   Comparing input and output sequences, the output sequence is identical to the input sequence, except a single '0' has been inserted immediately before the first non-zero digit encountered when reading the input from left to right.
    *   If the input starts with one or more zeros, these zeros remain in their original positions, and the new '0' is inserted before the first digit greater than zero.
    *   If the input starts with a non-zero digit, a '0' is inserted at the very beginning of the sequence.

*   **Facts:**
    
```yaml
    objects:
      - name: sequence
        properties:
          - type: list/array of integers (digits 0-9)
          - ordered
      - name: digit
        properties:
          - value: integer (0-9)
          - position: index within the sequence
    actions:
      - name: find_first_non_zero
        inputs:
          - sequence
        outputs:
          - index: position of the first digit > 0
      - name: insert_zero
        inputs:
          - sequence
          - index: position for insertion
        outputs:
          - modified_sequence
    relationships:
      - The insertion point for the '0' is the index returned by 'find_first_non_zero'.
      - The output sequence is the result of inserting a '0' at the determined index in the input sequence.
    ```


*   **Natural Language Program:**
    1.  Read the input sequence of digits.
    2.  Iterate through the sequence from the beginning (left to right) to find the index of the first digit that is not zero.
    3.  Create a new sequence by inserting a '0' digit at that found index within the original sequence.
    4.  Output the modified sequence.