
## train_1

**input:**
```
4 4 7 7 7 4 4 7 4 4
4 7 7 7 7 7 4 7 4 7
7 4 4 7 7 7 4 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 4 7 7 7 7
4 7 4 7 7 7 7 7 7 7
7 7 7 4 7 4 7 7 7 7
7 5 5 5 7 7 4 7 7 7
7 7 9 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 4
```


**output:**
```
4 4 7 7 7 4 4 7 4 4
4 7 7 7 7 7 4 7 4 7
7 7 7 7 7 7 4 7 7 7
7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 4 7 7 7 7
4 7 7 7 7 7 7 7 7 7
7 7 7 4 7 4 7 7 7 7
7 5 5 5 7 7 4 7 7 7
7 7 9 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 4
```


## train_2

**input:**
```
7 7 7 7 7 7 7 7 7 7 7 7
4 7 7 4 7 7 4 7 7 7 7 7
7 7 7 7 7 7 4 7 4 7 7 7
7 7 4 7 7 4 7 7 7 7 4 4
7 4 7 7 7 7 7 7 4 7 7 7
7 4 7 7 7 7 7 7 4 4 7 4
7 4 4 7 7 7 5 7 7 4 4 7
4 7 7 7 4 7 5 9 7 7 7 4
4 7 7 4 4 4 5 7 7 7 4 4
7 7 4 7 4 7 7 7 4 7 7 7
7 7 4 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 4 7 7
7 4 7 7 7 7 4 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 7 7
4 7 7 4 7 7 4 7 7 7 7 7
7 7 7 7 7 7 4 7 4 7 7 7
7 7 4 7 7 4 7 7 7 7 4 4
7 4 7 7 7 7 7 7 4 7 7 7
7 4 7 7 7 7 7 7 4 4 7 4
7 4 4 7 7 7 5 7 7 4 4 7
7 7 7 7 7 7 5 9 7 7 7 4
7 7 7 7 7 7 5 7 7 7 4 4
7 7 4 7 7 7 7 7 4 7 7 7
7 7 4 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 4 7 7
7 4 7 7 7 7 4 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7
```


## train_3

**input:**
```
7 4 7 7 7 7 7 7 7 7 7 7 7
4 4 7 7 5 7 7 4 7 7 7 7 7
4 4 7 9 5 7 7 4 7 4 4 7 7
7 7 7 7 5 7 7 4 7 4 7 7 4
7 7 7 7 7 7 7 4 7 7 7 7 7
7 7 7 7 7 7 4 4 4 7 7 7 7
7 4 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 4 7
7 7 7 7 4 7 7 7 7 7 4 7 7
7 4 7 4 7 7 7 7 7 7 7 7 7
```


**output:**
```
7 4 7 7 7 7 7 7 7 7 7 7 7
4 4 7 7 5 7 7 7 7 7 7 7 7
4 4 7 9 5 7 7 7 7 7 7 7 7
7 7 7 7 5 7 7 7 7 7 7 7 4
7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7
7 4 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 4 7
7 7 7 7 4 7 7 7 7 7 4 7 7
7 4 7 4 7 7 7 7 7 7 7 7 7
```

**Perception**

1.  **Grid Composition:** The grids are primarily composed of orange pixels (color 7), serving as a background.
2.  **Key Colors/Objects:** Distinctive colors present are yellow (4), gray (5), and maroon (9).
3.  **Gray Structures:** Gray pixels (5) form lines, either horizontal (Example 1) or vertical (Examples 2 and 3).
4.  **Maroon Pixel:** A single maroon pixel (9) appears in each grid, always adjacent (including diagonals) to the gray line structure.
5.  **Yellow Pixels:** Yellow pixels (4) are scattered throughout the grids.
6.  **Transformation Trigger:** A change occurs only in Example 3. Comparing the examples, the transformation seems conditional. The condition appears related to the configuration of the gray line and the adjacent maroon pixel.
7.  **Nature of Change:** In Example 3, *some* yellow pixels (4) are changed to orange (7). The gray line, the maroon pixel, and other yellow pixels remain unchanged.
8.  **Condition Analysis:**
    *   Example 1: Horizontal gray line. Maroon pixel below it. No change.
    *   Example 2: Vertical gray line. Maroon pixel to its right. No change.
    *   Example 3: Vertical gray line. Maroon pixel to its left. Change occurs.
9.  **Rule Identification:** The transformation happens *if and only if* there is a vertical gray line and the maroon pixel is located immediately to the *left* of any part of that vertical gray line.
10. **Transformation Detail:** When the condition is met (Example 3), the vertical gray line is located in column 4. The yellow pixels that change to orange are all located in columns *greater than* 4 (i.e., to the right of the vertical gray line). Yellow pixels in column 4 or less remain unchanged.

**Facts**


```yaml
elements:
  - object: background
    color: orange (7)
    property: fills most of the grid
  - object: gray_line
    color: gray (5)
    property: can be horizontal or vertical, contiguous line shape
    relationship: always adjacent (including diagonals) to the maroon pixel
  - object: maroon_pixel
    color: maroon (9)
    property: single pixel
    relationship: always adjacent (including diagonals) to the gray line
  - object: yellow_pixels
    color: yellow (4)
    property: scattered individual pixels

transformation_trigger:
  condition: A gray_line exists AND it is vertical AND the maroon_pixel is located in the cell immediately to the left (column index - 1) of any cell occupied by the vertical gray_line.

action_if_triggered:
  target: yellow_pixels
  condition: Only applies to yellow_pixels whose column index is greater than the column index of the vertical gray_line.
  effect: Change the color of the targeted yellow_pixels to orange (7).

action_if_not_triggered:
  effect: The output grid is identical to the input grid.
```


**Natural Language Program**

1.  Identify all gray pixels (5) in the input grid.
2.  Determine if the gray pixels form a single contiguous vertical line.
3.  If a vertical gray line is found:
    a.  Record the column index (`gray_col`) of this vertical line.
    b.  Search for a maroon pixel (9).
    c.  Check if the maroon pixel is located at coordinates (`r`, `gray_col - 1`) for any row `r` where a gray pixel exists at (`r`, `gray_col`).
    d.  If such a maroon pixel exists (to the immediate left of the vertical gray line):
        i.  Create a copy of the input grid to serve as the output grid.
        ii. Iterate through each cell (`r`, `c`) of the input grid.
        iii. If the cell color is yellow (4) AND its column index `c` is greater than `gray_col`:
            Change the color of the corresponding cell in the output grid to orange (7).
        iv. Return the modified output grid.
4.  If no vertical gray line is found, OR if a vertical gray line is found but the maroon pixel is not immediately to its left, return a copy of the input grid unchanged.
