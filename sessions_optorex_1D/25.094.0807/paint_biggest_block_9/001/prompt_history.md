
## train_1

**input:**
```
9 9 9 9 9 9 0 9 9 9 9 9
```


**output:**
```
1 1 1 1 1 1 0 9 9 9 9 9
```


## train_2

**input:**
```
9 9 9 9 9 9 0 9 9 9 0 0
```


**output:**
```
1 1 1 1 1 1 0 9 9 9 0 0
```


## train_3

**input:**
```
7 7 7 7 7 0 7 7 7 7 7 7
```


**output:**
```
7 7 7 7 7 0 1 1 1 1 1 1
```


## train_4

**input:**
```
0 8 8 8 8 8 0 0 0 8 8 8
```


**output:**
```
0 1 1 1 1 1 0 0 0 8 8 8
```


## train_5

**input:**
```
5 5 0 0 0 0 5 5 5 0 0 0
```


**output:**
```
5 5 0 0 0 0 1 1 1 0 0 0
```


## train_6

**input:**
```
0 0 4 4 4 4 4 4 0 4 4 4
```


**output:**
```
0 0 1 1 1 1 1 1 0 4 4 4
```


## train_7

**input:**
```
0 0 0 0 3 3 3 3 0 0 3 3
```


**output:**
```
0 0 0 0 1 1 1 1 0 0 3 3
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of Elements:**

1.  **Input/Output Format:** Both input and output are sequences (lists or arrays) of single-digit integers.
2.  **Key Digit '0':** The digit `0` appears to act as a separator or boundary within the sequences. It is never modified during the transformation.
3.  **Key Digit '1':** The digit `1` appears only in the output sequences and seems to replace other digits.
4.  **Transformation Focus:** The transformation modifies contiguous subsequences (runs) of identical *non-zero* digits.
5.  **Modification Rule:** A specific run of identical non-zero digits in the input is replaced by a run of `1`s of the same length in the output.
6.  **Selection Criteria:**
    *   The transformation targets the *longest* contiguous run of identical non-zero digits in the *entire* input sequence.
    *   If there are multiple runs of the same maximum length, the *first* such run encountered (reading from left to right) is the one selected for modification.
7.  **Conservation:** Digits not part of the selected run (including `0`s and other runs) remain unchanged in their positions.

**YAML Fact Documentation:**


```yaml
Task: Modify a sequence of digits based on runs of identical non-zero digits.

Objects:
  - InputSequence:
      type: List[int]
      description: The sequence of single-digit integers provided as input.
  - OutputSequence:
      type: List[int]
      description: The sequence of single-digit integers produced as output.
  - SubsequenceRun:
      type: Conceptual
      description: A contiguous block of identical non-zero digits within a sequence.
      properties:
        - value: int (the repeated digit, must be non-zero)
        - length: int (number of repetitions)
        - start_index: int
        - end_index: int
  - ZeroDigit:
      type: int
      value: 0
      description: Acts as a boundary or separator, never modified.
  - OneDigit:
      type: int
      value: 1
      description: The replacement digit used in the output for the selected subsequence.

Actions:
  - IdentifyRuns:
      description: Scan the InputSequence to find all SubsequenceRuns.
      inputs: InputSequence
      outputs: List[SubsequenceRun]
  - FindLongestRun:
      description: Determine the maximum length among all identified SubsequenceRuns.
      inputs: List[SubsequenceRun]
      outputs: max_length (int)
  - SelectTargetRun:
      description: Choose the first SubsequenceRun (by start_index) that matches the max_length.
      inputs:
        - List[SubsequenceRun]
        - max_length
      outputs: target_run (SubsequenceRun)
  - ReplaceRun:
      description: Modify a copy of the InputSequence by replacing the digits of the target_run with OneDigit.
      inputs:
        - InputSequence (or its copy)
        - target_run
        - OneDigit
      outputs: OutputSequence

Relationships:
  - OutputSequence has the same length as InputSequence.
  - ZeroDigits remain unchanged in position and value from InputSequence to OutputSequence.
  - Digits not part of the target_run remain unchanged in position and value.
  - The target_run is the first occurring run with the overall maximum length among all non-zero identical digit runs.
  - The digits within the target_run in the InputSequence are all replaced by OneDigit in the OutputSequence.
```


**Natural Language Program:**

1.  Receive the input sequence of digits.
2.  Initialize an empty list to store identified runs of identical non-zero digits.
3.  Iterate through the input sequence, identifying all contiguous runs of identical non-zero digits. For each run found, record its digit value, start index, end index, and length.
4.  If no such runs were found, return the original input sequence as the output.
5.  Determine the maximum length among all recorded runs.
6.  Find the first run (the one with the smallest start index) that has this maximum length. This is the "target run".
7.  Create a copy of the input sequence to serve as the initial output sequence.
8.  Iterate from the start index to the end index (inclusive) of the target run. For each position within this range in the output sequence copy, set the digit to `1`.
9.  Return the modified output sequence.
