
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 4 4 0 0 0 0 0 0
0 0 4 4 0 0 8 8 8 0
0 0 0 0 0 0 8 0 8 8
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4
4 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 2 2 2 0 0 7 7 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 6 6 6 6 0 0 0
0 0 0 0 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 6 6
0 6 6 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
0 0 3 0 0 5 0 0 5 0
0 0 3 0 0 5 5 5 5 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
8 8 8 8 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 0 0 5
5 5 5 5
```

Okay, let's break down this task.

## Perception of Elements

1.  **Input Grids:** The inputs are 10x10 grids containing a white background (color 0) and several distinct "objects".
2.  **Objects:** Objects are contiguous blocks of pixels sharing the same non-white color (e.g., yellow, azure, red in train_1; red, orange, magenta in train_2; green, gray, azure in train_3). Objects have different shapes, sizes (areas), and colors.
3.  **Output Grids:** The outputs are smaller grids. Each output grid contains exactly one of the objects from the corresponding input grid, cropped to its bounding box.
4.  **Transformation Goal:** The core task is to identify a specific rule or criterion to select exactly one object from the multiple objects present in the input grid. Once selected, the output is formed by extracting the rectangular region (bounding box) containing that object from the input grid.
5.  **Selection Criterion:** Analyzing the examples suggests a selection process based on object properties:
    *   The "density" of the object within its bounding box seems crucial. Density is defined as the ratio of the object's pixel count (area) to the total pixel count of its bounding box (width * height).
    *   The object with the highest density is selected.
    *   If multiple objects share the highest density, the tie is broken by selecting the object with the largest area (pixel count) among them.

## Facts


```yaml
task_type: object_selection_and_cropping
input_description: A grid containing a white background and multiple distinct objects (contiguous blocks of the same non-white color).
output_description: A smaller grid representing the content of the bounding box of a single selected object from the input grid.
elements:
  - type: grid
    properties:
      - background_color: white (0)
  - type: object
    properties:
      - color: non-white (1-9)
      - shape: variable, contiguous block of pixels
      - area: number of pixels in the object
      - bounding_box: minimum rectangular region enclosing the object
      - bounding_box_area: width * height of the bounding box
      - density: area / bounding_box_area
relationships:
  - Multiple objects exist within each input grid.
  - The output grid corresponds to exactly one input object.
selection_rule:
  - primary_criterion: Select the object(s) with the maximum density.
  - tie_breaker: If multiple objects have the maximum density, select the one with the largest area among them.
output_generation:
  - action: Extract the subgrid from the input corresponding to the bounding box of the selected object.
```


## Natural Language Program

1.  **Identify Objects:** Scan the input grid to find all distinct contiguous groups of non-white pixels. Each group represents an object.
2.  **Calculate Properties for Each Object:** For every object identified:
    a.  Record its color.
    b.  Count the number of pixels belonging to it (this is its `area`).
    c.  Determine its `bounding_box` (the minimum row, maximum row, minimum column, and maximum column containing the object's pixels).
    d.  Calculate the `bounding_box_area` ( (max\_row - min\_row + 1) * (max\_col - min\_col + 1) ).
    e.  Calculate its `density` by dividing the `area` by the `bounding_box_area`.
3.  **Find Maximum Density:** Determine the highest `density` value found among all objects.
4.  **Filter by Maximum Density:** Create a list of candidate objects that have this maximum `density`.
5.  **Apply Tie-Breaker (if necessary):**
    a.  If the list of candidates contains only one object, this is the selected object.
    b.  If the list contains multiple objects, find the object within this list that has the largest `area`. This is the selected object.
6.  **Extract Output:** Identify the `bounding_box` coordinates of the finally selected object. Extract the rectangular subgrid defined by these coordinates from the original input grid. This subgrid is the final output.
