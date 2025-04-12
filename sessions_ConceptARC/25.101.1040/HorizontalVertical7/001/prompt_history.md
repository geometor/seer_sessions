
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 0
0 0 8 8 8 2 8 8 8 0
0 0 8 8 8 8 8 8 8 0
0 0 8 8 8 8 8 8 8 0
0 0 8 8 8 8 8 8 8 0
0 0 8 8 8 2 8 8 8 0
0 0 8 8 8 8 8 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 0 0 0 0 0 0 0 0 0
2 0 8 8 8 8 8 8 8 0
2 0 8 8 8 2 8 8 8 0
2 0 8 8 8 8 8 8 8 0
2 0 8 8 8 8 8 8 8 0
2 0 8 8 8 8 8 8 8 0
2 0 8 8 8 2 8 8 8 0
2 0 8 8 8 8 8 8 8 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 4 4 4 4 2 0 0 0
0 4 4 4 4 4 4 4 0 0
0 0 4 4 4 4 2 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 0 0 0 0 0 0 0 0 0
2 0 0 0 4 0 0 0 0 0
2 0 0 4 4 4 0 0 0 0
2 0 4 4 4 4 2 0 0 0
2 4 4 4 4 4 4 4 0 0
2 0 4 4 4 4 2 0 0 0
2 0 0 4 4 4 0 0 0 0
2 0 0 0 4 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0 0 0
0 0 0 3 3 3 3 0 0 0
0 0 0 3 3 3 3 0 0 0
0 2 0 3 3 2 3 0 0 0
0 3 3 3 3 3 3 3 0 0
0 3 3 3 3 3 3 3 0 0
0 3 3 3 3 3 3 3 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 3 3 0 0 0
```


**output:**
```
2 2 2 2 2 2 2 2 2 2
0 0 3 3 3 3 3 0 0 0
0 0 0 3 3 3 3 0 0 0
0 0 0 3 3 3 3 0 0 0
0 2 0 3 3 2 3 0 0 0
0 3 3 3 3 3 3 3 0 0
0 3 3 3 3 3 3 3 0 0
0 3 3 3 3 3 3 3 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 3 3 0 0 0
```

**Perception:**

The input grids consist of a white background (0) containing a primary shape made of a single color (azure-8, yellow-4, or green-3) and one or more red pixels (2). The output grid is largely identical to the input grid, with one significant modification: either the first row (row 0) or the first column (column 0) is entirely filled with red pixels (2).

The determining factor for whether the first row or the first column is modified appears to be the spatial arrangement of the red pixels in the input grid.
- In examples 1 and 2, the red pixels are vertically aligned (share the same column index). In the corresponding outputs, the first column (column 0) is filled with red.
- In example 3, the red pixels are horizontally aligned (share the same row index). In the corresponding output, the first row (row 0) is filled with red.

The transformation rule seems to be:
1.  Locate all red pixels (2) in the input grid.
2.  Determine if all these red pixels lie on the same row or the same column.
3.  If they lie on the same row, modify the input grid by changing all pixels in the first row (row 0) to red (2).
4.  If they lie on the same column, modify the input grid by changing all pixels in the first column (column 0) to red (2).
5.  If there are no red pixels, or if they do not all share the same row or column, the output is likely identical to the input (though this case is not explicitly shown).

**Facts:**


```yaml
# Analysis of the transformation process across examples

# Example 1:
Input_Objects:
  - Object: Background
    Color: white (0)
    Location: Surrounds the main shape.
  - Object: Shape
    Color: azure (8)
    Structure: Large rectangle.
  - Object: Key_Pixels
    Color: red (2)
    Count: 2
    Locations: [(2, 5), (6, 5)] # row, col
    Alignment: Vertical (share column 5)
Output_Change:
  Action: Fill_Column
  Target: Column 0
  Color: red (2)
  Relationship: Triggered by vertical alignment of Key_Pixels.

# Example 2:
Input_Objects:
  - Object: Background
    Color: white (0)
    Location: Surrounds the main shape.
  - Object: Shape
    Color: yellow (4)
    Structure: Diamond-like.
  - Object: Key_Pixels
    Color: red (2)
    Count: 2
    Locations: [(3, 6), (5, 6)]
    Alignment: Vertical (share column 6)
Output_Change:
  Action: Fill_Column
  Target: Column 0
  Color: red (2)
  Relationship: Triggered by vertical alignment of Key_Pixels.

# Example 3:
Input_Objects:
  - Object: Background
    Color: white (0)
    Location: Surrounds the main shape.
  - Object: Shape
    Color: green (3)
    Structure: G-like/Spiral.
  - Object: Key_Pixels
    Color: red (2)
    Count: 2
    Locations: [(4, 1), (4, 5)]
    Alignment: Horizontal (share row 4)
Output_Change:
  Action: Fill_Row
  Target: Row 0
  Color: red (2)
  Relationship: Triggered by horizontal alignment of Key_Pixels.

# General Observation:
- The transformation identifies the alignment (horizontal or vertical) of all red (2) pixels present in the input.
- If all red pixels share the same row index, the first row (index 0) of the output grid is filled with red (2).
- If all red pixels share the same column index, the first column (index 0) of the output grid is filled with red (2).
- All other pixels retain their original color and position from the input grid.
```


**Natural Language Program:**

1.  Create a copy of the input grid to serve as the basis for the output grid.
2.  Find the coordinates (row, column) of all pixels in the input grid that have the color red (2).
3.  If no red pixels are found, return the unmodified copy of the input grid.
4.  If red pixels are found, check if all of them share the same row index.
5.  If all red pixels share the same row index, modify the output grid by setting the color of every pixel in the first row (row 0) to red (2).
6.  If all red pixels do *not* share the same row index, check if all of them share the same column index.
7.  If all red pixels share the same column index, modify the output grid by setting the color of every pixel in the first column (column 0) to red (2).
8.  Return the modified output grid.
