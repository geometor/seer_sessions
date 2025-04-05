
## train_1

**input:**
```
0 8 8 8 8 0 0 0 0 0 0 2
```


**output:**
```
0 0 8 8 8 8 0 0 0 0 0 2
```


## train_2

**input:**
```
0 0 2 0 0 0 0 0 0 4 4 4
```


**output:**
```
0 0 2 0 0 0 0 0 4 4 4 0
```


## train_3

**input:**
```
0 0 2 0 0 0 7 7 7 7 7 0
```


**output:**
```
0 0 2 0 0 7 7 7 7 7 0 0
```


## train_4

**input:**
```
4 4 4 4 4 4 4 4 4 4 2 0
```


**output:**
```
4 4 4 4 4 4 4 4 4 4 2 0
```


## train_5

**input:**
```
3 3 3 0 2 0 0 0 0 0 0 0
```


**output:**
```
0 3 3 3 2 0 0 0 0 0 0 0
```


## train_6

**input:**
```
2 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
2 8 8 8 8 8 8 8 8 8 8 8
```


## train_7

**input:**
```
0 0 0 0 0 3 3 3 3 3 3 2
```


**output:**
```
0 0 0 0 0 3 3 3 3 3 3 2
```

Okay, let's analyze the transformation.

**Perception of Task Elements:**

1.  **Input/Output Format:** Both input and output are sequences (lists) of single-digit integers.
2.  **Core Object:** The primary element being manipulated appears to be a *contiguous subsequence* of identical non-zero numbers.
3.  **Key Operation:** The transformation involves potentially *swapping* this identified subsequence with an adjacent element.
4.  **Condition:** The swap operation is conditional, depending on the values of the elements immediately *neighboring* the subsequence. Specifically, the value `2` acts as a blocker for the swap.
5.  **Target Subsequence:** The rule focuses on the *longest* such contiguous subsequence of identical non-zero numbers within the list.
6.  **Swap Direction:** The direction of the swap (with the preceding or succeeding element) depends on whether the subsequence starts at the beginning of the list.

**Facts:**


```yaml
objects:
  - name: input_list
    type: list
    properties:
      - elements: single-digit integers (0-9)
  - name: output_list
    type: list
    properties:
      - elements: single-digit integers (0-9)
      - derived_from: input_list
  - name: subsequence
    type: list
    properties:
      - elements: identical non-zero integers
      - contiguous: true
      - length: variable
      - location: defined by start_index and end_index within input_list
      - characteristic: longest matching sequence in the input_list
  - name: preceding_element
    type: integer
    properties:
      - location: input_list[start_index - 1]
      - exists: if start_index > 0
  - name: succeeding_element
    type: integer
    properties:
      - location: input_list[end_index + 1]
      - exists: if end_index < length(input_list) - 1
  - name: blocker_value
    type: integer
    value: 2

actions:
  - name: find_longest_subsequence
    input: input_list
    output: subsequence (including its start_index, end_index, and value)
    description: Iterates through the list to find the longest run of identical non-zero numbers.
  - name: check_neighbors
    input: input_list, subsequence (start_index, end_index)
    output: boolean (swap_allowed)
    description: Checks if preceding_element (if exists) is not 2 AND succeeding_element (if exists) is not 2.
  - name: perform_swap
    input: input_list, subsequence (start_index, end_index), swap_allowed
    output: output_list
    description: >
      If swap_allowed is true:
      If start_index > 0, swaps the subsequence (elements from start_index to end_index)
      with the preceding_element (at start_index - 1).
      If start_index == 0, swaps the subsequence (elements from start_index to end_index)
      with the succeeding_element (at end_index + 1).
      If swap_allowed is false, returns the input_list unchanged.

relationships:
  - The output_list is a transformation of the input_list.
  - The transformation centers around the longest contiguous subsequence of identical non-zero numbers.
  - The applicability of the swap action depends on the values of the elements adjacent to this subsequence.
  - The value '2' specifically prevents the swap action if it is adjacent to the subsequence.
```


**Natural Language Program:**

1.  Identify the longest contiguous sequence of identical non-zero numbers within the input list. If there are multiple sequences of the same maximum length, choose the first one encountered. If no such sequence exists (e.g., all zeros, or no repeated non-zero numbers), return the input list unchanged.
2.  Note the starting index (`start_index`) and ending index (`end_index`) of this identified sequence.
3.  Check the element immediately *before* the sequence (at `start_index - 1`), if it exists (`start_index > 0`). Let's call its value `pre_neighbor`.
4.  Check the element immediately *after* the sequence (at `end_index + 1`), if it exists (`end_index < length of list - 1`). Let's call its value `post_neighbor`.
5.  Determine if a swap should occur: The swap occurs if *neither* existing neighbor is equal to `2`. That is, if (`start_index == 0` OR `pre_neighbor != 2`) AND (`end_index == length of list - 1` OR `post_neighbor != 2`).
6.  If the swap condition is met:
    *   If the sequence starts at the beginning of the list (`start_index == 0`), swap the entire sequence with the element immediately following it (`post_neighbor` at `end_index + 1`).
    *   Otherwise (if `start_index > 0`), swap the entire sequence with the element immediately preceding it (`pre_neighbor` at `start_index - 1`).
7.  If the swap condition is *not* met, return the input list unchanged.
8.  Return the modified (or unchanged) list as the output.
