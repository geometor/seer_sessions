
## train_1

**input:**
```
0 0 7 1 6 4 6 3 4 6 2 7
```


**output:**
```
0 0 7 2 6 4 3 6 4 6 1 7
```


## train_2

**input:**
```
0 0 6 3 5 2 7 7 8 0 0 0
```


**output:**
```
0 0 8 7 7 2 5 3 6 0 0 0
```


## train_3

**input:**
```
0 0 0 8 2 5 2 4 9 2 7 6
```


**output:**
```
0 0 0 6 7 2 9 4 2 5 2 8
```


## train_4

**input:**
```
0 9 6 2 3 5 2 0 0 0 0 0
```


**output:**
```
0 2 5 3 2 6 9 0 0 0 0 0
```


## train_5

**input:**
```
0 0 2 5 3 1 4 8 8 8 0 0
```


**output:**
```
0 0 8 8 8 4 1 3 5 2 0 0
```


## train_6

**input:**
```
0 2 8 5 2 6 6 2 5 5 6 0
```


**output:**
```
0 6 5 5 2 6 6 2 5 8 2 0
```


## train_7

**input:**
```
0 0 0 0 5 1 8 9 0 0 0 0
```


**output:**
```
0 0 0 0 9 8 1 5 0 0 0 0
```

Okay, analyzing the provided examples to understand the transformation.

**Perception:**

1.  **Input/Output Format:** Both input and output are sequences of single digits (0-9) separated by spaces. They can be interpreted as lists of integers.
2.  **Key Structure:** The sequences appear to have three distinct parts:
    *   An optional sequence of leading zeros (`0`).
    *   A central contiguous block of non-zero digits (1-9).
    *   An optional sequence of trailing zeros (`0`).
3.  **Transformation Observation:** Comparing inputs and outputs, the leading and trailing zeros remain unchanged in their positions. The central block of non-zero digits appears to be reversed in the output compared to the input. This pattern holds consistently across all provided examples.

**Facts:**


```yaml
Objects:
  - InputSequence:
      type: list
      elements: integers (0-9)
      structure: [LeadingZeros, NonZeroBlock, TrailingZeros]
  - OutputSequence:
      type: list
      elements: integers (0-9)
      structure: [LeadingZeros, ReversedNonZeroBlock, TrailingZeros]
  - LeadingZeros:
      type: sub-sequence
      elements: integer (0)
      relation: Identical in InputSequence and OutputSequence
  - NonZeroBlock:
      type: sub-sequence
      elements: integers (1-9)
      property: contiguous
      location: between LeadingZeros and TrailingZeros in InputSequence
  - TrailingZeros:
      type: sub-sequence
      elements: integer (0)
      relation: Identical in InputSequence and OutputSequence
  - ReversedNonZeroBlock:
      type: sub-sequence
      elements: integers (1-9)
      location: between LeadingZeros and TrailingZeros in OutputSequence
      relation: Reverse order of NonZeroBlock from InputSequence

Actions:
  - Identify: Locate the start and end indices of the NonZeroBlock within the InputSequence.
  - Extract: Isolate the LeadingZeros, NonZeroBlock, and TrailingZeros sub-sequences.
  - Reverse: Reverse the order of elements within the extracted NonZeroBlock.
  - Reconstruct: Assemble the OutputSequence by concatenating LeadingZeros, ReversedNonZeroBlock, and TrailingZeros.

Relationships:
  - The core transformation is the reversal of the contiguous sub-sequence containing only non-zero digits.
  - The elements outside this non-zero sub-sequence (leading and trailing zeros) maintain their original positions and values.
```


**Natural Language Program:**

1.  Read the input sequence of digits.
2.  Find the index of the first non-zero digit (`start_index`). If no non-zero digits exist, the output is identical to the input.
3.  Find the index of the last non-zero digit (`end_index`).
4.  Extract the sub-sequence of digits from `start_index` to `end_index` (inclusive). This is the `NonZeroBlock`.
5.  Reverse the order of the digits within the extracted `NonZeroBlock`.
6.  Construct the output sequence by taking the digits before `start_index`, followed by the reversed `NonZeroBlock`, followed by the digits after `end_index`.
7.  Format the resulting sequence of digits back into a space-separated string for the final output.
