
## train_1

**input:**
```
0 0 0 0 0 2 2 2 2 2 2 0
```


**output:**
```
0 0 2 2 2 2 2 2 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 3 3 0 0 0 0
```


**output:**
```
0 0 0 3 3 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 2 2 2 2 0 0
```


**output:**
```
0 0 0 2 2 2 2 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 3 3 3 3 0 0 0
```


**output:**
```
0 0 3 3 3 3 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 8 8 8 0 0 0 0 0 0
```


**output:**
```
8 8 8 0 0 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 8 0 0 0 0 0 0
```


**output:**
```
0 0 8 0 0 0 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 6 6 6 6 6 6 6 6
```


**output:**
```
0 6 6 6 6 6 6 6 6 0 0 0
```

**Perception of Elements:**

The task involves processing sequences of single-digit numbers represented as space-separated strings. Each input sequence consists predominantly of zeros, with a single contiguous block of a non-zero digit (e.g., '2', '3', '8', '6'). The length of the sequences in the examples is consistently 12. The transformation rule appears to involve relocating the non-zero block within the sequence while preserving its length and the non-zero digit itself. The surrounding zeros adjust to accommodate the moved block. Specifically, the non-zero block is shifted three positions to the left.

**Facts:**


```yaml
objects:
  - name: sequence
    properties:
      - type: list of integers
      - representation: space-separated string
      - length: constant (12 in examples)
      - elements: single digits (0-9)
  - name: non_zero_block
    properties:
      - type: contiguous sub-sequence
      - elements: identical non-zero digits
      - location: defined by start and end index within the sequence
      - length: variable
      - digit_value: the non-zero digit comprising the block
  - name: zero_elements
    properties:
      - value: 0
      - location: elements outside the non_zero_block

actions:
  - name: identify_block
    inputs: sequence
    outputs: non_zero_block (digit_value, start_index, end_index)
    description: Finds the first non-zero element and determines the start and end indices of the contiguous block of that element.
  - name: shift_block_left
    inputs:
      - non_zero_block
      - shift_amount (constant value of 3)
    outputs: new_start_index
    description: Calculates the target starting position for the block in the output sequence by subtracting the shift amount from the original start index.
  - name: construct_output
    inputs:
      - original_sequence_length
      - non_zero_block (digit_value, original_start_index, original_end_index)
      - new_start_index
    outputs: output_sequence
    description: Creates a new sequence of the original length, initialized with zeros, and places the non_zero_block at the calculated new_start_index.

relationships:
  - The output sequence has the same length as the input sequence.
  - The output sequence contains the same non_zero_block as the input sequence, but potentially at a different location.
  - The non_zero_block in the output sequence starts 3 positions earlier (leftward shift) than in the input sequence.
  - Elements in the output sequence that are not part of the shifted non_zero_block are zeros.
```


**Natural Language Program:**

1.  Read the input sequence of space-separated digits.
2.  Identify the contiguous block of identical non-zero digits within the input sequence. Determine its value, its starting index, and its ending index.
3.  Create a new output sequence of the same length as the input sequence, initially filled with zeros.
4.  Calculate the target starting index for the non-zero block in the output sequence by subtracting 3 from its original starting index in the input sequence.
5.  Copy the identified non-zero block from the input sequence into the output sequence, starting at the calculated target starting index. Ensure that indices remain within the bounds of the sequence (indices less than 0 are effectively ignored as the corresponding block elements are not copied).
6.  Format the resulting output sequence back into a space-separated string.
