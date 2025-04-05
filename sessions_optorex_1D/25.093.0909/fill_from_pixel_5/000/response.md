*   **Perception of Elements:**
    *   The task operates on sequences of 12 digits.
    *   The core elements are digits, specifically distinguishing between zero (`0`) and non-zero digits (1-9).
    *   The transformation involves changing some zero digits to non-zero values based on their neighbors.
    *   Positional adjacency is crucial.
    *   Contiguous blocks of identical digits (both zeros and non-zeros) play a role. Specifically, whether a non-zero digit is part of a repeating block or stands alone seems important.

*   **YAML Facts:**
    ```
yaml
    elements:
      - type: sequence
        description: A fixed-length sequence of 12 digits (0-9).
        length: 12
      - type: digit
        value_range: 0-9
        properties:
          - is_zero: boolean (true if value is 0)
          - is_non_zero: boolean (true if value is 1-9)

    objects:
      - name: input_sequence
        type: sequence
      - name: output_sequence
        type: sequence
      - name: non_zero_digit
        type: digit
        properties:
          - is_non_zero: true
      - name: single_non_zero_digit
        type: non_zero_digit
        description: A non-zero digit whose immediate left and right neighbors (if they exist within the sequence boundaries) have different values from it.
      - name: zero_digit
        type: digit
        properties:
          - is_zero: true
      - name: contiguous_zero_block
        type: sequence
        description: A subsequence consisting only of one or more adjacent zero digits.

    relationships:
      - type: adjacency
        description: The property of digits being immediately next to each other (left or right) in the sequence.
      - type: context
        description: The value of neighboring digits determines if a non-zero digit is "single".
      - type: propagation
        description: The value of a "single" non-zero digit propagates into adjacent blocks of zeros.

    actions:
      - name: identify_singles
        description: Iterate through the input sequence to find non-zero digits that are not identical to their immediate left or right neighbors.
        input: input_sequence
        output: list of indices and values of single non-zero digits
      - name: fill_adjacent_zeros
        description: For each single non-zero digit, find contiguous blocks of zeros immediately to its left and right, and replace those zeros with the single digit's value.
        input: index and value of a single non-zero digit, sequence (initially input, progressively modified)
        output: modified sequence
    