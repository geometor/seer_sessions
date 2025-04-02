**Perception**

The input and output are both single rows (1D grids) of pixels.
Each input row contains a single contiguous block of non-white pixels surrounded by white (0) pixels.
The color and length of this block vary between examples (yellow, length 3; gray, length 6; orange, length 9).
In the output, this same block of non-white pixels appears shifted to the right compared to its position in the input.
The surrounding pixels remain white.
The amount of the shift appears to be constant across all examples: 3 positions to the right.

**Facts**


```yaml
Data:
  - type: 1D grid (row)
    structure: Input and Output are single rows of the same length.
Objects:
  - type: contiguous block
    properties:
      - color: non-white (variable, e.g., yellow, gray, orange)
      - length: variable (e.g., 3, 6, 9)
      - count: exactly one per input row
    location: surrounded by white pixels
Background:
  - type: pixel
    properties:
      - color: white (0)
Transformation:
  - action: shift
  - target: the contiguous block of non-white pixels
  - direction: right
  - amount: 3 positions
  - mechanism: The block moves 3 steps to the right. The original positions occupied by the block become white. The pixels to the right of the block are displaced by the shift.
Relationship:
  - The shift amount (3) is constant and independent of the block's color or length.
```


**Natural Language Program**

1.  Identify the contiguous sequence (block) of non-white pixels within the input row.
2.  Determine the starting and ending indices of this block.
3.  Create a new output row of the same length as the input, initially filled with white (0) pixels.
4.  Copy the identified block of non-white pixels into the output row, starting at an index that is 3 positions greater than its original starting index.