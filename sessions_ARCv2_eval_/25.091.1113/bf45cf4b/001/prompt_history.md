
## train_1

**input:**
```
4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 2 2 4 2 4 4
4 4 4 4 4 4 2 4 2 2 4 4
4 4 4 4 4 4 4 2 4 2 4 4
4 4 4 4 4 4 4 4 4 4 4 4
4 8 3 8 4 4 4 4 4 4 4 4
4 3 4 3 4 4 4 4 4 4 4 4
4 8 3 8 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4
```


**output:**
```
8 3 8 8 3 8 4 4 4 8 3 8
3 4 3 3 4 3 4 4 4 3 4 3
8 3 8 8 3 8 4 4 4 8 3 8
8 3 8 4 4 4 8 3 8 8 3 8
3 4 3 4 4 4 3 4 3 3 4 3
8 3 8 4 4 4 8 3 8 8 3 8
4 4 4 8 3 8 4 4 4 8 3 8
4 4 4 3 4 3 4 4 4 3 4 3
4 4 4 8 3 8 4 4 4 8 3 8
```


## train_2

**input:**
```
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 1 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 1 1 1 3 3 3 8 8 8 3 3 3 3 3 3
3 3 3 3 3 3 3 3 8 2 8 3 3 3 3 3 3
3 3 3 3 3 3 3 3 8 8 8 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3
```


**output:**
```
8 8 8 3 3 3 3 3 3
8 2 8 3 3 3 3 3 3
8 8 8 3 3 3 3 3 3
3 3 3 8 8 8 3 3 3
3 3 3 8 2 8 3 3 3
3 3 3 8 8 8 3 3 3
3 3 3 8 8 8 3 3 3
3 3 3 8 2 8 3 3 3
3 3 3 8 8 8 3 3 3
8 8 8 8 8 8 8 8 8
8 2 8 8 2 8 8 2 8
8 8 8 8 8 8 8 8 8
```


## train_3

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 6 6 6 1 1 1 1 1 1 1 1
1 6 1 6 1 1 1 1 1 1 1 1
1 1 6 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 9 9 8 1 1 1
1 1 1 1 1 9 4 4 9 1 1 1
1 1 1 1 1 9 4 4 9 1 1 1
1 1 1 1 1 8 9 9 8 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
```


**output:**
```
8 9 9 8 8 9 9 8 8 9 9 8
9 4 4 9 9 4 4 9 9 4 4 9
9 4 4 9 9 4 4 9 9 4 4 9
8 9 9 8 8 9 9 8 8 9 9 8
8 9 9 8 1 1 1 1 8 9 9 8
9 4 4 9 1 1 1 1 9 4 4 9
9 4 4 9 1 1 1 1 9 4 4 9
8 9 9 8 1 1 1 1 8 9 9 8
1 1 1 1 8 9 9 8 1 1 1 1
1 1 1 1 9 4 4 9 1 1 1 1
1 1 1 1 9 4 4 9 1 1 1 1
1 1 1 1 8 9 9 8 1 1 1 1
```

Okay, let's break down this task.

**Perception of the Elements:**

Each task example presents an input grid containing a background color and exactly two distinct "patterns" composed of other colors. These patterns are spatially separated. The output grid is constructed by using one of the input patterns (the "tile pattern") to tile a larger grid, where the arrangement of the tiles is determined by the structure of the *other* input pattern (the "shape pattern").

1.  **Background:** The most frequent color in the input grid acts as the background.
2.  **Patterns:** There are always two distinct objects or patterns composed of non-background colors. These patterns can be complex shapes but are treated by their bounding boxes.
3.  **Pattern Roles:** One pattern dictates the overall layout (Shape Pattern), while the other provides the repeating motif (Tile Pattern).
4.  **Selection Rule:** The pattern chosen as the Tile Pattern appears to be the one containing a greater variety of distinct non-background colors within its bounding box. The other pattern becomes the Shape Pattern.
5.  **Transformation:**
    *   The Shape Pattern is converted into a binary matrix (1 for non-background, 0 for background within its bounding box).
    *   The output grid's dimensions are determined by multiplying the dimensions of the Shape Pattern's bounding box by the dimensions of the Tile Pattern's bounding box.
    *   The output grid is constructed by placing copies of the Tile Pattern wherever the Shape Pattern's binary matrix has a '1', and placing solid blocks of the background color (matching the Tile Pattern's dimensions) wherever the Shape Pattern's binary matrix has a '0'.

**YAML Fact Document:**


