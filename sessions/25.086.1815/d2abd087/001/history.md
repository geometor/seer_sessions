
## train_1

**input:**
```
0 0 0 0 0 0 0 0 5 0
0 5 5 0 0 0 5 5 5 0
5 5 5 5 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 5 0 0 5 0
0 0 0 0 0 0 0 0 5 0
0 0 0 0 0 5 5 0 0 0
0 5 5 0 0 5 5 0 0 0
0 5 5 0 0 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 1 0
0 2 2 0 0 0 1 1 1 0
2 2 2 2 0 0 0 0 1 0
0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 0 0 1 0
0 0 0 0 0 0 0 0 1 0
0 0 0 0 0 2 2 0 0 0
0 1 1 0 0 2 2 0 0 0
0 1 1 0 0 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0
0 0 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 0 0
0 0 0 0 0 5 5 5 0 0
0 5 5 0 0 0 5 0 0 0
0 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 2 2 2 0 0
0 1 1 0 0 0 2 0 0 0
0 1 1 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
5 5 5 0 0 0 0 5 5 5
0 5 5 0 5 5 0 5 0 0
0 0 5 0 5 5 0 5 0 0
0 0 5 0 0 0 0 5 0 0
0 0 0 0 5 5 0 0 0 5
0 5 5 0 0 5 5 0 0 5
0 0 0 0 0 5 5 0 0 5
0 0 5 0 0 0 0 0 0 0
0 5 5 5 5 0 0 0 0 0
0 0 5 5 0 0 0 0 0 0
```


**output:**
```
1 1 1 0 0 0 0 2 2 2
0 1 1 0 1 1 0 2 0 0
0 0 1 0 1 1 0 2 0 0
0 0 1 0 0 0 0 2 0 0
0 0 0 0 2 2 0 0 0 1
0 1 1 0 0 2 2 0 0 1
0 0 0 0 0 2 2 0 0 1
0 0 1 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0
```

**Perception of Task Elements:**

1.  **Input/Output Grids:** Both input and output are 2D grids of the same dimensions.
2.  **Colors:** The input grids contain only white (0) and gray (5) pixels. The output grids contain white (0), blue (1), and red (2) pixels. White pixels remain unchanged. Gray pixels in the input are transformed into either blue or red pixels in the output.
3.  **Objects:** The gray pixels in the input form distinct contiguous objects (connected horizontally or vertically). Each gray object in the input corresponds to a uniformly colored object (either all blue or all red) in the output, occupying the exact same positions.
4.  **Transformation Logic:** The core task is to determine the rule that decides whether a gray object becomes blue or red. Analyzing the examples reveals a pattern related to the size (number of pixels) of each gray object.

**Analysis of Examples:**

*   **Train 1:** Objects of size 5, 4, 2, 4 become blue (1). Objects of size 6, 6 become red (2).
*   **Train 2:** Objects of size 6, 6 become red (2). Object of size 5 becomes blue (1).
*   **Train 3:** Objects of size 7, 4, 3, 2, 7 become blue (1). Objects of size 6, 6 become red (2).

**Conclusion:** Across all examples, gray objects with exactly 6 pixels are consistently transformed into red (2) objects. All other gray objects (sizes 2, 3, 4, 5, 7 in the examples) are transformed into blue (1) objects.

**YAML Fact Document:**


```yaml
task_context:
  description: Transform gray objects in a grid based on their size.
  grid_properties:
    - dimensions_preserved: True # Output grid has the same dimensions as the input grid.
    - background_color: white (0) # Background color is white and remains unchanged.
input_elements:
  - element: object
    attributes:
      - color: gray (5)
      - structure: contiguous pixels (4-connectivity)
      - property: size (pixel count)
output_elements:
  - element: object
    attributes:
      - color: blue (1) or red (2)
      - structure: contiguous pixels (derived from input gray objects)
      - position: same as corresponding input gray object
transformation:
  actions:
    - identify_objects: Find all contiguous groups of gray (5) pixels in the input grid.
    - analyze_objects:
        - for each gray object:
            - calculate: size (number of pixels)
    - recolor_objects:
        - based_on: size
        - rule:
            - condition: if size == 6
              action: change object color to red (2)
            - condition: if size != 6
              action: change object color to blue (1)
  unchanged_elements:
    - white (0) pixels remain white (0).

```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Find all distinct connected objects composed of gray (5) pixels in the input grid. Use 4-way connectivity (up, down, left, right).
3.  For each identified gray object:
    a.  Count the total number of pixels belonging to that object (this is its size).
    b.  Check if the object's size is exactly equal to 6.
    c.  If the size is 6, change the color of all pixels belonging to this object in the output grid to red (2).
    d.  If the size is not 6, change the color of all pixels belonging to this object in the output grid to blue (1).
4.  Return the modified output grid. White (0) pixels are implicitly unchanged as they are not part of any gray object.
