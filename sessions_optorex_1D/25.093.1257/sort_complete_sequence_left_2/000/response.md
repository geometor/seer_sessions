*   **Perception of Task Elements:**
    *   The input and output are sequences of 12 integers.
    *   The inputs generally start with four zeros (`0 0 0 0`).
    *   Following the initial zeros, there is typically a non-zero digit (e.g., 1, 2, 3, 9) that appears frequently in the rest of the sequence. Let's call this the 'dominant digit' (`X`).
    *   The transformation seems to involve rearranging or correcting the sequence based on this dominant digit `X`.
    *   In some cases (train\_1, train\_5), the input sequence is identical to the output sequence. These specific sequences follow the pattern `0 0 0 0 X X X 0 X X 0 X`.
    *   In other cases, the input sequence deviates from this pattern, and the output sequence is always transformed *into* this pattern: `0 0 0 0 X X X 0 X X 0 X`, using the dominant digit `X` identified from the input.
    *   The dominant digit `X` consistently appears at index 4 of the input sequence.

*   **Facts:**
    
```yaml
    objects:
      - name: input_sequence
        properties:
          - type: list of integers
          - length: 12
          - structure: Typically starts with [0, 0, 0, 0], followed by a mix of 0s and a dominant non-zero digit (X).
          - dominant_digit_index: 4
      - name: output_sequence
        properties:
          - type: list of integers
          - length: 12
          - structure: Always follows the pattern [0, 0, 0, 0, X, X, X, 0, X, X, 0, X]
      - name: dominant_digit (X)
        properties:
          - type: integer
          - value: Determined from input_sequence[4]
      - name: target_pattern
        properties:
          - type: list of integers
          - structure: [0, 0, 0, 0, X, X, X, 0, X, X, 0, X]
          - relationship: The output_sequence always matches this pattern.
    actions:
      - name: identify_dominant_digit
        inputs: [input_sequence]
        outputs: [dominant_digit]
        description: Extract the integer value at index 4 of the input sequence.
      - name: construct_target_sequence
        inputs: [dominant_digit]
        outputs: [output_sequence]
        description: Create a new 12-element sequence following the target_pattern using the identified dominant_digit.
    relationships:
      - The output_sequence is derived from the input_sequence by first identifying the dominant_digit (X) at input_sequence[4] and then constructing the target_pattern sequence using that digit X.
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of 12 integers.
    2.  Identify the dominant non-zero digit `X` by taking the value at index 4 of the input sequence.
    3.  Construct a new sequence of 12 integers according to the fixed pattern: `[0, 0, 0, 0, X, X, X, 0, X, X, 0, X]`, using the value of `X` determined in the previous step.
    4.  Return the newly constructed sequence as the output.