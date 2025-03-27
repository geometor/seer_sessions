*   **Perception:** The input grids contain multiple distinct objects (contiguous blocks of non-white pixels) scattered on a white background. The output grid contains only one of these objects, specifically the one that occupies the largest proportion of its own bounding box area. The output grid's dimensions match the bounding box of the selected object, and it contains the exact pixels (including background pixels) from that bounding box in the input.

*   **Facts:**
    
```yaml
    task_type: object_selection_and_extraction
    
    input_features:
      - description: Grid containing multiple distinct objects (contiguous blocks of non-white pixels) on a white background.
      - properties:
          - grid_size: variable (10x10 in examples)
          - background_color: white (0)
          - object_colors: various (non-white)
          - object_shapes: various
          - object_count: multiple (3 in examples)
    
    output_features:
      - description: Grid containing a single object extracted from the input.
      - properties:
          - grid_size: variable, determined by the bounding box of the selected object.
          - background_color: white (0), may be present within the bounding box.
          - object_color: single color, matching the selected object from input.
          - object_shape: matches the selected object from input.
    
    transformation:
      - step: Identify all distinct objects in the input grid.
        - criteria: Contiguous pixels of the same non-white color.
      - step: For each identified object:
        - calculate: Minimal bounding box (min_row, max_row, min_col, max_col).
        - calculate: Bounding box area ((max_row - min_row + 1) * (max_col - min_col + 1)).
        - calculate: Pixel count (number of pixels belonging to the object).
        - calculate: Fill ratio (Pixel count / Bounding box area).
      - step: Select the object with the maximum fill ratio.
        - tie_breaking: (Not specified in examples, assume unique maximum or default like top-most, left-most if needed).
      - step: Extract the subgrid corresponding to the bounding box of the selected object.
      - step: The extracted subgrid is the output grid.
    
    relationships:
      - The output grid is a subgrid of the input grid.
      - The object in the output is selected based on a calculated property (fill ratio) relative to other objects in the input.
      - The size of the output grid depends on the dimensions of the selected object's bounding box.
    ```


*   **Natural Language Program:**
    1.  Find all distinct groups of connected, non-white pixels in the input grid. Call these "objects".
    2.  For each object:
        a.  Determine its minimal bounding box (the smallest rectangle enclosing all its pixels).
        b.  Count the number of pixels belonging to the object (let this be `P`).
        c.  Calculate the area of the bounding box (height * width, let this be `A`).
        d.  Calculate the object's fill ratio `R = P / A`.
    3.  Identify the object that has the highest fill ratio `R`.
    4.  Determine the bounding box coordinates (top row, bottom row, left column, right column) of this selected object.
    5.  Create the output grid by copying the rectangular region defined by these bounding box coordinates from the input grid.