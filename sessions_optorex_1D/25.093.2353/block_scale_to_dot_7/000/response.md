*   **Perception:** The task involves transforming sequences of single-digit integers. The core operation appears to be conditionally replacing sequences of one or more zeros based on the non-zero numbers immediately preceding and succeeding the zero sequence. The specific value used for replacement depends on the value of the succeeding non-zero number. If the succeeding number is `2`, the preceding number is used for replacement; otherwise, the succeeding number is used. Sequences where zeros are not enclosed by non-zero numbers, or sequences without the specific `X 0...0 Y` pattern, remain unchanged.

*   **Facts:**
    
```yaml
    objects:
      - name: sequence
        type: list of integers
        description: Represents the input and output data structure.
      - name: element
        type: integer
        description: An individual number within the sequence.
      - name: zero_block
        type: sub-sequence
        description: A contiguous sequence of one or more '0' elements.
      - name: preceding_neighbor (X)
        type: integer
        description: The non-zero element immediately before a zero_block.
      - name: succeeding_neighbor (Y)
        type: integer
        description: The non-zero element immediately after a zero_block.
    properties:
      - object: element
        name: value
        type: integer (0-9)
      - object: element
        name: position
        type: integer (index)
      - object: element
        name: is_zero
        type: boolean
    relationships:
      - type: adjacency
        description: Defines elements that are next to each other in the sequence.
      - type: boundary
        description: A zero_block is bounded by a preceding_neighbor (X) and a succeeding_neighbor (Y). This forms the pattern X 0...0 Y.
    actions:
      - name: find_pattern
        description: Identify all occurrences of the X 0...0 Y pattern within the sequence.
      - name: determine_fill_value
        description: Based on the value of Y in a found pattern, decide the replacement value. If Y is 2, the value is X. Otherwise, the value is Y.
      - name: replace_zeros
        description: Modify the sequence by replacing the elements in a zero_block with the determined fill_value.

    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of integers.
    2.  Create a mutable copy of the input sequence to serve as the initial output sequence.
    3.  Iterate through the sequence from the second element (index 1) up to, but not including, the last element.
    4.  Identify the start (`i`) of every maximal contiguous block of zeros that is preceded by a non-zero number (`X` at index `i-1`) and followed by a non-zero number (`Y` at index `k+1`, where `k` is the end index of the zero block).
    5.  For each such identified block of zeros (from index `i` to `k`):
        a.  Let `X` be the value at index `i-1`.
        b.  Let `Y` be the value at index `k+1`.
        c.  Determine the value to fill (`fill_value`): if `Y` is equal to `2`, set `fill_value` to `X`; otherwise, set `fill_value` to `Y`.
        d.  Replace all elements in the output sequence from index `i` to `k` (inclusive) with the `fill_value`.
    6.  Ensure that the iteration process correctly handles modifications, perhaps by identifying all necessary changes first and then applying them, or by carefully adjusting the iteration index after a replacement to avoid re-evaluating modified sections incorrectly. A simple approach is to iterate and modify a copy, applying changes based on the original sequence's structure.
    7.  Return the modified sequence.