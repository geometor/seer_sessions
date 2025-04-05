*   **Perception of Task Elements:**
    *   The input and output are both sequences (or lists) of integers.
    *   Each sequence consistently contains 12 integers.
    *   The integers within the sequence appear to be single digits (0-9).
    *   The transformation preserves the exact set of numbers present in the input, merely rearranging their order.
    *   Comparing the positions of numbers between input and output suggests a consistent positional shift or rotation. Specifically, the elements from the beginning of the input sequence appear at the end of the output sequence, and the elements from later in the input sequence appear earlier in the output sequence. This pattern strongly indicates a cyclic shift or rotation operation.
    *   Observing `train_1`: `0 0 0 0 0 0 0 0 0 6 7 6` -> `0 0 0 0 0 6 7 6 0 0 0 0`. The first four elements `0 0 0 0` seem to have moved to the end.
    *   Observing `train_2`: `3 6 4 4 0 0 0 0 0 0 0 5` -> `0 0 0 0 0 0 0 5 3 6 4 4`. The first four elements `3 6 4 4` have moved to the end.
    *   This pattern holds across all examples, confirming a left cyclic shift by 4 positions.

*   **Facts:**
    
```yaml
    task_elements:
      - object: sequence
        properties:
          - type: list_of_integers
          - length: 12
          - item_range: 0-9 (observed)
    transformation:
      action: cyclic_shift
      direction: left
      amount: 4
      input: input_sequence
      output: output_sequence
    relationship:
      - The output sequence is the result of applying a 4-position left cyclic shift to the input sequence.
    ```


*   **Natural Language Program:**
    1.  Take the input sequence of 12 integers.
    2.  Perform a cyclic left shift (rotation) on the sequence by 4 positions.
    3.  The resulting sequence is the output.