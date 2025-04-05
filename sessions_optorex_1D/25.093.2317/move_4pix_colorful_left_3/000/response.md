*   **Perception of task elements:**
    *   The input and output are sequences of single digits, always 12 digits long.
    *   The sequences contain both zero and non-zero digits.
    *   The core transformation involves relocating a segment of the input sequence.
    *   Specifically, the contiguous block of digits starting from the first non-zero digit and ending with the last non-zero digit in the input sequence is identified.
    *   This identified block is then shifted 4 positions to the left to form the output sequence.
    *   Positions in the output sequence not filled by the shifted block are occupied by zeros.
    *   The relative order of the digits within the shifted block remains unchanged.
    *   If the calculated starting position after the shift is negative (i.e., index < 0), the block starts at index 0.

*   **Facts:**
    
```yaml
    Task: Shift a segment of a digit sequence.
    Objects:
      - InputSequence:
          Type: List of integers (digits 0-9)
          Properties:
            - Length: 12
            - Contains: Zeros and non-zero digits
      - OutputSequence:
          Type: List of integers (digits 0-9)
          Properties:
            - Length: 12 (same as input)
            - DerivedFrom: InputSequence
      - NonZeroSegment:
          Type: Sub-sequence of InputSequence
          Properties:
            - Starts: At the index of the first non-zero digit in InputSequence.
            - Ends: At the index of the last non-zero digit in InputSequence.
            - Content: All digits (including any zeros) between the start and end indices.
            - RelativeOrder: Preserved from InputSequence.
    Actions:
      - Identify: Locate the first and last non-zero digits in InputSequence to define NonZeroSegment.
      - CalculateShift: Determine the target start index for NonZeroSegment in OutputSequence.
          - Formula: `max(0, StartIndex_of_NonZeroSegment - 4)`
      - Construct: Create OutputSequence.
          - Initialize: Fill OutputSequence with zeros.
          - PlaceSegment: Copy NonZeroSegment into OutputSequence starting at the calculated target index.
    Relationships:
      - OutputSequence is a transformation of InputSequence.
      - NonZeroSegment is extracted from InputSequence.
      - The position of NonZeroSegment in OutputSequence depends on its original position in InputSequence and a fixed shift value (4).
    Constants:
      - SequenceLength: 12
      - ShiftAmount: 4 (positions to the left)
    ```


*   **Natural Language Program:**
    1.  Receive the input sequence of 12 digits.
    2.  Find the index of the first non-zero digit in the input sequence. If no non-zero digits exist, the output is the same as the input (all zeros).
    3.  Find the index of the last non-zero digit in the input sequence.
    4.  Extract the sub-sequence (the "segment") from the input sequence starting at the first non-zero index and ending at the last non-zero index (inclusive).
    5.  Calculate the target starting index for this segment in the output sequence by subtracting 4 from the original starting index (the first non-zero index). Ensure the target index is not less than 0; if it is, use 0 as the target index.
    6.  Create a new output sequence of 12 zeros.
    7.  Place the extracted segment into the output sequence, starting at the calculated target starting index. The digits following the segment in the output sequence remain zeros.
    8.  Return the constructed output sequence.