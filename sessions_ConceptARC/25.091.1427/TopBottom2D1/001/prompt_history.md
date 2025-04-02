
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 4 0
4 4 4
```


## train_2

**input:**
```
0 0 3 3 0 0 0 0
0 0 3 3 0 0 0 0
0 0 0 0 0 0 0 0
0 4 0 4 0 0 0 0
0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
3 3
3 3
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0
0 0 4 0 4 0 0 0
0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0
0 0 3 0 0 3 0 0
0 0 0 3 3 0 0 0
```


**output:**
```
0 4 0
4 0 4
0 4 0
```

*   **Perception:** The input grids each contain two distinct objects composed of non-white pixels against a white background. The objects have different colors (yellow and green in the examples) and varying shapes. The output grid contains only one of these objects, cropped to its minimal bounding box. The core task is to identify the rule used to select which of the two objects is kept for the output. Comparing the examples, the selection criterion appears to be based on the vertical position of the objects: the object that appears higher up (i.e., has the minimum row index for any of its pixels) is the one selected.

*   **YAML Facts:**
    
```yaml
    task_structure:
      - description: Input grid contains a white background (0) and exactly two distinct non-white objects.
      - examples: 4 pairs provided.
      - goal: Select one of the two objects based on a rule and output it cropped to its bounding box.

    object_properties:
      - object: A contiguous area of pixels with the same non-white color.
      - attributes:
          - color: The pixel value (e.g., 3 for green, 4 for yellow).
          - pixels: A list of (row, col) coordinates belonging to the object.
          - bounding_box: The smallest rectangle containing all the object's pixels.
          - top_row_index: The minimum row index among all pixels of the object.

    relationships_and_actions:
      - count: There are always two non-white objects in the input.
      - comparison: The top_row_index of the two objects is compared.
      - selection: The object with the smaller top_row_index (the higher object) is selected.
      - transformation: The selected object is extracted.
      - output_generation: The output grid consists of the selected object, cropped to its bounding box. Any pixels outside the object within its bounding box remain white (0).

    assumptions:
      - There will always be exactly two non-white objects.
      - The two objects will not have the same minimum row index (no tie-breaking rule observed or needed based on examples).
    ```


*   **Natural Language Program:**
    1.  Identify all distinct contiguous objects of non-white pixels in the input grid.
    2.  Verify that exactly two such objects exist.
    3.  For each of the two objects, determine the row index of its topmost pixel (the minimum row index across all pixels belonging to that object).
    4.  Compare the topmost row indices of the two objects.
    5.  Select the object whose topmost row index is smaller (the object positioned higher in the grid).
    6.  Determine the bounding box of the selected object (the minimum and maximum row and column indices containing the object).
    7.  Create a new output grid whose dimensions match the height and width of the selected object's bounding box.
    8.  Populate the output grid by copying the pixels corresponding to the selected object from the input grid, adjusting their coordinates relative to the top-left corner of the bounding box. Fill any positions within the output grid that do not correspond to the selected object's pixels with the background color (white, 0).
