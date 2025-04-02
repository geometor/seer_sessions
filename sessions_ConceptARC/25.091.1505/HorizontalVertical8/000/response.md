*   **Perception of task elements:**
    *   The input grids contain a background of white pixels (0) and several distinct objects composed of contiguous pixels of the same color (non-white).
    *   In each example, there is one prominent green object (color 3) which appears to be the largest or most central object.
    *   Other objects of various colors are scattered around the grid.
    *   The output grids retain the central green object and some of the other objects, while the remaining objects are removed (replaced with white pixels).
    *   The key transformation seems to involve identifying the central green object and then selectively removing other objects based on their spatial relationship to it. Specifically, objects that are *not* adjacent (including diagonally) to the central green object are removed.

*   **YAML Facts:**
    
```yaml
    task_description: Retain the largest green object and any other object directly adjacent (including diagonals) to it, removing all other objects.

    elements:
      - role: background
        color: white (0)
      - role: objects
        description: Contiguous blocks of non-white pixels.
        properties:
          - color: (1-9)
          - pixels: list of (row, col) tuples
          - size: count of pixels
          - is_green: boolean (color == 3)
          - is_largest_green: boolean (largest size among green objects)
          - adjacent_to_largest_green: boolean (shares a side or corner with any pixel of the largest green object)

    transformation:
      - step: 1
        action: Identify all distinct objects (contiguous non-white areas).
      - step: 2
        action: Find the green object with the maximum number of pixels. Designate this as the 'central_object'.
      - step: 3
        action: Create an output grid initialized as a copy of the input grid.
      - step: 4
        action: Iterate through all identified objects.
        condition: For each object that is NOT the 'central_object'.
        sub_step: a
          action: Check if any pixel of the current object is adjacent (8-connectivity: horizontal, vertical, or diagonal) to any pixel of the 'central_object'.
        sub_step: b
          action: If the object is NOT adjacent to the 'central_object'.
          effect: Change all pixels belonging to this object in the output grid to white (0).
      - step: 5
        action: Return the modified output grid.

    relationships:
      - type: adjacency
        definition: Two pixels are adjacent if they share a side or a corner (8-connectivity).
      - type: selection_criterion
        description: Objects are kept if they are the largest green object OR if they are adjacent to the largest green object. Objects not meeting this criterion are removed.
    ```


*   **Natural Language Program:**
    1.  Identify all connected components (objects) formed by contiguous pixels of the same non-white color in the input grid.
    2.  Among the objects identified in step 1, find all objects whose color is green (3).
    3.  Determine the green object that has the largest number of pixels. This is the 'central green object'.
    4.  Initialize the output grid as a copy of the input grid.
    5.  For every object identified in step 1:
        a.  If the object is the 'central green object', proceed to the next object.
        b.  If the object is not the 'central green object', check if any pixel within this object is adjacent (horizontally, vertically, or diagonally) to any pixel within the 'central green object'.
        c.  If no pixel of the current object is adjacent to the 'central green object', then update the output grid by changing all pixels corresponding to this object's location to white (0).
    6.  The final state of the output grid represents the result.