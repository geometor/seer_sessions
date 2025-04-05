
## train_1

**input:**
```
7 7 9 6 0 0 0 0 0 9 3 1
```


**output:**
```
0 0 0 0 0 9 3 1 7 7 9 6
```


## train_2

**input:**
```
5 9 2 3 7 5 1 8 8 0 0 0
```


**output:**
```
7 5 1 8 8 0 0 0 5 9 2 3
```


## train_3

**input:**
```
0 0 0 4 9 9 5 2 6 0 0 0
```


**output:**
```
9 9 5 2 6 0 0 0 0 0 0 4
```


## train_4

**input:**
```
0 0 0 0 1 6 9 7 3 3 0 0
```


**output:**
```
1 6 9 7 3 3 0 0 0 0 0 0
```


## train_5

**input:**
```
6 8 3 9 2 5 9 3 5 5 0 0
```


**output:**
```
2 5 9 3 5 5 0 0 6 8 3 9
```


## train_6

**input:**
```
9 0 4 7 5 1 1 2 1 7 1 6
```


**output:**
```
5 1 1 2 1 7 1 6 9 0 4 7
```


## train_7

**input:**
```
4 5 1 0 0 0 0 0 9 6 4 1
```


**output:**
```
0 0 0 0 9 6 4 1 4 5 1 0
```

**Perception:**

The input and output for each task are sequences of integers. The length of the input sequence is consistently 12, and the output sequence also has a length of 12. The core transformation appears to be a rearrangement of the elements within the sequence. Specifically, the sequence seems to be divided into two parts at a fixed position, and these two parts are then swapped to produce the output sequence. All examples consistently show the first four elements of the input sequence being moved to the end of the output sequence, while the remaining eight elements are moved to the beginning.

**Facts:**


```yaml
objects:
  - name: sequence
    properties:
      - type: list of integers
      - length: 12 (constant across examples)
      - elements: individual numbers
actions:
  - name: split
    parameters:
      - sequence: the input sequence
      - index: the position after which to split (observed as 4)
    results:
      - first_part: subsequence from the beginning up to the split index
      - second_part: subsequence from after the split index to the end
  - name: swap_and_concatenate
    parameters:
      - first_part: the initial subsequence
      - second_part: the latter subsequence
    results:
      - output_sequence: the concatenation of second_part followed by first_part
relationships:
  - The output sequence is composed of the same elements as the input sequence, but in a different order.
  - The transformation rule is consistent across all provided examples.
  - The split point is fixed after the 4th element.
```


**Natural Language Program:**

1.  Take the input sequence of 12 integers.
2.  Identify the first four elements as the "first part".
3.  Identify the remaining eight elements (from the 5th to the 12th element) as the "second part".
4.  Construct the output sequence by concatenating the "second part" followed by the "first part".
