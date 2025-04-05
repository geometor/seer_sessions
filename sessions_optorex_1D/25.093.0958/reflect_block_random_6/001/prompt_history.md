
## train_1

**input:**
```
0 0 0 0 0 0 0 4 7 9 1 0
```


**output:**
```
0 0 0 0 0 0 0 1 9 7 4 0
```


## train_2

**input:**
```
4 7 9 2 4 6 2 3 4 3 1 5
```


**output:**
```
5 1 3 4 3 2 6 4 2 9 7 4
```


## train_3

**input:**
```
0 0 0 8 6 6 6 6 1 8 1 3
```


**output:**
```
0 0 0 3 1 8 1 6 6 6 6 8
```


## train_4

**input:**
```
3 7 4 7 7 1 3 6 8 6 4 9
```


**output:**
```
9 4 6 8 6 3 1 7 7 4 7 3
```


## train_5

**input:**
```
0 9 6 7 5 8 9 2 2 3 1 0
```


**output:**
```
0 1 3 2 2 9 8 5 7 6 9 0
```


## train_6

**input:**
```
8 3 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 8 0 0 0 0 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 3 6 8 0 0 0 0 0 0 0
```


**output:**
```
0 0 8 6 3 0 0 0 0 0 0 0
```

*   **Perception**: The input and output are sequences of single digits separated by spaces. The transformation appears to involve reversing a portion of the sequence. Specifically, the contiguous subsequence containing all the non-zero digits is identified and reversed in place. The surrounding zero digits, both leading and trailing, remain in their original positions.

*   **Facts**:
    
```yaml
    task_type: sequence_transformation
    input_elements: sequence of single digits (represented as strings, separated by spaces)
    output_elements: sequence of single digits (represented as strings, separated by spaces)
    objects:
      - sequence: the input list of digits
      - subsequence: the contiguous part of the sequence starting from the first non-zero digit and ending at the last non-zero digit
      - leading_zeros: the sequence of zeros before the first non-zero digit
      - trailing_zeros: the sequence of zeros after the last non-zero digit
    properties:
      - digits: can be zero or non-zero
      - position: index within the sequence
    actions:
      - identify: find the start and end indices of the non-zero subsequence
      - extract: isolate the leading zeros, the non-zero subsequence, and the trailing zeros
      - reverse: reverse the order of the elements within the non-zero subsequence
      - concatenate: combine the leading zeros, the reversed subsequence, and the trailing zeros to form the output sequence
    relationships:
      - The output sequence maintains the same leading and trailing zeros as the input sequence.
      - The core part of the output sequence is the reverse of the core non-zero part of the input sequence.
      - If the input contains no non-zero digits, the output is identical to the input (inferred, not explicitly shown in examples).
      - If the input contains only non-zero digits, the entire output sequence is the reverse of the input sequence.
    ```


*   **Natural Language Program**:
    1.  Receive the input sequence of digits.
    2.  Find the index of the first non-zero digit in the sequence. If no non-zero digit exists, return the original sequence.
    3.  Find the index of the last non-zero digit in the sequence.
    4.  Extract the subsequence starting from the first non-zero digit's index up to and including the last non-zero digit's index.
    5.  Reverse the order of the digits within this extracted subsequence.
    6.  Construct the output sequence by concatenating:
        a.  The digits from the start of the original sequence up to (but not including) the first non-zero digit's index (the leading zeros).
        b.  The reversed subsequence.
        c.  The digits from the position immediately after the last non-zero digit's index to the end of the original sequence (the trailing zeros).
    7.  Return the constructed output sequence.
