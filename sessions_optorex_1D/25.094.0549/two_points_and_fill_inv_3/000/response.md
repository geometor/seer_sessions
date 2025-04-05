## Perception of Task Elements

The task involves transforming a 1D sequence of single-digit integers. The input sequences contain blocks (contiguous runs) of identical non-zero digits, surrounded by zeros. The transformation rule appears to operate specifically on these non-zero blocks. By comparing the input and output sequences across the examples, a pattern emerges:

1.  **Identification of Blocks:** The core operation is identifying contiguous sequences of the *same non-zero* digit.
2.  **Length Dependency:** The transformation applied to a block depends on its length.
3.  **Modification Rule:** If a block's length is greater than 2, only the first and last elements of the block are retained in their original positions in the output. All the elements *between* the first and last elements of that block are replaced with 0.
4.  **Short Blocks:** If a block's length is 2 or less (as seen in `train_1` and `train_4`), the block remains unchanged in the output.
5.  **Zeros:** Zeros in the input that are not part of the identified non-zero blocks remain unchanged in the output.

## YAML Fact Documentation


```yaml
Objects:
  - Sequence:
      description: A 1D list of single-digit integers.
      roles: [Input, Output]
  - Element:
      description: A single integer within a sequence (0-9).
  - Group:
      description: A contiguous subsequence of identical non-zero Elements within the Input Sequence.
      properties:
        - value: The non-zero integer that makes up the group.
        - start_index: The index of the first element of the group in the Input Sequence.
        - end_index: The index of the last element of the group in the Input Sequence.
        - length: The number of elements in the group (end_index - start_index + 1).

Relationships:
  - An Input Sequence is transformed into an Output Sequence.
  - A Group is identified within the Input Sequence.
  - The transformation rule depends on the `length` property of the Group.

Actions:
  - Identify_Groups: Scan the Input Sequence to find all Groups, noting their value, start_index, end_index, and length.
  - Modify_Sequence: Create a copy of the Input Sequence. For each identified Group:
      - Condition: Check if the Group's `length` is greater than 2.
      - If True:
          - Modify the copied sequence by setting the elements from `start_index + 1` up to `end_index - 1` (inclusive) to 0.
      - If False:
          - Make no changes to the copied sequence for this Group.
  - Output: Return the modified sequence.
```


## Natural Language Program

1.  Initialize the output sequence as a copy of the input sequence.
2.  Iterate through the input sequence to identify all contiguous groups of identical non-zero numbers. For each group found, record its starting index, ending index, and length.
3.  For each identified group:
    a.  Check if the length of the group is greater than 2.
    b.  If the length is greater than 2, then iterate through the indices of the output sequence starting from the index *after* the group's start index up to the index *before* the group's end index. Set the value at each of these indices in the output sequence to 0.
4.  Return the final output sequence.