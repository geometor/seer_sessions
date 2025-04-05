
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 4 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 8 8 8 8 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 2 4 2 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0
0 0 0 8 2 2 2 8 0 0
0 0 0 8 2 4 2 8 0 0
0 0 0 8 2 2 2 8 0 0
0 0 0 8 8 8 8 8 0 0
```


## train_2

**input:**
```
0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 6 1 6 0 0 0 0 0 0 0 0 0
0 6 1 1 1 6 0 0 0 0 0 0 0 0
0 0 6 1 6 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 0 0 0 0 0 8
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 6 1 6 0 0 0 0 0 0 0 0 0
0 6 1 1 1 6 0 0 0 0 0 0 0 0
0 0 6 1 6 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 8 0 0 6 0 0 8
0 0 0 0 0 0 0 8 0 6 1 6 0 8
0 0 0 0 0 0 0 8 6 1 1 1 6 8
0 0 0 0 0 0 0 8 0 6 1 6 0 8
0 0 0 0 0 0 0 8 0 0 6 0 0 8
0 0 0 0 0 0 0 8 8 8 8 8 8 8
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception of Task Elements:**
    *   The input consists of a grid containing numerical values, primarily zeros representing the background.
    *   Two distinct non-zero patterns or shapes exist within the grid, separated by the background zeros.
    *   One pattern consistently forms a hollow rectangle using the digit '8'. This acts as a "frame".
    *   The other pattern varies between examples (a plus shape with '2's and '4' in `train_1`, a diamond shape with '6's and '1's in `train_2`). This is the "content" pattern.
    *   The output grid modifies the input by placing a copy of the "content" pattern inside the hollow area of the "frame" pattern.
    *   The original positions of the "frame" and "content" patterns (outside the frame) remain unchanged in the output, except for the area within the frame which is overwritten.

*   **YAML Fact Document:**
    
```yaml
    task_elements:
      - object: Grid
        properties:
          - type: 2D array of integers
          - background_value: 0
      - object: FramePattern
        properties:
          - composed_of: integer 8
          - shape: hollow rectangle
          - role: container
      - object: ContentPattern
        properties:
          - composed_of: non-zero integers (varies, e.g., 2, 4, 1, 6)
          - shape: varies (e.g., plus, diamond)
          - role: content to be placed inside FramePattern
      - object: FrameInterior
        properties:
          - location: area enclosed by FramePattern
          - initial_content: background_value (0)
          - final_content: copy of ContentPattern
    relationships:
      - FramePattern contains FrameInterior
      - ContentPattern is separate from FramePattern in the input
    actions:
      - Identify FramePattern based on value (8) and shape (hollow rectangle).
      - Identify ContentPattern as the other distinct non-zero shape.
      - Determine the bounding box of the ContentPattern.
      - Extract the ContentPattern shape (including relative positions and values within its bounding box).
      - Determine the bounding box of the FrameInterior.
      - Copy the input grid to create the output grid.
      - Place the extracted ContentPattern into the FrameInterior location in the output grid, aligning the top-left corners.
    ```


*   **Natural Language Program:**
    1.  Start with the input grid.
    2.  Identify all connected components (shapes) made of non-zero numbers.
    3.  Find the component that forms a hollow rectangle using the number 8; designate this as the "Frame".
    4.  Find the *other* non-zero connected component; designate this as the "Pattern".
    5.  Calculate the minimum bounding box that encloses all cells of the "Pattern".
    6.  Create a subgrid representing the "Pattern" by extracting the values from the input grid within this bounding box, preserving their relative positions (treat cells outside the Pattern but inside the bounding box as background 0).
    7.  Identify the region inside the "Frame" (the area of zeros enclosed by the 8s); designate this as the "Frame Interior".
    8.  Calculate the minimum bounding box of the "Frame Interior".
    9.  Create the output grid by copying the input grid.
    10. Place the extracted "Pattern" subgrid into the output grid, starting at the top-left corner of the "Frame Interior" bounding box, overwriting the existing values (which should be 0s).
    11. Return the modified grid as the output.
