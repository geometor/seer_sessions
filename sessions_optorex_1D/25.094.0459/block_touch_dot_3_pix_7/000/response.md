*   **Perception:**
    *   The input and output are sequences (lists) of 12 integers.
    *   The integers seem to represent different types of elements: '0' likely represents empty space, '2' acts as a fixed or special boundary marker, and other digits (1, 4, 5, 6, 9) form contiguous blocks that can move.
    *   The core transformation involves identifying a single contiguous block of identical digits (not '0' or '2'), referred to as the "object block".
    *   This object block potentially swaps its position with an adjacent block of '0's (an "empty block").
    *   The direction of the potential swap is determined by the relative positions of the object block and the number '2'. The object block moves towards the '2' by swapping with the adjacent empty block that lies between it and the '2'.
    *   If the object block is already adjacent to the '2', or if there isn't an adjacent empty block between the object block and the '2', no swap occurs, and the input remains unchanged.
    *   Cases with no single object block (e.g., multiple blocks, or only '0's and '2's) also result in no change.

*   **Facts:**
    
```yaml
    objects:
      - name: sequence
        type: list of integers
        length: 12
      - name: element
        type: integer
        properties:
          - value: 0 (empty space)
          - value: 2 (boundary marker)
          - value: 1, 4, 5, 6, 9 (object components)
      - name: block
        type: contiguous subsequence of identical elements
        properties:
          - value: integer
          - start_index: integer
          - end_index: integer
          - length: integer
        subtypes:
          - name: object_block (value is not 0 or 2)
          - name: empty_block (value is 0)
          - name: boundary_marker (value is 2, length is 1)

    actions:
      - name: find_blocks
        input: sequence
        output: list of blocks (with value, start, end)
      - name: identify_boundary_marker
        input: list of blocks
        output: boundary_marker block (or null)
      - name: identify_object_blocks
        input: list of blocks
        output: list of object_blocks
      - name: identify_adjacent_empty_block
        input: object_block, boundary_marker, list of blocks
        output: adjacent_empty_block (or null) based on direction towards boundary_marker
      - name: swap_blocks
        input: block1, block2, sequence
        output: modified sequence
      - name: reconstruct_sequence
        input: list of blocks
        output: sequence

    relationships:
      - type: position
        between: [object_block, boundary_marker]
        value: [left_of, right_of]
      - type: adjacency
        between: [block, block]
        value: [immediately_left_of, immediately_right_of]
    ```


*   **Natural Language Program:**
    1.  Parse the input sequence into a list of consecutive blocks, recording the value, start index, and end index for each block.
    2.  Identify the block containing the value '2' (the boundary marker). If not found, return the original sequence.
    3.  Identify all object blocks (blocks with values other than '0' or '2').
    4.  If the number of object blocks is not exactly one, return the original sequence. Let the single object block be `B_obj`.
    5.  Determine if `B_obj` is to the left or right of the boundary marker '2'.
    6.  **If `B_obj` is to the left of '2':**
        *   Check if the block immediately to the right of `B_obj` exists and is an empty block (value '0'). Let this be `B_empty`.
        *   If such a `B_empty` exists, swap the positions of `B_obj` and `B_empty` in the sequence representation.
        *   Otherwise, do nothing.
    7.  **If `B_obj` is to the right of '2':**
        *   Check if the block immediately to the left of `B_obj` exists and is an empty block (value '0'). Let this be `B_empty`.
        *   If such a `B_empty` exists, swap the positions of `B_obj` and `B_empty` in the sequence representation.
        *   Otherwise, do nothing.
    8.  Reconstruct and return the modified sequence based on the potentially swapped block order.