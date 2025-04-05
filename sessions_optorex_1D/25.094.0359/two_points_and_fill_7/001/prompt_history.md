
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 2 2
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 2 2
```


## train_2

**input:**
```
0 2 0 0 0 0 0 2 0 0 0 0
```


**output:**
```
0 2 2 2 2 2 2 2 0 0 0 0
```


## train_3

**input:**
```
2 0 0 0 0 2 0 0 0 0 0 0
```


**output:**
```
2 2 2 2 2 2 0 0 0 0 0 0
```


## train_4

**input:**
```
4 0 4 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4 4 0 0 0 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 1 0 0 0 1 0 0
```


**output:**
```
0 0 0 0 0 1 1 1 1 1 0 0
```


## train_6

**input:**
```
0 7 0 0 0 0 0 7 0 0 0 0
```


**output:**
```
0 7 7 7 7 7 7 7 0 0 0 0
```


## train_7

**input:**
```
0 0 3 0 3 0 0 0 0 0 0 0
```


**output:**
```
0 0 3 3 3 0 0 0 0 0 0 0
```

## Perception of Elements:

The task involves processing a one-dimensional array (list) of single-digit integers. The core operation seems to be identifying specific patterns of non-zero numbers and modifying the zeros located between them. The key elements are:
1.  **Input/Output:** A list of integers.
2.  **Significant Values:** Non-zero integers. The value `0` acts as a placeholder or gap filler.
3.  **Pattern:** The presence of exactly two instances of the *same* non-zero integer within the list.
4.  **Action:** Filling the sequence of zeros (`0`) located *between* these two identical non-zero integers with the value of those integers.
5.  **Condition:** This filling action only occurs if there are precisely two instances of a specific non-zero digit. If the non-zero digits are adjacent (no zeros between them), or if there's only one instance, or more than two instances, or multiple different non-zero digits, the input remains unchanged.

## YAML Facts:


```yaml
objects:
  - name: input_array
    type: list
    contains: integers (0-9)
  - name: output_array
    type: list
    contains: integers (0-9)
  - name: non_zero_digit
    type: integer
    properties:
      - value > 0
      - count_in_array
      - indices_in_array
  - name: zero_digit
    type: integer
    properties:
      - value == 0
      - acts_as_gap

relationships:
  - type: spatial
    description: Zeros located between two instances of the same non_zero_digit.
  - type: conditional
    description: The transformation depends on the count of each unique non_zero_digit.

actions:
  - name: identify_non_zero_digits
    input: input_array
    output: list of unique non_zero_digits and their indices
  - name: count_occurrences
    input: unique non_zero_digit, input_array
    output: count
  - name: find_indices
    input: unique non_zero_digit, input_array
    output: list of indices
  - name: fill_gap
    input: array, start_index, end_index, fill_value
    output: modified_array
    condition: >
      A unique non_zero_digit occurs exactly twice.
      The start_index and end_index correspond to the positions of this digit.
      The fill_value is the value of this digit.

goal:
  - Transform input_array to output_array by conditionally filling gaps between pairs of identical non-zero digits.
```


## Natural Language Program:

1.  Examine the input array to identify all unique non-zero digits present.
2.  For each unique non-zero digit identified:
    a.  Count how many times this digit appears in the input array.
    b.  If the count is exactly two:
        i.  Find the first index (`idx1`) and the second index (`idx2`) where this digit appears.
        ii. Create a copy of the input array.
        iii. Change the value of all elements in the copied array from index `idx1 + 1` up to (but not including) index `idx2` to the value of the non-zero digit identified in step 2.
        iv. Return this modified array as the output.
3.  If, after checking all unique non-zero digits, none were found to occur exactly twice, return the original input array unchanged.
