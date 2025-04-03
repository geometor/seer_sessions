
## train_1

**input:**
```
0 0 0 5 2 9 9 7 6 0 0 0
```


**output:**
```
0 5 2 9 9 7 6 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 5 5 8 1 2 2 1 1 8
```


**output:**
```
0 5 5 8 1 2 2 1 1 8 0 0
```


## train_3

**input:**
```
0 0 0 0 0 1 9 0 0 0 0 0
```


**output:**
```
0 0 0 1 9 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 1 0 0
```


**output:**
```
0 0 0 0 0 0 0 1 0 0 0 0
```


## train_5

**input:**
```
0 0 0 7 5 6 5 2 2 3 1 3
```


**output:**
```
0 7 5 6 5 2 2 3 1 3 0 0
```


## train_6

**input:**
```
0 0 0 3 7 9 7 9 4 8 0 0
```


**output:**
```
0 3 7 9 7 9 4 8 0 0 0 0
```


## train_7

**input:**
```
0 0 0 5 9 1 2 7 5 0 0 0
```


**output:**
```
0 5 9 1 2 7 5 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The input and output are lists (or sequences) of single-digit integers.
    *   All input and output lists in the examples have the same length (12).
    *   The core transformation involves rearranging the positions of the elements, specifically the zero elements.
    *   The relative order of the non-zero elements appears to be preserved between input and output.
    *   The relative order of the zero elements amongst themselves is *not* necessarily preserved; specifically, leading zeros are moved.
    *   Comparing inputs and outputs, it appears that exactly two leading zeros from the input are moved to the end of the list in the output, while the rest of the elements maintain their relative order.

*   **Facts:**
    
```yaml
    objects:
      - name: data_list
        type: list
        properties:
          - elements: list of integers (0-9)
          - length: fixed (12 in examples)
      - name: element
        type: integer
        properties:
          - value: 0-9
          - is_zero: boolean (value == 0)
          - position: index within the list
          - role: leading_zero (element is 0 and appears before the first non-zero element)

    actions:
      - name: identify_leading_zeros
        input: data_list
        output: count or slice of leading zeros
      - name: remove_elements
        target: data_list
        elements: specific elements (e.g., first two)
      - name: append_elements
        target: data_list
        elements: specific elements (e.g., two zeros)
      - name: shift_elements
        description: Changing the position of elements while potentially preserving relative order.

    relationships:
      - type: relative_order
        description: The order of non-zero elements relative to each other remains unchanged.
      - type: transformation
        input: data_list
        output: data_list
        rule: The first two elements of the input list, if they are both zeros, are moved to the end of the list.
    ```


*   **Natural Language Program:**
    1.  Examine the first two elements of the input list.
    2.  If both the first and second elements are 0, create the output list by:
        a.  Taking the sub-list starting from the third element to the end of the input list.
        b.  Appending two 0s to the end of this sub-list.
    3.  Otherwise (if the first or second element is not 0, or the list has fewer than two elements), the output list is identical to the input list.
