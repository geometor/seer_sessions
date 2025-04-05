
## train_1

**input:**
```
9 0 0 0 0 0 0 0 0 9 9 9
```


**output:**
```
0 0 0 0 0 0 0 0 9 9 9 9
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 7
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 7 0
```


## train_3

**input:**
```
7 0 0 0 0 0 0 0 0 7 7 7
```


**output:**
```
0 0 0 0 0 0 0 0 7 7 7 7
```


## train_4

**input:**
```
0 0 0 0 0 0 7 7 0 0 0 0
```


**output:**
```
0 0 0 0 0 7 7 0 0 0 0 0
```


## train_5

**input:**
```
0 0 0 0 0 0 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 3 0 0 0 0 0 0
```


## train_6

**input:**
```
0 0 0 0 0 0 0 0 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 2 0 0 0 0
```


## train_7

**input:**
```
6 6 6 0 0 0 6 6 6 6 6 6
```


**output:**
```
6 6 0 0 0 6 6 6 6 6 6 6
```

Okay, I will analyze the provided examples to understand the transformation.

**Perception of Task Elements:**

The input and output are sequences (lists or arrays) of single-digit integers. The core transformation seems to involve locating the first non-zero digit (or the block it belongs to) and shifting or swapping elements based on its position. Zeros act as placeholders or space. The length of the sequence remains constant.

Two distinct patterns emerge based on the position of the *first* non-zero element:

1.  **First Non-Zero Element is NOT at the Beginning (Index > 0):** The first non-zero element is swapped with the element immediately preceding it (which is always a zero in the examples). See `train_2`, `train_4`, `train_5`, `train_6`.
2.  **First Non-Zero Element IS at the Beginning (Index 0):** The transformation is more complex. It involves the *end* of the initial block of non-zero numbers and the position *before* the *next* block of non-zero numbers. Specifically, the element at the end index of the first block swaps with the zero located just before the start of the second non-zero block. See `train_1`, `train_3`, `train_7`.

**Fact Documentation:**


```yaml
Task: Sequence Transformation

Input:
  Type: List of Integers
  Properties:
    - Contains single-digit integers (0-9)
    - Fixed length

Output:
  Type: List of Integers
  Properties:
    - Same length as input
    - Derived from input via element rearrangement

Objects:
  - Sequence: The list of integers.
  - Element: An individual integer within the sequence.
  - NonZeroElement: An element with a value > 0.
  - ZeroElement: An element with a value == 0.
  - Block: A contiguous sub-sequence of identical NonZeroElements.

Relationships:
  - Position: Index of an element within the sequence.
  - PrecedingElement: Element at index `i-1` relative to element at index `i`.
  - FollowingElement: Element at index `i+1` relative to element at index `i`.
  - FirstNonZero: The NonZeroElement with the lowest index.
  - FirstBlock: The Block containing the FirstNonZero element (if it's part of a block starting at index 0) or just the FirstNonZero element itself.
  - NextBlock: The first Block of NonZeroElements occurring after the FirstBlock.

Actions:
  - FindIndex: Locate the index of the FirstNonZero element.
  - FindBlockEnd: Determine the last index of a contiguous Block.
  - FindNextBlockStart: Determine the starting index of the NextBlock.
  - CheckValue: Verify if an element at a given index is zero.
  - Swap: Exchange the positions of two elements in the sequence.

TransformationRule:
  - Condition: Based on the index of the FirstNonZero element.
  - Case 1 (FirstNonZero at Index > 0):
    - Action: Swap the FirstNonZero element with its PrecedingElement.
  - Case 2 (FirstNonZero at Index 0):
    - Find the end index (`end_idx`) of the FirstBlock.
    - Find the start index (`next_start_idx`) of the NextBlock.
    - Check if NextBlock exists and if the element at `next_start_idx - 1` is a ZeroElement.
    - Action (if condition met): Swap the element at `end_idx` with the element at `next_start_idx - 1`.
    - Action (otherwise - although not explicitly shown in examples, implies no change or a default behavior if conditions aren't met): The sequence remains unchanged or follows a different rule not covered. Based on provided examples, the condition is always met for Case 2.

```


**Natural Language Program:**

1.  Create a mutable copy of the input sequence.
2.  Iterate through the sequence to find the index (`first_nz_idx`) of the first non-zero element. If no non-zero element exists, return the original sequence.
3.  **If `first_nz_idx` is greater than 0:**
    a.  Swap the element at `first_nz_idx` with the element at `first_nz_idx - 1`.
4.  **If `first_nz_idx` is 0:**
    a.  Identify the value (`val`) of the element at index 0.
    b.  Find the index (`end_idx`) of the last element in the initial contiguous block of `val` starting at index 0.
    c.  Search for the start index (`next_block_start_idx`) of the *next* contiguous block of *any* non-zero number that occurs after `end_idx`.
    d.  If such a `next_block_start_idx` is found AND the element at index `next_block_start_idx - 1` is 0:
        i.  Swap the element at `end_idx` with the element at `next_block_start_idx - 1`.
    e.  (If the condition in 4d is not met, no change occurs based on the examples provided).
5.  Return the modified sequence.
