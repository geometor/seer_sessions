
## train_1

**input:**
```
0 2 2 0 0 2 2 2 2 2 2 0
```


**output:**
```
0 8 2 0 0 8 8 8 2 2 2 0
```


## train_2

**input:**
```
0 0 2 2 0 0 0 2 2 2 0 0
```


**output:**
```
0 0 8 2 0 0 0 8 2 2 0 0
```


## train_3

**input:**
```
0 2 2 0 2 2 0 2 2 0 0 0
```


**output:**
```
0 8 2 0 8 2 0 8 2 0 0 0
```


## train_4

**input:**
```
0 2 2 2 2 0 0 0 2 2 0 0
```


**output:**
```
0 8 8 2 2 0 0 0 8 2 0 0
```


## train_5

**input:**
```
0 2 2 0 0 2 2 2 2 0 0 0
```


**output:**
```
0 8 2 0 0 8 8 2 2 0 0 0
```


## train_6

**input:**
```
2 2 2 0 2 2 0 0 0 0 0 0
```


**output:**
```
8 2 2 0 8 2 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 2 2 2 2 0 0 0 2 2 0
```


**output:**
```
0 0 8 8 2 2 0 0 0 8 2 0
```

**Perception:**

The task involves transforming a sequence of single-digit integers (specifically 0s and 2s) into another sequence of the same length, containing 0s, 2s, and 8s. The transformation rule appears to operate locally, focusing on consecutive runs of the digit '2'. The digit '0' seems to remain unchanged in all positions. The digit '2' is sometimes changed to '8', and sometimes remains '2'. The change from '2' to '8' depends on the position of the '2' within a contiguous block of '2's. Specifically, for any consecutive sequence of '2's of length N, the first `floor(N / 2)` elements are transformed into '8's, while the subsequent elements in that sequence remain '2's.

**Facts:**


```yaml
objects:
  - name: input_sequence
    type: list of integers
    properties:
      - contains digits 0 and 2
  - name: output_sequence
    type: list of integers
    properties:
      - contains digits 0, 2, and 8
      - same length as input_sequence
  - name: subsequence_of_twos
    type: contiguous block of '2's within the input sequence
    properties:
      - length: N (integer > 0)
actions:
  - name: identify_subsequences
    description: Find all maximal contiguous subsequences composed entirely of the digit '2' in the input sequence.
  - name: transform_subsequence
    description: For each identified subsequence of '2's with length N, change the first floor(N / 2) elements from '2' to '8'.
  - name: copy_elements
    description: Elements in the input sequence that are '0' or are '2's not part of the first floor(N/2) elements of a subsequence remain unchanged in the output sequence.
relationships:
  - The transformation of an element depends on its value and its position within a consecutive run of identical elements ('2's).
  - The number of '2's changed to '8's within a subsequence is determined by the integer division of the subsequence length (N) by 2.
```


**Natural Language Program:**

1.  Initialize an empty output sequence with the same length as the input sequence.
2.  Iterate through the input sequence, identifying the start and end indices of all maximal contiguous subsequences consisting solely of the digit '2'. Keep track of the indices that belong to these subsequences.
3.  For each identified subsequence of '2's starting at index `start`, ending at index `end`, and having length `N = end - start + 1`:
    a.  Calculate the number of elements to change: `num_to_change = N // 2` (integer division).
    b.  For the first `num_to_change` elements within this subsequence (from index `start` to `start + num_to_change - 1`), set the corresponding elements in the output sequence to '8'.
    c.  For the remaining elements within this subsequence (from index `start + num_to_change` to `end`), set the corresponding elements in the output sequence to '2'.
4.  Iterate through the input sequence again. For any element at an index `i` that was *not* part of any identified subsequence of '2's (meaning the input element must be '0'), copy the input element to the corresponding position `i` in the output sequence.
5.  Return the completed output sequence.
