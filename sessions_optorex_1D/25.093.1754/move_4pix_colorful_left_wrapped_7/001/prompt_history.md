
## train_1

**input:**
```
6 0 0 0 0 0 0 0 0 8 7 8
```


**output:**
```
0 0 0 0 0 8 7 8 6 0 0 0
```


## train_2

**input:**
```
0 9 1 4 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 9 1 4
```


## train_3

**input:**
```
2 8 6 7 2 5 0 0 0 1 8 9
```


**output:**
```
2 5 0 0 0 1 8 9 2 8 6 7
```


## train_4

**input:**
```
0 0 0 6 1 5 2 3 4 0 0 0
```


**output:**
```
1 5 2 3 4 0 0 0 0 0 0 6
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 2 0 0 0
```


**output:**
```
0 0 0 0 2 0 0 0 0 0 0 0
```


## train_6

**input:**
```
4 0 0 0 0 0 1 3 7 5 4 6
```


**output:**
```
0 0 1 3 7 5 4 6 4 0 0 0
```


## train_7

**input:**
```
7 4 3 7 2 1 6 0 0 0 0 5
```


**output:**
```
2 1 6 0 0 0 0 5 7 4 3 7
```

**Perception of Task Elements:**

The task operates on sequences of 12 numerical elements. The input sequence is transformed into an output sequence of the same length (12 elements). The core transformation appears to be a rearrangement of the elements within the sequence. Specifically, the sequence seems to be divided into two parts, which are then swapped to form the output sequence. The split point appears constant across all examples.

**YAML Facts:**


```yaml
objects:
  - name: sequence
    type: list of integers
    properties:
      - length: 12
  - name: element
    type: integer
  - name: first_part
    type: sub-sequence
    properties:
      - location: elements from index 0 up to (but not including) index 4
      - length: 4
  - name: second_part
    type: sub-sequence
    properties:
      - location: elements from index 4 up to the end (index 11)
      - length: 8

actions:
  - name: split
    description: Divide the input sequence into two parts.
    inputs:
      - sequence
    outputs:
      - first_part
      - second_part
    parameters:
      - split_index: 4
  - name: swap
    description: Exchange the positions of the two parts.
  - name: join
    description: Concatenate the swapped parts to form the output sequence.
    inputs:
      - second_part
      - first_part
    outputs:
      - output_sequence

relationships:
  - The output sequence is formed by concatenating the second_part followed by the first_part of the input sequence.
```


**Natural Language Program:**

1.  Take the input sequence of 12 numbers.
2.  Split the sequence into two parts: the first part consists of the first 4 elements, and the second part consists of the remaining 8 elements (from the 5th element to the 12th).
3.  Create the output sequence by concatenating the second part followed by the first part.
