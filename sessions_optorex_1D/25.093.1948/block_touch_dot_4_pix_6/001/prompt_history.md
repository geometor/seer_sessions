
## train_1

**input:**
```
0 7 7 7 7 7 7 2 0 0 0 0
```


**output:**
```
0 7 7 7 7 7 7 2 0 0 0 0
```


## train_2

**input:**
```
6 2 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 2 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 2 5 5 5 5 5 5 5 5 5
```


**output:**
```
0 0 2 5 5 5 5 5 5 5 5 5
```


## train_4

**input:**
```
0 0 0 0 0 0 0 2 3 3 3 3
```


**output:**
```
0 0 0 0 0 0 0 2 3 3 3 3
```


## train_5

**input:**
```
5 5 5 5 5 0 0 0 0 2 0 0
```


**output:**
```
0 0 0 0 5 5 5 5 5 2 0 0
```


## train_6

**input:**
```
0 0 0 0 0 4 0 2 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 4 2 0 0 0 0
```


## train_7

**input:**
```
2 0 5 5 5 5 5 5 5 5 5 0
```


**output:**
```
2 5 5 5 5 5 5 5 5 5 0 0
```

*   **Perception of Elements:** The task operates on sequences of single digits. Each sequence contains the digit `2` exactly once. The sequences also contain blocks of identical non-zero digits and potentially zeros (`0`). The core transformation involves the digit `2` and its relationship with adjacent non-zero blocks and intervening zeros. In some cases, the input and output are identical, suggesting the transformation conditions are not met. In other cases, zeros located between the `2` and an adjacent block of non-zero digits are moved to the outer side of that block.

*   **YAML Facts:**
    
```yaml
    Task: Rearrange digits in a sequence based on the position of '2'.

    Objects:
      - Sequence: A list of single-digit integers.
      - Digit '2': A unique marker within the sequence.
      - Non-Zero Block: A contiguous subsequence of identical digits greater than 0.
      - Intervening Zeros: Zeros located between the '2' and an adjacent Non-Zero Block.

    Properties:
      - Sequence: Has length, contains digits.
      - Digit '2': Has a specific index (position).
      - Non-Zero Block: Has a starting index, ending index, and a specific digit value.
      - Intervening Zeros: Have count and original positions.

    Relationships:
      - Adjacency: A Non-Zero Block can be adjacent to '2', potentially separated only by Intervening Zeros. Adjacency can be to the left or right of '2'.
      - Containment: Intervening Zeros are contained within the segment between '2' and the boundary of the adjacent Non-Zero Block.

    Actions:
      - Find: Locate the index of '2'.
      - Identify: Find Non-Zero Blocks adjacent (allowing for zeros) to '2'.
      - Collect: Gather Intervening Zeros between '2' and an adjacent Non-Zero Block.
      - Move: Relocate the collected Intervening Zeros to the outer side of the identified Non-Zero Block.
        - If the block is to the left of '2', move zeros to the position immediately before the block's start.
        - If the block is to the right of '2', move zeros to the position immediately after the block's end.
      - Reconstruct: Form the output sequence based on the moved elements.

    Conditionality:
      - The move action only occurs if Intervening Zeros exist between '2' and an adjacent Non-Zero Block.
      - If no such condition is met on either side of '2', the sequence remains unchanged.
      - The process checks one side (e.g., left) first. If a move occurs, the process may terminate without checking the other side (based on examples).
    ```


*   **Natural Language Program:**
    1.  Read the input sequence of digits.
    2.  Find the index position of the digit `2`.
    3.  Examine the segment of the sequence immediately to the left of the `2`. Scan leftwards from the position before the `2`.
    4.  Count and collect any consecutive `0`s found (`intervening_zeros`). Stop scanning left if a non-zero digit is encountered or the beginning of the sequence is reached.
    5.  If `intervening_zeros` were found AND a non-zero digit `d` was encountered immediately before them:
        a.  Identify the full contiguous block of `d` digits ending at this position (`adjacent_block`).
        b.  Remove the `intervening_zeros` from their original positions.
        c.  Insert the `intervening_zeros` into the sequence immediately before the start of the `adjacent_block`.
        d.  Output the modified sequence and terminate.
    6.  If no change was made in the previous steps, examine the segment of the sequence immediately to the right of the `2`. Scan rightwards from the position after the `2`.
    7.  Count and collect any consecutive `0`s found (`intervening_zeros`). Stop scanning right if a non-zero digit is encountered or the end of the sequence is reached.
    8.  If `intervening_zeros` were found AND a non-zero digit `d` was encountered immediately after them:
        a.  Identify the full contiguous block of `d` digits starting at this position (`adjacent_block`).
        b.  Remove the `intervening_zeros` from their original positions.
        c.  Insert the `intervening_zeros` into the sequence immediately after the end of the `adjacent_block`.
        d.  Output the modified sequence and terminate.
    9.  If no changes were made in any of the previous steps, output the original input sequence.
