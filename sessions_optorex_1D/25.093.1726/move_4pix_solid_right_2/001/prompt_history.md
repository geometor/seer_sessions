
## train_1

**input:**
```
0 9 9 9 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 9 9 9 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 5 5 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 5 5 0
```


## train_3

**input:**
```
0 0 1 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 1 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 4 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 4 0 0
```


## train_5

**input:**
```
0 0 0 0 0 6 6 6 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 6 6 6
```


## train_6

**input:**
```
0 0 0 2 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 0 0 0 0
```


## train_7

**input:**
```
0 4 4 4 4 4 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 4 4 4 4 4 0 0
```

## Perception

The input consists of a sequence of 12 single-digit integers. The sequence is characterized by containing mostly zeros and a single contiguous block of identical non-zero digits. The length of this non-zero block varies across examples.

The output is also a sequence of 12 single-digit integers. It retains the same non-zero digits and the same number of zeros as the input. The key difference is the position of the non-zero block.

The transformation involves identifying the contiguous block of non-zero digits in the input sequence and shifting this entire block exactly 4 positions to the right. The positions originally occupied by the block become zeros, and the positions where the block moves to adopt the non-zero digit values. All other zero positions remain unchanged.

## Facts


```yaml
objects:
  - name: sequence
    type: list
    properties:
      - length: 12
      - elements: single-digit integers (0-9)
  - name: non_zero_block
    type: sub-sequence
    properties:
      - elements: identical non-zero digits
      - contiguous: true
      - location: variable within the input sequence
      - length: variable (1 or more)
  - name: zero_elements
    type: integer
    value: 0
    role: padding/background

actions:
  - name: identify_block
    actor: system
    input: input sequence
    output: non_zero_block (value, start_index, end_index)
  - name: shift_block
    actor: system
    object: non_zero_block
    properties:
      - direction: right
      - distance: 4 positions
  - name: generate_output
    actor: system
    input:
      - input sequence
      - identified non_zero_block
      - shift parameters (direction=right, distance=4)
    output: output sequence
    process: Create a new sequence of the same length filled with zeros, then place the non_zero_block at the new shifted position.

relationships:
  - type: positional_change
    subject: non_zero_block
    details: The start and end indices of the non_zero_block increase by 4 from input to output.
  - type: value_preservation
    subject: non_zero_block
    details: The digits and length of the non_zero_block remain the same between input and output.
  - type: structure_preservation
    subject: sequence
    details: The length of the sequence (12) remains the same between input and output.
```


## Natural Language Program

1.  Receive the input sequence of 12 integers.
2.  Identify the contiguous sub-sequence composed of identical non-zero digits (the "block"). Record the value of the digit, the starting index, and the ending index of this block.
3.  Create a new output sequence of 12 integers, initially filled with zeros.
4.  Calculate the new starting index for the block by adding 4 to the original starting index.
5.  Calculate the new ending index for the block by adding 4 to the original ending index.
6.  Place the identified block (using its original digit value and length) into the output sequence starting at the new starting index and ending at the new ending index.
7.  Return the resulting output sequence.
