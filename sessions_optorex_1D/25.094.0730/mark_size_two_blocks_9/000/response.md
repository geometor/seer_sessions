*   **Perception of Task Elements:**
    *   The input and output are sequences (lists or arrays) of single-digit integers.
    *   Input sequences contain only 0s and 1s.
    *   Output sequences contain 0s, 1s, and 3s.
    *   The transformation modifies some of the 0s in the input sequence to 3s in the output sequence based on their proximity to specific patterns of 1s.
    *   The lengths of the input and output sequences are always identical.
    *   The positions of the 1s remain unchanged from input to output.
    *   The change from 0 to 3 seems conditional on the 0 being adjacent to a block of exactly two consecutive 1s.

*   **Facts:**
    
```yaml
    objects:
      - sequence:
          description: A list of integers.
          properties:
            - elements: Integers (0, 1 for input; 0, 1, 3 for output).
            - length: The number of elements in the sequence.
      - number:
          description: An integer element within the sequence.
          properties:
            - value: The integer itself (0, 1, or 3).
            - position: The index of the number within the sequence.
      - block:
          description: A contiguous sub-sequence of identical numbers.
          properties:
            - type: Consists of the number 1.
            - length: The count of consecutive 1s.
            - location: Starting and ending indices within the sequence.
    relationships:
      - adjacency:
          description: A number is directly next to a block (either immediately preceding its start index or immediately following its end index).
          applies_to: [number, block]
    actions:
      - identify_blocks:
          description: Find all contiguous blocks of the number 1 within the input sequence.
          constraints: The block must have a specific length (exactly 2).
      - check_adjacency:
          description: For each identified block of two 1s, check if the numbers at adjacent positions are 0.
      - modify_number:
          description: Change the value of an adjacent 0 to 3.
          condition: The 0 must be adjacent to a block of exactly two 1s.
          target: The output sequence at the corresponding position.
      - copy_number:
          description: If a number is not modified, copy its value from the input to the output at the same position.
          condition: Applies to all 1s and any 0s not meeting the modification condition.
          target: The output sequence.
    ```


*   **Natural Language Program:**
    1.  Iterate through the input sequence to identify all contiguous blocks consisting of exactly two 1s (i.e., sub-sequences `1 1`). Record the starting and ending indices of each such block.
    2.  Create a copy of the input sequence to serve as the initial output sequence.
    3.  For each identified block of two 1s found in step 1:
        a.  Check the element immediately *before* the block's starting index (if it exists within the sequence bounds). If this element is a 0, change its value to 3 in the output sequence.
        b.  Check the element immediately *after* the block's ending index (if it exists within the sequence bounds). If this element is a 0, change its value to 3 in the output sequence.
    4.  Return the modified sequence as the final output.