
## train_1

**input:**
```
0 1 9 5 4 2 5 6 4 2 0 0
```


**output:**
```
4 2 0 0 0 1 9 5 4 2 5 6
```


## train_2

**input:**
```
4 5 9 9 0 0 0 0 0 0 8 7
```


**output:**
```
0 0 8 7 4 5 9 9 0 0 0 0
```


## train_3

**input:**
```
6 2 1 4 4 9 1 3 1 5 0 4
```


**output:**
```
1 5 0 4 6 2 1 4 4 9 1 3
```


## train_4

**input:**
```
0 0 0 0 3 9 3 9 3 4 2 0
```


**output:**
```
3 4 2 0 0 0 0 0 3 9 3 9
```


## train_5

**input:**
```
1 2 8 2 3 3 8 0 0 0 0 0
```


**output:**
```
0 0 0 0 1 2 8 2 3 3 8 0
```


## train_6

**input:**
```
0 2 1 7 8 6 2 3 0 0 0 0
```


**output:**
```
0 0 0 0 0 2 1 7 8 6 2 3
```


## train_7

**input:**
```
0 7 6 4 3 4 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 7 6 4 3 4 3 0
```

*   **Perception:**
    *   The input and output are both sequences of integers.
    *   All examples show sequences of length 12.
    *   The numbers themselves are not altered, only their positions.
    *   There appears to be a consistent split point within the input sequence.
    *   The transformation involves moving a segment from the end of the input sequence to the beginning of the output sequence.

*   **Facts:**
    
```yaml
    task_type: sequence transformation
    input_type: list of integers
    output_type: list of integers
    element_type: integer
    input_length: 12 (constant across examples)
    output_length: 12 (constant across examples)
    transformation: rearrangement (cyclic shift)
    properties:
      - object: input_sequence
        attributes:
          - length: 12
      - object: output_sequence
        attributes:
          - length: 12
          - composition: same elements as input_sequence
    actions:
      - name: split
        input: input_sequence
        parameters:
          - split_point: after the 8th element
        outputs:
          - subsequence_1: first 8 elements
          - subsequence_2: last 4 elements
      - name: concatenate
        inputs:
          - subsequence_2
          - subsequence_1
        output: output_sequence
    relationships:
      - The output sequence is formed by placing the last 4 elements of the input sequence at the beginning, followed by the first 8 elements of the input sequence.
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of 12 integers.
    2.  Divide the input sequence into two parts: the first 8 integers (Part A) and the last 4 integers (Part B).
    3.  Create the output sequence by concatenating Part B followed by Part A.
