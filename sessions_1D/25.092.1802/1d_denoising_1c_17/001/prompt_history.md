
## train_1

**input:**
```
0 0 0 8 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 8 0 0 0 8 0 0 8 0 0 0
```


**output:**
```
0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
4 4 4 4 4 4 4 4 4 4 4 0 0 4 0 0 4 0 0 4 0 0 0 4 0 0 0 0 4 0 0 0 0
```


**output:**
```
4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

**Perception:**

1.  **Grid Structure:** Both input and output grids are single rows (1D arrays or vectors). All examples have the same width (33 pixels).
2.  **Colors:** Each example uses white (0) and one other color: azure (8) in train_1, blue (1) in train_2, and yellow (4) in train_3.
3.  **Input Pattern:** The input grids contain contiguous blocks of a non-white color, separated by white pixels. Some non-white blocks are extended (length > 1), while others are isolated single pixels (length = 1).
4.  **Output Pattern:** The output grid retains only *one* contiguous block of the non-white color from the input. All other pixels, including isolated non-white pixels and other non-white blocks from the input, are turned white (0).
5.  **Transformation:** The core transformation identifies the *largest* contiguous block of the non-white color in the input row and preserves it in the output. All other positions in the output row become white (0). The specific non-white color is maintained within the preserved block.

**Facts:**


```yaml
task_type: array_transformation
grid_dimensionality: 1D (represented as 2D with height 1)
grid_size: fixed (1x33 for all examples)
background_color: white (0)
objects:
  - type: contiguous_block
    color: non-white (varies per example: 8, 1, 4)
    properties:
      - length (number of pixels)
      - position (start and end index)
relationships:
  - type: comparison
    attribute: length
    among: non-white_contiguous_blocks
    criterion: maximum
action:
  - type: identify
    target: largest non-white contiguous block
  - type: preserve
    target: pixels within the largest block
  - type: change_color
    target: all other pixels
    to_color: white (0)
result: Output grid contains only the largest non-white block from the input, surrounded by white pixels.
```


**Natural Language Program:**

1.  Identify all contiguous horizontal blocks of non-white pixels in the input row. Note their color, start position, and length.
2.  Find the block with the maximum length among all identified non-white blocks. If there's a tie in length, any one of the longest blocks can be chosen (though the examples don't show ties).
3.  Create a new output row of the same size as the input, initially filled entirely with the background color (white, 0).
4.  Copy the pixels corresponding to the position and color of the single largest non-white block (identified in step 2) from the input row to the corresponding positions in the new output row.
5.  The resulting output row is the final output.
