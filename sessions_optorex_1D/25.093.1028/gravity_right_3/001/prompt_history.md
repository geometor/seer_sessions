
## train_1

**input:**
```
0 8 2 0 5 7 0 0 9 0 6 0
```


**output:**
```
0 0 0 0 0 0 8 2 5 7 9 6
```


## train_2

**input:**
```
1 0 6 0 0 9 0 0 0 7 0 7
```


**output:**
```
0 0 0 0 0 0 0 1 6 9 7 7
```


## train_3

**input:**
```
0 7 0 0 0 9 0 0 3 7 2 0
```


**output:**
```
0 0 0 0 0 0 0 7 9 3 7 2
```


## train_4

**input:**
```
0 0 0 2 0 6 8 0 2 0 0 4
```


**output:**
```
0 0 0 0 0 0 0 2 6 8 2 4
```


## train_5

**input:**
```
9 0 7 0 0 0 6 8 0 2 7 0
```


**output:**
```
0 0 0 0 0 0 9 7 6 8 2 7
```


## train_6

**input:**
```
0 0 4 0 0 7 7 0 0 8 0 8
```


**output:**
```
0 0 0 0 0 0 0 4 7 7 8 8
```


## train_7

**input:**
```
0 0 0 0 0 5 0 5 3 1 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 5 5 3 1
```

*   **Perception of Elements:**
    *   The input and output are sequences of single-digit integers represented as strings separated by spaces.
    *   The sequences contain two types of numbers: zero (0) and non-zero (1-9).
    *   The length of the output sequence is the same as the length of the input sequence.
    *   The multiset of numbers in the output is identical to the multiset of numbers in the input. The transformation is a reordering (permutation) of the input elements.

*   **YAML Facts:**
    
```yaml
    task_description: "Reorder a sequence of single-digit integers."
    input_elements:
      - type: sequence
        description: "A sequence of single-digit integers separated by spaces."
        item_type: integer (0-9)
    output_elements:
      - type: sequence
        description: "A reordered sequence of the input integers, separated by spaces."
        item_type: integer (0-9)
    objects:
      - name: input_sequence
        properties:
          - elements: list of integers
          - length: integer
      - name: output_sequence
        properties:
          - elements: list of integers
          - length: integer (same as input)
      - name: zero_elements
        properties:
          - subset_of: input_sequence
          - value: 0
      - name: non_zero_elements
        properties:
          - subset_of: input_sequence
          - value: range(1, 10)
          - relative_order: maintained from input
    relationships:
      - type: identity
        description: "The multiset of numbers in the output is identical to the input."
      - type: ordering
        description: "All zero elements from the input appear first in the output."
      - type: ordering
        description: "All non-zero elements from the input appear after the zeros in the output."
      - type: relative_ordering
        description: "The relative order of the non-zero elements in the output is the same as their relative order in the input."
    actions:
      - name: parse_input
        description: "Convert the input string into a list of integers."
      - name: partition
        description: "Separate the input list into two lists: one containing only zeros and one containing non-zeros while preserving the relative order of non-zeros."
      - name: concatenate
        description: "Combine the list of zeros followed by the list of non-zeros."
      - name: format_output
        description: "Convert the resulting list of integers back into a space-separated string."

    ```


*   **Natural Language Program:**
    1.  Read the input string representing a sequence of space-separated integers.
    2.  Parse the input string into a list of integers.
    3.  Create two new empty lists: one for zeros (`zeros_list`) and one for non-zeros (`non_zeros_list`).
    4.  Iterate through the parsed list of integers from the input:
        *   If the integer is 0, append it to the `zeros_list`.
        *   If the integer is not 0, append it to the `non_zeros_list`.
    5.  Concatenate the `zeros_list` and the `non_zeros_list` to form the final result list.
    6.  Convert the integers in the result list back to strings.
    7.  Join the string representations of the integers in the result list with spaces to form the output string.
    8.  Output the resulting string.
