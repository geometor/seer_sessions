
## train_1

**input:**
```
0 0 0 9 9 9 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 9 9 9 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 3 3 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 3 3
```


## train_3

**input:**
```
0 4 4 4 4 4 4 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 4 4 4 4 4 4 4
```


## train_4

**input:**
```
3 3 3 3 3 3 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 3 3 3 3 3 3 3 0
```


## train_5

**input:**
```
0 0 0 0 0 0 8 8 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 8 8
```


## train_6

**input:**
```
0 0 0 0 1 1 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 1 1 0 0
```


## train_7

**input:**
```
0 0 8 8 8 8 8 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 8 8 8 8 8 0
```

*   **Perception:** The input and output are one-dimensional sequences (lists or arrays) of integers, all having the same length (12 elements). Each input sequence consists mostly of zeros ('0') and one contiguous block of identical non-zero digits (e.g., '9 9 9', '3 3', '4 4 4 4 4 4 4'). The output sequence contains the same block of non-zero digits, but shifted to a different position within the sequence, with the remaining positions filled with zeros. The key transformation is the relocation of this non-zero block. By comparing the starting index of the block in the input and output, it appears the block is consistently shifted 4 positions to the right.

*   **Facts:**
    
```yaml
    task_type: sequence_transformation
    input_data:
      type: list_of_integers
      length: 12
      elements:
        - type: zero (background)
        - type: contiguous_block
          properties:
            - digits_are_identical
            - digit_value: non-zero_integer (varies per example)
            - length: variable (varies per example)
            - position: variable (varies per example)
    output_data:
      type: list_of_integers
      length: 12
      elements:
        - type: zero (background)
        - type: contiguous_block (same as input)
          properties:
            - position: shifted_right_by_4
    transformation:
      action: shift_block
      direction: right
      amount: 4_positions
      details: The contiguous block of non-zero identical digits is moved 4 positions to the right. The original positions occupied by the block, and any positions not occupied by the shifted block in the output, are filled with zeros.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous sub-sequence within the input list consisting of identical non-zero digits (the "block"). Note its starting index, length, and the value of the digit.
    2.  Create a new list of the same length as the input list, initialized entirely with zeros.
    3.  Calculate the new starting index for the block by adding 4 to its original starting index in the input list.
    4.  Place the identified block (using its original digit value and length) into the new list, starting at the calculated new starting index.
    5.  The resulting list is the output.
