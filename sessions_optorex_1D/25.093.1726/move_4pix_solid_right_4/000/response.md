*   **Perception of Task Elements:**
    *   The input and output are sequences (lists) of integers.
    *   Each sequence has a fixed length (12 in all examples).
    *   The sequences primarily contain zeros.
    *   Each input sequence contains exactly one contiguous block of identical non-zero integers (this block can be of length 1).
    *   The output sequence is derived from the input by moving this non-zero block.
    *   The movement is a shift to the right by a fixed number of positions.
    *   The positions previously occupied by the non-zero block become zeros in the output.
    *   The amount of the rightward shift appears to be constant across all examples (+4 positions).

*   **YAML Documentation of Facts:**
    
```yaml
    task_description: Shift a block of non-zero numbers within a sequence.
    elements:
      - object: sequence
        description: A list of integers representing the input and output data.
        properties:
          - length: Fixed (e.g., 12 in the examples)
          - content: Primarily zeros with one contiguous block of identical non-zero integers.
      - object: non_zero_block
        description: A contiguous sub-sequence of identical non-zero integers within the input sequence.
        properties:
          - value: The non-zero integer value.
          - start_index: The starting position (0-based) of the block in the input sequence.
          - end_index: The ending position (0-based) of the block in the input sequence.
          - length: The number of elements in the block.
      - object: zero
        description: The background element (integer 0).
    action:
      - name: shift_block_right
        description: Moves the non_zero_block to a new position in the sequence.
        parameters:
          - shift_amount: The number of positions to shift right (seems fixed at 4).
    relationships:
      - The output sequence is generated from the input sequence by applying the shift_block_right action.
      - The position of the non_zero_block in the output is determined by its start_index in the input plus the shift_amount.
      - The elements in the output sequence at the original position of the non_zero_block are replaced with zeros.
      - The length and the non-zero value of the block remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Initialize an output sequence of the same length as the input sequence, filled entirely with zeros.
    2.  Scan the input sequence to identify the contiguous block of identical non-zero numbers. Determine its value, its starting index, and its ending index.
    3.  Calculate the new starting index for the block in the output sequence by adding 4 to the original starting index found in step 2.
    4.  Copy the identified non-zero block (using its value and length) into the output sequence, starting at the calculated new starting index.
    5.  Return the modified output sequence.