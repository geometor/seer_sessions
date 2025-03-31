*   **Perception:**
    The task involves transforming an input grid into an output grid. The examples show different types of transformations based on the specific content of the input grid. The transformations involve identifying specific objects or pixels based on their color and spatial relationships, and then applying a rule (like shifting) based on the properties of those identified elements.

    *   **Analysis of `train_1`:**
        *   The input grid has a blue (1) background.
        *   There are distinct objects composed primarily of azure (8) pixels, some of which contain a single yellow (4) pixel. There is also one isolated yellow (4) pixel.
        *   In the output grid, the objects containing both azure (8) and yellow (4) have been shifted horizontally. The isolated yellow pixel and the blue background remain unchanged.
        *   The direction and magnitude of the shift depend on the original column position of the yellow (4) pixel within the azure/yellow object.
        *   The grid width is 8 columns (indices 0 to 7). The midpoint is effectively column index 4.
        *   Objects whose yellow pixel is in a column index less than 4 are shifted 3 columns to the right.
        *   Objects whose yellow pixel is in a column index greater than or equal to 4 are shifted 3 columns to the left.

*   **Facts (YAML format) for `train_1`:**


```yaml
grid_properties:
  - dimensions: Input grid is 18x8.
  - background_color: blue (1)

objects:
  - type: composite_object
    description: Connected components of non-background pixels.
    identification: Find contiguous pixels that are not blue (1).
  - type: target_object
    description: Specific composite objects containing both azure (8) and yellow (4) pixels.
    properties:
      - contains_azure: true
      - contains_yellow: true
  - type: anchor_pixel
    description: The yellow (4) pixel within a target_object.
    properties:
      - color: yellow (4)
      - location: (row, column) coordinates within the grid.
  - type: other_pixels
    description: Pixels not part of a target_object (includes background and other non-target objects/pixels like the standalone yellow pixel).

actions:
  - name: horizontal_shift
    target: target_object
    parameters:
      - direction: Based on the anchor_pixel's column index relative to the grid's vertical midpoint (column 4).
      - magnitude: 3 columns.
    condition: If anchor_pixel column < 4, shift right. If anchor_pixel column >= 4, shift left.
  - name: remain_unchanged
    target: other_pixels

relationships:
  - The anchor_pixel (yellow) determines the transformation applied to its containing target_object (azure/yellow structure).
  - The grid's width determines the midpoint column used in the shift condition.

output_construction:
  - Create a new grid initialized with the background color (blue).
  - Draw all 'other_pixels' at their original locations.
  - For each 'target_object', calculate its new position based on the horizontal_shift action and draw it in the new location.
```


*   **Natural Language Program for `train_1`:**

1.  Initialize the output grid as a copy of the input grid. (Or: Initialize the output grid with the background color, blue (1)).
2.  Identify all connected components (objects) formed by non-blue (1) pixels.
3.  For each identified object:
    a.  Check if the object contains at least one azure (8) pixel AND exactly one yellow (4) pixel.
    b.  If both conditions are true, this is a "target object". Find the coordinates (row, column) of the yellow (4) pixel (the "anchor pixel").
    c.  Determine the grid's vertical midpoint column index (which is 4 for an 8-wide grid).
    d.  If the anchor pixel's column index is less than 4: Define the transformation for this object as a horizontal shift of +3 columns (right).
    e.  If the anchor pixel's column index is greater than or equal to 4: Define the transformation for this object as a horizontal shift of -3 columns (left).
    f.  If the object is *not* a target object (e.g., the standalone yellow pixel), its transformation is identity (no change).
4.  Create the final output grid:
    a.  Start with a grid filled entirely with the background color (blue).
    b.  Iterate through all pixels of the input grid.
    c.  If a pixel belongs to an object that was *not* identified as a target object in step 3a, copy its color to the same position in the output grid.
    d.  For each target object identified in step 3a: Calculate the new coordinates for every pixel in that object by applying the determined horizontal shift (from step 3d or 3e). Draw these pixels with their original colors at their new coordinates in the output grid. (Ensure this overwrites any background pixels but respects potential overlaps if objects were complex, though none exist in the example).