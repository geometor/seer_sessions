
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 2 2 2
0 2 1 2 0 0 2 1 2
0 2 2 2 0 0 2 2 2
0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 8 8 8
0 4 1 4 0 0 8 1 8
0 4 4 4 0 0 8 8 8
0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 8 8 8
0 4 1 4 0 0 8 1 8
0 4 4 4 0 0 8 8 8
0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 3 3 3 3
0 6 6 6 0 0 3 7 7 7 3
0 6 7 6 0 0 3 7 7 7 3
0 6 6 6 0 0 3 7 7 7 3
0 0 0 0 0 0 3 3 3 3 3
5 5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 3 3 3 3 0 0
5 5 7 5 5 3 7 7 3 0 0
5 5 5 5 5 3 7 7 3 0 0
5 5 5 5 5 3 3 3 3 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0
0 6 7 6 0 0 0 0 0 0 0
0 6 6 6 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
5 5 7 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 1 1 1
0 4 0 0 0 4 0 0 0 1 0 1
0 4 4 4 4 4 0 0 0 1 0 1
0 0 0 0 0 4 4 4 0 1 0 1
0 0 0 0 0 4 0 4 0 1 1 1
7 7 7 0 0 4 0 4 0 0 0 0
7 0 7 0 0 4 4 4 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 0 1
0 0 0 0 0 0 0 0 0 1 1 1
7 7 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0 0 0
7 7 7 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the task based on the provided examples.

**Perception of Elements:**

1.  **Grid Structure:** The input and output are grids of digits. The digit '0' consistently represents the background.
2.  **Objects:** The non-zero digits form distinct connected components or "objects" separated by the background '0'. These objects can be composed of one or more different non-zero digits (e.g., train_1 has an object made of 4s and 8s).
3.  **Transformation:** The transformation involves selectively removing entire objects from the input grid. Objects identified for removal are completely replaced with the background color '0'. Some objects remain unchanged.
4.  **Selection Criteria:** The key determinant for whether an object is removed seems to be the presence of a specific "target removal color" within that object. If an object contains *any* instance of this specific color, the entire object is removed. This target removal color varies across the training examples (2 in train_1, 3 in train_2, 4 in train_3).

**YAML Fact Documentation:**


```yaml
task_elements:
  - element: Grid
    properties:
      - type: 2D array of integers
      - background_color: 0
  - element: Object
    properties:
      - definition: A connected component of non-zero cells in the grid (using 4-way or 8-way connectivity, typically 8-way in ARC).
      - composition: Can be composed of one or more distinct non-zero colors (digits).
      - location: Occupies a specific set of coordinates within the grid.
  - element: Target Removal Color
    properties:
      - definition: A specific non-zero color C.
      - role: Determines which objects are removed.
      - identification: Found by observing which color C, when present in an input object, leads to that object's complete removal in the output, while objects lacking color C remain.
relationships:
  - relationship: Object Membership
    involved_elements: [Grid, Object]
    description: Objects are subsets of cells within the Grid.
  - relationship: Color Presence
    involved_elements: [Object, Target Removal Color]
    description: An object either contains the Target Removal Color or it does not.
actions:
  - action: Identify Objects
    input: Input Grid
    output: Set of Objects (each defined by its constituent cells and colors)
    description: Use connectivity analysis (e.g., flood fill or similar) on non-zero cells to find distinct components.
  - action: Determine Target Removal Color
    input: Input Grid, Output Grid
    output: Target Removal Color C
    description: Find a non-zero color C present in some input objects such that all objects containing C are absent (replaced by 0) in the output, while at least one object not containing C persists.
  - action: Filter Objects
    input: Set of Objects, Target Removal Color C
    output: Set of Objects to Keep
    description: Select objects that do *not* contain the Target Removal Color C.
  - action: Generate Output Grid
    input: Input Grid Dimensions, Set of Objects to Keep, Background Color (0)
    output: Output Grid
    description: Create a new grid filled with the background color, then draw the cells of the "Objects to Keep" onto it using their original colors and positions.
```


**Natural Language Program:**

1.  **Analyze** the input and output grids to determine the single "target removal color" (let's call it `C`). `C` is a non-zero color found in the input such that every distinct connected non-zero object containing *any* cell with color `C` is entirely replaced by the background color (0) in the output, while at least one object *not* containing `C` remains in the output.
2.  **Identify** all distinct connected components (objects) of non-zero cells in the input grid. Record the set of cells belonging to each object.
3.  **Filter** these objects: For each identified object, check if any of its constituent cells have the color `C`. Keep only those objects that do *not* contain any cell with color `C`.
4.  **Construct** the output grid: Start with a grid of the same dimensions as the input, filled entirely with the background color (0). For each object that was kept in the filtering step, copy the colors of its constituent cells from the input grid to the corresponding positions in the output grid.
