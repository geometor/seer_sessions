
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

Okay, let's analyze the task examples.

**Perception of Task Elements:**

1.  **Input Structure:** The input grids contain multiple distinct shapes or objects. Each object is primarily composed of a single non-black color (let's call this the "Outer Color").
2.  **Object Characteristics:** The objects vary in shape (squares, rectangles, L-shapes, T-shapes) and Outer Color.
3.  **Shared Feature:** Within each input grid, all the identified objects seem to share a common characteristic: they all contain or surround pixels of a single, specific color (let's call this the "Inner Color"). This Inner Color is different from the Outer Color of the objects themselves.
    *   Example 1: Objects (Red, Yellow, Azure) all contain Blue (1). Inner Color = Blue (1).
    *   Example 2: Objects (Magenta, Green, Gray) all contain Orange (7). Inner Color = Orange (7).
    *   Example 3: Objects (Yellow, Blue, Orange) all contain Black (0). Inner Color = Black (0).
4.  **Transformation:** The transformation involves selectively removing *entire* objects based on their Outer Color. The output grid retains only a subset of the objects from the input grid, replacing the removed objects' pixels with the background color (Black, 0).
5.  **Removal Rule:** The decision of which object color(s) to remove appears to depend on a comparison or relationship between the Outer Colors present and the shared Inner Color.
    *   In Ex 1 (Inner=1), Outer={2, 4, 8}. Color 2 (smallest) is removed.
    *   In Ex 2 (Inner=7), Outer={3, 5, 6}. Color 3 (smallest) is removed.
    *   In Ex 3 (Inner=0), Outer={1, 4, 7}. Color 4 (second smallest) is removed.
    *   This suggests a rule based on the sorted order of Outer Colors, conditional on the Inner Color value.

**YAML Fact Document:**


```yaml
task_elements:
  - element: Grid
    description: A 2D array of pixels with colors 0-9. Black (0) is the background.
  - element: Object
    description: A contiguous region of pixels sharing the same non-black color (Outer Color).
    properties:
      - OuterColor: The primary color of the object's pixels.
      - Pixels: The coordinates of the pixels comprising the object.
      - BoundingBox: The minimum rectangle enclosing the object.
  - element: InnerColor
    description: A single color found within the spatial extent (e.g., bounding box or internal adjacency) of all Objects in a given input grid. This color differs from the OuterColor of the objects it is associated with. It can be Black (0).
    relationship: Contained within or adjacent internally to all Objects.
  - element: SetOfOuterColors
    description: The unique collection of Outer Colors of all objects present in the input grid.
    properties:
      - UniqueColors: List of distinct Outer Colors.
      - SortedColors: UniqueColors sorted numerically.
      - MinColor: The smallest color in UniqueColors.
      - SecondMinColor: The second smallest color in UniqueColors (if it exists).

actions:
  - action: IdentifyObjects
    description: Find all connected components of non-black pixels in the input grid.
    inputs: Input Grid
    outputs: List of Objects (with their OuterColor and Pixels).
  - action: IdentifyInnerColor
    description: Determine the single color shared internally by all identified objects.
    inputs: Input Grid, List of Objects
    outputs: InnerColor value.
  - action: SelectColorToRemove
    description: Choose which Outer Color objects should be removed based on the InnerColor and the sorted list of Outer Colors.
    inputs: InnerColor, Sorted List of Outer Colors
    outputs: ColorToRemove.
    logic: |
      If InnerColor is Black (0), ColorToRemove is the second element in Sorted List of Outer Colors.
      If InnerColor is not Black (0), ColorToRemove is the first element (minimum) in Sorted List of Outer Colors.
  - action: FilterObjects
    description: Remove objects based on the selected ColorToRemove.
    inputs: Input Grid, List of Objects, ColorToRemove
    outputs: Output Grid.
    logic: Create an output grid of the same size as the input, initially Black (0). Copy pixels of all objects whose OuterColor is NOT ColorToRemove from the input to the output.

relationships:
  - relationship: RemovalCondition
    description: The rule determining object removal depends on the InnerColor and the relative order of the OuterColors.
    entities: InnerColor, SetOfOuterColors, ColorToRemove
```


**Natural Language Program:**

1.  **Analyze the Input Grid:**
    *   Identify all distinct contiguous objects composed of a single non-black color. Record the color of each object (its "Outer Color") and the set of pixel coordinates belonging to it.
2.  **Find the Shared Inner Color:**
    *   Examine the input grid to find the single color ("Inner Color") that is located spatially within or immediately adjacent internally to *all* the identified objects. This Inner Color will be different from the Outer Colors of the objects themselves (it can be Black, 0).
3.  **Determine the Target Color for Removal:**
    *   Collect all unique Outer Colors found in step 1.
    *   Sort these unique Outer Colors numerically in ascending order.
    *   Check the value of the Inner Color found in step 2:
        *   If the Inner Color is Black (0), select the *second* color from the sorted list of Outer Colors.
        *   If the Inner Color is *not* Black (0), select the *first* color (i.e., the minimum value) from the sorted list of Outer Colors.
    *   The selected color is the "Color To Remove".
4.  **Construct the Output Grid:**
    *   Create a new grid with the same dimensions as the input grid, filled initially with the background color (Black, 0).
    *   Iterate through all the objects identified in step 1.
    *   If an object's Outer Color is *not* the "Color To Remove", copy all of its pixels from the input grid to the corresponding positions in the new output grid.
    *   The resulting grid is the final output.
