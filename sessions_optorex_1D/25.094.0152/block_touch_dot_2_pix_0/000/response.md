Okay, let's break down the transformation logic for these examples.

**Perception of Elements:**

1.  **Data Format:** The input and output are sequences of single-digit integers, presented as space-separated strings. They can be interpreted as 1D arrays or lists.
2.  **Key Digits:**
    *   `0`: Appears to represent empty space or background.
    *   `2`: Acts as a fixed point or separator. Its position does not change from input to output.
    *   Other non-zero digits (`3`, `4`, `6`, `7`, `9` in the examples): Form contiguous blocks.
3.  **Core Transformation:** The primary action is the shifting of the contiguous block of non-zero digits (excluding '2') towards the '2'.
4.  **Direction of Shift:**
    *   If the block is initially to the left of '2', it shifts rightward until its rightmost digit is immediately adjacent to the left of '2'.
    *   If the block is initially to the right of '2', it shifts leftward until its leftmost digit is immediately adjacent to the right of '2'.
5.  **Integrity:** The digits within the non-zero block maintain their relative order during the shift. The length of the sequence remains constant.
6.  **Filling:** The positions previously occupied by the shifted block become '0'.

**YAML Facts:**


```yaml
task_description: "Shift a contiguous block of non-zero digits (excluding '2') adjacent to the fixed digit '2'."
elements:
  - object: Sequence
    description: "A 1D list of single-digit integers."
    properties:
      - length: Integer, the number of digits in the sequence.
      - digits: List of integers [0-9].
  - object: Separator
    description: "The digit '2' which serves as a fixed anchor point."
    properties:
      - value: 2
      - index: Integer, the position of '2' in the sequence (remains constant).
  - object: NumberBlock
    description: "A contiguous sub-sequence of digits that are not '0' and not '2'."
    properties:
      - digits: List of non-zero, non-2 integers.
      - start_index: Integer, the starting position in the input sequence.
      - end_index: Integer, the ending position in the input sequence.
      - length: Integer, the number of digits in the block.
      - relative_position: String, either 'left_of_separator' or 'right_of_separator'.
  - object: Zero
    description: "The digit '0' representing empty space."
    properties:
      - value: 0
actions:
  - action: FindSeparator
    description: "Locate the index of the digit '2' in the input sequence."
    inputs: [InputSequence]
    outputs: [separator_index]
  - action: FindNumberBlock
    description: "Identify the contiguous block of non-zero, non-2 digits, its start/end indices, and its position relative to the separator."
    inputs: [InputSequence, separator_index]
    outputs: [NumberBlock (or null if none exists)]
  - action: ShiftBlock
    description: "Calculate the target start and end indices for the NumberBlock in the output sequence, placing it adjacent to the Separator."
    inputs: [NumberBlock, separator_index, sequence_length]
    outputs: [target_start_index, target_end_index]
  - action: ConstructOutput
    description: "Create the output sequence by placing the Separator at its original index, the NumberBlock at its target indices, and filling remaining positions with '0'."
    inputs: [sequence_length, separator_index, Separator.value, target_start_index, target_end_index, NumberBlock.digits]
    outputs: [OutputSequence]
relationships:
  - type: Adjacency
    description: "The NumberBlock in the output sequence is positioned immediately next to the Separator."
    condition_left: "If NumberBlock was left_of_separator, its end_index in output is separator_index - 1."
    condition_right: "If NumberBlock was right_of_separator, its start_index in output is separator_index + 1."
  - type: Preservation
    description: "The Separator ('2') maintains its original index. The relative order of digits within the NumberBlock is preserved."
  - type: Replacement
    description: "Positions not occupied by the Separator or the shifted NumberBlock in the output sequence are filled with Zero ('0')."
```


**Natural Language Program:**

1.  Read the input sequence of digits.
2.  Find the index of the digit '2' (the separator).
3.  Scan the sequence to find the start and end indices of the contiguous block of digits that are neither '0' nor '2'. Record the digits within this block.
4.  If no such block exists, the output is identical to the input; stop.
5.  Determine if the identified block is located to the left or right of the separator's index.
6.  Create a new output sequence of the same length as the input, initially filled entirely with '0'.
7.  Place the digit '2' into the output sequence at its original index (found in step 2).
8.  If the block was found to the left of the separator:
    a. Calculate the target end index for the block in the output sequence as `separator_index - 1`.
    b. Calculate the target start index as `target_end_index - length_of_block + 1`.
    c. Copy the recorded block digits into the output sequence from the target start index to the target end index.
9.  If the block was found to the right of the separator:
    a. Calculate the target start index for the block in the output sequence as `separator_index + 1`.
    b. Calculate the target end index as `target_start_index + length_of_block - 1`.
    c. Copy the recorded block digits into the output sequence from the target start index to the target end index.
10. Return the constructed output sequence.