*   **Perception of Elements:**
    *   The input and output are sequences (lists or arrays) of 12 integers.
    *   Each sequence contains mostly zeros (0).
    *   There is a single contiguous block of identical non-zero digits within each input sequence. The value of the digit varies (4, 8, 2, 9, 6). The length of the block also varies (1, 2, or 3 digits).
    *   The output sequence is derived from the input sequence by moving the non-zero block.

*   **YAML Facts:**
    
```yaml
    task_description: "Shift a contiguous block of identical non-zero digits within a sequence."
    elements:
      - name: sequence
        type: list_of_integers
        length: 12
        properties:
          - contains mostly zeros
          - contains a single contiguous block of identical non-zero digits
      - name: zero
        type: integer
        value: 0
        role: background filler
      - name: non_zero_block
        type: list_of_integers
        properties:
          - contains identical digits (value > 0)
          - contiguous within the main sequence
          - variable length
          - variable digit value
        location:
          - defined by start_index and end_index in the input sequence
    action:
      - name: shift_right
        target: non_zero_block
        parameter:
          - distance: 2 positions
    relationship:
      - input_sequence and output_sequence have the same length (12).
      - output_sequence contains the same non_zero_block as the input_sequence.
      - The position of the non_zero_block changes from input to output.
      - The positions originally occupied by the non_zero_block in the input become zeros in the output.
      - The positions to the left and right of the block (which are zeros) effectively shift to accommodate the moved block.
    transformation:
      - Identify the start and end indices of the non_zero_block in the input.
      - Calculate the new start index by adding 2 to the original start index.
      - Construct the output sequence by placing the non_zero_block at the new start index, filling all other positions with zeros.

    ```


*   **Natural Language Program:**
    1.  Parse the input string into a list of 12 integers.
    2.  Iterate through the input list to find the first non-zero integer. Record its value and its index (start\_index).
    3.  Continue iterating from the start\_index to find the end of the contiguous block of the same non-zero integer. Record the index of the last element in the block (end\_index).
    4.  Create a new list of 12 integers, initialized with all zeros.
    5.  Calculate the new starting index for the block by adding 2 to the original start\_index.
    6.  Copy the non-zero block (from original start\_index to end\_index) from the input list into the new list, starting at the calculated new starting index.
    7.  Convert the new list of integers back into a space-separated string for the output.