*   **Perception:** The task involves processing 10x10 grids containing numerical digits. The input grid displays several distinct "objects," which are connected groups of identical non-zero digits, set against a background of zeros. The output grid contains only one of these objects, specifically the one that extends furthest down vertically in the input grid. All other objects and background cells are represented by zeros in the output.

*   **Facts YAML:**
    
```yaml
    task_elements:
      - Input Grid:
          type: 2D array of integers
          description: Represents a 10x10 grid with a background (0) and several colored objects (non-zero digits).
          properties:
            - dimensions: 10x10
            - background_color: 0
      - Output Grid:
          type: 2D array of integers
          description: Represents a 10x10 grid containing only the 'lowest' object from the input grid.
          properties:
            - dimensions: 10x10
            - background_color: 0
      - Object:
          type: Conceptual element
          description: A connected component of identical non-zero digits within the input grid.
          properties:
            - color: The digit value (1-9)
            - pixels: Set of (row, column) coordinates comprising the object.
            - lowest_point: The maximum row index occupied by any pixel of the object.
    transformation:
      - action: Identify Objects
        description: Find all distinct connected components of non-zero values in the input grid.
      - action: Determine Lowest Point per Object
        description: For each identified object, find the maximum row index among its constituent pixels.
      - action: Select Lowest Object
        description: Identify the object whose lowest point has the highest row index compared to all other objects.
        assumptions:
          - There is a unique object that is the lowest. Tie-breaking rules are not evident from examples if multiple objects share the same maximum row index.
      - action: Generate Output
        description: Create a new grid of the same size, initialized with the background color (0). Copy the pixels of the selected lowest object from the input grid to their corresponding positions in the output grid.
    ```


*   **Natural Language Program:**
    1.  Initialize an empty output grid of the same dimensions as the input grid, filled with the background color 0.
    2.  Scan the input grid to identify all distinct connected objects formed by non-zero digits. Keep track of the color and coordinates of each pixel belonging to each object.
    3.  For each identified object, determine the maximum row index reached by any of its pixels (this represents the "lowest point" of the object).
    4.  Find the overall maximum row index among all the lowest points calculated in the previous step.
    5.  Identify the object(s) whose lowest point matches this overall maximum row index.
    6.  Iterate through the pixels of the identified lowest object(s). For each pixel (at row `r`, column `c`) belonging to the lowest object(s), set the corresponding cell in the output grid (`output[r][c]`) to the color (digit value) of that object.
    7.  Return the completed output grid.