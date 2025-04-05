**Perception of Task Elements:**

The task involves manipulating a sequence of integers. Each input consists of a list of numbers, primarily zeros, containing a single contiguous block of non-zero integers. The output is a sequence of the same length where the non-zero block from the input has been moved to a different position. The core elements are:
1.  The input sequence (a list of integers).
2.  The output sequence (a list of integers of the same length as the input).
3.  A contiguous block of non-zero integers within the input sequence.
4.  Zero padding surrounding the non-zero block.
5.  A consistent spatial shift applied to the non-zero block.

**Facts:**


```yaml
Task: Sequence Transformation

Input:
  Type: List of Integers
  Length: Fixed (12 in examples)
  Structure: Contains a single contiguous block of non-zero integers, surrounded by zeros.
  Example_Object: The non-zero block (e.g., `[7, 4]` in train_1, `[7, 6, 8]` in train_2).

Output:
  Type: List of Integers
  Length: Same as input (12 in examples)
  Structure: Contains the same non-zero block as the input, shifted, surrounded by zeros.

Transformation:
  Action: Shift the non-zero block.
  Direction: Right.
  Magnitude: Constant (4 positions in examples).
  Relationship:
    - The non-zero block in the output is identical to the non-zero block in the input.
    - The starting position of the non-zero block in the output is the starting position in the input plus 4.
    - All other elements in the output sequence are zeros.
```


**Natural Language Program:**

1.  Receive the input sequence of integers.
2.  Identify the contiguous subsequence composed entirely of non-zero integers. Determine its starting index and length.
3.  Create a new output sequence of the same length as the input sequence, initialized with all zeros.
4.  Calculate the new starting index for the non-zero subsequence by adding 4 to its original starting index in the input sequence.
5.  Place the identified non-zero subsequence into the output sequence, beginning at the calculated new starting index.
6.  Output the modified sequence.