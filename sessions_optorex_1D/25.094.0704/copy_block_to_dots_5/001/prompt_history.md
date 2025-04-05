
## train_1

**input:**
```
1 1 1 0 0 0 0 0 0 1 0 0
```


**output:**
```
1 1 1 0 0 0 0 0 1 1 1 0
```


## train_2

**input:**
```
1 1 1 0 0 0 1 0 0 0 0 0
```


**output:**
```
1 1 1 0 0 1 1 1 0 0 0 0
```


## train_3

**input:**
```
7 7 7 0 0 7 0 0 0 0 0 0
```


**output:**
```
7 7 7 0 7 7 7 0 0 0 0 0
```


## train_4

**input:**
```
7 7 7 0 0 7 0 0 0 7 0 0
```


**output:**
```
7 7 7 0 7 7 7 0 7 7 7 0
```


## train_5

**input:**
```
4 4 4 0 0 0 0 0 0 4 0 0
```


**output:**
```
4 4 4 0 0 0 0 0 4 4 4 0
```


## train_6

**input:**
```
5 5 5 0 0 0 5 0 0 0 0 0
```


**output:**
```
5 5 5 0 0 5 5 5 0 0 0 0
```


## train_7

**input:**
```
3 3 3 0 0 3 0 0 0 0 0 0
```


**output:**
```
3 3 3 0 3 3 3 0 0 0 0 0
```

*   **Perception of Elements:**
    *   The input and output are fixed-length sequences (12 elements) of single-digit integers.
    *   Each sequence consists primarily of zeros (`0`) and a single recurring non-zero digit (e.g., `1`, `7`, `4`, `5`, `3`). Let's call this the "active digit".
    *   The active digit typically appears in a block at the beginning of the sequence (e.g., `1 1 1`, `7 7 7`).
    *   The active digit may also appear sporadically later in the input sequence, surrounded by zeros.
    *   The transformation seems to involve "expanding" these later occurrences of the active digit.

*   **YAML Facts:**
    
```yaml
    task_description: Transform a sequence of 12 digits based on the position of a specific non-zero digit.
    elements:
      - sequence:
          type: List[int]
          length: 12
      - active_digit:
          type: int
          property: non-zero
          role: primary value and trigger
      - zero:
          type: int
          value: 0
          role: background/placeholder
    actions:
      - identify: Find the non-zero active_digit (usually the first element).
      - scan: Iterate through the input sequence.
      - trigger: An occurrence of the active_digit after the initial block (index > 2).
      - replace: Modify the output sequence based on trigger locations.
    transformation:
      - rule: For each trigger active_digit found at index 'i' in the input (where i > 2), set the elements at indices i-1, i, and i+1 in the output sequence to the active_digit.
      - initialization: The output sequence starts as a copy of the input sequence.
      - scope: Replacements modify the output based on the *original* input triggers.
    relationships:
      - The active_digit defines the value used for replacement.
      - The position (index 'i') of a trigger active_digit in the input determines the location (indices i-1, i, i+1) of the replacement block in the output.
    ```


*   **Natural Language Program:**
    1.  Initialize the output sequence as an identical copy of the input sequence.
    2.  Identify the non-zero "active digit" (this is typically the digit found at the first index of the input sequence).
    3.  Iterate through the *input* sequence from the 4th element (index 3) up to the 11th element (index 10).
    4.  For each element examined at index `i`:
        *   If the element at index `i` in the *input* sequence is equal to the "active digit":
            *   Modify the *output* sequence by setting the elements at index `i-1`, index `i`, and index `i+1` to the "active digit".
    5.  Return the modified output sequence.
