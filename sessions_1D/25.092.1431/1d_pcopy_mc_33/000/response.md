## Perception

The task operates on single-row grids. The core transformation involves identifying specific patterns of pixels and modifying them. The key pattern is a single non-white pixel horizontally surrounded by two white pixels (`0 C 0`). When this pattern is detected in the input, it is replaced by a block of three pixels of that same non-white color (`C C C`) in the output. Existing blocks of three identical non-white pixels (`C C C`) in the input are preserved in the output. All other pixels, primarily the white background, remain unchanged unless they are part of the `0 C 0` pattern being replaced. The transformation seems local, focusing on 3-pixel wide neighborhoods.

## Facts


```yaml
grid_properties:
  dimensionality: 1D (effectively, operates on a single row)
  height: 1
  width: variable (e.g., 32 in examples)
  input_output_size_relation: output width is identical to input width

pixel_colors:
  - background: 0 (white)
  - active_colors: 1-9 (non-white colors involved in patterns)

identified_patterns:
  - pattern_name: isolated_single
    structure: A sequence of three pixels `[P1, P2, P3]` where P1 is white (0), P2 is non-white (C), and P3 is white (0).
    location: Occurs at indices `[i-1, i, i+1]` in the input row.
  - pattern_name: solid_triplet
    structure: A sequence of three pixels `[P1, P2, P3]` where P1, P2, and P3 are the same non-white color (C).
    location: Occurs at indices `[j, j+1, j+2]` in the input row.

transformation_rules:
  - rule: expansion
    input_pattern: isolated_single (0, C, 0) at indices `[i-1, i, i+1]`
    output_pattern: solid_triplet (C, C, C) at indices `[i-1, i, i+1]`
    condition: Applies when the isolated_single pattern is found in the input.
  - rule: preservation
    input_elements: All pixels not part of an 'isolated_single' pattern detected in the input.
    output_elements: Copied directly from the input to the output at the same position.
    effect: This implicitly preserves existing 'solid_triplet' patterns and background pixels not overwritten by the 'expansion' rule.

processing_flow:
  - step: Initialize the output grid as a copy of the input grid.
  - step: Iterate through the input grid, checking for the 'isolated_single' pattern `(0, C, 0)` at each possible center position `i` (from index 1 to width-2).
  - step: If the 'isolated_single' pattern is found at input indices `[i-1, i, i+1]`, modify the output grid at indices `[i-1, i, i+1]` to `(C, C, C)`.
  - step: The final state of the output grid after checking all positions is the result.
```


## Natural Language Program

1.  Create a new grid, `output_grid`, identical in size and content to the `input_grid`.
2.  Iterate through the `input_grid` row, focusing on each pixel from the second position (index 1) to the second-to-last position (index `width - 2`). Let the index of the current central pixel be `i`.
3.  For each central pixel at index `i`, examine the triplet of pixels in the `input_grid` at indices `i-1`, `i`, and `i+1`.
4.  Check if this triplet matches the pattern: `white`, `non-white color C`, `white` (i.e., `input_grid[i-1] == 0`, `input_grid[i] == C` where `C != 0`, and `input_grid[i+1] == 0`).
5.  If the pattern is matched, update the `output_grid` by setting the pixels at indices `i-1`, `i`, and `i+1` all to the color `C` identified in the pattern.
6.  Continue this process for all possible central positions `i`.
7.  The final `output_grid` is the result of the transformation.