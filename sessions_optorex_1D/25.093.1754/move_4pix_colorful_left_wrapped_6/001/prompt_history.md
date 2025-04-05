
## train_1

**input:**
```
5 4 6 3 7 4 9 2 2 0 8 6
```


**output:**
```
7 4 9 2 2 0 8 6 5 4 6 3
```


## train_2

**input:**
```
0 0 0 0 0 6 7 5 6 8 3 0
```


**output:**
```
0 6 7 5 6 8 3 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 1 7 4 0 0 0 0 0 0
```


**output:**
```
7 4 0 0 0 0 0 0 0 0 0 1
```


## train_4

**input:**
```
0 0 0 0 0 2 9 4 4 2 1 0
```


**output:**
```
0 2 9 4 4 2 1 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 2 1 9 4 3 7 8 8 0
```


**output:**
```
1 9 4 3 7 8 8 0 0 0 0 2
```


## train_6

**input:**
```
0 0 4 1 4 9 6 6 3 7 0 0
```


**output:**
```
4 9 6 6 3 7 0 0 0 0 4 1
```


## train_7

**input:**
```
3 2 0 0 0 0 0 0 0 0 0 9
```


**output:**
```
0 0 0 0 0 0 0 9 3 2 0 0
```

*   **Perception of Elements:**
    *   The input and output are both sequences of integers.
    *   Each sequence contains 12 integers.
    *   The integers present in the output sequence are exactly the same as those in the input sequence, but their order is changed.
    *   Comparing the input and output sequences reveals a consistent pattern of rearrangement.

*   **YAML Facts:**
    
```yaml
    task_description: Rearrange a sequence of 12 integers.
    input_object:
      type: sequence
      subtype: integers
      properties:
        length: 12
        elements: digits (0-9)
    output_object:
      type: sequence
      subtype: integers
      properties:
        length: 12
        elements: same digits as input, rearranged
    transformation:
      action: cyclic_shift_left
      details: The first 4 elements of the input sequence are moved to the end of the sequence.
      split_point: after the 4th element
      segments:
        - segment_1: first 4 elements
        - segment_2: remaining 8 elements
      reordering: segment_2 followed by segment_1
    examples_consistency: The transformation rule holds true for all provided examples.
    ```


*   **Natural Language Program:**
    1.  Accept an input sequence of 12 integers.
    2.  Divide the sequence into two parts: the first part consists of the first 4 integers, and the second part consists of the integers from the 5th position to the 12th position.
    3.  Create the output sequence by appending the first part to the end of the second part.
    4.  Return the rearranged sequence.
