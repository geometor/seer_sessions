
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5
0 0 0 0 0 0 5 0 0 0 0 2 0 0 2 0 0
0 2 2 2 2 0 0 0 0 2 0 0 0 0 0 0 0
0 2 0 0 2 0 4 0 0 0 0 0 5 0 0 0 0
0 2 0 0 2 0 0 0 0 0 0 0 0 0 0 2 0
0 2 2 2 2 0 0 0 0 0 0 0 0 4 0 0 0
0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 5 0 4 0 0 5 0
0 2 0 0 5 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 4 0 0 4 0 5 5 5 5
0 0 0 0 0 4 0 0 4 0 0 0 0 5 0 0 5
0 4 0 5 0 4 4 4 4 0 0 0 2 5 0 0 5
0 0 0 0 0 0 0 0 0 0 5 0 0 5 5 5 5
0 0 5 0 0 0 0 0 0 0 0 0 5 0 0 0 0
```


**output:**
```
2 2 2 2 4 4 4 4 5 5 5 5
2 0 0 2 4 0 0 4 5 0 0 5
2 0 0 2 4 0 0 4 5 0 0 5
2 2 2 2 4 4 4 4 5 5 5 5
```


## train_2

**input:**
```
0 3 0 0 3 0 0 0 0 8 0 0 0 1 0 0 0 7 0 3 0
0 8 8 8 0 0 8 0 7 0 0 3 0 0 0 7 3 0 0 0 0
0 8 8 8 0 0 0 0 0 0 0 0 8 0 0 0 0 0 8 0 8
0 8 8 8 0 3 3 3 3 0 0 0 0 1 1 1 0 0 0 0 0
1 0 0 0 0 3 3 3 0 0 3 0 0 1 1 1 0 0 1 0 0
0 0 0 8 0 3 3 3 0 0 0 0 1 1 1 1 0 0 0 8 0
1 0 0 0 0 0 0 0 0 8 0 0 0 0 7 0 0 0 0 0 0
0 0 0 1 0 0 0 7 0 0 0 0 0 0 0 0 0 8 7 7 7
0 8 0 0 0 0 8 0 0 3 3 3 0 3 0 0 0 0 7 7 7
0 0 0 3 0 0 0 0 0 3 3 3 0 0 0 0 0 0 7 7 7
0 3 0 0 0 0 3 0 0 3 3 3 0 0 8 0 0 0 0 0 0
0 0 0 8 0 0 0 0 0 0 0 0 0 1 0 0 3 0 0 0 1
```


**output:**
```
8 8 8 3 3 3 3 3 3 1 1 1 7 7 7
8 8 8 3 3 3 3 3 3 1 1 1 7 7 7
8 8 8 3 3 3 3 3 3 1 1 1 7 7 7
```

## Perception of Elements

The task involves transforming an input grid of numbers (colors) into a smaller output grid. The core process seems to be identifying specific rectangular patterns within the input grid and representing them in a structured way in the output.

Two distinct types of patterns and corresponding rules are observed across the examples:

1.  **Hollow Rectangles (Example 1):** The input contains rectangles defined by a colored border with a '0' interior. The task identifies these hollow rectangles (e.g., 4x4 rectangles of colors 2, 4, and 5). The output consists of *solid* rectangles of the *same dimensions and color* as the identified hollow rectangles. These output rectangles are arranged horizontally, sorted by their color value (2, then 4, then 5).
2.  **Solid Rectangles (Example 2):** The input contains solid, monochromatic rectangles (e.g., 3x3 rectangles of colors 8, 3, 1, and 7). The task identifies these solid rectangles. The output consists of *solid* rectangles of the *same dimensions and color*. These output rectangles are arranged horizontally, sorted based on the *position* (column index first, then row index) of the top-left corner of the original rectangle in the input grid.

A unifying principle might be to first determine the "dominant" type of rectangular pattern in the input (hollow or solid) and then apply the corresponding extraction, transformation (always to solid), and sorting rule before arranging them horizontally in the output.

## YAML Facts


