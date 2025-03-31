
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 2 2 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 2 2 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 3 3 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 3 3 8 1 8 8 8 8 1 1 1 8 8
8 1 1 8 8 8 8 1 8 8 8 8 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 2
3 8
```


## train_2

**input:**
```
4 4 4 4 4 4 4 4 4 4 4 4 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 4 2 2 4 1 4 4 4 1 4
4 1 1 4 2 2 4 1 4 4 4 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 4 4 4 4 1 4 4 4 1 4
4 1 1 1 1 1 1 1 1 1 1 1 4
4 4 4 4 4 4 4 4 4 4 4 4 4
```


**output:**
```
2 4
4 4
```


## train_3

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 3 1 2 1 4 4 1 2 1 1 1 2 2 1
1 2 1 3 1 2 1 4 4 1 2 1 1 1 2 2 1
1 2 1 3 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 1 1 1 2 1 6 6 1 2 1 8 1 2 2 1
1 2 1 1 1 2 1 6 6 1 2 1 8 1 2 2 1
1 2 1 1 1 2 1 6 6 1 2 1 8 1 2 2 1
1 2 1 1 1 2 1 1 1 1 2 1 1 1 2 2 1
1 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```


**output:**
```
3 4 1
1 6 8
```

*   **Perception:** The task involves identifying distinct 'target' objects within a larger defined area in the input grid and representing their relative spatial arrangement in a smaller output grid. The colors of the frame, the main inner area, and the internal structures play roles in defining the context and identifying the target objects. The output grid seems to capture the essence of the target objects' layout, discarding the exact shapes, sizes, and the surrounding context from the input.

*   **Facts:**
    
```yaml
    task_elements:
      - Input Grid: A 2D array of pixels with integer values representing colors.
      - Output Grid: A smaller 2D array representing a distilled spatial relationship.
    
    grid_properties:
      - Frame Color (B1): The color forming the outer border of the input grid.
      - Main Area Color (C1): The dominant color filling the region inside the frame.
      - Internal Structure Color (B2): The color used for patterns/shapes within the C1 area. Observed that B1 == B2 in examples.
    
    objects:
      - Frame: The outermost border of the grid, defined by B1.
      - Main Area: The region enclosed by the frame, primarily filled with C1.
      - Internal Structures: Shapes within the Main Area, colored B1/B2.
      - Target Objects: Contiguous blocks of pixels within the Main Area whose color is neither C1 nor B1/B2. These are the objects of interest.
    
    object_properties:
      - Target Object Color: The color of a target object.
      - Target Object Position: The location (e.g., centroid) of a target object within the input grid.
      - Target Object Relative Position: The spatial location of a target object relative to others or a reference point (like the center of the Main Area).
    
    relationships:
      - Containment: Target Objects are contained within the Main Area.
      - Spatial Arrangement: Target Objects have relative positions (e.g., top-left, bottom-right) with respect to each other or a reference point.
      - Color Exclusion: Target Objects are defined by colors different from the Main Area (C1) and the Frame/Internal Structure (B1/B2).
    
    transformation:
      - Identification: Locate the Frame (B1), Main Area (C1), and Target Objects.
      - Abstraction: Extract the color and relative position of each Target Object.
      - Mapping: Create a new, smaller grid.
      - Placement: Arrange the Target Object colors in the output grid based on their relative spatial positions identified in the input.
      - Filling: Fill the remaining cells of the output grid with the Frame/Internal Structure color (B1/B2).
      - Size Determination: The output grid size depends on the number and arrangement of target objects (specifically, the number of unique relative rows and columns they occupy, with a special case for single objects resulting in a 2x2 grid).
    ```


*   **Natural Language Program:**
    1.  Identify the color of the outer frame (B1) and the color of the large central area (C1) in the input grid. Note that B1 is also used for structures within C1.
    2.  Find all contiguous shapes ("target objects") located within the C1 area whose color is neither C1 nor B1.
    3.  If there are no target objects, the process result is undefined by these examples (likely an empty grid or a grid filled with B1).
    4.  If there is exactly one target object:
        a.  Determine the center coordinates of the C1 area.
        b.  Determine the position of the single target object's centroid relative to the C1 center (top-left, top-right, bottom-left, or bottom-right quadrant).
        c.  Create a 2x2 output grid filled with color B1.
        d.  Place the target object's color into the cell corresponding to its relative quadrant.
    5.  If there are multiple target objects:
        a.  Calculate the centroid coordinates for each target object.
        b.  Create a sorted list of unique row coordinates from the centroids.
        c.  Create a sorted list of unique column coordinates from the centroids.
        d.  Determine the output grid dimensions: height = number of unique rows, width = number of unique columns.
        e.  Create the output grid of the determined size, filling it entirely with color B1.
        f.  For each target object, find the index of its centroid's row coordinate in the sorted unique row list (this is its relative row index).
        g.  For each target object, find the index of its centroid's column coordinate in the sorted unique column list (this is its relative column index).
        h.  Place the target object's color into the output grid at the cell specified by its (relative row index, relative column index).
    6.  Return the constructed output grid.
