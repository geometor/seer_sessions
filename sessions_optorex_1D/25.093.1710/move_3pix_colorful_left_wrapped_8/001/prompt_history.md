
## train_1

**input:**
```
3 1 7 2 2 7 0 0 0 0 0 0
```


**output:**
```
2 2 7 0 0 0 0 0 0 3 1 7
```


## train_2

**input:**
```
4 6 2 2 0 0 0 0 0 0 0 7
```


**output:**
```
2 0 0 0 0 0 0 0 7 4 6 2
```


## train_3

**input:**
```
0 6 3 3 7 6 6 8 9 0 0 0
```


**output:**
```
3 7 6 6 8 9 0 0 0 0 6 3
```


## train_4

**input:**
```
0 0 0 8 4 8 1 0 0 0 0 0
```


**output:**
```
8 4 8 1 0 0 0 0 0 0 0 0
```


## train_5

**input:**
```
6 8 0 0 0 0 0 0 0 4 8 8
```


**output:**
```
0 0 0 0 0 0 4 8 8 6 8 0
```


## train_6

**input:**
```
0 0 0 0 5 7 2 4 8 0 0 0
```


**output:**
```
0 5 7 2 4 8 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 9 2 1 3 0
```


**output:**
```
0 0 0 0 9 2 1 3 0 0 0 0
```

*   **Perception of Elements:**
    *   The input consists of a sequence of 12 integers.
    *   The output consists of a sequence of 12 integers, containing the same integers as the input but in a different order.
    *   The transformation involves rearranging blocks of numbers within the sequence.

*   **Facts:**
    
```yaml
    task_type: sequence_manipulation
    input:
      data_type: list
      element_type: integer
      length: 12
    output:
      data_type: list
      element_type: integer
      length: 12
      content: permutation of input elements
    transformation:
      action: split_and_concatenate
      split_point: after the 3rd element
      segments:
        - segment_1: first 3 elements of input
        - segment_2: elements from index 3 to 11 of input
      concatenation_order: [segment_2, segment_1]
      preserves_relative_order: true # Within each segment
    ```


*   **Natural Language Program:**
    1.  Read the input sequence of 12 integers.
    2.  Identify the first segment, which consists of the first 3 integers.
    3.  Identify the second segment, which consists of the integers from the 4th position to the 12th position (index 3 to 11).
    4.  Construct the output sequence by first placing the second segment, followed immediately by the first segment.
    5.  Output the resulting sequence.
