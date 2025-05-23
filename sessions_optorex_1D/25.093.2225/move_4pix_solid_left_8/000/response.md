*   **Perception**: The task involves manipulating sequences of 12 digits. Each input sequence contains a single contiguous block of identical non-zero digits, surrounded by zeros. The output sequence is generated by shifting this non-zero block exactly 4 positions to the left. The positions vacated by the shift, as well as the original positions of the leading zeros (up to the new start of the block), are filled with zeros. The length of the sequence remains 12.

*   **Facts**:
    
```yaml
    task_elements:
      - item: sequence
        properties:
          - type: list of digits
          - length: 12
          - content: primarily zeros with one contiguous block of identical non-zero digits
      - item: block
        properties:
          - type: contiguous sub-sequence
          - content: identical non-zero digits (e.g., 7, 6, 1)
          - location: defined by start and end indices within the sequence
        relationships:
          - part_of: sequence
      - item: zero
        properties:
          - type: digit
          - value: 0
          - role: background/filler
      - item: non_zero_digit
        properties:
          - type: digit
          - value: 1, 6, or 7 (based on examples)
          - role: constitutes the block
    transformation:
      - action: identify
        target: block
        details: Find the start index, end index, and value of the non-zero block in the input sequence.
      - action: calculate_new_position
        target: block
        details: Subtract 4 from the original start and end indices to determine the new position.
      - action: construct_output
        details:
          - Create a new sequence of 12 zeros.
          - Place the identified block into the new sequence at the calculated new position.
    constraints:
      - The input sequence length is always 12.
      - There is exactly one contiguous block of identical non-zero digits in the input.
      - The shift amount is consistently 4 positions to the left.
    ```


*   **Natural Language Program**:
    1.  Read the input sequence of 12 digits.
    2.  Identify the contiguous block of identical non-zero digits. Record its value, its start index, and its end index in the input sequence.
    3.  Create a new output sequence of 12 zeros.
    4.  Calculate the new start index for the block by subtracting 4 from its original start index.
    5.  Calculate the new end index for the block by subtracting 4 from its original end index.
    6.  Copy the identified block (using its recorded value) into the output sequence, starting at the calculated new start index and ending at the calculated new end index.
    7.  Return the modified output sequence.