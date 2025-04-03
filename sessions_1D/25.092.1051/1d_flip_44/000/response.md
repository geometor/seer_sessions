Okay, I will analyze the provided examples and generate the requested deliverables.

**Perception of Task Elements:**

The input and output grids are single rows (1D arrays essentially).
Each input grid contains a contiguous sequence of non-white pixels surrounded by white pixels (0).
This non-white sequence always starts with a single pixel of one color (let's call it the "head" color) followed immediately by a contiguous block of pixels of a second, different color (let's call it the "body" color).
The output grid is identical to the input grid except for the arrangement within this non-white sequence.
In the output, the block of "body" colored pixels appears first, immediately followed by the single "head" colored pixel. The relative order of the head pixel and the body block is reversed.
The surrounding white pixels remain unchanged in their positions.

**Facts:**


```yaml
task_type: array_transformation
grid_dimensionality: 1D (represented as 1xN 2D array)
background_color: white (0)
objects:
  - name: non_white_sequence
    description: A contiguous sequence of pixels with colors other than white (0).
    location: Embedded within the white background.
    structure:
      - component: head
        description: A single pixel of a specific color.
        position: Always at the beginning of the non_white_sequence in the input.
      - component: body
        description: A contiguous block of pixels of a single color, different from the head color.
        position: Immediately follows the head pixel in the input.
transformation:
  - action: identify
    target: non_white_sequence
    details: Find the start and end indices of the contiguous block of non-white pixels.
  - action: identify
    target: head
    details: The first pixel within the non_white_sequence.
  - action: identify
    target: body
    details: The remaining pixels within the non_white_sequence after the head pixel.
  - action: rearrange
    target: non_white_sequence
    details: Reorder the components within the sequence's original location so the body block comes first, followed by the head pixel.
    constraints:
      - The relative positions of pixels within the body block remain unchanged.
      - The position of the overall sequence within the grid remains unchanged.
      - Pixels outside the non_white_sequence (the white background) remain unchanged.
```


**Natural Language Program:**

1.  Identify the contiguous sequence of non-white pixels in the input grid. Determine its starting and ending positions.
2.  Within this sequence, identify the first pixel (the "head") and the block of pixels that follows it (the "body").
3.  Create a new sequence by placing the "body" block first, followed immediately by the "head" pixel.
4.  Construct the output grid by replacing the original non-white sequence in the input grid with the newly created rearranged sequence, keeping all other pixels (the surrounding white pixels) in their original positions.