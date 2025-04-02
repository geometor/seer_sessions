**Perception:**
The input and output are both 1-dimensional grids (represented as a sequence of numbers). Each input grid contains a single contiguous block of a non-white color (orange, yellow, or red in the examples) surrounded by white pixels (value 0). The output grid shows that this colored block has been moved horizontally. Specifically, in all provided examples, the colored block is shifted exactly 3 positions to the right. The size, shape (length), and color of the block remain unchanged. The rest of the grid remains filled with white pixels.

**Facts:**

```yaml
task_elements:
  - description: Input and Output Grids
    properties:
      format: 1-dimensional array of integers (colors)
      background_color: white (0)
      content: Contains a single contiguous block of a non-white color.
  - description: Non-white Color Block (Object)
    properties:
      identity: A contiguous sequence of identical non-white pixels.
      color: Varies between examples (orange=7, yellow=4, red=2).
      size: Length of the contiguous sequence, remains constant between input and output.
    relationships:
      location_input: Defined by the start and end indices in the input grid.
      location_output: Defined by the start and end indices in the output grid.
  - description: Transformation Action
    properties:
      type: Horizontal Shift
      direction: Right
      magnitude: 3 positions
    operates_on: The Non-white Color Block
    result: The block's start index increases by 3. The grid positions previously occupied by the start of the block, and the positions between the old start and new start, become white. The overall grid size remains constant.
```


**Natural Language Program:**
1.  Identify the single contiguous block of non-white pixels in the input grid. Note its color, starting position, and length.
2.  Create a new output grid of the same size as the input grid, initially filled with the background color (white, 0).
3.  Calculate the new starting position for the non-white block by adding 3 to its original starting position.
4.  Place the identified non-white block (with its original color and length) into the output grid starting at the calculated new position.
5.  Return the modified grid as the output.