
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 9 9 9 0 0 0 7 4 4 0 0 0 0
0 0 8 8 9 0 0 0 7 4 7 0 0 0 0
0 0 8 8 9 0 0 0 7 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 3 3 0 0 0 0
0 0 0 0 0 0 0 0 1 2 2 0 0 0 0
0 0 0 0 0 0 0 0 1 3 2 0 0 0 0
0 0 3 6 6 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 6 6 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 3 3
1 2 2
1 3 2
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 5 5 0 0 0 0 0 0 0 0 0
0 0 0 6 8 8 0 0 0 0 0 0 0 0 0
0 0 0 6 5 5 0 0 9 9 9 0 0 0 0
0 0 0 0 0 0 0 0 4 4 9 0 0 0 0
0 0 0 0 0 0 0 0 4 9 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 7 1 0 0 0 0 0
0 0 0 3 2 2 0 7 1 7 0 0 0 0 0
0 0 0 2 2 2 0 7 7 7 0 0 0 0 0
0 0 0 3 2 3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
5 5 5
6 8 8
6 5 5
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 5 5 0 0 0 0 0 0 0 0 0 0
0 0 5 7 5 0 0 0 1 6 2 0 0 0 0
0 0 5 7 7 0 0 0 6 1 1 0 0 0 0
0 0 0 0 0 0 0 0 2 6 1 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 0 0 0 0 0 0 0 0 0 0
0 0 3 3 8 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 0 0 0 9 4 4 0 0 0 0
0 0 0 0 0 0 0 0 4 9 4 0 0 0 0
0 0 0 0 0 0 0 0 4 4 9 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 6 2
6 1 1
2 6 1
```

*   **Perception:**
    *   Each input grid is 15x15 and contains a white background (color 0) with four distinct, non-overlapping, colored objects.
    *   Each object appears to be roughly 3x3 in size, composed of multiple colors.
    *   The output grid is always 3x3 and is an exact copy of one of the objects found in the input grid.
    *   By examining the colors within each object in the input examples, it appears the object selected for the output is the one composed of the largest number of *different* colors. In all training examples, the selected object has three distinct colors, while the other three objects each have only two distinct colors.

*   **Facts:**
    
```yaml
    task_type: object_selection_and_extraction
    
    input_features:
      - description: Input grid dimensions
        value: 15x15 (consistent across examples)
      - description: Background color
        value: 0 (white)
      - description: Objects
        details:
          - count: 4 distinct non-white objects per input grid.
          - composition: Each object is composed of multiple pixels and multiple colors.
          - size: Objects are small, typically 3x3.
          - separation: Objects are non-overlapping and separated by background pixels.
    
    output_features:
      - description: Output grid dimensions
        value: 3x3 (consistent across examples)
      - description: Content
        value: A direct copy of one specific object from the input grid.
    
    transformation_logic:
      - step: Identify all distinct, contiguous, non-background objects in the input grid.
      - step: For each identified object, count the number of unique colors it contains (excluding the background color).
      - step: Select the object that has the maximum count of unique colors. (Assume uniqueness based on examples).
      - step: Extract the selected object, preserving its internal structure and colors.
      - step: The extracted object forms the output grid, cropped to its bounding box.
    
    relationships:
      - The output grid is a subgrid of the input grid.
      - The selection criterion is based on the property of "color diversity" within each object.
    
    example_specific_observations:
      - train_1: Output object (Blue/Green/Red) has 3 unique colors. Other objects have 2 unique colors.
      - train_2: Output object (Gray/Magenta/Azure) has 3 unique colors. Other objects have 2 unique colors.
      - train_3: Output object (Blue/Magenta/Red) has 3 unique colors. Other objects have 2 unique colors.
    ```


*   **Natural Language Program:**
    1.  Identify all separate objects in the input grid that are not the background color (white). An object is a contiguous group of non-white pixels.
    2.  For each identified object, determine the set of unique colors present within that object. Count the number of unique colors in this set.
    3.  Find the object that has the highest count of unique colors.
    4.  Create a new grid containing only the pixels corresponding to this selected object, maintaining their original colors and relative positions. Crop this new grid tightly around the object (remove any surrounding rows/columns that are entirely background color). This cropped grid is the output.
