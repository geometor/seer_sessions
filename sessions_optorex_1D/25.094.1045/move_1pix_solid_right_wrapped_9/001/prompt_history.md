
## train_1

**input:**
```
0 0 5 5 5 5 5 0 0 0 0 0
```


**output:**
```
0 0 0 5 5 5 5 5 0 0 0 0
```


## train_2

**input:**
```
3 3 3 3 3 0 0 0 3 3 3 3
```


**output:**
```
3 3 3 3 3 3 0 0 0 3 3 3
```


## train_3

**input:**
```
0 4 4 4 4 4 4 0 0 0 0 0
```


**output:**
```
0 0 4 4 4 4 4 4 0 0 0 0
```


## train_4

**input:**
```
0 0 0 1 1 1 1 1 0 0 0 0
```


**output:**
```
0 0 0 0 1 1 1 1 1 0 0 0
```


## train_5

**input:**
```
2 0 0 0 0 0 0 0 0 2 2 2
```


**output:**
```
2 2 0 0 0 0 0 0 0 0 2 2
```


## train_6

**input:**
```
6 6 6 6 6 6 0 0 0 0 0 6
```


**output:**
```
6 6 6 6 6 6 6 0 0 0 0 0
```


## train_7

**input:**
```
4 4 4 4 4 4 0 0 4 4 4 4
```


**output:**
```
4 4 4 4 4 4 4 0 0 4 4 4
```

*   **Perception:** The task operates on sequences of single-digit integers. The core operation involves identifying the longest contiguous block of zeros within the sequence. The transformation rule depends on whether this longest block of zeros is located at the very end of the sequence or not. Based on its position, either an element following the block is moved to the start of the block, or the first zero of the block is moved to the position of the first non-zero element preceding the block.

*   **YAML Facts:**
    
```yaml
    objects:
      - sequence:
          type: list of integers
          properties:
            - elements: single digits (0-9)
            - length
      - block_of_zeros:
          type: contiguous subsequence
          properties:
            - value: all elements are 0
            - start_index
            - end_index
            - length
      - element:
          type: integer
          properties:
            - value
            - index (position in sequence)
    properties:
      - is_longest: boolean property of a block_of_zeros, compared to other blocks_of_zeros
      - is_first: boolean property of a block_of_zeros, relevant when multiple blocks share the maximum length
      - position: indicates location (e.g., 'at_end', 'not_at_end', 'preceding', 'following')
      - is_non_zero: boolean property of an element
    actions:
      - find_blocks: identify all contiguous blocks of zeros
      - find_longest_block: determine the block(s) with the maximum length
      - select_block: choose the first block among those with maximum length
      - check_position: determine if the selected block is at the end of the sequence
      - find_element_after: locate the element immediately following the selected block
      - find_first_preceding_non_zero: locate the first non-zero element before the selected block
      - remove_element: delete an element from the sequence at a specific index
      - insert_element: add an element to the sequence at a specific index
    relationships:
      - longest: relationship between a block of zeros and all other blocks of zeros based on length
      - first: relationship between blocks of the same maximum length based on start_index
      - preceding: relationship between an element/index and a block based on position
      - following: relationship between an element/index and a block based on position
    ```


*   **Natural Language Program:**
    1.  Identify all contiguous blocks of zeros within the input sequence.
    2.  Find the block(s) with the greatest length. If there is more than one block with the maximum length, select the one that starts at the earliest index.
    3.  Determine if the selected block of zeros ends at the last index of the sequence.
    4.  **If the block is at the end of the sequence:**
        a.  Find the index of the first element *before* the start of the block that has a non-zero value. If all preceding elements are zero, use index 0 as the target index.
        b.  Take the first zero from the selected block (the element at the block's start index).
        c.  Remove this zero from its original position.
        d.  Insert this zero into the sequence at the target index found in step 4a.
    5.  **If the block is *not* at the end of the sequence:**
        a.  Identify the element immediately following the selected block.
        b.  Remove this element from its position.
        c.  Insert the removed element at the starting index of the selected block of zeros.
    6.  Return the modified sequence.
