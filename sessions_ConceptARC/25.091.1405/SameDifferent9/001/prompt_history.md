
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 4 0 0 4 0 0 0 0 0
0 4 0 0 4 0 0 0 0 0
0 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 7 7 7
0 0 0 0 0 0 7 0 0 7
0 0 0 0 0 0 7 0 0 7
0 0 0 0 0 0 7 7 7 7
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 0 0 0 0 0
0 8 0 0 8 0 0 0 0 0
0 8 0 0 8 0 0 0 0 0
0 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8
0 0 0 0 0 0 8 0 0 8
0 0 0 0 0 0 8 0 0 8
0 0 0 0 0 0 8 8 8 8
```


## train_2

**input:**
```
0 0 0 0 0 0 7 7 7 7
0 0 0 0 0 0 7 0 0 7
0 0 0 0 0 0 7 0 0 7
0 0 0 0 0 0 7 7 7 7
0 4 4 4 4 4 0 0 0 0
0 4 0 0 0 4 0 0 0 0
0 4 0 0 0 4 0 0 0 0
0 4 0 0 0 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 5 5 5 5
0 0 0 0 0 0 5 0 0 5
0 0 0 0 0 0 5 0 0 5
0 0 0 0 0 0 5 5 5 5
0 5 5 5 5 5 0 0 0 0
0 5 0 0 0 5 0 0 0 0
0 5 0 0 0 5 0 0 0 0
0 5 0 0 0 5 0 0 0 0
0 5 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 0
0 0 0 0 0 0 4 0 4 0
7 7 7 7 0 0 4 4 4 0
7 0 0 7 0 0 0 0 0 0
7 0 0 7 0 0 0 0 0 0
7 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 5 5 5 0
0 0 0 0 0 0 5 0 5 0
5 5 5 5 0 0 5 5 5 0
5 0 0 5 0 0 0 0 0 0
5 0 0 5 0 0 0 0 0 0
5 5 5 5 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_4

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0
0 0 4 0 4 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 7 0 7
0 0 0 0 0 0 0 7 7 7
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0
0 0 8 0 8 0 0 0 0 0
0 0 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 8 8
0 0 0 0 0 0 0 8 0 8
0 0 0 0 0 0 0 8 8 8
0 0 0 0 0 0 0 0 0 0
```

**Perception**

1.  **Input Grid Structure:** Each input grid contains a white background (color 0) and exactly two distinct shapes.
2.  **Shape Properties:**
    *   The shapes are hollow rectangles.
    *   One rectangle is always composed of yellow pixels (color 4).
    *   The other rectangle is always composed of orange pixels (color 7).
    *   The shapes do not overlap and are separated by the background color.
    *   The size and position of these rectangles vary across examples.
3.  **Output Grid Structure:** The output grid retains the exact size and structure of the input grid. The background remains white (color 0). The positions and shapes of the rectangles are preserved.
4.  **Transformation:** The core transformation involves changing the color of all yellow (4) and orange (7) pixels to a single new color. The background pixels (0) are unchanged.
5.  **Color Change Rule:** The target color depends on the relative number of pixels composing the yellow and orange rectangles:
    *   If the number of yellow pixels is equal to the number of orange pixels, both shapes are colored azure (color 8) in the output.
    *   If the number of yellow pixels is *not* equal to the number of orange pixels, both shapes are colored gray (color 5) in the output.

**Facts**


```yaml
Task: Recolor two shapes based on pixel count comparison.

Input_Features:
  - Grid: 2D array of integers (colors).
  - Background_Color: Always white (0).
  - Objects:
    - Two distinct, non-overlapping, hollow rectangular shapes.
    - Object_1_Color: Yellow (4).
    - Object_2_Color: Orange (7).
    - Properties:
      - Position: Variable.
      - Size: Variable (number of colored pixels).
      - Shape: Hollow rectangle.

Output_Features:
  - Grid: Same dimensions as input.
  - Background_Color: Preserved white (0).
  - Objects:
    - Same two shapes as input (position and structure preserved).
    - Color: All pixels originally yellow (4) or orange (7) are changed to a single new color.
      - New_Color_Option_1: Azure (8).
      - New_Color_Option_2: Gray (5).

Transformation_Rule:
  - Identify all pixels with color yellow (4).
  - Identify all pixels with color orange (7).
  - Count the number of yellow pixels (Count_Yellow).
  - Count the number of orange pixels (Count_Orange).
  - Condition: Compare Count_Yellow and Count_Orange.
    - If Count_Yellow equals Count_Orange:
      - Action: Change all yellow (4) and orange (7) pixels to azure (8).
    - If Count_Yellow does not equal Count_Orange:
      - Action: Change all yellow (4) and orange (7) pixels to gray (5).
  - Preserve all background (0) pixels.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Scan the input grid to count the total number of pixels with the color yellow (4). Store this count as `yellow_count`.
3.  Scan the input grid to count the total number of pixels with the color orange (7). Store this count as `orange_count`.
4.  Compare `yellow_count` and `orange_count`.
5.  If `yellow_count` is equal to `orange_count`, set the target replacement color to azure (8).
6.  Otherwise (if `yellow_count` is not equal to `orange_count`), set the target replacement color to gray (5).
7.  Iterate through each cell (pixel) of the input grid.
8.  If the current cell's color is yellow (4) or orange (7), change the color of the corresponding cell in the output grid to the target replacement color determined in step 5 or 6.
9.  Leave all other cells (specifically, the background white (0) cells) unchanged in the output grid.
10. Return the modified output grid.
