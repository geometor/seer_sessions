*   **Perception:** The task involves processing a 10x10 grid containing several distinct "objects" composed of non-zero digits against a background of zeros. The goal is to identify a specific object based on certain properties and extract its bounding box as the output grid.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - element: input_grid
        description: A 10x10 grid of single digits (0-9).
        properties:
          - dimensions: [10, 10]
          - background_digit: 0
          - contains: non_zero_objects
      - element: non_zero_objects
        description: Connected components of identical non-zero digits.
        properties:
          - digit_value: The digit making up the object (1-9).
          - cells: List of coordinates [(row, col), ...] occupied by the object.
          - cell_count: Number of cells in the object.
          - bounding_box: The smallest rectangle containing all object cells [min_row, max_row, min_col, max_col].
          - bbox_area: The area of the bounding box ((max_row - min_row + 1) * (max_col - min_col + 1)).
          - density: Ratio of cell_count to bbox_area.
      - element: output_grid
        description: A rectangular subgrid extracted from the input grid.
        properties:
          - content: Matches the content within the bounding box of a selected non_zero_object from the input.
          - dimensions: Determined by the bounding box size of the selected object.

    transformation:
      input: input_grid
      output: output_grid
      steps:
        - action: identify_objects
          description: Find all distinct connected non-zero objects in the input grid.
          input: input_grid
          output: list_of_objects_with_properties
        - action: calculate_properties
          description: For each object, calculate its cell_count, bounding_box, bbox_area, and density.
          input: list_of_objects_with_properties
          output: list_of_objects_with_calculated_properties
        - action: find_max_density
          description: Determine the maximum density value among all objects.
          input: list_of_objects_with_calculated_properties
          output: max_density_value
        - action: filter_by_max_density
          description: Identify all objects having the maximum density.
          input: list_of_objects_with_calculated_properties, max_density_value
          output: candidate_objects
        - action: select_object
          description: >
            If only one candidate object exists, select it.
            If multiple candidate objects exist (tie in density), select the one with the largest bounding box area among them.
          input: candidate_objects
          output: selected_object
        - action: extract_subgrid
          description: Extract the subgrid from the input_grid corresponding to the bounding_box of the selected_object.
          input: input_grid, selected_object.bounding_box
          output: output_grid

    relationships:
      - The output_grid's content and dimensions are directly derived from the bounding box of the selected_object.
      - The selected_object is chosen based on maximizing density, with bounding box area used as a tie-breaker.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct connected groups (objects) of non-zero digits in the input grid.
    2.  For each identified object:
        a.  Determine its bounding box (the smallest rectangle enclosing the object).
        b.  Calculate the area of the bounding box.
        c.  Count the number of cells occupied by the object.
        d.  Calculate the object's density by dividing its cell count by its bounding box area.
    3.  Find the maximum density value among all calculated densities.
    4.  Select all objects that have this maximum density.
    5.  If only one object has the maximum density, choose this object.
    6.  If multiple objects share the maximum density, choose the object among them that has the largest bounding box area.
    7.  Extract the rectangular region from the input grid defined by the bounding box of the chosen object. This extracted region is the output grid.