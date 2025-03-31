
## train_1

**input:**
```
7 1 7 8 0
0 8 7 7 1
7 7 7 7 7
8 7 7 7 1
0 1 7 8 5
```


**output:**
```
5 1 7 8 0
0 8 7 5 1
7 7 7 7 7
8 5 7 0 1
0 1 7 8 5
```


## train_2

**input:**
```
8 9 7 9 3
3 7 7 7 8
7 7 7 7 7
8 7 7 7 8
2 9 7 9 2
```


**output:**
```
8 9 7 9 3
3 2 7 2 8
7 7 7 7 7
8 3 7 3 8
2 9 7 9 2
```


## train_3

**input:**
```
7 4 7 4 5
4 3 7 7 3
7 7 7 7 7
5 7 7 4 3
3 4 7 5 7
```


**output:**
```
5 4 7 4 5
4 3 7 4 3
7 7 7 7 7
5 4 7 4 3
3 4 7 5 4
```

Okay, let's analyze the provided examples to understand the transformation logic.

**Perception of Elements:**

1.  **Input/Output Structure:** Each example consists of a 5x5 input grid and a corresponding 5x5 output grid. The grids contain pixels represented by integers 0-9 (colors).
2.  **Central Feature:** A prominent feature in all examples is a central cross shape made of the color orange (7). This cross consists of the middle row (row index 2) and the middle column (column index 2).
3.  **Changes:** Differences between the input and output grids primarily involve certain orange (7) pixels being changed to other colors.
4.  **Stability:** The central orange cross remains unchanged in all examples. Pixels that are *not* orange in the input also seem to remain unchanged.
5.  **Target Pixels:** The pixels that change are always orange (7) pixels located *outside* the central orange cross.
6.  **Transformation Logic:** The new color assigned to a changed orange pixel appears to depend on the colors of its neighboring pixels (considering all 8 neighbors - cardinal and diagonal). Specifically, it seems related to the unique set of colors present among its neighbors, excluding orange itself.

**YAML Facts:**


```yaml
task_description: Change the color of specific orange pixels based on their non-orange neighbors.
grid_properties:
  size: 5x5 for all examples
 ثابت_elements:
  - type: structure
    shape: cross
    color: orange (7)
    location: central (middle row and middle column)
    behavior: remains unchanged in the output
  - type: pixels
    color: any color except orange (7) located outside the central cross region
    behavior: remains unchanged in the output
transformed_elements:
  - type: pixels
    initial_color: orange (7)
    location: outside the central cross
    trigger: presence of non-orange neighbors
    action: color changes based on a rule
transformation_rule:
  - condition: Pixel is orange (7) AND is NOT part of the central cross.
  - process:
      - step: Identify all 8 neighbors (cardinal and diagonal) of the target orange pixel.
      - step: Collect the colors of these neighbors.
      - step: Filter out any orange (7) neighbors.
      - step: Create a unique set of the remaining non-orange neighbor colors.
      - step: Determine the new color for the target pixel using a mapping based on this set of neighbor colors.
  - specific_mappings_observed: # (Neighbor Set -> Output Color)
      - {white(0), blue(1), azure(8)} -> gray(5)
      - {blue(1), gray(5), azure(8)} -> white(0)
      - {green(3), azure(8), maroon(9)} -> red(2)
      - {red(2), azure(8), maroon(9)} -> green(3)
      - {green(3), yellow(4)} -> gray(5)
      - {green(3), yellow(4), gray(5)} -> yellow(4)
      - {green(3), gray(5)} -> yellow(4)
output_grid_construction:
  - Copy all unchanged pixels (central orange cross, non-orange pixels) from the input.
  - Place the newly calculated colors for the transformed orange pixels into their corresponding positions.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the coordinates of the central row and central column of the input grid.
3.  Iterate through each pixel of the input grid using its row and column index.
4.  For the current pixel, check if its color is orange (7).
5.  If the pixel is orange, check if it lies on the central row OR the central column.
6.  If the orange pixel is *not* on the central row or central column (i.e., it's a target pixel):
    a.  Find all 8 neighboring pixels (up, down, left, right, and diagonals), being careful with grid boundaries.
    b.  Create a list of the colors of these neighbors.
    c.  Filter this list to keep only colors that are *not* orange (7).
    d.  Create a set from the filtered list to get the unique non-orange neighbor colors.
    e.  Determine the new color for the current pixel based on the following mapping rules applied to the set of unique non-orange neighbor colors:
        *   If the set is {white(0), blue(1), azure(8)}, the new color is gray(5).
        *   If the set is {blue(1), gray(5), azure(8)}, the new color is white(0).
        *   If the set is {green(3), azure(8), maroon(9)}, the new color is red(2).
        *   If the set is {red(2), azure(8), maroon(9)}, the new color is green(3).
        *   If the set is {green(3), yellow(4)}, the new color is gray(5).
        *   If the set is {green(3), yellow(4), gray(5)}, the new color is yellow(4).
        *   If the set is {green(3), gray(5)}, the new color is yellow(4).
        *   (Add other mappings if discovered from more examples).
    f.  Update the color of the corresponding pixel in the output grid with the new color.
7.  If the pixel is not orange, or if it is an orange pixel on the central cross, its value in the output grid remains the same as the input (already copied in step 1).
8.  After checking all pixels, return the final output grid.
