**Perception:**

The input and output are single-row grids containing sequences of pixels. The primary colors involved are white (0), used as a background, and other colors like green (3), orange (7), and magenta (6) forming a central "figure". This figure is always a contiguous block of non-white pixels.

Observing the examples:
1.  `train_1`: The figure is `7 3 3 3 3 3 3 3`. It transforms to `3 3 3 3 3 3 3 7`. The single orange pixel swaps places with the block of green pixels.
2.  `train_2`: The figure is `3 7 7 7 7 7 7 7 7`. It transforms to `7 7 7 7 7 7 7 7 3`. The single green pixel swaps places with the block of orange pixels.
3.  `train_3`: The figure is `6 7 7 7 7 7 7 7`. It transforms to `7 7 7 7 7 7 7 6`. The single magenta pixel swaps places with the block of orange pixels.

The core transformation appears to be identifying the non-white sequence (the figure) and within that sequence, swapping the position of a single pixel of one color with the adjacent contiguous block of pixels of another color. The background pixels remain unchanged.

**Facts:**


```yaml
task_type: object_manipulation
grid_dimensionality: 1D # Represented as a single row
components:
  - type: background
    color: white (0)
    description: Surrounds the main figure. Remains static.
  - type: figure
    description: A contiguous sequence of non-white pixels.
    composition:
      - part_a:
          description: A single pixel of a specific non-white color.
          quantity: 1
      - part_b:
          description: A contiguous block of one or more pixels of another specific non-white color.
          quantity: variable (>= 1)
    relationship: part_a and part_b are adjacent within the figure.
transformation:
  action: swap_elements
  target: figure
  details: The position of part_a (single pixel) and part_b (block of pixels) within the figure are swapped. The rest of the grid (background) remains unchanged.
```


**Natural Language Program:**

1.  Identify the contiguous sequence of non-white pixels in the input grid (this is the "figure"). Note its starting and ending positions.
2.  Within the figure, identify the single pixel that has a different color from its neighbors (let's call this the "unique pixel").
3.  Identify the remaining block of pixels within the figure, which all share the same color (let's call this the "color block").
4.  Determine the relative order of the unique pixel and the color block in the input figure (e.g., unique pixel followed by color block, or vice-versa).
5.  Create a new sequence by reversing the order of the unique pixel and the color block.
6.  Construct the output grid by replacing the original figure sequence (at its original start/end positions) with the newly created sequence. Keep all white background pixels in their original positions.