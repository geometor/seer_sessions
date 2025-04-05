
## train_1

**input:**
```
0 3 3 3 0 0 3 3 3 3 3 0
```


**output:**
```
0 2 2 2 0 0 1 1 1 1 1 0
```


## train_2

**input:**
```
3 3 3 3 3 3 0 3 3 3 3 0
```


**output:**
```
1 1 1 1 1 1 0 2 2 2 2 0
```


## train_3

**input:**
```
0 0 3 3 3 3 0 0 3 3 3 0
```


**output:**
```
0 0 1 1 1 1 0 0 2 2 2 0
```


## train_4

**input:**
```
0 0 0 0 0 3 3 0 3 3 3 0
```


**output:**
```
0 0 0 0 0 2 2 0 1 1 1 0
```


## train_5

**input:**
```
0 0 3 3 0 0 0 0 3 3 3 3
```


**output:**
```
0 0 2 2 0 0 0 0 1 1 1 1
```


## train_6

**input:**
```
0 3 3 3 3 3 0 0 3 3 0 0
```


**output:**
```
0 1 1 1 1 1 0 0 2 2 0 0
```


## train_7

**input:**
```
0 0 0 3 3 0 3 3 3 3 3 0
```


**output:**
```
0 0 0 2 2 0 1 1 1 1 1 0
```

**Perception:**

The input and output consist of sequences of single digits. The input sequences contain only the digits '0' and '3'. The output sequences contain '0', '1', and '2'. The length of the output sequence is always identical to the length of the input sequence.

The digit '0' appears to act as a separator and remains unchanged in the output. The transformation rule applies specifically to contiguous groups (or runs) of the digit '3'. All examples show exactly two such groups of '3's separated by '0's.

The core logic involves identifying these two groups of '3's, comparing their lengths, and then replacing each group with a sequence of either '1's or '2's based on this comparison. The group that appeared first in the input sequence (left-to-right) is designated as Group 1, and the second as Group 2. The replacement value ('1' or '2') depends on whether Group 1 is shorter or longer than Group 2.

**Facts:**


```yaml
objects:
  - name: sequence
    type: list of integers
    description: Represents both the input and output data structures.
  - name: segment
    type: contiguous sub-sequence of identical digits
    description: The sequence can be broken down into segments (e.g., [0, 0], [3, 3, 3], [0]).
  - name: group_of_zeros
    type: segment
    properties:
      - value: 0
    description: A segment consisting only of zeros.
  - name: group_of_threes
    type: segment
    properties:
      - value: 3
      - length: integer (number of digits in the group)
      - order: integer (1st, 2nd group of threes encountered)
    description: A segment consisting only of threes. The examples provided always contain exactly two such groups.

relationships:
  - type: comparison
    between: [group_of_threes (order 1), group_of_threes (order 2)]
    property: length
    result: determines which group transforms to '1's and which to '2's.

actions:
  - name: identify_segments
    input: sequence
    output: list of segments
    description: Break the input sequence into contiguous segments of identical digits.
  - name: filter_groups_of_threes
    input: list of segments
    output: ordered list of group_of_threes (Group 1, Group 2)
    description: Extract the segments containing only '3's, preserving their order of appearance.
  - name: compare_lengths
    input: [Group 1, Group 2]
    output: comparison result (Group 1 shorter, Group 1 longer)
    description: Compare the lengths of the two identified groups of threes.
  - name: transform_group
    input: group_of_threes, target_digit (1 or 2)
    output: segment (of target_digit with same length)
    description: Replace a group of threes with a segment of the same length, filled with the target digit.
  - name: preserve_zeros
    input: group_of_zeros
    output: group_of_zeros
    description: Groups of zeros remain unchanged.
  - name: reconstruct_sequence
    input: list of transformed/preserved segments
    output: final output sequence
    description: Combine the segments back in their original order.
```


**Natural Language Program:**

1.  Process the input sequence from left to right to identify contiguous segments of identical digits.
2.  Isolate the segments that consist solely of the digit '3'. Label these segments as `Group 1` and `Group 2` based on their order of appearance in the input sequence. (The provided examples always have exactly two such groups).
3.  Keep track of the segments consisting solely of the digit '0'; these will remain unchanged.
4.  Compare the length (number of digits) of `Group 1` with the length of `Group 2`.
5.  If the length of `Group 1` is less than the length of `Group 2`:
    a.  Replace every '3' in `Group 1` with the digit '2'.
    b.  Replace every '3' in `Group 2` with the digit '1'.
6.  If the length of `Group 1` is greater than the length of `Group 2`:
    a.  Replace every '3' in `Group 1` with the digit '1'.
    b.  Replace every '3' in `Group 2` with the digit '2'.
7.  (Handle the case where lengths are equal, if necessary, though not present in examples. A default might be G1->1, G2->2 or vice versa).
8.  Reconstruct the output sequence by concatenating the preserved '0' segments and the newly transformed '1' or '2' segments in their original order.
