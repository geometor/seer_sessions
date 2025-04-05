
## train_1

**input:**
```
0 0 6 3 9 3 2 8 0 0 0 0
```


**output:**
```
0 0 0 0 0 6 3 9 3 2 8 0
```


## train_2

**input:**
```
9 9 9 6 5 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 9 9 9 6 5 0 0 0 0
```


## train_3

**input:**
```
0 0 0 3 1 7 2 3 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 3 1 7 2 3 0
```


## train_4

**input:**
```
6 5 2 5 1 8 8 0 0 0 0 0
```


**output:**
```
0 0 0 6 5 2 5 1 8 8 0 0
```


## train_5

**input:**
```
0 0 0 0 4 2 9 1 6 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 4 2 9 1 6
```


## train_6

**input:**
```
0 0 0 4 7 4 7 3 9 0 0 0
```


**output:**
```
0 0 0 0 0 0 4 7 4 7 3 9
```


## train_7

**input:**
```
4 4 6 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 4 4 6 0 0 0 0 0 0
```

Okay, let's break down the transformation logic based on the provided examples.

**Perception of Elements:**

*   **Input/Output Structure:** Both input and output are sequences of single digits separated by spaces.
*   **Key Components:** The sequences consist of '0' digits and non-zero digits (1-9).
*   **Pattern:** In each input sequence, there's a contiguous block of non-zero digits. This block might be at the beginning, end, or somewhere in the middle, surrounded by '0's.
*   **Transformation:** The core transformation appears to be a positional shift of the contiguous block of non-zero digits. The non-zero block itself remains unchanged in terms of the digits it contains and their order. The surrounding '0's adjust their positions to accommodate this shift. Specifically, the block consistently moves 3 positions to the right.

**Facts:**


```yaml
task_description: "Shift a contiguous block of non-zero digits within a sequence 3 positions to the right."
elements:
  - name: sequence
    type: list_of_digits
    description: "A sequence of single digits (0-9) separated by spaces."
  - name: zero_digit
    type: digit
    value: 0
    description: "Represents empty space or padding within the sequence."
  - name: non_zero_block
    type: sub_sequence
    description: "A contiguous sub-sequence containing only non-zero digits (1-9)."
    relationship: "Contained within the main sequence."
  - name: shift_amount
    type: integer
    value: 3
    description: "The fixed number of positions the non_zero_block is moved to the right."
actions:
  - name: identify_non_zero_block
    input: sequence
    output: non_zero_block, start_index, end_index
    description: "Find the first and last non-zero digits to define the boundaries of the non_zero_block."
  - name: shift_block_right
    input: sequence, non_zero_block, start_index, shift_amount
    output: modified_sequence
    description: "Move the non_zero_block 3 positions to the right within the sequence, adjusting the positions of the zero digits accordingly."
constraints:
  - "The length of the sequence remains unchanged."
  - "The digits within the non_zero_block and their relative order remain unchanged."
  - "There is only one contiguous block of non-zero digits in the input sequence."
  - "The shift is always exactly 3 positions to the right."
```


**Natural Language Program:**

1.  Receive the input sequence of digits.
2.  Identify the contiguous block of non-zero digits within the sequence. Determine its starting and ending positions.
3.  If no non-zero block exists (all zeros), return the input sequence unchanged.
4.  Create a new sequence of the same length, initially filled with zeros.
5.  Calculate the new starting position for the non-zero block by adding 3 to its original starting position.
6.  Copy the identified non-zero block into the new sequence, starting at the calculated new position.
7.  Return the new sequence.
