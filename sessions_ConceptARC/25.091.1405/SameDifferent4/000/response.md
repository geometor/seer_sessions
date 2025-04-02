*   **Perception:** The task involves analyzing a grid containing several distinct lines or shapes composed of different colors against a white background. The transformation selectively removes some of these shapes based on their orientation (horizontal, vertical, or diagonal). By comparing the input and output grids in the examples, it appears that the orientation present in the majority of the shapes is identified, and all shapes *not* matching that majority orientation are removed (turned white).

*   **YAML Facts:**
    
```yaml
    task_description: Selectively remove shapes/lines based on their orientation relative to the majority orientation.
    
    elements:
      - element: grid
        description: A 2D array of pixels representing colors (0-9). Contains a background color and multiple shapes.
        properties:
          - background_color: white (0)
          - dimensions: Variable (e.g., 10x10 in examples)
      - element: shape/line
        description: A contiguous object of a single non-white color.
        properties:
          - color: Any color except white (0)
          - connectivity: Pixels of the same color are adjacent (including diagonals for identification, but the shape itself defines orientation).
          - orientation: Can be Horizontal, Vertical, or Diagonal.
            - Horizontal: All pixels share the same row index.
            - Vertical: All pixels share the same column index.
            - Diagonal: Neither purely horizontal nor purely vertical (in these examples, they form straight diagonal lines).
    
    transformation:
      - action: identify_objects
        description: Find all distinct contiguous shapes of non-white colors in the input grid.
      - action: determine_orientation
        description: Classify each identified shape as Horizontal, Vertical, or Diagonal.
      - action: count_orientations
        description: Count the number of shapes belonging to each orientation category.
      - action: find_majority_orientation
        description: Identify the orientation category with the highest count.
      - action: filter_shapes
        description: Remove shapes (set their pixels to white) whose orientation does not match the majority orientation. Keep shapes that match the majority orientation.
      - action: generate_output
        description: Create the output grid containing only the background and the shapes matching the majority orientation.
    
    relationships:
      - The decision to keep or remove a shape depends on its orientation relative to the orientations of all other shapes in the grid.
      - Shapes with the most common orientation type are preserved.
      - Shapes with less common orientation types are removed.
    
    examples_analysis:
      - train_1:
          - Input shapes: Blue (Diagonal, 1), Magenta (Vertical, 1), Yellow (Vertical, 1), Red (Horizontal, 1)
          - Orientation counts: Vertical=2, Diagonal=1, Horizontal=1
          - Majority orientation: Vertical
          - Shapes removed: Blue (Diagonal), Red (Horizontal)
          - Output: Contains only Magenta (Vertical), Yellow (Vertical) shapes.
      - train_2:
          - Input shapes: Green (Diagonal, 1), Red (Horizontal, 1), Maroon (Vertical, 1), Orange (Horizontal, 1)
          - Orientation counts: Horizontal=2, Diagonal=1, Vertical=1
          - Majority orientation: Horizontal
          - Shapes removed: Green (Diagonal), Maroon (Vertical)
          - Output: Contains only Red (Horizontal), Orange (Horizontal) shapes.
    ```


*   **Natural Language Program:**
    1.  Scan the input grid to identify all distinct connected objects (shapes) composed of non-white pixels. Use a method like Breadth-First Search (BFS) or Depth-First Search (DFS) to find all connected pixels of the same color for each object, ensuring each pixel is assigned to only one object.
    2.  For each identified object, determine its orientation:
        *   If all pixels in the object have the same row coordinate, classify it as "Horizontal".
        *   If all pixels in the object have the same column coordinate, classify it as "Vertical".
        *   Otherwise (if neither of the above conditions is met), classify it as "Diagonal".
    3.  Count how many objects fall into each orientation category (Horizontal, Vertical, Diagonal).
    4.  Identify the "majority orientation" - the orientation category with the highest count of objects. (Assume there will be a unique majority based on the examples).
    5.  Create a new grid, initially identical to the input grid. This will become the output grid.
    6.  Iterate through all the objects identified in step 1.
    7.  For each object, compare its orientation (determined in step 2) to the majority orientation (determined in step 4).
    8.  If an object's orientation is *different* from the majority orientation, change the color of all pixels belonging to that object to white (0) in the output grid.
    9.  The final state of the modified grid is the result of the transformation.