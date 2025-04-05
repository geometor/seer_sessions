*   **Perception of Elements:**
    *   The input and output are sequences (lists or arrays) of 12 integers.
    *   The sequences primarily contain the integer 0.
    *   Each input sequence contains a single contiguous block of identical non-zero integers.
    *   The transformation involves moving this non-zero block within the sequence.

*   **YAML Fact Document:**
    
```yaml
    task_elements:
      - name: sequence
        type: list_of_integers
        properties:
          - length: 12
          - contains_zeros: true
          - contains_non_zero_block: true
      - name: zero
        type: integer
        value: 0
        role: background_element
      - name: non_zero_block
        type: list_of_integers
        properties:
          - contiguity: true
          - uniformity: all elements are identical and non-zero
          - variable_length: true
          - variable_value: true (e.g., 2, 6, 5, 9, 4, 1)
          - variable_position: true
    actions:
      - name: identify_block
        input: sequence
        output: non_zero_block_details (value, start_index, end_index)
      - name: shift_block
        input: non_zero_block_details
        parameter: shift_amount (integer)
        output: new_start_index, new_end_index
      - name: construct_output
        input: original_sequence_length, non_zero_block_details, new_start_index, new_end_index
        output: output_sequence
    relationships:
      - type: positional_shift
        element_1: non_zero_block (in input)
        element_2: non_zero_block (in output)
        detail: The start index of the block in the output is exactly 4 greater than the start index of the block in the input.
      - type: replacement
        location: original position of non_zero_block
        new_value: zero
    constants:
      - name: sequence_length
        value: 12
      - name: shift_distance
        value: 4
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of identical non-zero integers within the 12-element input sequence. Note its starting index, ending index, and the value of the integers in the block.
    2.  Create a new output sequence of 12 zeros.
    3.  Calculate the new starting index for the block by adding 4 to the original starting index found in step 1.
    4.  Calculate the new ending index for the block by adding 4 to the original ending index found in step 1.
    5.  Place the identified non-zero block (using the value from step 1) into the output sequence starting at the new starting index and ending at the new ending index calculated in steps 3 and 4.
    6.  Return the modified output sequence.