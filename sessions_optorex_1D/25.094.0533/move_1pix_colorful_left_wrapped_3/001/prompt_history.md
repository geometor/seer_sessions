
## train_1

**input:**
```
0 0 0 0 0 4 8 5 0 0 0 0
```


**output:**
```
0 0 0 0 4 8 5 0 0 0 0 0
```


## train_2

**input:**
```
0 0 4 6 1 1 4 5 9 5 8 0
```


**output:**
```
0 4 6 1 1 4 5 9 5 8 0 0
```


## train_3

**input:**
```
0 0 5 9 7 0 0 0 0 0 0 0
```


**output:**
```
0 5 9 7 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
3 7 3 9 9 2 0 0 8 9 3 2
```


**output:**
```
7 3 9 9 2 0 0 8 9 3 2 3
```


## train_5

**input:**
```
0 0 0 0 0 3 7 3 0 0 0 0
```


**output:**
```
0 0 0 0 3 7 3 0 0 0 0 0
```


## train_6

**input:**
```
5 9 8 8 0 0 0 0 0 0 0 7
```


**output:**
```
9 8 8 0 0 0 0 0 0 0 7 5
```


## train_7

**input:**
```
2 0 0 0 0 6 2 6 7 2 4 7
```


**output:**
```
0 0 0 0 6 2 6 7 2 4 7 2
```

## Perception

The input and output are both sequences of integers.
Comparing the input and output sequences, it appears that the first element of the input sequence is moved to the end of the sequence to form the output. The relative order of the remaining elements is preserved. This operation is equivalent to a single left rotation of the sequence.

## Facts


```yaml
objects:
  - type: sequence
    properties:
      - name: elements
        type: list[integer]
      - name: length
        value_description: The number of integers in the sequence.
actions:
  - name: left_rotate
    description: Moves the first element of the sequence to the end.
    input:
      - name: input_sequence
        type: sequence
    output:
      - name: output_sequence
        type: sequence
        description: The input sequence after moving the first element to the last position.
relationships:
  - type: transformation
    description: The output sequence is derived from the input sequence by performing a single left rotation.
    input: input_sequence
    output: output_sequence
    rule: Take the first element of the input sequence and append it to the end of the sequence formed by the remaining elements.
```


## Natural Language Program

1.  Receive the input sequence of integers.
2.  Identify the first integer in the sequence.
3.  Create a new sequence containing all integers from the input sequence *except* the first one, maintaining their original relative order.
4.  Append the first integer (identified in step 2) to the end of the new sequence created in step 3.
5.  Return the resulting sequence as the output.
