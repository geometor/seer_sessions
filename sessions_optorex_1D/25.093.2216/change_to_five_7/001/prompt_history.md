
## train_1

**input:**
```
8 1 9 0 7 6 8 0 0 3 0 0
```


**output:**
```
5 5 5 0 5 5 5 0 0 5 0 0
```


## train_2

**input:**
```
6 7 3 1 8 1 0 3 7 4 3 5
```


**output:**
```
5 5 5 5 5 5 0 5 5 5 5 5
```


## train_3

**input:**
```
9 2 1 0 6 4 0 0 5 5 3 1
```


**output:**
```
5 5 5 0 5 5 0 0 5 5 5 5
```


## train_4

**input:**
```
8 1 0 0 3 1 0 5 0 0 6 9
```


**output:**
```
5 5 0 0 5 5 0 5 0 0 5 5
```


## train_5

**input:**
```
8 5 8 2 3 9 0 9 0 7 0 0
```


**output:**
```
5 5 5 5 5 5 0 5 0 5 0 0
```


## train_6

**input:**
```
0 0 7 2 0 0 1 5 1 0 5 0
```


**output:**
```
0 0 5 5 0 0 5 5 5 0 5 0
```


## train_7

**input:**
```
2 0 0 0 6 0 9 4 6 8 0 4
```


**output:**
```
5 0 0 0 5 0 5 5 5 5 0 5
```

**Perception:**

The input and output are sequences of single-digit integers of the same length. The transformation operates on each element of the input sequence independently to produce the corresponding element in the output sequence. The rule seems to depend solely on whether the input element is zero or non-zero. Specifically, zeros in the input map to zeros in the output, and any non-zero digit (1 through 9) in the input maps to the digit 5 in the output.

**Facts:**


```yaml
task_description: "Transform a sequence of digits element-wise based on whether each digit is zero or non-zero."
elements:
  - name: sequence
    type: list of integers
    role: input and output structure
  - name: digit
    type: integer (0-9)
    role: element within the sequence
properties:
  - object: digit
    name: value
    description: The numerical value of the digit (0-9).
transformation:
  - name: map_digit
    inputs:
      - digit (from input sequence)
    outputs:
      - digit (for output sequence)
    rule: >
      If the input digit's value is 0, the output digit's value is 0.
      If the input digit's value is non-zero (1-9), the output digit's value is 5.
relationship:
  - type: positional_correspondence
    description: >
      The digit at index 'i' in the output sequence is the result of applying the
      map_digit transformation to the digit at index 'i' in the input sequence.
    applies_to:
      - input sequence
      - output sequence
```


**Natural Language Program:**

1.  Iterate through each digit in the input sequence, keeping track of its position (index).
2.  For each input digit:
    a.  If the digit is equal to 0, the corresponding output digit at the same position is 0.
    b.  If the digit is not equal to 0 (i.e., it is 1, 2, 3, 4, 5, 6, 7, 8, or 9), the corresponding output digit at the same position is 5.
3.  Construct the output sequence using the transformed digits.
