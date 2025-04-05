*   **Perception of Elements:** The input and output are 1D sequences (arrays) of single digits. The digit '0' appears frequently and seems to represent empty space or background. The digit '2' appears exactly once in each sequence and acts as a reference point or pivot. Other non-zero digits ('5', '6', '7', '8', '9') form contiguous blocks. The transformation involves the potential movement (shifting) of one such block relative to the '2'.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - element: sequence
        properties:
          - type: 1D array of digits
          - contains_pivot: true
      - element: digit_0
        properties:
          - role: background/empty_space
          - condition_for_shift: must be adjacent to a block on the side away from the pivot
      - element: digit_2
        properties:
          - role: pivot/reference_point
          - cardinality: exactly one per sequence
          - determines_shift_direction: true
      - element: non_zero_digit_block
        properties:
          - type: contiguous sequence of identical non-zero digits (e.g., 5 5 5)
          - can_be_subject_to_action: true
    actions:
      - action: shift_block
        properties:
          - target: non_zero_digit_block
          - direction: towards_pivot ('2')
          - magnitude: one position
          - condition: block must be adjacent to a '0' on the side away from the pivot
          - effect_on_block: moves one position towards pivot
          - effect_on_adjacent_0: replaced by the digit from the moving block
          - effect_on_original_end_of_block: the cell at the original trailing edge (leftmost for right shift, rightmost for left shift) becomes '0'
          - cardinality: at most one shift per transformation
    relationships:
      - relationship: position_relative_to_pivot
        between: [non_zero_digit_block, digit_2]
        properties:
          - determines if a potential shift is leftward or rightward
      - relationship: adjacency
        between: [non_zero_digit_block, digit_0]
        properties:
          - required condition for shift (on the side opposite the pivot)
    invariants:
      - The digit '2' remains in its original position.
      - Digits not part of the shifted block and not the replaced '0' remain in their original positions.
      - The length of the sequence remains constant.
      - Only one block shifts per transformation.
    ```


*   **Natural Language Program:**
    1.  Identify the position of the unique digit '2' in the input sequence.
    2.  Scan the sequence to find all contiguous blocks of identical non-zero digits.
    3.  For each block found:
        a.  Determine if the block is located entirely to the left or entirely to the right of the '2'.
        b.  **If the block is to the right of '2':** Check if the cell immediately preceding the block contains a '0'. If it does, this block is the target for shifting.
        c.  **If the block is to the left of '2':** Check if the cell immediately following the block contains a '0'. If it does, this block is the target for shifting.
    4.  If a target block for shifting was identified:
        a.  **If the target block was to the right of '2' (and preceded by '0'):** Create the output sequence by copying the input, then change the '0' immediately before the block to the digit of the block, and change the last digit of the original block position to '0'.
        b.  **If the target block was to the left of '2' (and followed by '0'):** Create the output sequence by copying the input, then change the '0' immediately after the block to the digit of the block, and change the first digit of the original block position to '0'.
    5.  If no target block for shifting was identified (either no blocks exist, or none meet the adjacency-to-'0' condition), the output sequence is identical to the input sequence.