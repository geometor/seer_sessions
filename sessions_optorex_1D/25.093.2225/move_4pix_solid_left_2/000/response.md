**Perception of Elements:**

The task involves manipulating sequences of digits. Each input and output is a string of 12 digits separated by spaces. The core element within each sequence is a contiguous block of identical non-zero digits, surrounded by zeros. The transformation rule consistently alters the position of this non-zero block within the sequence, while keeping the block's content (the specific digit and its repetition count) and the overall sequence length unchanged. The surrounding elements are always zeros.

**Facts:**


```yaml
Task: Shift a block of non-zero digits within a fixed-length sequence.

Input:
  Type: String
  Format: Space-separated sequence of 12 digits.
  Content: Contains a single contiguous block of identical non-zero digits, padded with zeros.
  Example_Structure: '0 ... 0 X X ... X 0 ... 0' where X is a non-zero digit.

Output:
  Type: String
  Format: Space-separated sequence of 12 digits.
  Content: The non-zero block from the input, shifted to a new position, padded with zeros.

Objects:
  - Name: Sequence
    Properties:
      - Type: List of integers (derived from input/output string)
      - Length: 12
  - Name: NonZeroBlock
    Properties:
      - Type: Sub-sequence of identical non-zero integers
      - Digit: The non-zero digit composing the block (e.g., 5, 9, 7)
      - Length: Number of times the digit repeats (variable)
      - Position: Start and end indices within the sequence.

Action:
  - Name: ShiftLeft
  - Target: NonZeroBlock
  - Parameter: ShiftAmount = 4 positions
  - Description: The start index of the NonZeroBlock in the output sequence is 4 less than its start index in the input sequence.

Relationships:
  - The output sequence is a transformation of the input sequence.
  - The NonZeroBlock's digit and length are preserved from input to output.
  - The position of the NonZeroBlock changes predictably (shifted left by 4).
  - Zeros fill the positions not occupied by the shifted NonZeroBlock.
```


**Natural Language Program:**

1.  Read the input string and convert it into a list of 12 integers.
2.  Identify the contiguous block of identical non-zero digits within the list. Record the non-zero digit itself, the length of the block, and its starting index in the input list.
3.  Create a new list of 12 integers, initializing all elements to zero.
4.  Calculate the target starting index for the non-zero block in the new list by subtracting 4 from its starting index in the original input list.
5.  Place the identified non-zero block (using the recorded digit and length) into the new list, starting at the calculated target index.
6.  Convert the new list of integers back into a space-separated string to produce the output.