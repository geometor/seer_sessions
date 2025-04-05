
## train_1

**input:**
```
0 9 1 8 9 8 6 1 4 4 2 0
```


**output:**
```
0 0 9 1 8 9 8 6 1 4 4 2
```


## train_2

**input:**
```
8 7 9 9 9 8 1 3 9 0 0 0
```


**output:**
```
0 8 7 9 9 9 8 1 3 9 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 2 4 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 4 0 0 0
```


## train_4

**input:**
```
0 0 0 0 4 3 7 3 1 8 0 0
```


**output:**
```
0 0 0 0 0 4 3 7 3 1 8 0
```


## train_5

**input:**
```
0 0 0 0 2 9 5 6 0 0 0 0
```


**output:**
```
0 0 0 0 0 2 9 5 6 0 0 0
```


## train_6

**input:**
```
0 5 8 6 2 3 6 8 7 8 9 0
```


**output:**
```
0 0 5 8 6 2 3 6 8 7 8 9
```


## train_7

**input:**
```
7 9 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 7 9 0 0 0 0 0 0 0 0 0
```

*   **Perception of Task Elements:**
    *   The input and output are both sequences of single digits, represented as space-separated strings.
    *   All provided examples have an input sequence length of 12 and an output sequence length of 12.
    *   The output sequence appears to be derived from the input sequence by inserting a '0' at a specific position and then potentially truncating the result to maintain the original length.
    *   The position of the inserted '0' seems related to the position of the first non-zero digit in the input sequence.
    *   Comparing the input and output sequences reveals that the relative order of the original digits is preserved in the output, but shifted to the right starting from the insertion point. The last element of the sequence after insertion is effectively dropped to maintain the original length.

*   **Facts:**
    
```yaml
    objects:
      - name: input_sequence
        type: list of digits
        properties:
          - length: integer (e.g., 12 in examples)
          - elements: digits (0-9)
      - name: output_sequence
        type: list of digits
        properties:
          - length: integer (same as input_sequence length)
          - elements: digits (0-9)
      - name: target_digit
        value: 0
        role: digit to be inserted
    actions:
      - name: find_first_non_zero_index
        input: input_sequence
        output: index (integer)
        description: Locates the numerical index (0-based) of the first digit in the input_sequence that is not equal to 0.
      - name: insert_digit
        target_object: input_sequence (conceptually, a copy is modified)
        parameters:
          - digit_to_insert: target_digit (0)
          - insertion_index: result of find_first_non_zero_index
        output: intermediate_sequence (list of digits, length = input_sequence length + 1)
        description: Creates a new sequence by inserting the target_digit at the specified insertion_index within the input_sequence. Elements from the insertion_index onwards are shifted right.
      - name: truncate_sequence
        input: intermediate_sequence
        parameters:
          - desired_length: length of original input_sequence
        output: output_sequence
        description: Takes the first 'desired_length' elements of the intermediate_sequence.
    relationships:
      - The output_sequence is derived from the input_sequence through a series of actions: finding an index, inserting a digit at that index, and truncating the result.
      - The length of the output_sequence is constrained to be equal to the length of the input_sequence.
      - The insertion_index is determined by the position of the first non-zero element in the input_sequence.
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of digits. Record its length.
    2.  Iterate through the input sequence from the beginning (index 0) to find the index of the first digit that is not '0'. Let this index be `insertion_index`.
    3.  Create a new sequence by inserting the digit '0' into the input sequence at the `insertion_index`.
    4.  Take the first N elements from the sequence created in step 3, where N is the original length of the input sequence recorded in step 1. This resulting sequence is the output.
