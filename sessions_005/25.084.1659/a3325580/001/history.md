
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 6 0 0 0
0 0 8 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
8
8
8
```


## train_2

**input:**
```
0 0 0 0 0 0 0 4 4 4
0 0 0 0 0 0 0 4 0 4
0 0 0 0 0 0 0 0 0 4
0 9 0 0 0 6 0 0 4 4
0 9 9 0 0 6 0 0 0 4
9 9 0 0 6 6 6 0 0 0
0 9 0 0 0 0 6 0 0 0
0 9 9 0 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
9 4
9 4
9 4
9 4
9 4
9 4
9 4
9 4
9 4
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 1
7 7 7 0 0 2 2 0 0 1
0 0 7 0 0 0 2 2 0 1
0 0 0 0 0 0 2 0 0 1
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2
2
2
2
2
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 3 0 0 0
0 2 0 0 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 3
2 3
2 3
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8
0 0 4 0 0 0 0 0 0 8
0 0 4 0 0 6 6 0 0 8
0 0 4 4 0 0 6 0 0 0
0 0 4 0 0 6 6 0 0 0
0 0 0 0 0 0 0 0 0 0
0 3 3 0 0 0 0 0 0 0
3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 6 8
4 6 8
4 6 8
4 6 8
4 6 8
```


## train_6

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 8 8 8
0 1 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 4 8
1 4 8
1 4 8
```

Okay, let's analyze the task examples.

## Perception

1.  **Input/Output Structure:** The inputs are 10x10 grids containing a white background (0) and several objects composed of non-white pixels (1-9). The outputs are smaller rectangular grids, often taller than they are wide.
2.  **Objects:** The non-white pixels in the input form distinct contiguous objects. An object is defined as a group of connected pixels of the same color (sharing sides, not just corners).
3.  **Color Relevance:** The colors present in the output grid are always a subset of the non-white colors present in the input grid.
4.  **Object Size:** The size (number of pixels) of each object appears crucial.
5.  **Transformation Pattern:**
    *   The process seems to involve identifying all distinct objects in the input grid.
    *   Calculating the size of each object.
    *   Finding the maximum size among all identified objects.
    *   Identifying the colors of all objects that achieve this maximum size.
    *   The output grid's dimensions are determined by this analysis: the height equals the maximum object size, and the width equals the number of distinct colors that have objects of the maximum size.
    *   The colors identified are sorted numerically (by their integer value, ascending).
    *   The output grid is constructed column by column, with each column filled entirely by one of the sorted colors.

## Facts (YAML)


```yaml
task_elements:
  - type: grid
    role: input
    description: A 2D grid of pixels with values 0-9 representing colors. Contains a background (color 0) and multiple distinct objects.
    properties:
      height: 10
      width: 10
  - type: grid
    role: output
    description: A smaller 2D grid of pixels representing a selection and arrangement of colors from the input.
    properties:
      height: Variable, equals the maximum size of the selected objects from the input.
      width: Variable, equals the count of selected colors from the input.
      content: Columns filled with specific colors.

objects:
  - type: connected_component
    source: input
    definition: A contiguous block of pixels of the same non-zero color. Connectivity is defined by adjacent pixels (sharing an edge).
    properties:
      - color: The integer value (1-9) of the pixels in the object.
      - size: The count of pixels belonging to the object.
      - pixels: List of coordinates (row, col) for each pixel in the object.

relationships:
  - type: size_comparison
    description: Objects are compared based on their size (pixel count).
  - type: selection
    criteria: Objects whose size is equal to the maximum size found among all objects in the input grid.
  - type: color_extraction
    source: selected objects
    target: output grid columns
    rule: The colors of the selected objects determine the colors used in the output grid columns.
  - type: sorting
    elements: colors of selected objects
    order: Numerical ascending (based on color index 1-9).
  - type: construction
    target: output grid
    based_on:
      - maximum object size (determines height)
      - count of selected colors (determines width)
      - sorted selected colors (determines column fill colors)

transformation:
  - step: Identify all connected components (objects) of non-zero colors in the input grid.
  - step: Calculate the size (pixel count) for each identified object.
  - step: Determine the maximum size (`max_size`) among all objects.
  - step: Identify all distinct colors (`selected_colors`) corresponding to objects that have a size equal to `max_size`.
  - step: Sort the `selected_colors` numerically in ascending order.
  - step: Determine the output grid dimensions: height = `max_size`, width = number of `selected_colors`.
  - step: Construct the output grid where each column `j` (0-indexed) is filled entirely with the color `selected_colors[j]`.
```


## Natural Language Program

1.  Scan the input grid to identify all distinct objects. An object is a group of connected pixels (sharing edges) that all have the same non-white color. Keep track of each object's color and its size (the number of pixels it contains).
2.  After identifying all objects, find the maximum size observed among them. Let this be `max_size`.
3.  Create a list of all the *colors* that have at least one object with size equal to `max_size`.
4.  Sort this list of colors numerically in ascending order. Let the sorted list be `output_colors`.
5.  Determine the dimensions of the output grid: the height will be `max_size`, and the width will be the number of colors in the `output_colors` list.
6.  Create the output grid. For each column index `j` (starting from 0), fill the entire column with the color `output_colors[j]`.
