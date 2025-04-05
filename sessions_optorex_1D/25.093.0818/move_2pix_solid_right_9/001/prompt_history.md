
## train_1

**input:**
```
6 6 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 6 6 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
4 4 4 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 4 4 4 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 4 4 4 4 4 0 0
```


**output:**
```
0 0 0 0 0 0 0 4 4 4 4 4
```


## train_4

**input:**
```
0 9 9 9 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 9 9 9 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 8 8 8 8 8 8 0 0 0
```


**output:**
```
0 0 0 0 0 8 8 8 8 8 8 0
```


## train_6

**input:**
```
0 0 0 5 5 5 5 5 5 5 0 0
```


**output:**
```
0 0 0 0 0 5 5 5 5 5 5 5
```


## train_7

**input:**
```
0 0 0 0 0 7 7 7 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 7 7 7 0 0
```

## Perception

The input and output are both sequences (lists or arrays) of integers.
Each sequence consists primarily of zeros (0) and a single contiguous block of identical non-zero digits (e.g., `6 6`, `4 4 4`, `9 9 9`).
The transformation involves relocating this contiguous block of non-zero digits within the sequence.
By comparing the starting position of the non-zero block in the input to its starting position in the output, it's evident that the block is consistently shifted two positions to the right.
The positions vacated by the block become zeros, and the overall length of the sequence remains unchanged.

## Facts


```yaml
objects:
  - name: sequence
    type: list_of_integers
    properties:
      - contains_zeros: true
      - contains_non_zero_block: true
  - name: non_zero_block
    type: sublist_of_integers
    properties:
      - contiguous: true
      - elements_are_identical: true
      - elements_are_non_zero: true
    location:
      - property: start_index_input
      - property: end_index_input
      - property: start_index_output
      - property: end_index_output
  - name: background
    type: integer
    value: 0

actions:
  - name: shift_block
    target: non_zero_block
    properties:
      - direction: right
      - amount: 2_positions

relationships:
  - type: transformation
    from: sequence_input
    to: sequence_output
    rule: shift_non_zero_block_right_by_2
  - type: positional_change
    object: non_zero_block
    details: start_index_output = start_index_input + 2
```


## Natural Language Program

1.  Identify the input sequence of integers.
2.  Locate the contiguous block of identical non-zero integers within the input sequence. Determine its starting and ending indices.
3.  Create a new output sequence of the same length as the input sequence, initially filled with zeros.
4.  Copy the identified non-zero block from the input sequence into the output sequence, placing its starting element at an index two positions greater than its original starting index in the input sequence.
