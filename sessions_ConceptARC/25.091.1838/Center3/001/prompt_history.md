
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0
0 1 0 3 3 3 3 0 0 2 2 2 0 0 0 0 1 0
0 1 0 3 0 0 3 0 0 2 0 2 0 0 0 0 1 0
0 1 0 3 0 0 3 0 0 2 2 2 0 0 0 0 1 0
0 1 0 3 3 3 3 0 0 0 0 0 0 0 0 0 1 0
0 1 0 0 0 0 0 4 4 4 4 0 0 0 0 0 1 0
0 1 0 0 0 0 0 4 0 0 4 0 0 0 0 0 1 0
0 1 0 0 0 0 0 4 0 0 4 0 0 0 0 0 1 0
0 1 0 0 0 0 0 4 4 4 4 7 7 7 7 7 1 0
0 1 0 0 0 0 0 0 0 0 0 7 0 0 0 7 1 0
0 1 0 0 0 0 0 8 8 8 8 7 0 0 0 7 1 0
0 1 0 0 0 0 0 8 0 0 8 7 0 0 0 7 1 0
0 1 0 0 0 0 0 8 0 0 8 7 7 7 7 7 1 0
0 1 0 0 0 0 0 8 8 8 8 0 0 0 0 0 1 0
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4 4 4
4 0 0 4
4 0 0 4
4 4 4 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2 0 0
2 0 0 0 0 0 0 0 0 2 0 0
2 3 3 0 0 0 7 7 0 2 0 0
2 3 3 0 0 0 7 7 0 2 0 0
2 0 0 0 6 6 0 0 0 2 0 0
2 0 0 0 6 6 0 0 0 2 0 0
2 0 9 9 0 0 0 0 0 2 0 0
2 0 9 9 0 1 1 0 0 2 0 0
2 0 0 0 0 1 1 0 0 2 0 0
2 2 2 2 2 2 2 2 2 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6
6 6
```


## train_3

**input:**
```
0 0 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 4 0 0 0 0 0 3 3 3 3 3 3 0 4
0 0 4 0 0 0 0 0 3 0 0 0 0 3 0 4
0 0 4 0 0 0 0 0 3 0 0 0 0 3 0 4
0 0 4 0 0 0 0 0 3 0 0 0 0 3 0 4
0 0 4 0 0 0 4 4 4 4 4 4 0 3 0 4
0 0 4 0 0 0 4 0 3 3 3 4 3 3 0 4
0 0 4 0 0 0 4 0 0 0 0 4 0 0 0 4
0 0 4 0 0 0 4 4 4 4 4 4 0 0 0 4
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 4 4 4 4 4 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4 4 4 4 4
4 0 0 0 0 4
4 0 0 0 0 4
4 4 4 4 4 4
```

Okay, let's break down this task.

**Perception of Elements:**

1.  **Input Structure:** The input grids consist of a background (white, 0), an outer frame of a single color, and multiple distinct colored objects enclosed within the frame.
2.  **Object Types:** The objects within the frame appear to be geometric shapes, primarily rectangles. These rectangles can be solid (filled with a single color) or hollow (an outline of a single color with a background-colored interior). Some shapes might be more complex or irregular (like the green shape in example 3).
3.  **Output Structure:** The output is always a smaller grid representing one of the rectangular objects from the input grid, cropped to its bounding box.
4.  **Transformation Goal:** The core task is to identify *which* specific rectangular object from the input should be extracted to form the output.

**YAML Fact Document:**


```yaml
task_description: Extract a specific rectangular object from within a framed area in the input grid.

elements:
  - element: grid
    description: A 2D array of pixels with color values 0-9.
  - element: background
    property: color
    value: white (0)
    description: The typically most frequent color, surrounding other elements.
  - element: frame
    property: shape
    value: rectangle (usually 1 pixel thick)
    property: location
    value: outermost non-background border
    property: color
    value: variable (blue, red, yellow in examples)
    description: Encloses other objects. Not present in the output.
  - element: object
    property: location
    value: enclosed within the frame
    property: color
    value: variable (non-background)
    property: shape
    value: variable (contiguous pixels of the same color)
    description: Distinct items inside the frame.
  - element: perfect_rectangle_object
    description: An object forming a solid or hollow rectangle.
    property: type
    value: solid or hollow
    property: color
    value: single color
    property: area
    value: calculated from bounding box (width * height)
    relationship: subset of 'object'

transformation:
  input: grid
  output: subgrid (cropped perfect_rectangle_object)
  steps:
    - identify: background color (usually white=0).
    - identify: frame (outermost non-background border).
    - find: all contiguous non-background, non-frame objects inside the frame.
    - filter: keep only objects that are 'perfect rectangles' (solid or hollow with background-colored interior).
    - selection_logic:
        condition: if only one perfect rectangle exists
        action: select that rectangle.
        condition: if multiple perfect rectangles exist
        action:
          - calculate: bounding box area for each perfect rectangle.
          - determine: median area among them.
          - filter: keep only rectangles with the median area.
          - determine: median color index among the remaining rectangles.
          - select: the rectangle with the median color index.
    - final_step: extract the selected perfect rectangle object and crop it to its bounding box to create the output grid.

```


**Natural Language Program:**

1.  Identify the background color (typically white, color 0).
2.  Identify all contiguous groups of non-background pixels within the input grid.
3.  From these groups, identify the objects that form "perfect rectangles". A perfect rectangle can be either:
    *   A solid rectangle (a rectangular block of a single color).
    *   A hollow rectangle (a rectangular outline of a single color, at least one pixel thick, surrounding a rectangular area filled with the background color).
4.  Ignore any object that constitutes the outermost frame of the grid (if one exists). Focus only on objects fully contained within any such frame.
5.  Count the number of perfect rectangle objects identified in step 4.
6.  **If** exactly one perfect rectangle object was found, this object is the target.
7.  **Else (if multiple perfect rectangle objects were found):**
    a.  Calculate the bounding box area (width * height) for each perfect rectangle object.
    b.  Find the median value among these calculated areas.
    c.  Filter the list of perfect rectangles, keeping only those whose area matches the median area.
    d.  From this filtered list (of median-area rectangles), get the color index of each rectangle.
    e.  Find the median value among these color indices.
    f.  The target object is the perfect rectangle whose color index matches this median color index. (If there's an even number of items when finding the median color index, clarification might be needed - standard median definition usually averages the middle two, but ARC colors are discrete. Assume it takes the lower of the two middle indices if necessary, although examples suggest an odd number).
8.  Create the output grid by taking the selected target object and cropping the input grid to the exact bounding box of this object.
