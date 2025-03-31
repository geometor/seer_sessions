
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 1 8 8
1 0 0 8
4 0 0 2
4 4 2 2
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 1 1 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
8 8 2 2
8 0 0 2
3 0 0 1
3 3 1 1
```

*   **Perception:** The input grid contains four distinct, small, L-shaped objects, each composed of three pixels of a single non-white color, set against a white background. The output grid is always 4x4 and seems to be a composite representation of the four input objects. Each input L-shape is mapped to a 2x2 subgrid within the output. The color of the input object is preserved in its corresponding 2x2 output subgrid. The placement of each 2x2 subgrid within the 4x4 output grid appears to depend solely on the specific orientation (shape type) of the input L-shape, not its position in the input grid. The 2x2 subgrid itself represents the L-shape using its color for the three filled pixels and white for the one empty pixel within the 2x2 bounding box.

*   **Facts:**
    
```yaml
    task_context:
      grid_properties:
        background_color: white (0)
        output_size: 4x4
      input_elements:
        objects:
          count: 4
          type: connected component of non-white pixels
          properties:
            color: single non-white color (blue, red, green, yellow, azure, etc.)
            pixel_count: 3
            shape: L-shape (one of four orientations filling 3 cells of a 2x2 area)
      output_elements:
        subgrids:
          count: 4
          size: 2x2
          location: one in each quadrant of the 4x4 output grid (top-left, top-right, bottom-left, bottom-right)
          content: representation of an input L-shape (3 pixels of the input object's color, 1 white pixel)
      relationships:
        - mapping: Each input L-shaped object corresponds to exactly one 2x2 subgrid in the output.
        - color_preservation: The color of the input object determines the non-white color used in its corresponding 2x2 output subgrid.
        - shape_to_position_mapping: The specific orientation (shape type) of the input L-shape determines the quadrant position (top-left, top-right, bottom-left, bottom-right) of its 2x2 representation in the output grid.
            - L-shape with empty bottom-right corner maps to output top-left quadrant.
            - L-shape with empty top-right corner maps to output bottom-left quadrant.
            - L-shape with empty top-left corner maps to output bottom-right quadrant.
            - L-shape with empty bottom-left corner maps to output top-right quadrant.
        - shape_representation: The 2x2 output subgrid visually represents the input L-shape within a 2x2 bounding box, using white for the empty cell.
    ```


*   **Natural Language Program:**
    1.  Initialize a 4x4 grid filled with the background color (white, 0). This will be the output grid.
    2.  Find all distinct objects in the input grid. An object is defined as a connected group of pixels with the same non-white color. Expect to find exactly four objects, each being a 3-pixel L-shape.
    3.  For each identified object:
        a.  Note its color.
        b.  Determine the orientation of the L-shape by identifying the position of the empty cell within its minimal 2x2 bounding box. There are four possible orientations (empty cell at top-left, top-right, bottom-left, or bottom-right).
        c.  Create a 2x2 grid representing this L-shape. Fill the three cells corresponding to the object's pixels with the object's color, and fill the fourth cell (the empty one) with the background color (white, 0).
        d.  Determine the target quadrant in the 4x4 output grid based *only* on the orientation identified in step 3b:
            i.  If the empty cell in the 2x2 representation is at the bottom-right, place the 2x2 grid in the top-left quadrant of the output (rows 0-1, columns 0-1).
            ii. If the empty cell is at the top-right, place the 2x2 grid in the bottom-left quadrant of the output (rows 2-3, columns 0-1).
            iii. If the empty cell is at the top-left, place the 2x2 grid in the bottom-right quadrant of the output (rows 2-3, columns 2-3).
            iv. If the empty cell is at the bottom-left, place the 2x2 grid in the top-right quadrant of the output (rows 0-1, columns 2-3).
    4.  Return the completed 4x4 output grid.
