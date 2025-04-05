
## train_1

**input:**
```
2 1 0 0 0 0 0 0 2 0 1 2
```


**output:**
```
2 2 2 1 1 0 0 0 0 0 0 0
```


## train_2

**input:**
```
1 1 2 0 1 1 0 1 1 2 1 2
```


**output:**
```
2 2 2 1 1 1 1 1 1 1 0 0
```


## train_3

**input:**
```
2 2 2 0 1 2 0 0 2 0 0 0
```


**output:**
```
2 2 2 2 2 1 0 0 0 0 0 0
```


## train_4

**input:**
```
0 2 2 0 0 0 0 2 0 0 2 0
```


**output:**
```
2 2 2 2 0 0 0 0 0 0 0 0
```


## train_5

**input:**
```
2 1 0 0 1 2 1 0 1 2 0 0
```


**output:**
```
2 2 2 1 1 1 1 0 0 0 0 0
```


## train_6

**input:**
```
1 2 0 2 1 0 0 2 0 0 0 1
```


**output:**
```
2 2 2 1 1 1 0 0 0 0 0 0
```


## train_7

**input:**
```
0 1 0 0 0 0 1 0 0 0 0 0
```


**output:**
```
1 1 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task involves transforming a sequence of single-digit numbers (0, 1, or 2) into another sequence of the same length containing the same digits. Observing the input and output pairs reveals that the output sequence contains the same count of each digit (0, 1, 2) as the input sequence. The key difference is the order: the output sequence is always sorted in descending order (all 2s first, then all 1s, then all 0s).

*   **Facts:**
    
```yaml
    task_type: sequence_transformation
    input_data:
      type: list
      element_type: integer
      possible_values: [0, 1, 2]
      length: variable (observed as 12 in examples)
    output_data:
      type: list
      element_type: integer
      possible_values: [0, 1, 2]
      length: same as input length
      properties: sorted_descending
    transformation:
      action: sort
      order: descending
      preserves_elements: true
      preserves_counts: true
    relationships:
      - The output sequence is a permutation of the input sequence.
      - The output sequence is sorted in descending numerical order.
      - The count of each distinct digit (0, 1, 2) is the same in both the input and output sequences.
    ```


*   **Natural Language Program:**
    1.  Accept the input sequence of digits.
    2.  Sort the digits within the sequence in descending order (from 2 down to 0).
    3.  Return the sorted sequence as the output.
