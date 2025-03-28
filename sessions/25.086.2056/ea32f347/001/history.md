
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
5 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 5 5 5 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0 0
0 0 2 2 2 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0
0 5 0 0 5 0 0 0 0 0
0 5 0 0 5 0 0 0 0 0
0 5 0 0 5 0 0 5 0 0
0 5 0 0 5 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 4 0 0 1 0 0 0 0 0
0 4 0 0 1 0 0 0 0 0
0 4 0 0 1 0 0 2 0 0
0 4 0 0 1 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 5 5 5 5 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 5 5 5 5 5 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0
0 2 2 2 2 0 0 1 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 1 0 0
0 4 4 4 4 4 0 1 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0
0 5 0 0 5 0 0 0 0 0
0 5 0 0 5 0 0 0 0 0
0 5 0 0 5 0 0 5 0 0
0 5 0 0 5 0 0 5 0 0
0 5 0 0 5 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 0 0
0 1 0 0 4 0 0 0 0 0
0 1 0 0 4 0 0 0 0 0
0 1 0 0 4 0 0 2 0 0
0 1 0 0 4 0 0 2 0 0
0 1 0 0 4 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task involves identifying distinct gray objects within a grid and recoloring them based on their order and shape. The input grid contains a white background (0) and several gray objects (5). The output grid retains the background but replaces the gray pixels with blue (1), red (2), or yellow (4). There are always exactly three gray objects in the input examples.

*   **Analysis:**
    1.  **Object Identification:** The gray pixels form connected components (objects). In the examples, these are simple horizontal or vertical lines.
    2.  **Object Ordering:** The objects seem to be processed in a specific order. Ordering them by their top-leftmost pixel (row-first, then column) appears consistent. Let's call them Obj1, Obj2, and Obj3 based on this order.
    3.  **Color Assignment:**
        *   Obj1 is consistently colored blue (1).
        *   Obj2 and Obj3 are colored red (2) and yellow (4), but the specific assignment depends on the shapes of Obj2 and Obj3.
    4.  **Shape Dependency:** The shapes relevant seem to be "Horizontal Line" (height=1, width>1) and "Vertical Line" (width=1, height>1).
    5.  **Rule Discovery:**
        *   If Obj2 and Obj3 (determined by reading order) are *both* horizontal lines, then Obj2 becomes red (2) and Obj3 becomes yellow (4).
        *   In all other combinations of shapes for Obj2 and Obj3 (e.g., V-line/V-line, V-line/H-line, H-line/V-line), Obj2 becomes yellow (4) and Obj3 becomes red (2).

*   **Facts:**
    
```yaml
    task_elements:
      - background:
          color: white (0)
          property: static
      - objects:
          source_color: gray (5)
          target_colors: [blue (1), red (2), yellow (4)]
          quantity: 3
          identification: connected components (4-connectivity)
          properties:
            - shape: (Horizontal line, Vertical line)
            - position: (top-left coordinate)
            - order: based on top-left coordinate (row-major)
    transformation:
      type: recoloring
      rules:
        - Find all gray objects.
        - Order objects (Obj1, Obj2, Obj3) by top-left coordinate.
        - Determine shape (H-line, V-line) for each object.
        - Recolor Obj1 to blue (1).
        - If Obj2 is H-line AND Obj3 is H-line:
            Recolor Obj2 to red (2).
            Recolor Obj3 to yellow (4).
        - Else:
            Recolor Obj2 to yellow (4).
            Recolor Obj3 to red (2).
    definitions:
      - H-line: object height = 1 and width > 1
      - V-line: object width = 1 and height > 1
    ```


*   **Natural Language Program:**
    1.  Identify all distinct groups of connected gray (5) pixels in the input grid. Treat adjacent (up, down, left, right) gray pixels as part of the same group (object).
    2.  For each gray object found, determine its top-leftmost pixel's coordinates (minimum row index, then minimum column index).
    3.  Sort these objects based on their top-leftmost coordinates, first by row index (ascending), then by column index (ascending). Label these sorted objects as Object 1, Object 2, and Object 3.
    4.  For each object, determine its bounding box (minimum/maximum row/column). Calculate its height and width.
    5.  Define an object as a "Horizontal Line" if its height is 1 and its width is greater than 1.
    6.  Define an object as a "Vertical Line" if its width is 1 and its height is greater than 1.
    7.  Create the output grid by copying the input grid.
    8.  Change the color of all pixels belonging to Object 1 to blue (1) in the output grid.
    9.  Check if Object 2 is a Horizontal Line AND Object 3 is a Horizontal Line.
        a.  If true: Change the color of all pixels belonging to Object 2 to red (2) and all pixels belonging to Object 3 to yellow (4) in the output grid.
        b.  If false: Change the color of all pixels belonging to Object 2 to yellow (4) and all pixels belonging to Object 3 to red (2) in the output grid.
    10. The modified grid is the final output.
