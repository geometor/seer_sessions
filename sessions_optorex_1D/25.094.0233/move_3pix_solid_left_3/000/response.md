*   **Perception of Task Elements:**
    *   The input and output are lists (or arrays) of single-digit integers.
    *   The length of the input and output lists is constant (12 in all examples).
    *   Each input list contains a single contiguous block of identical non-zero numbers, surrounded by zeros.
    *   Each output list also contains a single contiguous block of the same non-zero number as the input, surrounded by zeros.
    *   The length of the non-zero block is preserved from input to output.
    *   The value of the non-zero number is preserved from input to output.
    *   The position of the non-zero block changes between the input and output. Specifically, the block is shifted to the left.
    *   Observing the start index of the block in the input and output across examples reveals a consistent leftward shift of 3 positions.

*   **YAML Facts:**
    
```yaml
    task_type: sequence_transformation
    data_type: list_of_integers
    list_length: 12
    elements:
      - type: zero
        role: background/padding
      - type: non_zero_digit
        role: object/pattern
        properties:
          - contiguity: forms a single block in the input
          - value_preservation: value remains the same in the output
          - length_preservation: block length remains the same in the output
    transformation:
      action: shift_block
      details:
        - object: the contiguous block of non-zero numbers
        - direction: left
        - magnitude: 3 positions
        - behavior:
            - identify the start index of the non-zero block in the input.
            - calculate the target start index in the output by subtracting 3.
            - construct the output list with zeros.
            - place the non-zero block at the target start index in the output list.
    ```


*   **Natural Language Program:**
    1.  Initialize an output list of the same length as the input list, filled with zeros.
    2.  Scan the input list to find the first non-zero element. Record its index (let's call it `start_index`) and its value.
    3.  Determine the length of the contiguous block of this non-zero value starting at `start_index`.
    4.  Calculate the new starting index for the block in the output list by subtracting 3 from `start_index`.
    5.  Copy the contiguous block of non-zero numbers from the input into the output list, starting at the calculated new index.