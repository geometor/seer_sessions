
## train_1

**input:**
```
0 0 0 0 9 3 2 5 0 0 0 0
```


**output:**
```
9 3 2 5 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 6 8 3 4 9 8 0
```


**output:**
```
0 6 8 3 4 9 8 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 4 6 3 4 0 0
```


**output:**
```
0 0 4 6 3 4 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 8 1 7 0 0 0
```


**output:**
```
0 0 8 1 7 0 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 3 4 2 1 2 7 1
```


**output:**
```
0 3 4 2 1 2 7 1 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 0 0 0 0 8 1
```


**output:**
```
0 0 0 0 0 0 8 1 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 2 8 7 0 0 0 0
```


**output:**
```
0 2 8 7 0 0 0 0 0 0 0 0
```

*   **Perception of the elements:**
    *   The input and output are sequences of single-digit integers, separated by spaces.
    *   Each sequence has a fixed length (12 digits in the examples).
    *   The sequences contain both zero and non-zero digits.
    *   The core transformation involves repositioning a contiguous block of digits within the sequence.
    *   This block is defined by the first and last non-zero digits in the input sequence, including any zeros that fall between them.
    *   The block of digits is shifted to the left by a fixed amount.
    *   The positions outside the shifted block in the output are filled with zeros.

*   **Facts:**
    
```yaml
    task_elements:
      - object: sequence
        properties:
          - type: list of integers
          - length: 12 (based on examples)
          - elements: single digits (0-9)
      - object: digit_block
        properties:
          - content: contiguous subsequence from the input sequence
          - definition: starts at the index of the first non-zero digit, ends at the index of the last non-zero digit
          - includes: all digits (zero and non-zero) within its start and end indices
      - object: index
        properties:
          - type: integer
          - role: indicates position within the sequence (0-based)
    relationships:
      - type: identification
        description: Identify the first non-zero digit and its index (input_start_index).
      - type: identification
        description: Identify the last non-zero digit and its index (input_end_index).
      - type: extraction
        description: Extract the digit_block from input_start_index to input_end_index.
      - type: calculation
        description: Calculate the target start index for the block in the output sequence (output_start_index).
        formula: output_start_index = input_start_index - 4
      - type: construction
        description: Create the output sequence.
        steps:
          - Initialize an output sequence of the same length as the input, filled with zeros.
          - Place the extracted digit_block into the output sequence starting at the calculated output_start_index.
    ```


*   **Natural Language Program:**
    1.  Read the input sequence of digits.
    2.  Find the index of the first non-zero digit in the input sequence (let this be `first_nz_idx`). If no non-zero digit exists, the output is the same as the input (or a sequence of all zeros, depending on interpretation - examples suggest a block always exists).
    3.  Find the index of the last non-zero digit in the input sequence (let this be `last_nz_idx`).
    4.  Extract the contiguous sub-sequence (the "block") from the input sequence starting at `first_nz_idx` and ending at `last_nz_idx` (inclusive).
    5.  Calculate the target starting index for this block in the output sequence by subtracting 4 from `first_nz_idx` (let this be `output_start_idx`).
    6.  Create a new sequence of the same length as the input, initially filled entirely with zeros.
    7.  Place the extracted block into this new sequence, starting at `output_start_idx`.
    8.  The resulting sequence is the output.
