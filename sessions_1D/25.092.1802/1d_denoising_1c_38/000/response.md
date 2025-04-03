**Perception:**

The task operates on single-row grids (effectively 1D arrays). Each input row consists of pixels of two colors: a background color (white, represented by 0) and a single foreground color (yellow, blue, or azure in the examples). The foreground color appears in multiple, separate contiguous blocks of varying lengths within the input row.

The transformation identifies the *longest* contiguous block of the foreground color within the input row. The output row is constructed to be the same length as the input. This longest foreground block is preserved in its original position in the output row. All other pixels in the output row, including those that were part of shorter foreground blocks or the original background in the input, are set to the background color (white, 0).

**Facts:**


```yaml
task_type: object_selection_and_filtering
input_features:
  - grid_dimensionality: 1D (single row)
  - background_color: white (0)
  - foreground_color: single non-white color (varies per example)
  - foreground_pixels_form_blocks: Yes, multiple contiguous blocks of the foreground color exist.
  - block_properties:
      - contiguity: horizontal
      - size: variable length
output_features:
  - grid_dimensionality: 1D (single row)
  - dimensions: same as input row length
  - background_color: white (0)
  - foreground_color: same as input foreground color
  - foreground_pixels_form_blocks: Yes, exactly one contiguous block of the foreground color exists.
relationship_input_output:
  - preservation: The single output foreground block corresponds exactly in color, size, and position to the largest foreground block found in the input.
  - modification: All pixels in the output that do not belong to the preserved largest block are set to the background color (white, 0).
objects:
  - object: background
    color: white (0)
  - object: foreground_block
    definition: A maximal contiguous sequence of non-white pixels.
    properties:
      - color: non-white (consistent within a block and within an example)
      - length: number of pixels in the sequence
  - object: target_block
    definition: The foreground_block with the maximum length in the input.
actions:
  - identify_foreground_color: Determine the non-white color present in the input.
  - find_contiguous_blocks: Locate all contiguous sequences (blocks) of the foreground color in the input row.
  - measure_block_length: Calculate the length of each identified foreground block.
  - select_largest_block: Identify the foreground block with the maximum length. If multiple blocks share the maximum length, the examples suggest any one will suffice (implicitly, perhaps the first one encountered).
  - create_output_row: Initialize a new row of the same length as the input, filled entirely with the background color (white, 0).
  - copy_target_block: Copy the pixels of the selected largest block from the input into the corresponding positions in the output row.
```


**Natural Language Program:**

1.  Determine the dimensions (length) of the input row.
2.  Identify the two colors present: the background color (white, 0) and the single foreground color.
3.  Scan the input row to find all contiguous blocks (sequences) of the foreground color. Record the start index, end index, and length of each block.
4.  Compare the lengths of all identified foreground blocks and select the block with the maximum length. Note its start and end indices.
5.  Create a new output row with the same length as the input row, initially filled entirely with the background color (white, 0).
6.  Copy the pixels corresponding to the selected largest foreground block (from its start index to its end index in the input) into the same positions in the new output row.
7.  The resulting row is the final output.