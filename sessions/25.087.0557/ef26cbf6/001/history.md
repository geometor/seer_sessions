
## train_1

**input:**
```
0 0 0 4 0 0 0 4 0 0 0
0 3 0 4 0 2 0 4 0 6 0
0 0 0 4 0 0 0 4 0 0 0
4 4 4 4 4 4 4 4 4 4 4
1 0 0 4 0 1 0 4 1 0 1
0 1 0 4 1 1 1 4 1 0 1
1 1 1 4 1 0 1 4 0 1 0
```


**output:**
```
0 0 0 4 0 0 0 4 0 0 0
0 3 0 4 0 2 0 4 0 6 0
0 0 0 4 0 0 0 4 0 0 0
4 4 4 4 4 4 4 4 4 4 4
3 0 0 4 0 2 0 4 6 0 6
0 3 0 4 2 2 2 4 6 0 6
3 3 3 4 2 0 2 4 0 6 0
```


## train_2

**input:**
```
0 0 0 4 1 0 0
0 7 0 4 0 1 1
0 0 0 4 0 1 0
4 4 4 4 4 4 4
0 0 0 4 1 1 0
0 3 0 4 0 1 0
0 0 0 4 1 1 1
4 4 4 4 4 4 4
0 0 0 4 1 1 0
0 8 0 4 0 1 1
0 0 0 4 1 0 1
```


**output:**
```
0 0 0 4 7 0 0
0 7 0 4 0 7 7
0 0 0 4 0 7 0
4 4 4 4 4 4 4
0 0 0 4 3 3 0
0 3 0 4 0 3 0
0 0 0 4 3 3 3
4 4 4 4 4 4 4
0 0 0 4 8 8 0
0 8 0 4 0 8 8
0 0 0 4 8 0 8
```

**Perception**

1.  **Grid Structure:** The input and output grids are separated into horizontal regions by solid horizontal lines of yellow pixels (color 4). These yellow lines remain unchanged in the output.
2.  **Objects:** Within each region (excluding the yellow separators), there are distinct objects composed of contiguous pixels of the same color, set against a white (color 0) background.
3.  **Key Colors:**
    *   Yellow (4): Static separators.
    *   White (0): Static background.
    *   Blue (1): Represents "target" objects whose color will be changed.
    *   Other colors (2, 3, 6, 7, 8 in examples): Represent "source" objects providing the new color for the targets.
4.  **Transformation Logic:** The core transformation involves changing the color of the blue (1) objects. The new color comes from a "source" object. The specific way the source color is determined depends on the arrangement within the regions:
    *   **Scenario 1 (e.g., `train_2`):** If a region contains both a blue (target) object and exactly one non-blue, non-yellow, non-white (source) object, the blue object's color is changed to the source object's color.
    *   **Scenario 2 (e.g., `train_1`):** If source objects are in one region and blue (target) objects are in a different region, the colors of the source objects are transferred to the target objects based on their relative horizontal positions (leftmost source color goes to leftmost target, etc.).
5.  **Source Object Handling:** After a source object's color is used to update a target object, the pixels originally belonging to the source object are changed to white (0) in the output.

**Facts**


```yaml
elements:
  - type: grid
    description: A 2D array of pixels with colors 0-9.
  - type: separator
    color: 4 (yellow)
    shape: horizontal line
    role: divides the grid into horizontal regions, remains static.
  - type: background
    color: 0 (white)
    role: fills empty space, remains static.
  - type: target_object
    color: 1 (blue)
    shape: variable contiguous blocks
    role: receives a new color based on a source object.
  - type: source_object
    color: any color except 0, 1, 4
    shape: variable contiguous blocks
    role: provides the new color for a target object. Original location becomes white (0).
  - type: region
    definition: A horizontal section of the grid bounded by yellow separators or grid edges.
    role: Defines the scope for identifying corresponding source and target objects.

relationships:
  - type: spatial
    description: Objects exist within regions defined by separators.
  - type: mapping
    description: A rule determines which source object's color applies to which target object.
    conditions:
      - if source and target are in the same region: target takes the color of the single source in that region.
      - if source(s) and target(s) are in different regions: colors are mapped based on left-to-right positional order between the set of source objects and the set of target objects.

actions:
  - name: identify_separators
    input: grid
    output: list of row indices containing yellow lines.
  - name: identify_regions
    input: grid, separator indices
    output: list of regions (subgrids or coordinate sets).
  - name: find_objects
    input: region, colors_to_find
    output: list of objects (pixel coordinates, color, bounding box).
  - name: determine_mapping_rule
    input: source objects list, target objects list, region information
    output: mapping pairs (source_color, target_object_pixels).
  - name: apply_color_change
    input: output_grid, target_object_pixels, new_color
    output: modified output_grid.
  - name: clear_source_pixels
    input: output_grid, source_object_pixels
    output: modified output_grid (source pixels set to 0).
```


**Natural Language Program**

1.  Initialize the `output_grid` as a copy of the `input_grid`.
2.  Identify all horizontal lines composed entirely of yellow pixels (color 4). These lines act as separators.
3.  Define the regions based on these separators. A region is a horizontal slice of the grid located between two separators, above the first separator, or below the last separator.
4.  Create two lists: `all_source_objects` and `all_target_objects`. Iterate through all regions:
    a.  Find all contiguous objects of blue color (1) within the current region. Add them to `all_target_objects`, storing their pixel coordinates and region index.
    b.  Find all contiguous objects of any color other than white (0), blue (1), or yellow (4) within the current region. Add them to `all_source_objects`, storing their pixel coordinates, color, and region index.
5.  Determine the source-target mapping:
    a.  Create an empty list `mappings`.
    b.  First, check for same-region mappings: Iterate through each region index `r`. Find source objects (`region_sources`) and target objects (`region_targets`) belonging to region `r`. If `region_sources` contains exactly one source object and `region_targets` contains one or more target objects, then for each target object in `region_targets`, add a mapping pair (source object's color, target object's pixels) to the `mappings` list. Mark these source and target objects as "mapped".
    c.  Next, check for cross-region mappings: Collect all "unmapped" source objects and "unmapped" target objects from all regions. If both collections are non-empty:
        i.  Sort the unmapped source objects based on their horizontal position (e.g., by the minimum column index of their bounding box, from left to right).
        ii. Sort the unmapped target objects similarly based on their horizontal position.
        iii. Assuming the number of unmapped sources equals the number of unmapped targets, iterate through the sorted lists. For the k-th source object and the k-th target object, add a mapping pair (k-th source object's color, k-th target object's pixels) to the `mappings` list. Mark these objects as "mapped".
6.  Apply the transformations based on the `mappings`:
    a.  Iterate through each `(source_color, target_pixels)` pair in the `mappings` list. For every pixel coordinate in `target_pixels`, set the corresponding pixel in the `output_grid` to `source_color`.
7.  Clear the original source object locations: Iterate through `all_source_objects`. For each source object that was used in a mapping (i.e., marked as "mapped" or present in the `mappings`), iterate through its original pixel coordinates. Set the corresponding pixels in the `output_grid` to white (0).
8.  Return the final `output_grid`.
