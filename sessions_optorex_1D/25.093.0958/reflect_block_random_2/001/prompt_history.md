
## train_1

**input:**
```
2 6 2 3 6 7 4 4 8 1 1 3
```


**output:**
```
3 1 1 8 4 4 7 6 3 2 6 2
```


## train_2

**input:**
```
2 7 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
7 2 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 6 9 3 9 2 1 7 1 7 4
```


**output:**
```
0 0 4 7 1 7 1 2 9 3 9 6
```


## train_4

**input:**
```
0 0 2 1 8 1 0 0 0 0 0 0
```


**output:**
```
0 0 1 8 1 2 0 0 0 0 0 0
```


## train_5

**input:**
```
2 1 5 3 3 8 0 0 0 0 0 0
```


**output:**
```
8 3 3 5 1 2 0 0 0 0 0 0
```


## train_6

**input:**
```
8 8 6 7 5 9 9 7 2 2 6 1
```


**output:**
```
1 6 2 2 7 9 9 5 7 6 8 8
```


## train_7

**input:**
```
0 0 0 6 2 1 4 1 6 8 2 1
```


**output:**
```
0 0 0 1 2 8 6 1 4 1 2 6
```

Okay, let's analyze the transformation.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are sequences of single-digit integers, separated by spaces.
2.  **Sequence Length:** The length of the input and output sequences is consistent within each example pair (always 12 digits in the provided examples).
3.  **Content:** The digits present in the output are the same digits as in the input, suggesting a rearrangement or reordering operation.
4.  **Zero Handling:** Zeros often appear at the beginning and/or end of the sequences. These leading and trailing zeros seem to maintain their positions relative to the start and end of the sequence.
5.  **Core Transformation:** The non-zero portion of the sequence appears to be reversed. In examples without leading or trailing zeros (train\_1, train\_6), the entire sequence is reversed. In examples with leading/trailing zeros, only the block of digits between the first non-zero digit and the last non-zero digit is reversed.

**YAML Facts:**


```yaml
task_elements:
  - item: sequences
    properties:
      - type: list of single-digit integers
      - length: fixed (12 in examples)
      - role: input and output
objects:
  - object: input_sequence
    properties:
      - contains digits (0-9)
      - may contain leading zeros
      - may contain trailing zeros
  - object: output_sequence
    properties:
      - contains the same digits as input
      - same length as input
  - object: non_zero_subsequence
    derivation: The contiguous block of digits in the input sequence starting from the first non-zero digit and ending at the last non-zero digit.
    properties:
      - may be the entire sequence if no leading/trailing zeros exist
      - may be empty if the input sequence contains only zeros
relationships:
  - relationship: position_preservation
    between: leading zeros in input_sequence
    and: leading zeros in output_sequence
    description: Leading zeros in the input maintain their positions at the start of the output.
  - relationship: position_preservation
    between: trailing zeros in input_sequence
    and: trailing zeros in output_sequence
    description: Trailing zeros in the input maintain their positions at the end of the output.
actions:
  - action: identify_boundaries
    on: input_sequence
    produces: start_index (index of first non-zero), end_index (index of last non-zero)
  - action: extract_subsequence
    on: input_sequence
    using: start_index, end_index
    produces: non_zero_subsequence
  - action: reverse_sequence
    on: non_zero_subsequence
    produces: reversed_non_zero_subsequence
  - action: construct_output
    using:
      - leading zeros (input[0:start_index])
      - reversed_non_zero_subsequence
      - trailing zeros (input[end_index+1:])
    produces: output_sequence
```


**Natural Language Program:**

1.  Read the input sequence of digits.
2.  Find the index of the first non-zero digit in the input sequence. If no non-zero digit exists, the output is identical to the input; stop.
3.  Find the index of the last non-zero digit in the input sequence.
4.  Identify the sub-sequence of digits starting from the first non-zero digit up to and including the last non-zero digit.
5.  Reverse the order of the digits within this identified sub-sequence.
6.  Construct the output sequence by concatenating:
    a.  The digits from the beginning of the input sequence up to (but not including) the first non-zero digit.
    b.  The reversed sub-sequence from step 5.
    c.  The digits from the input sequence starting just after the last non-zero digit until the end of the sequence.
7.  Output the constructed sequence.
