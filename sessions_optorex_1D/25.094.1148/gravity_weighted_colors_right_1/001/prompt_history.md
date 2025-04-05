
## train_1

**input:**
```
0 2 0 1 1 2 0 0 1 0 1 1
```


**output:**
```
2 2 1 1 1 1 1 0 0 0 0 0
```


## train_2

**input:**
```
1 1 0 2 0 2 1 0 1 1 1 0
```


**output:**
```
2 2 1 1 1 1 1 1 0 0 0 0
```


## train_3

**input:**
```
0 1 2 1 2 0 0 0 1 0 2 1
```


**output:**
```
2 2 2 1 1 1 1 0 0 0 0 0
```


## train_4

**input:**
```
2 2 2 0 0 2 1 0 2 1 1 1
```


**output:**
```
2 2 2 2 2 1 1 1 1 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 1 1 0 1 1 2
```


**output:**
```
2 1 1 1 1 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 1 2 0 1 1 2 0 0 0 0 0
```


**output:**
```
2 2 1 1 1 0 0 0 0 0 0 0
```


## train_7

**input:**
```
0 2 0 0 0 0 1 2 0 1 0 2
```


**output:**
```
2 2 2 1 1 0 0 0 0 0 0 0
```

## Perception

The input and output are both sequences of integers, specifically containing only the digits 0, 1, and 2. Each sequence appears to have a fixed length of 12 elements. By comparing the input and output sequences across multiple examples, a consistent pattern emerges: the output sequence contains the same integers as the input sequence, but they are arranged in a different order. Specifically, the output sequence seems to be sorted in descending order (from largest to smallest value).

## Facts


```yaml
task_elements:
  - name: input_sequence
    type: List[int]
    description: A sequence of 12 integers, containing only values 0, 1, or 2.
    properties:
      length: 12
      elements: [0, 1, 2]
  - name: output_sequence
    type: List[int]
    description: A sequence of 12 integers derived from the input sequence.
    properties:
      length: 12
      elements: [0, 1, 2]
      relationship_to_input: Contains the same multiset of elements as the input sequence.

transformation:
  action: sort
  input: input_sequence
  output: output_sequence
  rule: The elements of the input sequence are rearranged to produce the output sequence.
  details: The rearrangement follows a descending order sort rule (largest values appear first).
```


## Natural Language Program

1.  Take the input sequence of 12 integers.
2.  Sort the integers within the sequence in descending order (from largest to smallest).
3.  Return the sorted sequence as the output.
