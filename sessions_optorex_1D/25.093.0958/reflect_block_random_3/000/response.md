Okay, let's analyze the input-output pairs.

**Perception of Task Elements:**

1.  **Input/Output Format:** Both input and output are sequences of 12 single digits, separated by spaces.
2.  **Core Operation:** The primary transformation appears to be a reversal of a specific portion of the sequence.
3.  **Boundary Identification:** The reversal does not always apply to the entire sequence. Leading and trailing zeros seem to act as boundaries, remaining fixed in their positions.
4.  **Target Segment:** The segment of the sequence that undergoes reversal is the portion lying between the first non-zero digit and the last non-zero digit (inclusive).
5.  **Edge Cases:**
    *   If the sequence consists entirely of zeros, the output is identical to the input.
    *   If there are no leading or trailing zeros, the entire sequence is reversed.
    *   If there are only leading zeros or only trailing zeros, the reversal applies to the segment starting/ending with the first/last non-zero digit.

**Facts (YAML):**


```yaml
Data:
  Type: Sequence of digits
  Length: 12
  Delimiter: Space
Objects:
  - Sequence: The list of 12 input digits.
  - NonZeroSegment: The contiguous sub-sequence starting from the first non-zero digit and ending with the last non-zero digit.
  - LeadingZeros: The sequence of zeros preceding the NonZeroSegment.
  - TrailingZeros: The sequence of zeros following the NonZeroSegment.
Properties:
  - Sequence Length: Fixed at 12.
  - Digit Value: Integers from 0 to 9.
Actions:
  - Identify: Find the start and end indices of the NonZeroSegment.
  - Extract: Isolate the LeadingZeros, NonZeroSegment, and TrailingZeros.
  - Reverse: Reverse the order of digits within the NonZeroSegment.
  - Reconstruct: Combine the LeadingZeros, the reversed NonZeroSegment, and the TrailingZeros to form the output sequence.
Relationships:
  - The output sequence is derived from the input sequence.
  - The NonZeroSegment is defined by the positions of the first and last non-zero digits in the input sequence.
  - LeadingZeros and TrailingZeros maintain their original positions relative to the overall sequence structure.
SpecialConditions:
  - If the input sequence contains only zeros, the output sequence is identical to the input sequence.
```


**Natural Language Program:**

1.  Receive the input sequence of 12 digits.
2.  Scan the sequence to find the index of the first non-zero digit (`first_nz_idx`) and the index of the last non-zero digit (`last_nz_idx`).
3.  If no non-zero digits are found (i.e., the sequence consists entirely of zeros), return the original input sequence as the output.
4.  Otherwise:
    a.  Extract the sub-sequence of leading zeros (from the beginning up to, but not including, `first_nz_idx`).
    b.  Extract the sub-sequence of digits between `first_nz_idx` and `last_nz_idx` (inclusive). This is the segment to be reversed.
    c.  Extract the sub-sequence of trailing zeros (from the position after `last_nz_idx` to the end).
    d.  Reverse the order of the digits in the segment extracted in step 4b.
    e.  Concatenate the leading zeros (from step 4a), the reversed segment (from step 4d), and the trailing zeros (from step 4c) in that order.
5.  Return the resulting concatenated sequence as the output.