## Perception

The input grids contain a white background (color 0) and several distinct objects, each composed of a single non-white color. Typically, there are three different non-white colors/objects in each input grid. The objects have varying shapes and sizes and are scattered across the grid.

The output grid is significantly smaller than the input grid and represents a cropped view containing exactly one of the objects from the input grid. The cropping is defined by the bounding box of the selected object. The selection criteria for which object is chosen appears to be based on the numerical value of the colors present.

Specifically, in each example, there are three distinct non-white colors. Let these colors be `c1`, `c2`, and `c3`. If we sort these color values numerically, the object chosen for the output corresponds to the color whose value lies *between* the minimum and maximum color values present in the input grid.

## Facts


```yaml
task_type: object_selection_and_extraction
input_characteristics:
  - grid_background: white (0)
  - contains_multiple_objects: true
  - object_definition: contiguous block of same non-white color
  - number_of_distinct_non_white_colors: 3 (in all examples)
output_characteristics:
  - grid_background: potentially mixed (includes original object pixels and potentially white pixels from within the object's bounding box)
  - contains_single_object: true
  - output_content: bounding box of a selected object from the input
selection_rule:
  - identify_distinct_colors: Find all unique non-white color values (c1, c2, c3) in the input.
  - sort_colors: Order the colors numerically (min_c, mid_c, max_c).
  - select_object_by_color: The object selected is the one whose color is `mid_c`.
extraction_rule:
  - find_object_pixels: Locate all pixels corresponding to the selected color `mid_c`.
  - calculate_bounding_box: Determine the minimum and maximum row and column indices containing these pixels.
  - crop_grid: Extract the subgrid defined by the bounding box from the original input grid.
relationships:
  - The output is a subgrid of the input.
  - The specific subgrid (object) chosen depends on a numerical comparison of the color values of all objects present.
```


## Natural Language Program

1.  Scan the input grid to identify all unique non-white pixel color values present.
2.  Determine the minimum, maximum, and median (middle value) of these unique color values.
3.  Identify the object in the input grid that consists of pixels matching the median color value.
4.  Determine the bounding box of this selected object (the smallest rectangle containing all pixels of the median color).
5.  Create the output grid by extracting the portion of the input grid corresponding to this bounding box.