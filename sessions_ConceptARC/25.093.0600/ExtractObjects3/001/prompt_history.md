
## train_1

**input:**
```
0 0 0 0 3 3 3 3 3 0 0 0 0
0 2 2 2 3 2 2 2 3 2 2 2 0
0 2 0 2 3 2 0 2 3 2 0 2 0
0 2 2 2 3 2 2 2 3 2 2 2 0
0 0 0 0 3 3 3 3 3 0 0 0 0
0 2 2 2 0 2 2 2 0 2 2 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0
0 2 2 2 0 2 2 2 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 2 2 2 0 2 2 2 0
0 2 0 2 0 2 0 2 0 2 0 2 0
0 2 2 2 0 2 2 2 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3
3 0 0 0 3
3 0 0 0 3
3 0 0 0 3
3 3 3 3 3
```


## train_2

**input:**
```
6 6 6 6 6 0 0 0 0 0 0
6 3 3 3 6 0 3 3 3 3 0
6 3 0 0 6 0 3 0 0 3 0
6 3 0 0 6 0 3 0 0 3 0
6 6 6 6 6 0 3 3 3 3 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 3 3 3 3
0 0 3 0 0 3 0 3 0 0 3
0 0 3 0 0 3 0 3 0 0 3
0 0 3 3 3 3 0 3 3 3 3
0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 6 6 6
6 0 0 0 6
6 0 0 0 6
6 0 0 0 6
6 6 6 6 6
```

Okay, analyzing the provided examples to understand the transformation.

**Perception of Elements:**

*   The input and output are grids of integers, likely representing colors (0 being the background).
*   The input grids contain multiple distinct shapes or patterns made of different non-zero colors.
*   The output grid seems to be a cropped section of the input grid, focusing on one specific shape.
*   In both examples, the target shape in the input is a rectangular frame (a border of one color surrounding an interior of another color or background).
*   The output grid represents this frame structure. The color of the frame itself is preserved, while the color(s) *inside* the frame in the input are replaced with the background color (0) in the output.
*   The dimensions of the output grid match the bounding box of the identified frame structure in the input.
*   The specific frame structure chosen seems to be the first one encountered (potentially scanning top-left).

**YAML Facts:**


```yaml
task_type: object_extraction_and_transformation
input_domain: 2D_grid_of_integers
output_domain: 2D_grid_of_integers
elements:
  - name: grid
    type: 2D_array
    properties:
      - cells: contain non-negative integers (colors)
      - background_color: 0
  - name: object
    type: connected_component_of_cells
    properties:
      - color: non-zero integer
      - shape: varies, includes rectangular frames
actions:
  - name: identify_target_object
    description: Find a specific object within the input grid, characterized as a rectangular frame made of a single non-zero color. It appears to be the first such object found.
    inputs: input_grid
    outputs: target_object_location, target_object_frame_color
  - name: extract_bounding_box
    description: Determine the subgrid corresponding to the bounding box of the target object.
    inputs: input_grid, target_object_location
    outputs: subgrid
  - name: transform_colors
    description: Modify the colors within the extracted subgrid based on the target object's frame color.
    inputs: subgrid, target_object_frame_color
    outputs: transformed_subgrid
  - name: generate_output
    description: Create the final output grid from the transformed subgrid.
    inputs: transformed_subgrid
    outputs: output_grid
relationships:
  - The output grid's dimensions are determined by the bounding box of the identified target object in the input grid.
  - The output grid's cell values are derived from the corresponding input grid cells within the bounding box.
  - Cells in the output corresponding to the target object's frame color retain that color.
  - Cells in the output corresponding to any other color *inside* the frame in the input are changed to the background color (0).
```


**Natural Language Program:**

1.  Scan the input grid to locate the bounding box of the first distinct rectangular frame object formed by a single, non-zero color (let this be `frame_color`).
2.  Determine the dimensions (height and width) of this bounding box.
3.  Create a new output grid with these dimensions.
4.  Iterate through each cell (`input_cell`) within the identified bounding box in the input grid. Let the corresponding cell in the new output grid be `output_cell`.
5.  If the color of `input_cell` is equal to `frame_color`, set the color of `output_cell` to `frame_color`.
6.  Otherwise (if the color of `input_cell` is *not* `frame_color`), set the color of `output_cell` to 0.
7.  Return the generated output grid.
