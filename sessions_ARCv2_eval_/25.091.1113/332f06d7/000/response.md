Okay, let's analyze the task examples.

**Perception of the Elements:**

1.  **Grid Structure:** The task operates on 2D grids of varying sizes filled with colors (represented by integers 0-9).
2.  **Key Colors:** The significant colors involved in the transformation appear to be Green (3 - background/unchanged), Blue (1 - object/path), Red (2 - marker), and White (0 - marker).
3.  **Objects:** We can identify contiguous blocks of non-Green colors as objects. Specifically, blocks of Red, White, and Blue pixels seem to be the primary actors or targets of the transformation.
4.  **Transformation Pattern:** The core transformation seems to involve changing the color of specific blocks based on the presence and properties (like size) of Red and White marker blocks.
    *   White blocks consistently turn into Blue blocks of the same size and position.
    *   Red blocks act as triggers. If there's a unique Blue block elsewhere in the grid with the *exact same dimensions* as the Red block, that Blue block turns White. If there isn't a unique matching Blue block, the original Red block itself turns White.
5.  **Background:** The Green (3) pixels generally remain unchanged, forming the background or boundaries.

**YAML Fact Sheet:**


```yaml
task_context:
  grid_properties:
    - type: 2D array
    - cell_values: integers 0-9 (colors)
    - dimensions: variable (up to 30x30)
  key_colors:
    - value: 3 (Green) - Primarily background, generally static.
    - value: 1 (Blue) - Represents objects or paths, subject to change.
    - value: 2 (Red) - Marker object, triggers changes, can change itself.
    - value: 0 (White) - Marker object, changes color.
objects:
  - type: contiguous block of same-colored pixels
  - relevant_colors: [Red (2), White (0), Blue (1)]
  - properties:
      - color
      - shape (implicitly defined by contiguous pixels)
      - dimensions (height, width)
      - position
relationships:
  - Red block size comparison: A Red block's dimensions (height, width) are compared to the dimensions of all Blue blocks.
  - Uniqueness: The transformation triggered by a Red block depends on finding a *unique* Blue block with matching dimensions.
actions:
  - Identify Blocks: Find all distinct contiguous blocks of Red, White, and Blue pixels.
  - Color Change (White -> Blue): All pixels within any identified White block are changed to Blue.
  - Color Change (Triggered by Red):
      - Condition: Find a unique Blue block with the same dimensions as the Red block.
      - Action (if condition met): Change all pixels of that *Blue* block to White.
      - Action (if condition not met): Change all pixels of the *Red* block itself to White.
invariance:
  - Grid dimensions remain constant between input and output.
  - Green (3) pixels generally remain unchanged.
  - Blue blocks not targeted by a Red block trigger remain unchanged (unless they were originally White).
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Find all distinct, contiguous blocks of Red (2) pixels in the input grid. Record their locations and dimensions (height, width).
3.  Find all distinct, contiguous blocks of White (0) pixels in the input grid. Record their locations.
4.  Find all distinct, contiguous blocks of Blue (1) pixels in the input grid. Record their locations and dimensions.
5.  For each identified White block:
    *   Change the color of all pixels corresponding to this block's location in the output grid to Blue (1).
6.  For each identified Red block:
    *   Count how many Blue blocks have the *exact same dimensions* (height and width) as the current Red block.
    *   If the count is exactly one:
        *   Identify the location of that unique matching Blue block.
        *   Change the color of all pixels corresponding to that *Blue* block's location in the output grid to White (0).
    *   Else (if the count is zero or greater than one):
        *   Change the color of all pixels corresponding to the *Red* block's location in the output grid to White (0).
7.  Return the modified output grid.