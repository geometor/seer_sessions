
## train_1

**input:**
```
0 0 0 0 5 5 0 5 0 5 5 5
```


**output:**
```
0 0 0 0 5 5 5 0 5 5 0 5
```


## train_2

**input:**
```
0 0 0 0 4 0 4 4 4 0 4 4
```


**output:**
```
0 0 0 0 4 4 4 0 4 4 0 4
```


## train_3

**input:**
```
0 0 0 0 6 0 6 6 6 0 6 6
```


**output:**
```
0 0 0 0 6 6 6 0 6 6 0 6
```


## train_4

**input:**
```
0 0 0 0 3 0 3 3 0 3 3 3
```


**output:**
```
0 0 0 0 3 3 3 0 3 3 0 3
```


## train_5

**input:**
```
0 0 0 0 2 2 2 0 2 0 2 2
```


**output:**
```
0 0 0 0 2 2 2 0 2 2 0 2
```


## train_6

**input:**
```
0 0 0 0 7 7 7 0 7 0 7 7
```


**output:**
```
0 0 0 0 7 7 7 0 7 7 0 7
```


## train_7

**input:**
```
0 0 0 0 1 0 1 1 1 0 1 1
```


**output:**
```
0 0 0 0 1 1 1 0 1 1 0 1
```

*   **Perception:**
    *   The input and output are sequences of 12 single-digit integers.
    *   Both input and output sequences consistently start with `0 0 0 0`.
    *   The remaining 8 digits (from index 4 to 11) in the input contain zeros and repetitions of a single non-zero digit (let's call it the 'significant digit', X). The pattern of zeros and X varies across inputs.
    *   The transformation only affects the sequence from index 4 onwards.
    *   The output sequence from index 4 to 11 always follows a fixed pattern relative to the significant digit X: `X X X 0 X X 0 X`.
    *   The significant digit X is determined from the input sequence (it's the first non-zero digit encountered).

*   **YAML Facts:**
    
```yaml
    task_elements:
      - object: sequence
        properties:
          format: list of 12 integers
          structure: consists of a prefix and a suffix
      - object: prefix
        properties:
          location: indices 0-3
          value: [0, 0, 0, 0]
          relation: constant across all examples, identical in input and output
      - object: suffix
        properties:
          location: indices 4-11
          length: 8
          input_content: contains zeros and multiple instances of a significant non-zero digit (X)
          output_content: follows a fixed pattern based on X
      - object: significant_digit (X)
        properties:
          value: the first non-zero digit found in the input sequence
          relation: determines the non-zero values in the output suffix
      - object: output_suffix_pattern
        properties:
          value: [X, X, X, 0, X, X, 0, X]
          relation: replaces the input suffix in the output

    transformation:
      action: replace
      input_object: input suffix (indices 4-11)
      output_object: output suffix (indices 4-11)
      rule: Identify the significant digit (X) from the input. Construct the output suffix using the pattern [X, X, X, 0, X, X, 0, X]. Combine the original prefix [0, 0, 0, 0] with the new suffix.
    ```


*   **Natural Language Program:**
    1.  Parse the input sequence of 12 digits.
    2.  Identify the significant non-zero digit (X) present in the input sequence (it will be the first non-zero digit).
    3.  Keep the first four digits (which are always `0 0 0 0`) as the prefix of the output sequence.
    4.  Construct the suffix of the output sequence (for indices 4 through 11) using the fixed pattern: `X, X, X, 0, X, X, 0, X`, where X is the significant digit identified in step 2.
    5.  Concatenate the prefix and the constructed suffix to form the final 12-digit output sequence.
