
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 3 6
```


**output:**
```
6 0 0 0 0 0 0 0 0 0 0 3
```


## train_2

**input:**
```
4 8 9 0 0 0 3 4 1 7 5 6
```


**output:**
```
6 4 8 9 0 0 0 3 4 1 7 5
```


## train_3

**input:**
```
0 0 9 2 3 3 1 9 1 0 0 0
```


**output:**
```
0 0 0 9 2 3 3 1 9 1 0 0
```


## train_4

**input:**
```
2 4 1 9 0 0 0 0 0 0 5 1
```


**output:**
```
1 2 4 1 9 0 0 0 0 0 0 5
```


## train_5

**input:**
```
0 4 1 4 4 8 1 7 2 9 0 0
```


**output:**
```
0 0 4 1 4 4 8 1 7 2 9 0
```


## train_6

**input:**
```
6 0 0 0 0 0 0 0 0 8 5 1
```


**output:**
```
1 6 0 0 0 0 0 0 0 0 8 5
```


## train_7

**input:**
```
0 0 0 0 0 1 5 6 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 1 5 6 2 0 0
```

**Perception of Task Elements:**

The task involves transforming a sequence of numbers into another sequence of the same length. The input and output sequences appear to contain the same set of numbers, but their order is different. Observing the examples reveals a consistent pattern: the last number in the input sequence becomes the first number in the output sequence, and all preceding numbers are shifted one position to the right. This operation is commonly known as a right circular shift or rotation.

**Facts:**


```yaml
objects:
  - name: sequence
    type: list of integers
    properties:
      - ordered elements
      - fixed length (12 in examples)
actions:
  - name: rotate_right
    input: sequence
    output: sequence
    description: Moves the last element of the input sequence to the first position, shifting all other elements one position to the right.
relationships:
  - type: transformation
    input: input_sequence
    output: output_sequence
    rule: output_sequence is the result of applying the rotate_right action to the input_sequence.
```


**Natural Language Program:**

1.  Identify the input sequence of numbers.
2.  Take the last number from the input sequence.
3.  Take all numbers from the input sequence *except* the last one.
4.  Construct the output sequence by placing the number identified in step 2 at the beginning, followed by the numbers identified in step 3 in their original relative order.
