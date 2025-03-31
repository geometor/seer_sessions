
## train_1

**input:**
```
4 4 7 7 7 7 9 7 6 6
4 4 7 7 7 7 9 9 7 6
7 7 7 7 7 7 9 9 8 6
7 7 7 7 5 7 7 7 7 6
7 7 7 7 5 5 7 7 7 7
7 5 7 7 7 7 7 7 7 7
7 5 5 7 7 7 7 7 7 7
7 7 7 8 7 7 7 7 7 7
2 7 8 8 7 7 7 7 9 7
2 7 7 7 7 7 7 7 9 9
```


**output:**
```
2 4 7 7 7 7 9 7 4 4
2 4 7 7 7 7 9 9 4 4
7 7 7 7 7 7 9 9 8 6
7 7 7 7 5 7 7 7 7 6
7 7 7 7 5 5 7 7 7 7
7 5 7 7 7 7 7 7 7 7
7 5 5 7 7 7 7 7 6 6
7 7 7 8 7 7 7 7 7 6
9 7 8 8 7 7 7 7 9 6
9 9 7 7 7 7 7 7 9 6
```


## train_2

**input:**
```
5 7 3 7 7 7 9 9
5 7 3 7 7 7 9 9
5 7 7 7 7 7 7 7
7 7 7 5 5 5 7 7
7 7 7 7 3 7 7 7
7 7 7 7 3 7 7 5
7 2 2 7 3 7 7 5
7 2 2 7 7 7 7 5
```


**output:**
```
5 7 3 7 7 7 9 5
5 7 3 7 7 7 9 5
5 7 7 7 7 7 7 5
7 7 7 5 5 5 7 7
7 7 7 7 3 7 7 7
5 7 7 7 3 7 7 5
5 2 2 7 3 7 9 9
5 2 2 7 7 7 9 9
```


## train_3

**input:**
```
6 7 3 3 7 2 2 2
6 7 3 3 7 7 7 6
7 7 7 5 7 7 7 6
7 2 7 7 5 7 7 7
7 2 2 2 7 7 7 7
7 7 7 6 6 7 7 7
5 5 7 7 7 7 7 4
5 5 7 7 7 7 7 4
```


**output:**
```
5 5 3 3 7 2 2 6
5 5 3 3 7 7 7 6
7 7 7 5 7 7 7 6
7 2 7 7 5 7 7 7
7 2 2 2 7 7 7 7
7 7 7 6 6 7 7 7
4 5 7 7 7 7 7 4
4 5 7 7 7 2 2 2
```

Okay, let's analyze the task based on the provided examples.

## Perception

1.  **Grid Structure:** The inputs and outputs are grids of varying sizes (10x10, 8x8, 8x8) filled primarily with an orange background color (7).
2.  **Objects:** Within the grids, there are distinct objects composed of contiguous blocks of non-background colors. These objects vary in color, shape, and size.
3.  **Focus Area:** The changes between input and output grids occur exclusively in the regions near the four corners. Objects located away from the corners remain unchanged.
4.  **Corner Objects:** For each corner, there is an associated "corner object". This object is the contiguous block of non-background color that either includes the corner pixel itself or is the first non-background block encountered when moving inward from the corner along the grid edges.
5.  **Transformation Pattern:** The color of each corner object in the output depends on the colors of the objects on the *diagonally opposite* corners in the input. Specifically:
    *   The new colors for the Top-Left (TL) and Bottom-Right (BR) corner objects are determined *together* based on the original colors of the TL and BR objects.
    *   Similarly, the new colors for the Top-Right (TR) and Bottom-Left (BL) corner objects are determined *together* based on the original colors of the TR and BL objects.
6.  **Color Mapping Rules:** There appear to be fixed transformation rules for pairs of colors across diagonals:
    *   **Diagonal 1 (TL <-> BR):**
        *   If input is (Yellow 4, Maroon 9), output is (Red 2, Magenta 6).
        *   If input is (Gray 5, Gray 5), output is (Gray 5, Maroon 9).
        *   If input is (Magenta 6, Yellow 4), output is (Gray 5, Red 2).
    *   **Diagonal 2 (TR <-> BL):**
        *   If input is (Magenta 6, Red 2), output is (Yellow 4, Maroon 9).
        *   If input is (Maroon 9, Red 2), output is (Gray 5, Gray 5).
        *   If input is (Red 2, Gray 5), output is (Magenta 6, Yellow 4).
7.  **Object Integrity:** When a corner object's color changes, all pixels belonging to that object adopt the new color. The shape and extent of the object remain the same.

## YAML Facts


