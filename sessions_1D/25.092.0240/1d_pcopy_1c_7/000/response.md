**Perception of Task Elements:**

1.  **Grid Structure:** Both input and output grids are single rows (1D arrays) of varying lengths.
2.  **Color Palette:** Each example uses white (0) and one other specific color (green=3, maroon=9, or red=2). The non-white color is consistent within each input/output pair but varies between pairs.
3.  **Input Pattern:** The input grid contains scattered pixels of the non-white color, sometimes forming small contiguous blocks, separated by white pixels.
4.  **Output Pattern:** The output grid retains the white pixels outside the range of the non-white pixels. Within the range defined by the first and last non-white pixel in the input, all pixels (including the originally white ones) are filled with the non-white color.
5.  **Transformation:** The core transformation identifies the span covered by the non-white pixels in the input row (from the first occurrence to the last occurrence) and fills this entire span with that non-white color in the output row.

**Facts:**


```yaml
task_type: fill_segment
grid_dimensionality: 1D (single row)
color_usage:
  - background: white (0)
  - foreground: one single non-white color (C) per example (variable C)
objects:
  - type: pixel
    color: non-white (C)
    attributes:
      - position (index)
relationships:
  - type: span
    definition: The range of indices from the minimum index of a non-white pixel to the maximum index of a non-white pixel in the input row.
    color: C
actions:
  - type: identify_color
    description: Determine the single non-white color (C) present in the input grid.
  - type: find_indices
    description: Find all indices where the non-white color (C) appears in the input grid.
  - type: calculate_span
    description: Determine the minimum (min_idx) and maximum (max_idx) indices found in the previous step.
  - type: fill_span
    input: original grid, color C, min_idx, max_idx
    output: modified grid
    description: Create the output grid by copying the input grid, then changing the color of all pixels from index min_idx to max_idx (inclusive) to the non-white color C.
```


**Natural Language Program:**

1.  Identify the single non-white color (let's call it `C`) present in the input row.
2.  Find the index of the first occurrence of color `C` in the input row (let's call it `first_index`).
3.  Find the index of the last occurrence of color `C` in the input row (let's call it `last_index`).
4.  Create the output row, initially identical to the input row.
5.  For every index `i` from `first_index` to `last_index` (inclusive), set the color of the pixel at index `i` in the output row to `C`.
6.  Pixels in the output row outside this range (i.e., index `< first_index` or index `> last_index`) retain their original color from the input row (which will be white).