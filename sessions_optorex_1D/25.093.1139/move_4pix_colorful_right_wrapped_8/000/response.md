*   **Perception of task elements:**
    *   The input and output are sequences of 12 integers each.
    *   The transformation involves rearranging the elements of the input sequence to produce the output sequence.
    *   The sequence appears to be treated as three distinct blocks of four elements each.
    *   The rearrangement follows a consistent pattern across all examples: the blocks are reordered.

*   **Facts:**
    
```yaml
    task_elements:
      - object: input_list
        properties:
          - type: list
          - item_type: integer
          - length: 12
      - object: output_list
        properties:
          - type: list
          - item_type: integer
          - length: 12
      - object: blocks
        properties:
          - count: 3
          - size: 4 elements each
          - source: derived from input_list by splitting it into three equal parts
            - block_1: elements at indices 0-3
            - block_2: elements at indices 4-7
            - block_3: elements at indices 8-11
    actions:
      - name: rearrange_blocks
        inputs:
          - block_1
          - block_2
          - block_3
        outputs:
          - output_list
        rule: Concatenate the blocks in the order: block_3, block_1, block_2.
    relationships:
      - The output_list is composed of the same elements as the input_list, but rearranged.
      - The rearrangement rule is based on splitting the input_list into three fixed-size blocks and reordering these blocks.
    ```


*   **Natural Language Program:**
    1.  Take the input list of 12 integers.
    2.  Divide the input list into three consecutive blocks, each containing 4 elements:
        *   Block 1 consists of the first 4 elements (indices 0-3).
        *   Block 2 consists of the next 4 elements (indices 4-7).
        *   Block 3 consists of the last 4 elements (indices 8-11).
    3.  Construct the output list by concatenating these blocks in the following order: Block 3, then Block 1, then Block 2.