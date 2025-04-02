
## train_1

**input:**
```
0 0 0 0 0 0 0 0 3 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0
0 0 0 0 3 0 3 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0
```


**output:**
```
3 3 3
0 0 3
0 0 3
0 0 3
0 0 3
```


## train_2

**input:**
```
0 4 4 0 0 0 0 0 0 0
4 4 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 4
0 0 0 4 0 0 0 0 0 0
4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
```


**output:**
```
0 4 4
4 4 0
4 0 0
4 0 0
```


## train_3

**input:**
```
0 0 0 6 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 6 0 0 6 6 6 6 0 0
0 6 0 0 6 0 0 0 0 0
0 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
6 0 0 6 0 0 0 0 0 0
```


**output:**
```
6 6 6 6 0 0 0
6 0 0 6 6 6 6
6 0 0 6 0 0 0
6 6 6 6 0 0 0
```

Okay, let's break down this task.

**Perception of Task Elements:**

1.  **Input/Output:** Both are grids of pixels represented by numbers 0-9 (colors). The output grid is always smaller than the input grid.
2.  **Colors:** Each example uses only two colors: white (0) and one other color (green, yellow, or magenta). The non-white color is preserved in the output.
3.  **Objects:** The non-white pixels form distinct shapes or objects within the input grid. These objects can be single pixels or larger contiguous blocks.
4.  **Transformation:** The core transformation appears to be a selection or cropping process. The output grid seems to focus on a specific region of the input grid containing a prominent non-white object.
5.  **Key Feature:** By comparing the input and output, the output grid seems to be the smallest rectangular area (bounding box) that fully encloses the *largest* contiguous object of the non-white color present in the input.

**YAML Facts:**


```yaml
task_description: Crop the input grid to the bounding box of the largest contiguous non-background object.
components:
  - role: grid
    input_grid: Input 2D array of pixels (0-9).
    output_grid: Output 2D array of pixels (0-9), a subgrid of the input.
  - role: background
    color: white (0)
  - role: objects
    description: Contiguous blocks of non-white pixels.
    properties:
      - color: The specific non-white color (e.g., green, yellow, magenta).
      - size: The number of pixels in the object.
      - position: Coordinates of the pixels comprising the object.
      - bounding_box: The minimum rectangle enclosing the object (defined by min/max row/column).
actions:
  - name: identify_objects
    description: Find all distinct contiguous groups of non-white pixels in the input grid.
    inputs: input_grid
    outputs: list_of_objects
  - name: calculate_object_sizes
    description: Determine the number of pixels for each identified object.
    inputs: list_of_objects
    outputs: list_of_object_sizes
  - name: find_largest_object
    description: Identify the object with the maximum size. Assumes a single largest object based on examples.
    inputs: list_of_objects, list_of_object_sizes
    outputs: largest_object
  - name: calculate_bounding_box
    description: Determine the minimum and maximum row and column indices that contain all pixels of the largest object.
    inputs: largest_object
    outputs: bounding_box_coordinates (min_row, max_row, min_col, max_col)
  - name: crop_grid
    description: Extract the subgrid from the input grid defined by the bounding box coordinates.
    inputs: input_grid, bounding_box_coordinates
    outputs: output_grid
relationships:
  - The output grid's content and dimensions are determined by the bounding box of the single largest non-white object found in the input grid.
```


**Natural Language Program:**

1.  Scan the input grid to identify all separate, contiguous objects formed by non-white pixels (any color other than white/0).
2.  For each identified object, count the number of pixels it contains (its size).
3.  Determine which object has the largest size.
4.  Find the minimum bounding box for this largest object. This means finding the minimum row index, maximum row index, minimum column index, and maximum column index occupied by any pixel belonging to this largest object.
5.  Create the output grid by extracting the rectangular portion of the input grid defined by these minimum and maximum row and column indices (inclusive).
