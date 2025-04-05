
## train_1

**input:**
```
0 0 0 0 6 0 0 0 6 0 0 0
```


**output:**
```
0 0 0 0 6 6 6 6 6 0 0 0
```


## train_2

**input:**
```
0 0 7 0 0 0 0 0 0 0 7 0
```


**output:**
```
0 0 7 7 7 7 7 7 7 7 7 0
```


## train_3

**input:**
```
0 0 2 0 0 0 0 0 0 2 0 0
```


**output:**
```
0 0 2 2 2 2 2 2 2 2 0 0
```


## train_4

**input:**
```
0 0 1 0 0 0 0 0 1 0 0 0
```


**output:**
```
0 0 1 1 1 1 1 1 1 0 0 0
```


## train_5

**input:**
```
0 8 0 0 0 0 0 0 0 0 0 8
```


**output:**
```
0 8 8 8 8 8 8 8 8 8 8 8
```


## train_6

**input:**
```
0 0 0 8 0 8 0 0 0 0 0 0
```


**output:**
```
0 0 0 8 8 8 0 0 0 0 0 0
```


## train_7

**input:**
```
8 0 0 0 0 8 0 0 0 0 0 0
```


**output:**
```
8 8 8 8 8 8 0 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The input and output are both sequences (lists or arrays) of single-digit integers, represented as space-separated strings.
    *   The length of the input sequence is preserved in the output sequence.
    *   Each input sequence contains exactly two instances of a single non-zero digit, with all other elements being zero.
    *   The non-zero digit from the input is the same as the non-zero digit used in the output.
    *   The output sequence essentially "fills" the gap between the first and last occurrence of the non-zero digit found in the input, including the positions of the original non-zero digits.

*   **Facts:**
    
```yaml
    objects:
      - input_sequence:
          type: list of integers
          properties:
            - length: fixed (e.g., 12 in examples)
            - contains exactly two identical non-zero elements
            - remaining elements are zero
      - output_sequence:
          type: list of integers
          properties:
            - length: same as input_sequence
            - contains a contiguous block of a single non-zero digit
            - remaining elements are zero
      - non_zero_digit:
          type: integer
          properties:
            - value: derived from the non-zero elements in the input_sequence
      - start_index:
          type: integer
          properties:
            - value: index of the first occurrence of the non_zero_digit in the input_sequence
      - end_index:
          type: integer
          properties:
            - value: index of the last occurrence of the non_zero_digit in the input_sequence
    actions:
      - identify: find the unique non-zero digit in the input_sequence
      - locate: find the first and last indices (start_index, end_index) of the non_zero_digit in the input_sequence
      - create: generate an initial output_sequence filled with zeros, matching the input_sequence length
      - fill: populate the output_sequence with the non_zero_digit from start_index to end_index (inclusive)
    relationships:
      - The non_zero_digit in the output_sequence is identical to the non_zero_digit in the input_sequence.
      - The segment of non_zero_digits in the output_sequence spans the range defined by the start_index and end_index derived from the input_sequence.
    ```


*   **Natural Language Program:**
    1.  Identify the unique non-zero integer value present in the input sequence; let this value be `d`.
    2.  Find the index of the first occurrence of `d` in the input sequence; let this be `start_index`.
    3.  Find the index of the last occurrence of `d` in the input sequence; let this be `end_index`.
    4.  Create a new sequence of the same length as the input sequence, initially filled with zeros.
    5.  Iterate through the indices from `start_index` to `end_index` (inclusive). For each index in this range, set the value in the new sequence at that index to `d`.
    6.  The resulting sequence is the output.
