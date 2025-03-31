
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 8 8 4 0 0 0 0 0 0
0 4 8 4 0 0 0 0 0 0
0 8 8 4 0 0 0 0 0 0
0 0 0 0 0 0 3 2 2 0
0 0 0 0 0 0 3 3 2 0
0 0 0 0 0 0 3 2 2 0
0 0 0 0 0 0 0 0 0 0
0 0 3 6 3 0 0 0 0 0
0 0 3 6 3 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 4 4 8 0 0 0 0 0 0
0 8 4 8 0 0 0 0 0 0
0 4 4 8 0 0 0 0 0 0
0 0 0 0 0 0 2 3 3 0
0 0 0 0 0 0 2 2 3 0
0 0 0 0 0 0 2 3 3 0
0 0 0 0 0 0 0 0 0 0
0 0 6 3 6 0 0 0 0 0
0 0 6 3 6 0 0 0 0 0
0 0 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0
0 5 8 5 0 0 0
0 5 8 5 0 0 0
0 8 8 8 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 8 5 8 0 0 0
0 8 5 8 0 0 0
0 5 5 5 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0
0 8 1 8 0 0 0 3 2 3 0 0
0 8 8 8 0 0 0 2 2 2 0 0
0 0 0 0 0 0 0 2 3 2 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 1 1 0 0 0 0 0 0
0 0 0 1 6 6 0 0 0 0 0 0
0 0 0 1 6 6 0 0 4 4 5 0
0 0 0 0 0 0 0 0 4 5 5 0
0 0 0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0
0 1 8 1 0 0 0 2 3 2 0 0
0 1 1 1 0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 3 2 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 6 6 0 0 0 0 0 0
0 0 0 6 1 1 0 0 0 0 0 0
0 0 0 6 1 1 0 0 5 5 4 0
0 0 0 0 0 0 0 0 5 4 4 0
0 0 0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down the transformation process based on the provided examples.

**Perception of Task Elements:**

*   The input and output grids have the same dimensions.
*   The background color is white (0) and remains unchanged in the output.
*   The input grids contain multiple distinct "objects".
*   Each object appears to be composed of pixels of exactly two different non-background colors.
*   These objects are contiguous blocks of pixels of these two specific colors.
*   In the output grid, the positions and shapes of these objects remain the same.
*   The key transformation happens *within* each object: the two colors that make up the object are swapped. For example, if an object is made of color A and color B, all pixels of color A become color B, and all pixels of color B become color A in the output.
*   Objects that are spatially separated are treated independently.

**YAML Fact Documentation:**


```yaml
task_description: Swap the two constituent colors within each distinct multi-colored object, leaving the background unchanged.

grid_properties:
  - background_color: white (0)
  - background_persistence: The background color and its positions remain unchanged between input and output.
  - dimensions_persistence: Input and output grids have the same height and width.

objects:
  - definition: A contiguous group of non-background pixels composed of exactly two distinct colors. Adjacency includes diagonals.
  - count_persistence: The number of objects in the input matches the number of objects in the output.
  - location_persistence: The bounding box or general location of each object remains the same.
  - shape_persistence: The overall shape formed by the combined pixels of an object remains the same.
  - color_composition: Each object consists of exactly two distinct non-white colors (let's call them color C1 and color C2).

actions:
  - name: color_swap
  - description: Within each identified object, replace all occurrences of color C1 with color C2, and all occurrences of color C2 with color C1.
  - scope: Applied independently to each object.

relationships:
  - Objects are distinct entities based on connectivity and color composition.
  - The transformation rule applies uniformly to all objects meeting the criteria.
```


**Natural Language Program:**

1.  Initialize an output grid with the same dimensions as the input grid, filled with the background color (white, 0).
2.  Identify all distinct objects in the input grid. An object is a connected component of pixels (using side and diagonal adjacency) that are not the background color (white, 0).
3.  For each identified object:
    a.  Determine the two unique non-background colors present within that object (let these be Color A and Color B).
    b.  Iterate through all the pixel coordinates belonging to this specific object in the input grid.
    c.  For each pixel coordinate within the object:
        i.  If the input pixel color is Color A, set the corresponding pixel in the output grid to Color B.
        ii. If the input pixel color is Color B, set the corresponding pixel in the output grid to Color A.
4.  Return the completed output grid.
