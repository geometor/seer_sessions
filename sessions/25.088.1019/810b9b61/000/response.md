Okay, let's analyze the task examples.

**Perception**

1.  **Grid Structure:** The inputs and outputs are 2D grids containing pixels of different colors, primarily white (0) and blue (1) in the input, and white (0), blue (1), and green (3) in the output.
2.  **Background:** The background color is consistently white (0) and remains unchanged between input and output.
3.  **Objects:** The non-background pixels form distinct shapes or objects. In the input, these objects are exclusively blue (1).
4.  **Transformation:** The core transformation involves changing the color of *some* of the blue objects to green (3). Other blue objects remain unchanged.
5.  **Identifying Feature:** Comparing the blue objects that change to green with those that stay blue reveals a consistent pattern: the objects that turn green contain at least one "hole" – a white (0) pixel completely enclosed within the blue (1) pixels of that object. Objects without such enclosed white pixels remain blue.
6.  **Connectivity:** Objects are defined by contiguous blocks of the same color (blue in this case), considering side-by-side adjacency (not diagonal). The "hole" must be surrounded by pixels belonging to the *same* contiguous blue object.

**Facts**


```yaml
task_description: "Recolor blue objects based on whether they contain an internal 'hole'."
grid_properties:
  background_color: 0  # white
objects:
  - type: "contiguous_shape"
    input_color: 1  # blue
    properties:
      - name: "has_internal_hole"
        description: "Contains at least one white (0) pixel completely surrounded (4-connectivity) by pixels of this blue object."
        value_type: boolean
transformation:
  - description: "Identify all distinct blue objects."
    input_elements: "grid"
    output_elements: "list_of_blue_objects"
  - description: "For each blue object, determine if it has the 'has_internal_hole' property."
    input_elements: "blue_object"
    output_elements: "boolean_flag (has_hole)"
  - description: "Based on the flag, decide the output color."
    input_elements: "blue_object, has_hole_flag"
    logic: "If has_hole is true, output_color is green (3). Otherwise, output_color is blue (1)."
    output_elements: "output_color"
  - description: "Construct the output grid by replacing input blue objects with their determined output color. Keep background pixels unchanged."
    input_elements: "input_grid, list_of_blue_objects, list_of_output_colors"
    output_elements: "output_grid"
unchanged_elements:
  - type: "pixel"
    color: 0 # white background
  - type: "object"
    input_color: 1 # blue
    condition: "Object does not have the 'has_internal_hole' property."
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all distinct connected objects composed of blue (1) pixels in the input grid. Use 4-way adjacency (up, down, left, right) to determine connectivity.
3.  For each identified blue object:
    a.  Check if there exists at least one white (0) pixel such that all four of its immediate neighbors (up, down, left, right) are blue pixels belonging *to this specific object*.
    b.  If such a white pixel (a "hole") is found for the object:
        i.  Iterate through all the pixel coordinates belonging to this blue object.
        ii. For each pixel coordinate, change its color in the *output* grid to green (3).
4.  Return the modified output grid. (Blue objects without holes and the white background remain unchanged from the initial copy).