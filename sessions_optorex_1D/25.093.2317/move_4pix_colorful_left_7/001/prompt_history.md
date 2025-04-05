
## train_1

**input:**
```
0 0 0 0 0 0 0 0 5 0 0 0
```


**output:**
```
0 0 0 0 5 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 5 8 2 0 0 0
```


**output:**
```
0 0 5 8 2 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 4 9 0 0 0
```


**output:**
```
0 0 0 4 9 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 1 2 0 0 0
```


**output:**
```
0 0 0 1 2 0 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 8 3 6 4 9 5 3 0
```


**output:**
```
8 3 6 4 9 5 3 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 0 0 8 8 1 6
```


**output:**
```
0 0 0 0 8 8 1 6 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 0 8 6 5 6
```


**output:**
```
0 0 0 0 8 6 5 6 0 0 0 0
```

## Perception of Elements

The task involves transforming a sequence of integers.
- **Input:** A sequence of 12 integers, separated by spaces. These sequences contain mostly zeros, but also include some non-zero digits.
- **Output:** A sequence of 12 integers, also separated by spaces. The non-zero integers from the input sequence appear in the output, but their positions are shifted.
- **Relationship:** The output sequence is derived from the input sequence by shifting the elements. Observing the examples, the elements are consistently shifted 4 positions to the left in a circular manner (elements shifted off the beginning reappear at the end, although in these examples, the first 4 elements are always zero, so they just become trailing zeros).

## Documented Facts


```yaml
task_type: sequence_transformation
input_object:
  type: sequence
  element_type: integer
  length: 12
  properties:
    - contains_zeros: true
    - contains_non_zero_digits: true
output_object:
  type: sequence
  element_type: integer
  length: 12
  properties:
    - derived_from_input: true
transformation:
  action: circular_shift
  direction: left
  amount: 4
  description: The input sequence is cyclically shifted 4 positions to the left to produce the output sequence.
examples_analysis:
  - example: train_1
    input: [0, 0, 0, 0, 0, 0, 0, 0, 5, 0, 0, 0]
    output: [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0]
    shift_match: true
  - example: train_2
    input: [0, 0, 0, 0, 0, 0, 5, 8, 2, 0, 0, 0]
    output: [0, 0, 5, 8, 2, 0, 0, 0, 0, 0, 0, 0]
    shift_match: true
  - example: train_5
    input: [0, 0, 0, 0, 8, 3, 6, 4, 9, 5, 3, 0]
    output: [8, 3, 6, 4, 9, 5, 3, 0, 0, 0, 0, 0]
    shift_match: true
  - example: train_6
    input: [0, 0, 0, 0, 0, 0, 0, 0, 8, 8, 1, 6]
    output: [0, 0, 0, 0, 8, 8, 1, 6, 0, 0, 0, 0]
    shift_match: true
```


## Natural Language Program

1.  Read the input sequence of 12 integers.
2.  Perform a circular left shift operation on the sequence by 4 positions.
3.  Output the resulting sequence.
