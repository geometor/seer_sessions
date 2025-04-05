
## train_1

**input:**
```
5 5 5 5 5 5 5 5 2 0 0 0
```


**output:**
```
5 5 5 5 5 5 5 5 2 0 0 0
```


## train_2

**input:**
```
0 0 4 4 4 4 4 4 4 4 4 2
```


**output:**
```
0 0 4 4 4 4 4 4 4 4 4 2
```


## train_3

**input:**
```
9 9 9 9 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 9 9 9 9 2 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 6 6 6 6 0 0 0 0 2
```


**output:**
```
0 0 0 0 0 0 0 6 6 6 6 2
```


## train_5

**input:**
```
0 0 0 6 6 6 6 6 2 0 0 0
```


**output:**
```
0 0 0 6 6 6 6 6 2 0 0 0
```


## train_6

**input:**
```
0 0 0 2 0 0 0 0 5 5 5 5
```


**output:**
```
0 0 0 2 5 5 5 5 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 4 4 4 2 0
```


**output:**
```
0 0 0 0 0 0 0 4 4 4 2 0
```

*   **Perception of Elements:**
    *   The input and output are sequences of 12 single-digit integers.
    *   The digits '0' and '2' appear to have special roles. '0' acts as a filler or space, and '2' appears to be a fixed anchor point.
    *   Each input contains a single contiguous block of identical non-zero digits (other than '2'). For example, `5 5 5 5 5 5 5 5` in `train_1`, `4 4 4 4 4 4 4 4 4` in `train_2`, `9 9 9 9` in `train_3`.
    *   The transformation involves potentially repositioning this block of non-zero digits relative to the '2'.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: sequence
        properties:
          - type: list of integers
          - length: 12
      - object: digit_zero
        properties:
          - value: 0
          - role: filler/space, movable
      - object: digit_two
        properties:
          - value: 2
          - role: anchor/pivot, fixed position relative to other non-zero blocks
      - object: digit_block
        properties:
          - type: contiguous sequence of identical digits
          - value: non-zero, not equal to 2
          - count_per_input: 1
          - role: primary movable element
    relationships:
      - type: spatial
        between: [digit_block, digit_two]
        description: The block can be to the left or right of the '2'.
      - type: separation
        between: [digit_block, digit_two]
        medium: digit_zero
        description: Zeroes may exist between the block and the '2'.
    action:
      - type: conditional_swap
        condition: Zeros exist between the digit_block and digit_two.
        elements_involved: [digit_block, sequence of digit_zero between block and two]
        effect: The digit_block and the intermediate sequence of zeros swap positions, moving the block adjacent to the '2'.
        directionality: The block moves towards the '2'.
    invariants:
      - The position of '2' relative to the start/end of the sequence if no swap happens.
      - The position of '2' relative to the *other* digits (not involved in the block or the intermediate zeros) remains the same.
      - The order and values of digits within the `digit_block` remain unchanged.
      - The total count of each digit remains the same.
      - The length of the sequence remains 12.
    ```


*   **Natural Language Program:**
    1.  Identify the single occurrence of the digit '2' and its index within the input sequence.
    2.  Identify the contiguous block of identical digits that are not '0' and not '2'. Record its starting index, ending index, and the digit value.
    3.  Determine if this block is located to the left or right of the '2'.
    4.  If the block is to the left of '2':
        *   Check if all elements between the end of the block (exclusive) and the index of '2' (exclusive) are '0'.
        *   If yes, and if there is at least one such '0', perform a swap: Move the identified block of digits immediately to the left of '2', and move the sequence of intermediate '0's to the original starting position of the block.
    5.  If the block is to the right of '2':
        *   Check if all elements between the index of '2' (exclusive) and the start of the block (exclusive) are '0'.
        *   If yes, and if there is at least one such '0', perform a swap: Move the identified block of digits immediately to the right of '2', and move the sequence of intermediate '0's to the position immediately following the block's original end position.
    6.  If no intermediate '0's exist between the block and '2' (i.e., they are adjacent or separated only by other non-zero numbers not part of the block), make no changes to the sequence.
    7.  Return the potentially modified sequence.
