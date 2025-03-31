
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 2 0 0 0 0 6 6 6 0
0 0 2 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 2 0 0
6 6 6 0 0 0 0 0 2 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
7 7
7 7
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 0 0 0 0
0 0 5 0 0 0 0 4 0 0 0
0 0 5 0 0 0 0 4 0 2 0
0 0 5 0 0 0 0 4 0 2 0
0 0 5 0 0 0 0 0 0 2 0
0 0 0 0 5 0 0 0 0 2 0
0 0 0 0 5 0 0 0 0 0 0
4 0 0 0 5 0 0 0 0 0 0
4 0 0 0 5 0 0 0 0 0 0
4 0 0 0 5 0 0 0 0 0 0
```


**output:**
```
2
2
2
2
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 0 2 3 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 2 1 2 0
0 0 0 0 0 0 0 0 0 1 1 1 0
0 2 2 2 0 0 0 0 0 0 0 0 0
0 2 3 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 1 2
1 1 1
```

*   **Perception:** The task requires identifying and isolating a specific object from the input grid. The input grids contain multiple distinct objects composed of different colors and shapes scattered on a white background. The output grid is the minimal bounding box containing the selected object. The key challenge lies in determining the criteria for selecting the correct object among several candidates. The examples suggest a two-step process: first, identifying objects whose specific pattern (color and shape) is unique within the input grid, and second, selecting from these unique objects based on a property, which appears to be symmetry. The object with the highest degree of symmetry (preferring both horizontal and vertical, then either one) among the uniquely patterned objects is chosen.

*   **Facts:**
    
```yaml
    task_type: object_extraction
    input_domain: 2D grid with colored pixels (0-9)
    output_domain: 2D grid, typically smaller than input
    background_color: white (0)
    objects:
      - definition: Contiguous blocks of non-white pixels.
      - properties: color, shape, size, position, pattern (internal color arrangement), symmetry.
      - relationships: Objects are distinct and scattered; some objects might share the same color or shape pattern.
    transformation:
      - step: Identify all distinct objects in the input grid.
      - step: For each object, determine its pattern signature (colors and relative positions within its bounding box).
      - step: Count the occurrences of each unique pattern signature.
      - step: Filter to find objects whose pattern signature occurs exactly once (unique patterns).
      - step: From the set of unique-pattern objects, identify the one with the highest symmetry (preference: H+V symmetry > H or V symmetry > no symmetry).
      - step: If ties in symmetry, further criteria might be needed (not observed in examples, could be size, color, simplicity).
      - step: Extract the selected object, cropping it to its minimal bounding box.
      - step: The extracted bounding box forms the output grid.
    selection_criteria:
      - primary: Uniqueness of the object's pattern signature (color and relative shape) within the input grid.
      - secondary: Highest degree of symmetry among the objects with unique patterns.
    ```


*   **Natural Language Program:**
    1.  Scan the input grid to identify all distinct objects (connected components of non-white pixels).
    2.  For each identified object, create a representation of its pattern (the configuration of colors within its minimal bounding box).
    3.  Compare the patterns of all objects and count how many times each unique pattern appears in the grid.
    4.  Create a candidate list containing only the objects whose pattern appears exactly once in the grid.
    5.  Evaluate the symmetry of each object in the candidate list (check for horizontal symmetry, vertical symmetry, or both).
    6.  Select the object from the candidate list that exhibits the highest degree of symmetry. Prioritize objects with both horizontal and vertical symmetry, then objects with either horizontal or vertical symmetry. If there's still a tie, assume the examples provided cover the necessary logic (or potentially use other factors like size or color if needed, though symmetry seems sufficient for these examples).
    7.  Extract the minimal bounding box containing the selected object.
    8.  Return this extracted bounding box as the output grid.
