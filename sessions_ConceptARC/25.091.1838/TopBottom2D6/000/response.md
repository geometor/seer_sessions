*   **Perception**: The input grid contains multiple distinct objects composed of non-white pixels on a white background. The output grid contains one of the objects from the input grid, cropped to its minimal bounding box. The key transformation involves selecting a specific object from the input based on its vertical position.

*   **Facts**:
    
```yaml
    task_type: object_selection_extraction
    background_color: 0 # white
    input_features:
      - property: objects
        description: Contiguous blocks of non-background pixels.
        value: Multiple objects of different colors and shapes exist in each input.
      - property: object_position
        description: The vertical position of each object.
        value: Objects are located at different row indices.
    transformation:
      - action: identify_objects
        description: Find all contiguous groups of non-background pixels.
      - action: determine_lowest_point
        description: For each object, find the maximum row index occupied by its pixels.
      - action: select_object
        description: Choose the object whose lowest point has the highest row index compared to other objects.
      - action: extract_bounding_box
        description: Determine the minimum rectangular area enclosing the selected object.
      - action: crop_object
        description: Create the output grid containing only the pixels of the selected object within its bounding box.
    output_features:
      - property: grid_content
        description: The pixels forming the selected object.
        value: Matches the shape and color of the lowest object from the input.
      - property: grid_size
        description: The dimensions of the output grid.
        value: Corresponds to the minimal bounding box of the selected object.
    relationships:
      - type: positional_selection
        description: The object selected for the output is the one positioned lowest (maximum row index) in the input grid.
    ```


*   **Natural Language Program**:
    1.  Identify all distinct contiguous objects in the input grid that are not the background color (white, 0).
    2.  For each identified object, find the row index of its lowest pixel (the maximum row index among all pixels belonging to that object).
    3.  Select the object that has the highest maximum row index (i.e., the object that extends furthest down the grid).
    4.  Determine the minimal bounding box coordinates (top row, bottom row, left column, right column) that enclose the selected object.
    5.  Create a new output grid with dimensions equal to the height and width of the bounding box.
    6.  Copy the pixels belonging to the selected object from the input grid into the output grid, maintaining their relative positions within the bounding box. Pixels within the bounding box that are not part of the selected object should be represented by the background color (white, 0).