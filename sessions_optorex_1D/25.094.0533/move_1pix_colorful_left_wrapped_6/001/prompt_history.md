
## train_1

**input:**
```
4 4 5 3 9 7 0 0 9 7 3 5
```


**output:**
```
4 5 3 9 7 0 0 9 7 3 5 4
```


## train_2

**input:**
```
0 0 0 0 0 3 6 1 1 3 2 0
```


**output:**
```
0 0 0 0 3 6 1 1 3 2 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 3 6 0 0
```


**output:**
```
0 0 0 0 0 0 0 3 6 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 0 0 0 0
```


## train_5

**input:**
```
0 2 9 4 9 0 0 0 0 0 0 0
```


**output:**
```
2 9 4 9 0 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 6 7 4 5 0 0 0 0 0
```


**output:**
```
0 0 6 7 4 5 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 6 7 9 0 0 0 0 0 0 0
```


**output:**
```
0 6 7 9 0 0 0 0 0 0 0 0
```

## Perception of Task Elements

The task involves transforming a sequence of integers into another sequence of integers of the same length. The input and output sequences consist of single-digit non-negative integers separated by spaces. Observing the examples, the core operation appears to be a rearrangement of the elements within the sequence. Specifically, the first element of the input sequence is relocated to the end of the sequence, while the relative order of the other elements is preserved. This is consistent across all provided examples.

## Task Facts


```yaml
Data:
  type: sequence
  element_type: integer
  separator: space
Transformation:
  type: rearrangement
  operation: cyclic_shift
  direction: left
  amount: 1
Details:
  - object: input_sequence
    properties:
      - list of integers
      - has a first element
      - has remaining elements
  - object: output_sequence
    properties:
      - list of integers
      - same length as input_sequence
  - action: move_first_to_last
    input: input_sequence
    output: output_sequence
    steps:
      - identify the first element of the input sequence
      - create a new sequence consisting of the elements from the second position to the end of the input sequence
      - append the identified first element to the end of the new sequence
Relationships:
  - The output sequence is derived from the input sequence.
  - The output sequence contains the same elements as the input sequence, but in a different order.
  - The order of elements from the second position onwards in the input sequence is maintained in the beginning of the output sequence.
  - The first element of the input sequence becomes the last element of the output sequence.
```


## Natural Language Program

1.  Read the input sequence of integers.
2.  Identify and store the first integer in the sequence.
3.  Create a new sequence containing all integers from the second position to the end of the original input sequence.
4.  Append the stored first integer to the end of this new sequence.
5.  Output the resulting sequence.
