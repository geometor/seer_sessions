*   **Perception of the elements:**
    *   The input grids contain multiple distinct objects (contiguous blocks of non-white pixels) on a white background.
    *   One prominent object is always composed of blue pixels (color 1). This blue object often forms a frame or a boundary, typically rectangular or L-shaped, near one edge or corner of the grid.
    *   Other objects are composed of various colors (red, green, yellow, gray, magenta, azure, maroon, orange).
    *   Some of these other colored objects appear inside or touching the area defined by the blue frame, while others are located distinctly separate from it.
    *   The output grid contains a subset of the non-blue objects from the input grid.
    *   The objects present in the output are those from the input that were *not* located inside or touching the blue frame.
    *   The relative positions of the kept objects are preserved in the output.
    *   The output grid is smaller than the input grid and seems sized to tightly fit the collection of kept objects.

*   **YAML Facts:**
    
```yaml
    task_elements:
      - element: grid
        properties:
          - background_color: white (0)
          - contains: multiple objects
      - element: object
        properties:
          - type: blue_frame
            color: blue (1)
            shape: variable (often rectangular or L-shaped frame)
            role: boundary marker or filter region
          - type: colored_shape
            color: non-white (0), non-blue (1)
            shape: variable geometric forms
            role: content to be potentially filtered
    relationships:
      - type: spatial
        nodes: [colored_shape, blue_frame]
        property: adjacency (8-connectivity - sharing edge or corner)
        significance: Determines filtering; shapes adjacent to the blue_frame are excluded.
      - type: spatial
        nodes: [kept_colored_shapes] # Shapes not adjacent to blue_frame
        property: relative_position
        significance: Preserved between input and output.
    actions:
      - identify: all non-white objects
      - classify: objects into 'blue_frame' and 'colored_shape'
      - check: adjacency between each 'colored_shape' pixel and any 'blue_frame' pixel
      - filter: keep 'colored_shape' objects that have no adjacency to the 'blue_frame'
      - calculate: minimum bounding box containing all kept 'colored_shape' objects
      - construct: output grid based on bounding box size
      - place: kept 'colored_shape' objects into the output grid, maintaining relative positions
    ```


*   **Natural Language Program:**
    1.  Identify all distinct contiguous objects composed of non-white (0) pixels within the input grid.
    2.  Separate these objects into two categories: those composed entirely of blue (1) pixels (the "frame objects") and all other non-white objects (the "content objects").
    3.  Initialize an empty list to store the content objects that should be kept.
    4.  For each content object:
        a.  Iterate through all pixels belonging to this content object.
        b.  For each pixel, check its 8 neighbors (including diagonals).
        c.  If any neighbor belongs to any of the blue frame objects identified in step 2, mark this content object as "adjacent to frame" and stop checking for this object.
        d.  If, after checking all pixels of the content object, it has not been marked as "adjacent to frame", add it to the list of kept objects.
    5.  If no objects are kept, the output is empty or handled as per specific task rules (likely an empty grid or a minimal 1x1 white grid, though examples show non-empty outputs).
    6.  If objects are kept:
        a.  Determine the minimum bounding box (minimum row, maximum row, minimum column, maximum column) that encompasses all pixels of all the kept objects.
        b.  Calculate the height and width of this bounding box.
        c.  Create a new output grid with this calculated height and width, initialized with the white (0) background color.
        d.  For each kept object, copy its pixels into the new output grid, translating their coordinates so that their positions relative to the top-left corner of the bounding box are maintained. (Specifically, subtract the minimum row and minimum column of the bounding box from the original coordinates of each pixel before placing it in the output grid).
    7.  Return the newly constructed output grid.