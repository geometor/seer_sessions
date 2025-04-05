**Perception of Task Elements:**

1.  **Input/Output Format:** Both input and output are lists/sequences of 12 integers.
2.  **Key Elements:** The sequences contain:
    *   Zeros (`0`).
    *   A pivot element: the number `2`, which appears exactly once in every example.
    *   A target block: a contiguous sequence of one or more identical non-zero integers (e.g., `9 9`, `5 5`, `8`, `1 1`, `3`). This block is distinct from the pivot `2`.
3.  **Implicit Structure:** The sequence represents positions in a line. The core components are the pivot `2` and the target block. Zeros act as spacers or filler.
4.  **Transformation Goal:** The fundamental change involves altering the relative positions of the target block and the pivot `2`.

**YAML Fact Documentation:**


```yaml
task_description: Swap the relative position of a target block of identical non-zero numbers with respect to a fixed pivot element '2', preserving the gap between them.

elements:
  - object: sequence
    properties:
      - type: list of integers
      - length: 12
  - object: pivot
    properties:
      - value: 2
      - count: 1 per sequence
      - role: fixed reference point
  - object: target_block
    properties:
      - type: contiguous subsequence
      - content: identical non-zero integers (not equal to 2)
      - length: variable (>= 1)
      - count: 1 per sequence
      - role: element to be repositioned
  - object: zero
    properties:
      - value: 0
      - role: filler/spacer

relationships:
  - type: position
    between: [target_block, pivot]
    states: [target_block_left_of_pivot, target_block_right_of_pivot]
  - type: separation
    between: [target_block, pivot]
    properties:
      - name: gap
      - value: number of zeros between the block and the pivot
      - conserved: yes (the gap size is preserved during transformation)

actions:
  - action: identify
    target: pivot (2)
    details: Find its value and index.
  - action: identify
    target: target_block
    details: Find its value, start index, end index, and length.
  - action: determine_relative_position
    elements: [target_block, pivot]
    output: left or right
  - action: calculate_gap
    elements: [target_block, pivot]
    output: number of zeros between them
  - action: construct_output_sequence
    details: Create a new sequence of 12 zeros.
  - action: place_pivot
    target: output_sequence
    details: Place the pivot '2' at its original index.
  - action: place_target_block
    target: output_sequence
    details: |
      Place the target block on the opposite side of the pivot '2'
      compared to its input position, ensuring the calculated gap
      (number of zeros) between the pivot and the block is maintained.
```


**Natural Language Program:**

1.  Start with an empty output sequence of 12 zeros.
2.  Find the index (position) of the pivot element `2` in the input sequence.
3.  Place the pivot element `2` into the output sequence at this same index.
4.  Identify the contiguous block of identical non-zero numbers in the input sequence that are not `2` (this is the "target block"). Record its value, start index, end index, and length.
5.  Determine if the target block is located to the left or right of the pivot `2` in the input sequence.
6.  Calculate the "gap", which is the number of zeros strictly between the target block and the pivot `2` in the input sequence.
7.  If the target block was to the left of the pivot `2` in the input:
    *   Calculate the starting index for the target block in the output sequence as `(index of 2) + 1 + gap`.
    *   Place the target block into the output sequence starting at this calculated index.
8.  If the target block was to the right of the pivot `2` in the input:
    *   Calculate the ending index for the target block in the output sequence as `(index of 2) - 1 - gap`.
    *   Calculate the starting index by subtracting the block length minus 1 from the ending index.
    *   Place the target block into the output sequence starting at this calculated starting index.
9.  The resulting sequence, containing the correctly placed pivot `2`, the repositioned target block, and zeros elsewhere, is the final output.