*   **Perception of Task Elements:**
    *   The input and output are grids of numbers (colors), where 0 represents the background.
    *   The input grid contains multiple distinct connected regions (objects) of non-zero numbers.
    *   Objects are defined by connected cells (sharing an edge, i.e., orthogonal connectivity) having non-zero values. An object can sometimes contain cells of different non-zero colors (e.g., train\_3, bottom object).
    *   The transformation involves removing some of these objects, replacing their cells with the background color 0.
    *   The decision to remove an object seems related to its position, specifically its proximity to the top border of the grid. Objects touching the top border are removed. Furthermore, objects directly adjacent (orthogonally) to those touching the top border are also removed. This removal seems contagious; if object A touches the top, it's removed. If object B touches A, B is removed. If object C touches B, C is removed, and so on. Objects that do not touch the top border and are not connected via a chain of adjacency to a top-border-touching object are kept.

*   **YAML Facts:**
    
```yaml
    Grid:
      Type: 2D array of integers
      Background_Color: 0
      Objects:
        Definition: Connected components of non-zero cells (orthogonal connectivity)
        Properties:
          - Cells: List of (row, col) coordinates
          - Colors: Set of non-zero integers present in the object's cells
          - Touches_Top_Border: Boolean (True if any cell has row index 0)
          - Adjacent_Objects: List of other objects sharing an orthogonal edge with this object
    Transformation:
      Action: Conditional Removal of Objects
      Rule:
        1. Identify all objects.
        2. Determine which objects touch the top border.
        3. Iteratively identify objects orthogonally adjacent to objects identified in step 2 or subsequently identified objects.
        4. All objects identified in steps 2 and 3 are marked for removal.
        5. Objects not marked for removal are kept.
      Output: A new grid where cells belonging to removed objects are set to 0, and cells belonging to kept objects retain their original color.
    ```


*   **Natural Language Program:**
    1.  Identify all distinct connected components (objects) of non-zero cells in the input grid using orthogonal adjacency (cells sharing an edge are connected). Treat adjacent non-zero cells as part of the same object, regardless of their specific color.
    2.  Initialize a set of "objects to remove".
    3.  Add all objects that contain at least one cell in the top row (row 0) to the "objects to remove" set.
    4.  Initialize a set of "newly added objects" with the objects identified in step 3.
    5.  While the "newly added objects" set is not empty:
        a.  Create an empty temporary set called "adjacent objects found in this iteration".
        b.  For each object `O1` in the "newly added objects" set:
            i.  Find all other objects `O2` in the grid that are orthogonally adjacent to `O1`.
            ii. For each such adjacent object `O2`, if `O2` is not already in the "objects to remove" set, add `O2` to both the "objects to remove" set and the "adjacent objects found in this iteration" set.
        c.  Update the "newly added objects" set to be the "adjacent objects found in this iteration" set for the next loop.
    6.  Create the output grid, initially identical to the input grid.
    7.  For each object in the final "objects to remove" set, set the color of all cells belonging to that object in the output grid to 0.
    8.  Return the modified output grid.