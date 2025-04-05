
## train_1

**input:**
```
0 0 1 0 0 1 1 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 1 1 0 0 0 0 0
```


## train_2

**input:**
```
0 7 0 0 7 0 7 7 7 7 7 7
```


**output:**
```
0 0 0 0 0 0 7 7 7 7 7 7
```


## train_3

**input:**
```
3 3 3 3 3 3 3 0 3 0 0 3
```


**output:**
```
3 3 3 3 3 3 3 0 0 0 0 0
```


## train_4

**input:**
```
0 6 6 6 6 6 6 0 6 0 0 0
```


**output:**
```
0 6 6 6 6 6 6 0 0 0 0 0
```


## train_5

**input:**
```
8 8 8 8 0 0 8 0 0 8 0 0
```


**output:**
```
8 8 8 8 0 0 0 0 0 0 0 0
```


## train_6

**input:**
```
0 0 7 0 0 7 7 7 7 0 7 0
```


**output:**
```
0 0 0 0 0 7 7 7 7 0 0 0
```


## train_7

**input:**
```
4 0 4 0 0 4 4 4 4 4 0 4
```


**output:**
```
0 0 0 0 0 4 4 4 4 4 0 0
```

## Perception

The task involves transforming an input sequence of 12 integers into an output sequence of the same length. The transformation logic focuses on identifying contiguous blocks (groups) of non-zero numbers within the input sequence. The core operation is to filter these groups based on their length, keeping only the longest group(s) and replacing all other elements (including shorter non-zero groups and original zeros) with zeros in the output.

**Observations:**

1.  **Input/Output Format:** Both input and output are fixed-length sequences (length 12) of single-digit integers.
2.  **Grouping:** The key operation involves identifying contiguous runs of non-zero numbers. Zeros act as separators between these groups. The specific non-zero value within a group does not seem to affect the grouping itself, only its distinction from zero.
3.  **Filtering Logic:** The primary criterion for keeping a group is its length (number of consecutive non-zero elements). Only the group(s) with the maximum length found in the input sequence are preserved in the output.
4.  **Output Construction:** The output sequence is constructed by placing the longest group(s) from the input into an initially zero-filled sequence at their original positions. Elements belonging to shorter non-zero groups or original zero elements become zero in the output.

## Facts


```yaml
objects:
  - name: sequence
    properties:
      - type: list of integers
      - length: 12
      - elements: integers (0-9 observed)
  - name: group
    properties:
      - type: contiguous sub-sequence
      - composition: consists of one or more non-zero integers
      - boundaries: delimited by zeros or sequence ends
      - attributes:
          - start_index: integer
          - end_index: integer
          - length: integer (number of elements)
          - elements: list of non-zero integers from the input sequence

actions:
  - name: identify_groups
    description: Scan the input sequence to find all contiguous groups of non-zero numbers.
    inputs:
      - input_sequence: sequence
    outputs:
      - list_of_groups: list of group objects (each with start_index, end_index, length)
  - name: find_max_length
    description: Determine the maximum length among all identified groups.
    inputs:
      - list_of_groups: list of group objects
    outputs:
      - max_length: integer
  - name: filter_groups
    description: Select only those groups whose length equals the maximum length.
    inputs:
      - list_of_groups: list of group objects
      - max_length: integer
    outputs:
      - longest_groups: list of group objects
  - name: construct_output
    description: Create the output sequence by placing the elements of the longest groups at their original positions in a sequence otherwise filled with zeros.
    inputs:
      - input_sequence: sequence
      - longest_groups: list of group objects
      - sequence_length: integer (e.g., 12)
    outputs:
      - output_sequence: sequence

relationships:
  - A group's elements are a subset of the input sequence's elements.
  - The output sequence preserves elements from the input sequence only if they belong to a group with the maximum length.
  - All other positions in the output sequence are filled with zero.
```


## Natural Language Program

1.  Initialize an empty list to store information about identified non-zero groups (start index, end index, length).
2.  Iterate through the input sequence, identifying the start and end indices of each contiguous group of non-zero numbers. For each group found, record its start index, end index, and calculate its length. Add this information to the list of groups.
3.  If no non-zero groups are found, the output is a sequence of zeros of the same length as the input.
4.  If groups were found, determine the maximum length among all recorded groups.
5.  Initialize an output sequence of the same length as the input, filled entirely with zeros.
6.  Iterate through the recorded list of groups. For each group whose length is equal to the determined maximum length:
    a.  Retrieve the segment of the original input sequence corresponding to this group (from its start index to its end index).
    b.  Copy this segment into the output sequence at the same indices.
7.  Return the constructed output sequence.
