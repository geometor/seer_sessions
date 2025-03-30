**Perception of Task Elements:**

1.  **Input:** The input is a grid containing several distinct, non-overlapping, single-color objects scattered on a white background. These objects are simple lines or small rectangles.
2.  **Output:** The output is a smaller, square grid. It represents a composite image formed by layering the input objects concentrically.
3.  **Transformation:** The transformation involves identifying all colored objects, determining their relative sizes (based on bounding boxes), and arranging them as centered layers in the output grid. The outermost layer corresponds to the object with the largest bounding box, and the innermost layer corresponds to the object with the smallest bounding box.
4.  **Object Identification:** Objects are contiguous blocks of non-white pixels.
5.  **Ordering:** Objects need to be ordered based on the size of their bounding boxes. The area of the bounding box appears to be the primary sorting key. The object with the smallest bounding box area becomes the center of the output pattern. In case of ties for the smallest area, the object whose bounding box is most square-like (aspect ratio closest to 1) is chosen as the center. The remaining objects are ordered from smallest area to largest area.
6.  **Output Construction:**
    *   The output grid dimensions are determined by the largest dimension (width or height) of the bounding box of the object with the *largest* area. The output grid is always square.
    *   The construction proceeds layer by layer, starting from the outside. The outermost layer (the entire output grid) is filled with the color of the object with the largest bounding box area.
    *   Subsequent inner layers are created by taking the object with the next largest bounding box area. A centered square/rectangle is drawn with this object's color. The size of this inner square is 2 units smaller (in both height and width) than the layer immediately outside it.
    *   This process repeats, moving inwards, using the ordered objects (from largest area towards smallest), until the central object (smallest area) is drawn in the innermost layer.

**Facts (YAML):**


```yaml
task_description: Create a composite image by layering input objects concentrically based on size.

input_elements:
  - type: grid
    description: Contains a white background (color 0) and multiple distinct, non-overlapping, single-color objects.
    properties:
      - colors_present: [0, and others from 1-9]
      - object_shapes: simple lines or small rectangles

output_elements:
  - type: grid
    description: A square grid representing layered objects from the input.
    properties:
      - size: Determined by the largest dimension of the largest input object's bounding box.
      - content: Concentric layers of colors corresponding to input objects.
      - background: No background color; the grid is fully filled by layers.

transformation_steps:
  - step: 1
    action: find_objects
    description: Identify all contiguous blocks of non-white pixels in the input grid.
    inputs:
      - input_grid
    outputs:
      - list_of_objects: Each object represented by its color and pixel coordinates.
  - step: 2
    action: calculate_bounding_boxes
    description: Determine the bounding box (top-left corner, width, height) and area for each identified object.
    inputs:
      - list_of_objects
    outputs:
      - objects_with_bboxes: List of objects, each with color, bbox coordinates, width, height, and area.
  - step: 3
    action: identify_center_object
    description: Find the object with the minimum bounding box area. Use aspect ratio (closest to 1) as a tie-breaker.
    inputs:
      - objects_with_bboxes
    outputs:
      - center_object
      - other_objects
  - step: 4
    action: sort_other_objects
    description: Sort the 'other_objects' list by bounding box area in ascending order.
    inputs:
      - other_objects
    outputs:
      - sorted_other_objects
  - step: 5
    action: determine_output_size
    description: Find the object with the maximum bounding box area from the combined list (center_object + sorted_other_objects). The output size is a square grid with side length equal to the maximum dimension (width or height) of this object's bounding box.
    inputs:
      - center_object
      - sorted_other_objects
    outputs:
      - output_size
      - largest_object: The object determining the output size.
  - step: 6
    action: initialize_output_grid
    description: Create an empty output grid of the calculated 'output_size'.
    inputs:
      - output_size
    outputs:
      - output_grid
  - step: 7
    action: draw_layers
    description: Draw concentric square layers onto the output grid, starting from the largest object down to the center object.
    inputs:
      - output_grid
      - largest_object
      - sorted_other_objects (reversed, from largest area to smallest)
      - center_object
    process:
      - Combine `largest_object` and `sorted_other_objects` (reversed) into an ordered list `layer_objects`.
      - Set `current_layer_size` = `output_size`.
      - For each object in `layer_objects`:
          - Fill a centered square of size `current_layer_size` with the object's color.
          - `current_layer_size` = `current_layer_size` - 2
      - Fill a centered square of size `current_layer_size` with the `center_object`'s color.
    outputs:
      - final_output_grid

relationships:
  - type: layering
    description: Objects are layered based on the size of their bounding boxes.
    elements:
      - input objects
      - output grid layers
  - type: sizing
    description: The output grid size is determined by the largest dimension of the largest object. Layer sizes decrease concentrically.
    elements:
      - largest input object bounding box
      - output grid dimensions
      - layer sizes
```


**Natural Language Program:**

1.  Identify all distinct colored objects (groups of connected pixels of the same color, excluding white) in the input grid.
2.  For each object, determine its color and its bounding box (minimum rectangle enclosing the object). Calculate the area of each bounding box (width * height) and its aspect ratio (max(width, height) / min(width, height)).
3.  Find the object with the smallest bounding box area. If multiple objects share the minimum area, select the one whose bounding box aspect ratio is closest to 1 (most square-like). This is the "center object".
4.  Create a list of all other objects. Sort this list in ascending order based on their bounding box area.
5.  Identify the object with the largest bounding box area among all objects (including the center object). Let its bounding box dimensions be W and H. The size of the output square grid will be N x N, where N is the maximum of W and H.
6.  Create an N x N output grid.
7.  Start the drawing process:
    a.  Take the object identified in step 5 (the one with the largest area). Fill the entire N x N output grid with its color. This is the outermost layer. Let the current layer dimension be N.
    b.  Iterate through the sorted list of other objects, from the one with the largest area down to the one with the smallest area (the list created in step 4, processed in reverse order). For each object:
        i.  Decrease the current layer dimension by 2 (New Dimension = Current Dimension - 2).
        ii. Fill a centered square of size New Dimension x New Dimension in the output grid with the current object's color.
        iii. Update the current layer dimension to this New Dimension.
    c.  Finally, take the center object (identified in step 3). Decrease the current layer dimension by 2. Fill a centered square of this final size with the center object's color.
8.  The resulting grid is the final output.