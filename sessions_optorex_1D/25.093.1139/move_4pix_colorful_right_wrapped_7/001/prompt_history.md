
## train_1

**input:**
```
4 3 7 0 0 0 0 0 0 0 2 7
```


**output:**
```
0 0 2 7 4 3 7 0 0 0 0 0
```


## train_2

**input:**
```
4 8 0 0 0 0 0 0 0 9 8 9
```


**output:**
```
0 9 8 9 4 8 0 0 0 0 0 0
```


## train_3

**input:**
```
0 9 9 5 3 4 2 1 3 7 0 0
```


**output:**
```
3 7 0 0 0 9 9 5 3 4 2 1
```


## train_4

**input:**
```
2 6 9 2 3 0 0 2 1 2 6 6
```


**output:**
```
1 2 6 6 2 6 9 2 3 0 0 2
```


## train_5

**input:**
```
0 0 7 6 2 5 5 3 5 8 0 0
```


**output:**
```
5 8 0 0 0 0 7 6 2 5 5 3
```


## train_6

**input:**
```
0 0 0 9 9 8 8 5 5 4 4 0
```


**output:**
```
5 4 4 0 0 0 0 9 9 8 8 5
```


## train_7

**input:**
```
2 4 7 5 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 4 7 5 0 0 0 0
```

## Perception

1.  **Input/Output Structure:** Both input and output are sequences of 12 single-digit integers, presented as space-separated strings.
2.  **Transformation Type:** The transformation appears to be a structural rearrangement of the input sequence elements. No arithmetic operations or changes to the individual digits are observed.
3.  **Key Observation:** The last four elements of the input sequence consistently appear as the first four elements of the output sequence. The first eight elements of the input sequence consistently appear as the last eight elements of the output sequence.
4.  **Inferred Action:** The transformation involves splitting the input sequence into two segments (the first 8 elements and the last 4 elements) and then concatenating them in reverse order (last 4 followed by first 8). This is equivalent to a cyclic shift or rotation of the sequence.

## Facts


```yaml
Task: Sequence Rotation

Objects:
  - name: input_sequence
    type: List[int]
    properties:
      - length: 12
      - elements: single-digit integers
  - name: output_sequence
    type: List[int]
    properties:
      - length: 12
      - elements: single-digit integers
  - name: first_segment
    type: List[int]
    properties:
      - source: input_sequence
      - elements: First 8 elements of input_sequence
      - length: 8
  - name: second_segment
    type: List[int]
    properties:
      - source: input_sequence
      - elements: Last 4 elements of input_sequence
      - length: 4

Actions:
  - name: Split
    description: Divide the input_sequence into two segments.
    inputs:
      - input_sequence
      - split_point: index 8 (after the 8th element)
    outputs:
      - first_segment (elements 0 through 7)
      - second_segment (elements 8 through 11)
  - name: Concatenate
    description: Combine the segments in a specific order to form the output_sequence.
    inputs:
      - second_segment
      - first_segment
    outputs:
      - output_sequence

Relationships:
  - The output_sequence is formed by placing the second_segment before the first_segment.
  - output_sequence = second_segment + first_segment
```


## Natural Language Program

1.  Take the input sequence of 12 digits.
2.  Identify the last 4 digits of the input sequence.
3.  Identify the first 8 digits of the input sequence.
4.  Construct the output sequence by placing the identified last 4 digits at the beginning, followed immediately by the identified first 8 digits.
