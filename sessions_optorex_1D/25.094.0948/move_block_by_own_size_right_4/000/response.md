*   **Perception:** The task involves manipulating sequences of integers. Each input sequence contains a single contiguous block of identical non-zero integers, surrounded by zeros. The output sequence is generated by shifting this block of non-zero integers to the right. The magnitude of the shift appears to be directly related to the number of elements in the non-zero block.

*   **Facts:**
    
```yaml
    task_type: sequence_manipulation
    input_type: list_of_integers
    output_type: list_of_integers
    input_features:
      - contains_zeros: true
      - contains_non_zeros: true
      - single_contiguous_block_of_identical_non_zeros: true
    output_features:
      - preserves_length: true
      - preserves_non_zero_values: true
      - modifies_positions: true
    transformation:
      - action: identify_block
        target: contiguous block of identical non-zero integers
        properties:
          - start_index
          - end_index
          - value
          - length (calculated as end_index - start_index + 1)
      - action: calculate_shift
        basis: length of the identified block
        result: shift_amount (equal to block length)
      - action: shift_block
        direction: right
        amount: shift_amount
      - action: construct_output
        elements:
          - original non-zero block placed at new position (start_index + shift_amount)
          - zeros filling all other positions
    relationships:
      - shift_amount == length of the non-zero block
      - new_start_index == old_start_index + shift_amount
    ```


*   **Natural Language Program:**
    1.  Scan the input list to find the first contiguous block of identical non-zero numbers. Record its starting index, ending index, and the value of the numbers in the block.
    2.  Calculate the length of this block (number of elements in it).
    3.  Create a new list of the same size as the input list, initially filled with zeros.
    4.  Calculate the new starting index for the block in the output list by adding the block's length to its original starting index.
    5.  Copy the block of non-zero numbers from the input list into the new list, starting at the calculated new starting index.
    6.  Return the new list.