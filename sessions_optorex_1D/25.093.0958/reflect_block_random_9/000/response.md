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