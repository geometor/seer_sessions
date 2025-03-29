## Perception

1.  **Grid Structure:** The input grids have a consistent background color, azure (8).
2.  **Objects:** Multiple distinct objects (contiguous areas of non-azure colors) are present within each input grid. These objects are separated by the azure background.
3.  **Object Composition:** Some objects are composed solely of white (0) pixels with potentially one other non-white, non-azure pixel. Other objects have a more complex structure, often involving yellow (4) pixels alongside other colors like red (2), green (3), or blue (1), as well as white (0).
4.  **Selection Criterion:** In each example, exactly one object contains yellow (4) pixels. The other object(s) do not contain yellow.
5.  **Transformation:** The output grid isolates the object containing yellow pixels.
6.  **Output Format:** The output grid represents the selected object within its minimal bounding box. The original azure background pixels within this bounding box are replaced with white (0) pixels in the output. The colors and arrangement of the pixels belonging to the selected object itself are preserved.

## Facts


```yaml
task_context:
  - description: Selects and isolates a specific object from the input grid based on its color composition.
  - input_grid_properties:
      - background_color: azure (8)
      - contains_multiple_objects: true
      - objects_separated_by_background: true
  - output_grid_properties:
      - background_color: white (0)
      - contains_single_object: true
      - dimensions: minimal bounding box of the selected object

objects:
  - id: background
    - color: azure (8) in input, white (0) in output (within bounding box)
  - id: object_to_select
    - description: The contiguous non-azure object that contains at least one yellow (4) pixel.
    - properties:
        - must_contain_color: yellow (4)
        - colors_preserved_in_output: true
        - position_relative_to_output_grid: fills the grid
  - id: other_objects
    - description: Contiguous non-azure objects that do NOT contain any yellow (4) pixels.
    - properties:
        - excluded_from_output: true

actions:
  - 1_identify_objects: Find all contiguous groups of non-azure (8) pixels in the input grid.
  - 2_filter_objects: Select the single object that includes at least one yellow (4) pixel.
  - 3_determine_bounding_box: Find the minimum and maximum row and column indices containing the selected object.
  - 4_crop_object: Extract the portion of the input grid defined by the bounding box.
  - 5_replace_background: Change all azure (8) pixels within the cropped area to white (0).
  - 6_generate_output: Create the final output grid from the modified cropped area.

relationships:
  - selection_rule: The presence of yellow (4) pixels uniquely identifies the object to be transformed into the output.
  - spatial_transformation: The output is a subgrid (crop) of the input, focused on the selected object.
  - color_transformation: The background color within the cropped area changes from azure (8) to white (0). Object colors remain unchanged.
```


## Natural Language Program

1.  Scan the input grid to identify all distinct, contiguous objects composed of non-azure (8) pixels.
2.  Examine each identified object to determine if it contains any yellow (4) pixels.
3.  Select the unique object that contains at least one yellow (4) pixel.
4.  Calculate the bounding box (minimum and maximum row and column indices) that encloses the selected object.
5.  Create a new output grid with dimensions matching the height and width of the bounding box.
6.  Iterate through each cell within the calculated bounding box coordinates in the *input* grid.
7.  For each cell:
    a.  If the input grid cell color is azure (8), place a white (0) pixel in the corresponding position in the output grid.
    b.  Otherwise (if the input grid cell color is not azure), copy the original color from the input grid cell to the corresponding position in the output grid.
8.  The resulting grid is the final output.