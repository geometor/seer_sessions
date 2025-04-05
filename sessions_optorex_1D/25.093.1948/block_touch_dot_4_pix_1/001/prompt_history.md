
## train_1

**input:**
```
0 0 2 0 0 0 0 4 4 4 4 0
```


**output:**
```
0 0 2 4 4 4 4 0 0 0 0 0
```


## train_2

**input:**
```
2 0 0 0 0 7 7 7 7 7 7 0
```


**output:**
```
2 7 7 7 7 7 7 0 0 0 0 0
```


## train_3

**input:**
```
0 2 0 0 3 3 3 3 3 3 0 0
```


**output:**
```
0 2 3 3 3 3 3 3 0 0 0 0
```


## train_4

**input:**
```
0 2 0 0 0 0 0 0 3 3 3 3
```


**output:**
```
0 2 0 0 3 3 3 3 0 0 0 0
```


## train_5

**input:**
```
2 7 7 7 7 7 7 7 7 7 7 7
```


**output:**
```
2 7 7 7 7 7 7 7 7 7 7 7
```


## train_6

**input:**
```
9 9 9 9 9 9 2 0 0 0 0 0
```


**output:**
```
9 9 9 9 9 9 2 0 0 0 0 0
```


## train_7

**input:**
```
0 2 0 1 1 1 1 1 1 1 0 0
```


**output:**
```
0 2 1 1 1 1 1 1 1 0 0 0
```

Okay, let's break down the transformation logic for this task.

## Perception

1.  **Input/Output Format:** Both input and output are sequences of 12 single-digit integers.
2.  **Key Elements:** The sequences consist of zeros and non-zero digits. A significant feature appears to be contiguous blocks of identical non-zero digits.
3.  **Core Transformation:** The primary action involves relocating a specific block of identical non-zero digits. This block seems to "slide" leftwards, moving over some or all of the zeros that immediately precede it. The zeros that are "overwritten" by the sliding block are then moved to the end of the sequence.
4.  **Trigger Condition:** This transformation seems contingent on finding a non-zero digit, followed by one or more zeros, followed by a block of identical non-zero digits. If this pattern doesn't exist, or if there are no zeros between the initial non-zero digit and the block, the sequence remains unchanged.
5.  **Shift Amount:** The distance the block shifts left seems limited by either the number of preceding zeros or the length of the block itself, whichever is smaller.

## Facts


```yaml
Objects:
  - Sequence:
      Properties:
        - A list of 12 single-digit integers.
        - Contains Digits.
  - Digit:
      Properties:
        - Value (0-9).
        - Position (index in the sequence).
      Types:
        - ZeroDigit (Value is 0).
        - NonZeroDigit (Value is 1-9).
  - Block:
      Properties:
        - A contiguous sub-sequence of identical NonZeroDigits.
        - StartPosition (index of the first digit).
        - EndPosition (index of the last digit).
        - Length (number of digits in the block).
        - DigitValue (the repeated non-zero digit).
  - AnchorDigit:
      Properties:
        - The first NonZeroDigit encountered before a potential Block, when scanning left-to-right.
        - Must be followed by at least one ZeroDigit before the Block starts.
  - PrecedingZeros:
      Properties:
        - A contiguous sub-sequence of ZeroDigits.
        - Located between an AnchorDigit and a Block.
        - Count (number of zeros).

Relationships:
  - An AnchorDigit *precedes* PrecedingZeros.
  - PrecedingZeros *precede* a Block.
  - The transformation *acts upon* the first occurrence of the AnchorDigit -> PrecedingZeros -> Block pattern.

Action:
  - Identify: Find the first AnchorDigit, the subsequent PrecedingZeros, and the immediately following Block.
  - Calculate Shift: Determine the number of positions to shift (`shift_count`) as the minimum of the PrecedingZeros count and the Block length.
  - Conditional Execution: If `shift_count` is greater than 0:
      - Remove: Delete the `shift_count` ZeroDigits immediately before the Block.
      - Relocate: Move the entire Block `shift_count` positions to the left.
      - Append: Add `shift_count` ZeroDigits to the very end of the Sequence.
  - No Action: If no AnchorDigit -> PrecedingZeros -> Block pattern is found, or if `shift_count` is 0, the Sequence remains unchanged.

```


## Natural Language Program

1.  Parse the input string into a list of integers.
2.  Iterate through the list to find the first instance of the following pattern:
    *   A non-zero digit (the "anchor").
    *   Followed immediately by one or more zeros (the "preceding zeros").
    *   Followed immediately by a contiguous block of identical non-zero digits (the "moving block").
3.  If this pattern is not found, return the original list.
4.  If the pattern is found:
    *   Record the index of the anchor digit.
    *   Count the number of preceding zeros (`zero_count`).
    *   Record the starting index of the moving block.
    *   Determine the length of the moving block (`block_length`).
    *   Record the value of the digit in the moving block.
5.  Calculate the number of positions to shift the block left (`shift_amount`) as the minimum of `zero_count` and `block_length`.
6.  If `shift_amount` is 0, return the original list.
7.  If `shift_amount` > 0:
    *   Create a new list.
    *   Copy elements from the original list up to (but not including) the first preceding zero that will be removed.
    *   Append the digits of the moving block to the new list.
    *   Append any remaining digits from the original list that were *after* the moving block.
    *   Append `shift_amount` zeros to the end of the new list.
8.  Return the modified list.
9.  Format the final list back into a space-separated string for the output.
