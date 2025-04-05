
## train_1

**input:**
```
0 0 6 5 2 7 1 9 9 8 7 0
```


**output:**
```
0 0 7 8 9 9 1 7 2 5 6 0
```


## train_2

**input:**
```
1 6 2 6 1 8 1 3 5 8 5 0
```


**output:**
```
5 8 5 3 1 8 1 6 2 6 1 0
```


## train_3

**input:**
```
0 0 7 2 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 2 7 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
6 2 6 8 4 4 4 6 7 4 6 4
```


**output:**
```
4 6 4 7 6 4 4 4 8 6 2 6
```


## train_5

**input:**
```
0 1 9 3 2 3 9 4 5 8 6 0
```


**output:**
```
0 6 8 5 4 9 3 2 3 9 1 0
```


## train_6

**input:**
```
8 3 4 8 9 1 0 0 0 0 0 0
```


**output:**
```
1 9 8 4 3 8 0 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 3 4 9 4 8 0
```


**output:**
```
0 0 0 0 0 0 8 4 9 4 3 0
```

**Perception of Task Elements:**

1.  **Input/Output:** Both input and output are sequences of single digits, presented as space-separated strings.
2.  **Sequence Length:** The length of the sequence remains constant between input and output (12 digits in all examples).
3.  **Core Transformation:** The primary operation is the reversal of a *portion* of the sequence.
4.  **Identifying the Reversed Portion:** The subsequence that gets reversed appears to be delimited by the first non-zero digit and the last non-zero digit found within the input sequence.
5.  **Boundary Handling:** Digits before the first non-zero digit (leading zeros) and digits after the last non-zero digit (trailing zeros) seem to retain their original positions.
6.  **Edge Cases:**
    *   If the entire sequence consists of non-zero digits (e.g., train_4), the whole sequence is reversed.
    *   If there are no non-zero digits or only one non-zero digit, the sequence should logically remain unchanged (as reversing a single element or an empty sequence results in the same sequence). Although not explicitly shown, this is a consistent deduction.

**YAML Documentation:**


```yaml
Task: Reverse Subsequence Between First and Last Non-Zero Digits

Input:
  type: list
  elements:
    type: integer
    range: 0-9
  description: A sequence of single digits.
  constraints: Fixed length (e.g., 12 in examples).

Output:
  type: list
  elements:
    type: integer
    range: 0-9
  description: A sequence of single digits, transformed from the input.
  constraints: Same length as input.

Transformation:
  action: reverse_subsequence
  target: a portion of the input list
  subsequence_definition:
    start_boundary: index of the first non-zero digit in the input list
    end_boundary: index of the last non-zero digit in the input list
    inclusive: yes
  unchanged_elements:
    - elements before the start_boundary
    - elements after the end_boundary
  edge_cases:
    - if no non-zero digits exist, the sequence remains unchanged.
    - if only one non-zero digit exists, the sequence remains unchanged.

Relationships:
  - The output sequence length is identical to the input sequence length.
  - The digits outside the identified subsequence maintain their original positions relative to the start and end of the main sequence.
  - The digits within the identified subsequence maintain their identity but have their order reversed relative to each other within that subsequence's original position.
```


**Natural Language Program:**

1.  Receive the input sequence of digits.
2.  Identify the index of the first non-zero digit in the sequence. If no non-zero digit exists, return the original sequence.
3.  Identify the index of the last non-zero digit in the sequence. (If step 2 found no non-zero digit, this step is skipped).
4.  Extract the subsequence starting from the first non-zero index up to and including the last non-zero index.
5.  Reverse the order of the digits within this extracted subsequence.
6.  Construct the output sequence by concatenating:
    a.  The portion of the original sequence *before* the first non-zero index.
    b.  The *reversed* subsequence.
    c.  The portion of the original sequence *after* the last non-zero index.
7.  Return the constructed output sequence.
