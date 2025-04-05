Okay, I will analyze the provided examples and generate the requested deliverables.

**Perception of the Elements:**

1.  **Data Format:** Both input and output are strings representing sequences of integers separated by spaces.
2.  **Sequence Length:** The length of the sequence (number of integers) remains constant between the input and the output (12 integers in all examples).
3.  **Core Content:** Each input sequence contains a contiguous block of numbers that includes all the non-zero elements present. This block may also contain zeros if they fall between the first and last non-zero elements.
4.  **Transformation:** The primary transformation is the shifting (movement) of this "content block" within the sequence.
5.  **Padding:** The positions outside the moved content block in the output sequence are filled with zeros.
6.  **Movement Pattern:** The content block appears to shift leftwards by a specific amount (4 positions), but it doesn't shift past the beginning of the sequence (index 0). The relative order of the numbers within the content block is preserved.

**Fact Documentation:**


```yaml
Task: Shift a content block within a sequence of integers.

Objects:
  - Input_Sequence:
      Type: List of integers.
      Origin: Parsed from the input string.
      Properties:
        - length: The total number of integers in the sequence.
        - elements: Individual integer values at specific indices.
  - Output_Sequence:
      Type: List of integers.
      Destination: Formatted into the output string.
      Properties:
        - length: Same as Input_Sequence length.
        - elements: Derived from Input_Sequence based on transformation rule.
  - Content_Block:
      Type: Sub-list of integers.
      Origin: Extracted from Input_Sequence.
      Definition: The contiguous segment of the Input_Sequence starting at the index of the first non-zero integer and ending at the index of the last non-zero integer.
      Properties:
        - start_index_input: The index in Input_Sequence where the block begins.
        - end_index_input: The index in Input_Sequence where the block ends.
        - length: Number of elements in the block (end_index_input - start_index_input + 1).
        - elements: The sequence of integers within the block, preserving relative order.
  - Zero_Element:
      Type: Integer.
      Value: 0.
      Role: Acts as padding/background in the sequences.

Relationships:
  - Derivation: Output_Sequence is derived from Input_Sequence.
  - Extraction: Content_Block is extracted from Input_Sequence.
  - Preservation: The relative order of elements within the Content_Block is maintained from Input_Sequence to Output_Sequence.
  - Positioning: The starting position of the Content_Block in the Output_Sequence depends on its starting position in the Input_Sequence.

Actions:
  - Parse: Convert input string to Input_Sequence (list of integers).
  - Identify_Block: Find the start_index_input and end_index_input of the Content_Block by locating the first and last non-zero elements. Handle the case where no non-zero elements exist.
  - Extract: Create the Content_Block sub-list from Input_Sequence.
  - Calculate_Output_Start: Determine the target starting index for the Content_Block in the Output_Sequence using the rule: `output_start = max(0, start_index_input - 4)`.
  - Initialize_Output: Create an Output_Sequence of the same length as Input_Sequence, filled with zeros.
  - Place_Block: Copy the elements of the Content_Block into the Output_Sequence starting at the calculated `output_start` index.
  - Format: Convert the final Output_Sequence back to a space-separated string.
```


**Natural Language Program:**

1.  Receive the input as a string of space-separated integers.
2.  Convert the input string into a list of integers.
3.  Scan the list to find the index of the first non-zero integer (`start_index`) and the index of the last non-zero integer (`end_index`).
4.  If no non-zero integers are found, create an output list consisting of zeros with the same length as the input list, format it as a space-separated string, and return it.
5.  If non-zero integers exist, extract the sub-list (the "content block") from the input list, ranging from `start_index` to `end_index` inclusive.
6.  Calculate the target starting index (`output_start`) for placing this block in the output list by taking the `start_index` and subtracting 4, ensuring the result is not less than 0 (i.e., `output_start = max(0, start_index - 4)`).
7.  Create a new list of the same length as the input list, initially filled with zeros.
8.  Place the extracted "content block" into this new list, starting at the `output_start` index.
9.  Convert the new list back into a string of space-separated integers.
10. Return the resulting string.