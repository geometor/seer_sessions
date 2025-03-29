Okay, let's analyze the provided task examples.

## Perception

1.  **Input/Output Structure:** Both input and output are grids of colored pixels (represented by numbers 0-9). The background is predominantly white (0).
2.  **Objects:** The grids contain distinct objects, which are contiguous areas of non-white pixels. Some objects are simple rectangles (e.g., the yellow and green rectangles in train_1, the magenta rectangles in train_2), while others are more complex shapes (e.g., the green boundary with a yellow interior in train_2).
3.  **Key Transformation Trigger:** The transformation appears to be triggered by *single pixels* of a specific color. In train_1, single yellow pixels trigger a change. In train_2, single green pixels trigger a change.
4.  **Transformation Action:** When a single pixel (a 'seed') of a certain color is found, it seems to 'invoke' or 'copy' a pattern associated with that color from elsewhere in the input grid.
5.  **Identifying the Pattern/Template:** The pattern being copied appears to be derived from the *largest* contiguous object of the *same color* as the seed pixel. Specifically, the content within the bounding box of this largest object is used as the template. This template can include multiple colors if they fall within the bounding box of the largest object of the seed's color.
6.  **Placement of the Copied Pattern:** The copied template pattern is placed onto the grid such that its top-left corner aligns exactly with the location of the original seed pixel.
7.  **Overwriting:** The copying process overwrites any existing pixels in the target area.
8.  **Persistence:** Objects that are not single pixels and are not the largest object of a color with seeds remain unchanged in their original positions. White background pixels also remain unless overwritten by a copied pattern.

## Facts


```yaml
facts:
  - Rationale: Define the basic element of the grid.
    fact: The grid is composed of pixels, each having a color (represented by an integer 0-9) and a location (row, column).
  - Rationale: Define 'object' based on connectivity and color.
    fact: An object is a group of one or more contiguous pixels of the same non-white color. Contiguity includes adjacent (horizontal/vertical) and diagonal connections. (Correction: Standard ARC usually uses only horizontal/vertical adjacency. Let's assume horizontal/vertical unless evidence suggests otherwise. Re-evaluating based on H/V adjacency only).
      - Re-evaluation based on H/V adjacency:
        - Train 1: Yellow object at (1,1) is 4x5. Green object at (6,12) is 3x5. Seeds are single pixels. This still works.
        - Train 2: Green/Yellow object boundary at (3,1) is contiguous H/V. Yellow inside is contiguous H/V. Magenta objects are contiguous H/V. Seeds are single pixels. This still works.
    fact: Re-state object definition: An object is a group of one or more contiguous (sharing a side, not just a corner) pixels of the same non-white color.
  - Rationale: Identify properties of objects needed for the transformation.
    fact: Objects have properties including:
      - color: The color of the pixels forming the object.
      - pixels: The set of coordinates {(row, col)} belonging to the object.
      - size: The number of pixels in the object.
      - bounding_box: The smallest rectangle containing all pixels of the object, defined by {min_row, min_col, max_row, max_col}.
      - is_seed: A boolean property, true if the object size is 1, false otherwise.
  - Rationale: Identify the source pattern for copying.
    fact: For each non-white color present in the input grid, there might be a 'template pattern'.
    fact: The 'template pattern' for a given color is determined by finding the object of that color with the largest size (pixel count).
    fact: The actual template copied is the rectangular region of the grid defined by the bounding box of this largest object. This region might contain pixels of colors other than the object's primary color.
  - Rationale: Identify the trigger for the copying action.
    fact: 'Seed' objects (objects of size 1) trigger the copying action.
  - Rationale: Describe the copying action itself.
    fact: When a seed object of a specific color is found at location (seed_row, seed_col):
      - The 'template pattern' associated with that color is retrieved.
      - This template pattern (a rectangular grid patch) is copied onto the output grid.
  - Rationale: Specify the placement rule for the copied pattern.
    fact: The top-left corner of the copied template pattern is placed at the location (seed_row, seed_col) of the seed object.
  - Rationale: Specify how copying interacts with existing grid content.
    fact: The copy operation overwrites the pixels in the destination area on the output grid.
  - Rationale: Specify what happens to non-participating elements.
    fact: All pixels from the input grid that are not overwritten by a copy operation are retained in their original positions in the output grid.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct non-white colors present in the input grid.
3.  For each distinct non-white color (`C`) found:
    a.  Find all contiguous objects composed solely of color `C`. Use horizontal and vertical adjacency.
    b.  Determine the object of color `C` with the largest number of pixels. If there's a tie in size, the choice might require refinement (e.g., topmost, leftmost), but based on examples, assume a unique largest or identical shapes suffice. Let this be the `LargestObject_C`.
    c.  If no objects of color `C` exist, continue to the next color.
    d.  If `LargestObject_C` exists, determine its bounding box: `BBox_C = {min_row, min_col, max_row, max_col}`.
    e.  Extract the rectangular subgrid defined by `BBox_C` from the input grid. This is the `TemplatePattern_C`.
    f.  Identify all objects of color `C` that consist of exactly one pixel. These are the `SeedPixels_C`, each with a location `(seed_row, seed_col)`.
    g.  For each `(seed_row, seed_col)` in `SeedPixels_C`:
        i.  Paste the `TemplatePattern_C` onto the *output grid*, placing the top-left corner of the pattern at `(seed_row, seed_col)`. Overwrite any existing pixels in the target area of the output grid.
4.  After processing all colors, the modified output grid is the final result.