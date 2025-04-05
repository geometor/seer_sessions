
## train_1

**input:**
```
0 0 0 0 1 1 1 1 7 0 0 0
```


**output:**
```
0 0 0 0 1 1 1 1 7 7 7 7
```


## train_2

**input:**
```
0 0 9 9 9 9 9 2 0 0 0 0
```


**output:**
```
0 0 9 9 9 9 9 2 2 2 2 2
```


## train_3

**input:**
```
0 2 2 2 2 2 5 0 0 0 0 0
```


**output:**
```
0 2 2 2 2 2 5 5 5 5 5 5
```


## train_4

**input:**
```
0 0 0 0 1 1 1 1 1 1 5 0
```


**output:**
```
0 0 0 0 1 1 1 1 1 1 5 5
```


## train_5

**input:**
```
0 0 0 1 8 8 8 8 8 8 0 0
```


**output:**
```
1 1 1 1 8 8 8 8 8 8 0 0
```


## train_6

**input:**
```
0 0 7 9 9 9 9 9 9 0 0 0
```


**output:**
```
7 7 7 9 9 9 9 9 9 0 0 0
```


## train_7

**input:**
```
0 0 6 6 6 6 9 0 0 0 0 0
```


**output:**
```
0 0 6 6 6 6 9 9 9 9 9 9
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of the Elements:**

1.  **Input/Output Format:** Both input and output are sequences (lists) of single-digit integers.
2.  **Key Objects:** The core objects are the individual digits within the sequence, specifically differentiating between zero (`0`) and non-zero digits (e.g., `1`, `2`, `5`, `6`, `7`, `8`, `9`).
3.  **Observed Pattern:** The transformation primarily involves modifying the zero digits at the beginning and end of the sequence.
    *   Zeros at the *beginning* of the sequence are replaced by the value of the *first* non-zero digit encountered when scanning from left to right.
    *   Zeros at the *end* of the sequence are replaced by the value of the *last* non-zero digit encountered when scanning from left to right (or the first non-zero digit when scanning from right to left).
    *   The non-zero digits and any zeros *between* the first and last non-zero digits remain unchanged.
4.  **Implicit Action:** The process seems to involve identifying the boundaries defined by the first and last non-zero digits and then "filling" the regions outside these boundaries (leading and trailing zeros) with the respective boundary non-zero values.

**YAML Facts:**


```yaml
Objects:
  - Sequence: A list of single-digit integers.
  - Digit: An element within the sequence.
    Properties:
      - Value: The integer value (0-9).
      - IsZero: Boolean (True if value is 0, False otherwise).
      - Position: The index within the sequence.

Relationships:
  - LeftmostNonZero: The first digit in the sequence (from left) whose value is not 0.
  - RightmostNonZero: The last digit in the sequence (from left) whose value is not 0.
  - LeadingZeros: All digits with value 0 preceding the LeftmostNonZero digit.
  - TrailingZeros: All digits with value 0 succeeding the RightmostNonZero digit.

Actions:
  - Identify: Find the LeftmostNonZero and RightmostNonZero digits and their positions/values.
  - Propagate Left: Replace the value of all LeadingZeros with the value of the LeftmostNonZero digit.
  - Propagate Right: Replace the value of all TrailingZeros with the value of the RightmostNonZero digit.
```


**Natural Language Program:**

1.  Take the input sequence of digits.
2.  Find the index and value of the first non-zero digit from the left (LeftmostNonZero). If no non-zero digits exist, the sequence remains unchanged.
3.  Find the index and value of the last non-zero digit from the left (RightmostNonZero).
4.  Create a copy of the input sequence to serve as the output sequence.
5.  Iterate from the beginning of the output sequence up to (but not including) the index of the LeftmostNonZero digit. Set the value of each digit in this range to the value of the LeftmostNonZero digit.
6.  Iterate from the end of the output sequence backwards, starting from the index after the RightmostNonZero digit. Set the value of each digit in this range to the value of the RightmostNonZero digit.
7.  Return the modified output sequence.
