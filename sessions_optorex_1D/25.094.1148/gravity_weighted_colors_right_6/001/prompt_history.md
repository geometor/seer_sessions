
## train_1

**input:**
```
0 0 2 1 2 0 0 2 1 0 1 1
```


**output:**
```
2 2 2 1 1 1 1 0 0 0 0 0
```


## train_2

**input:**
```
0 1 1 2 0 2 1 0 0 1 2 2
```


**output:**
```
2 2 2 2 1 1 1 1 0 0 0 0
```


## train_3

**input:**
```
0 0 0 2 0 0 1 0 0 0 1 2
```


**output:**
```
2 2 1 1 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
1 0 2 0 1 0 2 2 0 0 0 2
```


**output:**
```
2 2 2 2 1 1 0 0 0 0 0 0
```


## train_5

**input:**
```
2 0 1 1 0 1 2 0 0 2 0 1
```


**output:**
```
2 2 2 1 1 1 1 0 0 0 0 0
```


## train_6

**input:**
```
2 0 2 2 1 0 0 0 2 0 0 2
```


**output:**
```
2 2 2 2 2 1 0 0 0 0 0 0
```


## train_7

**input:**
```
0 2 2 0 1 2 2 0 0 0 0 1
```


**output:**
```
2 2 2 2 1 1 0 0 0 0 0 0
```

*   **Perception of Task Elements:**
    *   The input is a sequence of integers, specifically the digits 0, 1, and 2, presented as a space-separated string.
    *   The output is also a sequence of the same digits (0, 1, 2), presented in the same format (space-separated string).
    *   The length of the input sequence is consistently 12 digits across all examples.
    *   The length of the output sequence is always identical to the length of the corresponding input sequence.
    *   The core transformation appears to be a reordering of the input digits.
    *   Comparing the input and output sequences, the output sequence always contains the same digits as the input, but arranged in descending order (all 2s first, then all 1s, then all 0s). The counts of each digit (0, 1, 2) are preserved between input and output.

*   **YAML Fact Document:**
    
```yaml
    task_elements:
      - object: input_sequence
        properties:
          - type: string
          - format: space-separated integers
          - allowed_values: [0, 1, 2]
          - length: 12 (observed in examples)
      - object: output_sequence
        properties:
          - type: string
          - format: space-separated integers
          - allowed_values: [0, 1, 2]
          - length: same as input_sequence
    relationships:
      - type: transformation
        action: sorting
        input: input_sequence
        output: output_sequence
        details: The digits from the input_sequence are sorted in descending order (2 > 1 > 0) to produce the output_sequence.
      - type: constraint
        property: element_conservation
        description: The multiset of digits in the input_sequence is identical to the multiset of digits in the output_sequence.
      - type: constraint
        property: length_conservation
        description: The length of the output_sequence is equal to the length of the input_sequence.
    ```


*   **Natural Language Program:**
    1.  Parse the input string into a sequence of individual integers.
    2.  Sort this sequence of integers in descending numerical order.
    3.  Format the sorted sequence back into a space-separated string.
    4.  Output the resulting string.
