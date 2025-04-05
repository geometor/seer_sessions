
## train_1

**input:**
```
0 0 7 6 1 9 1 9 5 4 8 0
```


**output:**
```
0 7 6 1 9 1 9 5 4 8 0 0
```


## train_2

**input:**
```
8 8 3 0 0 0 0 0 3 4 6 2
```


**output:**
```
8 3 0 0 0 0 0 3 4 6 2 8
```


## train_3

**input:**
```
0 0 0 0 0 0 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 3 0 0 0 0 0 0
```


## train_4

**input:**
```
6 2 4 1 0 0 0 0 0 1 9 7
```


**output:**
```
2 4 1 0 0 0 0 0 1 9 7 6
```


## train_5

**input:**
```
0 0 0 0 7 1 6 0 0 0 0 0
```


**output:**
```
0 0 0 7 1 6 0 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 0 0 0 2 5 0
```


**output:**
```
0 0 0 0 0 0 0 0 2 5 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 4 3 0 0 0 0
```


**output:**
```
0 0 0 0 0 4 3 0 0 0 0 0
```

## Perception

The input and output are both sequences of single-digit integers, presented as space-separated strings. Comparing the input and output sequences across all examples reveals a consistent pattern: the first element of the input sequence is relocated to the end of the sequence to produce the output. All other elements retain their original relative order, shifting one position to the left to fill the space vacated by the first element.

## Facts


```yaml
objects:
  - name: input_sequence
    type: list of integers
    description: The sequence of numbers provided as input.
  - name: output_sequence
    type: list of integers
    description: The sequence of numbers produced as output.
  - name: first_element
    type: integer
    description: The element at the beginning (index 0) of the input_sequence.
  - name: remaining_elements
    type: list of integers
    description: The elements of the input_sequence starting from the second element (index 1) to the end.

actions:
  - name: move_first_to_end
    actor: transformation_process
    object: input_sequence
    result: output_sequence
    steps:
      - identify the first_element of the input_sequence.
      - identify the remaining_elements of the input_sequence.
      - construct the output_sequence by concatenating the remaining_elements followed by the first_element.

relationships:
  - type: transformation
    from: input_sequence
    to: output_sequence
    rule: The output_sequence is formed by taking the first_element of the input_sequence and appending it to the end of the remaining_elements.
  - type: composition
    container: output_sequence
    contains:
      - remaining_elements (in original relative order)
      - first_element (at the end)
```


## Natural Language Program

1.  Read the input sequence of integers.
2.  Identify the first integer in the sequence.
3.  Create a new sequence containing all integers from the input sequence *except* the first one, maintaining their original relative order.
4.  Append the identified first integer to the end of this new sequence.
5.  Output the resulting sequence.
