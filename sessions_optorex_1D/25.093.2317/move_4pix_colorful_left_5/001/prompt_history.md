
## train_1

**input:**
```
0 0 0 0 7 1 3 2 2 7 4 0
```


**output:**
```
7 1 3 2 2 7 4 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 1 2 0 0 0 0 0 0
```


**output:**
```
1 2 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 3 4 9 2 1 0 0
```


**output:**
```
0 3 4 9 2 1 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 2 6 1 8 6 0
```


**output:**
```
0 0 2 6 1 8 6 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 2 8 2 2 4 0 0 0
```


**output:**
```
2 8 2 2 4 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 8 9 5 7 5 0
```


**output:**
```
0 0 8 9 5 7 5 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 2 1 4 0 0 0 0 0
```


**output:**
```
2 1 4 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output are both sequences of 12 single-digit integers.
    *   The digits present in the output are the same as the digits in the input, but their order is changed.
    *   Comparing inputs and outputs, it appears the sequence is being shifted or rotated.
    *   Specifically, the first four elements of the input sequence seem to be moved to the end of the sequence in the output. This corresponds to a cyclic shift or left rotation of the sequence.
    *   Testing this hypothesis across all examples confirms that the output is consistently obtained by rotating the input sequence 4 positions to the left. For example, in `train_1`, the input `0 0 0 0 7 1 3 2 2 7 4 0` becomes `7 1 3 2 2 7 4 0 0 0 0 0` after moving the first four `0`s to the end. In `train_3`, `0 0 0 0 0 3 4 9 2 1 0 0` becomes `0 3 4 9 2 1 0 0 0 0 0 0` after moving the first four `0`s to the end.

*   **Facts:**
    
```yaml
    task_elements:
      - item: input_sequence
        description: A sequence of 12 single-digit integers.
        properties:
          - length: 12
          - elements: single-digit integers (0-9)
      - item: output_sequence
        description: A sequence of 12 single-digit integers derived from the input sequence.
        properties:
          - length: 12
          - elements: single-digit integers (0-9), same multiset as input
      - item: transformation
        description: The process applied to the input sequence to produce the output sequence.
        type: cyclic_shift
        properties:
          - direction: left
          - magnitude: 4 positions
        relationship: The output_sequence is the result of applying a cyclic shift (left rotation) of 4 positions to the input_sequence.
    ```


*   **Natural Language Program:**
    1.  Take the input sequence of 12 digits.
    2.  Perform a cyclic shift (left rotation) on the sequence by 4 positions.
    3.  The resulting sequence is the output.
