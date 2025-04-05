Okay, let's analyze the provided examples to understand the transformation rule.

**Perception of Elements:**

1.  **Data Structure:** The input and output are sequences (lists) of 12 integers.
2.  **Key Element '2':** The number `2` appears exactly once in every input and output sequence. Its position remains unchanged during the transformation. It acts as a fixed pivot point.
3.  **Data Block:** Apart from the `2` and `0`s, there is typically a contiguous block of other non-zero integers (e.g., `3 3`, `5 5 5`, `7`, `1 1 1 1 1`, `8 8 8 8 8 8 8 8`). Let's call this the "data block". In some cases (`train_4`, `train_6`), the `2` is immediately adjacent to this block.
4.  **Zeros:** Zeros act as background or padding elements.
5.  **Transformation:** The core transformation involves shifting the "data block" relative to the fixed position of the `2`. Zeros fill the space created or displaced by the shift.
6.  **Shift Logic:**
    *   If the data block is to the left of the `2`, it shifts rightwards towards the `2`.
    *   If the data block is to the right of the `2`, it shifts leftwards towards the `2`.
    *   If the data block is already adjacent to the `2` (or if there's no data block other than `2`), no shift occurs.
7.  **Shift Amount:** The amount of the shift depends on the gap (number of zeros) between the data block and the `2`.
    *   If the gap is 0 (adjacent), the shift is 0.
    *   If the gap is 1, the shift is 1 position (towards the `2`).
    *   If the gap is greater than 1, the shift is 2 positions (towards the `2`).

**YAML Facts:**


```yaml
Objects:
  - Sequence:
      Properties:
        - Type: List of Integers
        - Length: 12
  - Pivot:
      Properties:
        - Value: 2
        - Count: 1
        - Position: Fixed (remains same in output as input)
  - DataBlock:
      Properties:
        - Type: Contiguous sub-sequence of non-zero integers (excluding Pivot)
        - Existence: Typically one per sequence (can be absent or adjacent to Pivot)
        - Position: Relative to Pivot (Left, Right, Adjacent)
        - Length: Variable
  - Filler:
      Properties:
        - Value: 0
        - Role: Background, occupies space not used by Pivot or DataBlock

Relationships:
  - RelativePosition: Between DataBlock and Pivot (Left, Right, Adjacent)
  - Gap:
      Properties:
        - Type: Number of Fillers (zeros) strictly between DataBlock and Pivot
        - Value: Integer >= 0

Actions:
  - LocatePivot: Find the index of the Pivot (value 2).
  - IdentifyDataBlock: Find the start index, end index, and values of the contiguous non-zero sequence (excluding Pivot).
  - CalculateGap: Determine the number of zeros between the DataBlock and the Pivot based on their indices.
  - DetermineShift:
      Based on Gap:
        - If Gap = 0, Shift Amount = 0
        - If Gap = 1, Shift Amount = 1
        - If Gap > 1, Shift Amount = 2
      Based on RelativePosition:
        - If DataBlock is Left of Pivot, Shift Direction = Right
        - If DataBlock is Right of Pivot, Shift Direction = Left
        - If DataBlock is Adjacent or Absent, Shift Direction = None
  - ApplyShift: Calculate the new start and end indices for the DataBlock.
  - ConstructOutput: Create a new sequence of length 12, place the Pivot at its original index, place the shifted DataBlock at its new indices, and fill remaining positions with Filler (0).

```


**Natural Language Program:**

1.  Receive the input sequence of 12 integers.
2.  Find the index (position) of the integer `2`; this is the `pivot_index`.
3.  Scan the input sequence to locate the contiguous block of non-zero integers, excluding the `2`. Record its starting index (`block_start`), ending index (`block_end`), and the sequence of values (`block_values`). If no such block exists, proceed to step 8.
4.  Determine the relative position of the block to the `pivot_index`:
    *   If `block_end < pivot_index`, the block is "Left".
    *   If `block_start > pivot_index`, the block is "Right".
    *   Otherwise, the block is "Adjacent".
5.  Calculate the `gap` (number of zeros strictly between the block and the `2`):
    *   If "Left", `gap = pivot_index - block_end - 1`.
    *   If "Right", `gap = block_start - pivot_index - 1`.
    *   If "Adjacent", `gap = 0`.
6.  Calculate the `shift_amount`:
    *   If `gap == 0`, `shift_amount = 0`.
    *   If `gap == 1`, `shift_amount = 1`.
    *   If `gap > 1`, `shift_amount = 2`.
7.  Calculate the new indices for the block (`new_block_start`, `new_block_end`):
    *   If "Left", `new_block_start = block_start + shift_amount`, `new_block_end = block_end + shift_amount`.
    *   If "Right", `new_block_start = block_start - shift_amount`, `new_block_end = block_end - shift_amount`.
    *   If "Adjacent", `new_block_start = block_start`, `new_block_end = block_end`.
8.  Create the output sequence, initially filled with 12 zeros.
9.  Place the integer `2` at the `pivot_index` in the output sequence.
10. If a data block was found in step 3, place the `block_values` into the output sequence starting at `new_block_start` and ending at `new_block_end`.
11. Return the completed output sequence.