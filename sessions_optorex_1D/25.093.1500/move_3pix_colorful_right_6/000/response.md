*   **Perception of Task Elements:**
    *   The input and output are both sequences (lists) of integers.
    *   All provided examples have sequences of length 12.
    *   The core transformation involves relocating a contiguous block of non-zero numbers within the sequence.
    *   The relative order and values of the non-zero numbers are preserved.
    *   The block of non-zero numbers is consistently shifted 3 positions to the right.
    *   The output sequence is padded with zeros in the positions not occupied by the shifted block.
    *   The length of the sequence remains constant (12).

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: input_list
        properties:
          - type: list
          - contains: integers
          - length: fixed (e.g., 12)
      - object: output_list
        properties:
          - type: list
          - contains: integers
          - length: same as input_list
          - derived_from: input_list
      - object: non_zero_block
        properties:
          - type: sublist
          - derived_from: input_list
          - content: sequence of elements starting from the first non-zero element to the last non-zero element in the input_list
          - relative_order: preserved from input_list
          - values: preserved from input_list
      - object: zero_padding
        properties:
          - value: 0
          - role: fills positions in output_list not occupied by the non_zero_block
    actions:
      - name: identify_block
        input: input_list
        output: non_zero_block, start_index, end_index
        description: Find the first and last non-zero elements in the input_list to define the block and its original indices. If no non-zero elements exist, the block is empty.
      - name: calculate_new_position
        input: start_index, end_index, shift_amount (constant: 3)
        output: new_start_index, new_end_index
        description: Add the shift_amount to the original start and end indices.
      - name: construct_output
        input: non_zero_block, new_start_index, new_end_index, list_length
        output: output_list
        description: Create a new list of the specified length, filled initially with zeros. Place the non_zero_block at the calculated new_start_index. Ensure indices stay within bounds.
    relationships:
      - type: transformation
        from: input_list
        to: output_list
        rule: shift non_zero_block right by 3 positions
      - type: positional_shift
        object: non_zero_block
        direction: right
        amount: 3 positions
    constants:
      - shift_amount: 3
      - padding_value: 0
    ```


*   **Natural Language Program:**
    1.  Receive the input list of integers.
    2.  Initialize an output list of the same length as the input list, filled entirely with zeros.
    3.  Identify the index of the first non-zero element in the input list (`first_nz_index`). If no non-zero elements exist, the output list remains all zeros; proceed to step 7.
    4.  Identify the index of the last non-zero element in the input list (`last_nz_index`).
    5.  Extract the sublist (the "block") from the input list starting at `first_nz_index` and ending at `last_nz_index` (inclusive).
    6.  Place this extracted block into the output list, starting at index `first_nz_index + 3`. Ensure the elements are placed correctly relative to this new starting position.
    7.  Return the constructed output list.