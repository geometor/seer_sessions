
## train_1

**input:**
```
0 0 0 8 8 8 8 8 8 8 8 0
```


**output:**
```
0 0 8 8 8 8 8 8 8 8 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 6 6 6
```


**output:**
```
0 0 0 0 0 0 0 0 6 6 6 0
```


## train_3

**input:**
```
0 0 5 5 5 5 5 0 0 0 0 0
```


**output:**
```
0 5 5 5 5 5 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 8 8 0 0 0 0 0
```


**output:**
```
0 0 0 0 8 8 0 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 0 2 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 2 0 0
```


## train_6

**input:**
```
0 0 0 6 6 6 6 6 0 0 0 0
```


**output:**
```
0 0 6 6 6 6 6 0 0 0 0 0
```


## train_7

**input:**
```
0 0 0 0 0 0 0 2 2 2 0 0
```


**output:**
```
0 0 0 0 0 0 2 2 2 0 0 0
```

Okay, let's break down the task based on the provided examples.

**Perception of Task Elements:**

The input and output are sequences of single digits, presented as space-separated strings. The primary characteristic of the input sequences is the presence of a contiguous block of identical non-zero digits surrounded by zeros. The transformation appears to involve shifting this non-zero block one position towards the beginning of the sequence, effectively swapping it with the zero immediately preceding it.

**YAML Fact Documentation:**


```yaml
Task: Shift Non-Zero Block Left

Input:
  Type: String
  Format: Space-separated single digits
  Content: Contains a sequence of digits, primarily '0', with one contiguous block of identical non-zero digits.

Output:
  Type: String
  Format: Space-separated single digits
  Content: A permutation of the input sequence.

Objects:
  - Sequence: The list of digits derived from the input/output string.
  - Zero: The digit '0'.
  - NonZeroBlock: A contiguous sub-sequence within the main Sequence, containing identical digits other than '0'.
  - PrecedingZero: The '0' element immediately before the NonZeroBlock in the input Sequence.

Relationships:
  - NonZeroBlock is surrounded by Zero elements in the input (except potentially at the very ends, although examples show internal blocks).
  - The Output Sequence is formed by moving the NonZeroBlock one position earlier in the Sequence compared to the Input Sequence.
  - The PrecedingZero from the input moves to the position immediately after where the NonZeroBlock ends in the output.

Actions:
  - Identify: Locate the start and end indices of the NonZeroBlock.
  - Identify: Locate the index of the PrecedingZero (which is start_index - 1).
  - Shift: Move the NonZeroBlock one position to the left.
  - Relocate: Move the PrecedingZero to the position immediately following the shifted NonZeroBlock.

Transformation:
  Rule: Swap the NonZeroBlock with the single Zero element immediately preceding it. All other elements retain their relative order.
  Constraint: Assumes there is exactly one such NonZeroBlock and at least one Zero preceding it.
```


**Natural Language Program:**

1.  Parse the input string into a list of digit strings.
2.  Find the starting index of the first non-zero digit block. If no non-zero digits exist, return the original input list joined back into a string.
3.  Find the ending index of this contiguous non-zero digit block.
4.  If the starting index is 0 (the block is already at the beginning), return the original input list joined back into a string.
5.  Extract the non-zero block (from the start index to the end index, inclusive).
6.  Extract the zero element immediately preceding the block (at start index - 1).
7.  Construct the output list:
    a.  Take all elements from the beginning of the input list up to (but not including) the preceding zero (index `start_index - 1`).
    b.  Append the extracted non-zero block.
    c.  Append the extracted preceding zero.
    d.  Append all remaining elements from the input list that came *after* the non-zero block (from index `end_index + 1` to the end).
8.  Join the elements of the newly constructed output list with spaces to form the final output string.
