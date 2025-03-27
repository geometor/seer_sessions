
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0
0 0 2 2 2 0 0 0
0 0 2 2 0 0 0 0
```


**output:**
```
0 2 0 0 2 0
2 2 2 2 2 2
2 2 0 2 2 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0
0 0 8 0 0 0 0 0
0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
8 8 0 8 8 0
0 8 0 0 8 0
8 8 8 8 8 8
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 0
0 0 0 0 1 0 0 0
0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 1 1 0 1 1
1 0 0 1 0 0
0 1 0 0 1 0
```

*   **Perception:** Each input grid contains a single connected object composed of a non-white color against a white background. The output grid is derived from the input object. Specifically, the output appears to be constructed by taking the minimal rectangular bounding box surrounding the non-white object in the input and then concatenating this bounding box content horizontally with itself. The output grid's height matches the bounding box height, and its width is twice the bounding box width.

*   **Facts:**
    
```yaml
    task_type: object_transformation
    input_features:
      - grid_elements:
          - type: background
            color: white (0)
          - type: object
            count: 1
            contiguity: connected
            color: variable (non-white, e.g., red, azure, blue)
            shape: variable
    output_features:
      - grid_elements:
          - type: background
            color: white (0)
          - type: pattern
            color: same as input object color
            structure: derived from input object's bounding box
    transformation:
      - action: find_object
        target: non-white connected pixels
      - action: compute_bounding_box
        target: identified object
        scope: minimal
      - action: extract_subgrid
        source: input grid
        region: computed bounding box
      - action: concatenate
        source: extracted subgrid
        direction: horizontal
        count: 2 (self-concatenation)
        result: output grid
    relationships:
      - output grid dimensions depend on the input object's bounding box dimensions (height = bbox_height, width = 2 * bbox_width)
      - output grid content is a direct duplication and arrangement of the input object's bounding box content.
    ```


*   **Natural Language Program:**
    1.  Identify the single contiguous object composed of non-white pixels in the input grid.
    2.  Determine the minimal bounding box that tightly encloses this object. Record the top-left and bottom-right coordinates of this box.
    3.  Extract the subgrid from the input grid defined by these bounding box coordinates.
    4.  Construct the output grid by placing two copies of the extracted subgrid side-by-side horizontally. The resulting output grid will have the same height as the extracted subgrid and twice its width.
