*   **Perception:**
    *   The input and output are both sequences of integers.
    *   All examples show sequences of length 12.
    *   The numbers themselves are not altered, only their positions.
    *   There appears to be a consistent split point within the input sequence.
    *   The transformation involves moving a segment from the end of the input sequence to the beginning of the output sequence.

*   **Facts:**
    
```yaml
    task_type: sequence transformation
    input_type: list of integers
    output_type: list of integers
    element_type: integer
    input_length: 12 (constant across examples)
    output_length: 12 (constant across examples)
    transformation: rearrangement (cyclic shift)
    properties:
      - object: input_sequence
        attributes:
          - length: 12
      - object: output_sequence
        attributes:
          - length: 12
          - composition: same elements as input_sequence
    actions:
      - name: split
        input: input_sequence
        parameters:
          - split_point: after the 8th element
        outputs:
          - subsequence_1: first 8 elements
          - subsequence_2: last 4 elements
      - name: concatenate
        inputs:
          - subsequence_2
          - subsequence_1
        output: output_sequence
    relationships:
      - The output sequence is formed by placing the last 4 elements of the input sequence at the beginning, followed by the first 8 elements of the input sequence.
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of 12 integers.
    2.  Divide the input sequence into two parts: the first 8 integers (Part A) and the last 4 integers (Part B).
    3.  Create the output sequence by concatenating Part B followed by Part A.