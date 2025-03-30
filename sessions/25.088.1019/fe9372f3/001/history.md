
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 0 0 8 0 0 1 0 0 0 0 0 0 0 0 0
0 1 0 8 0 1 0 0 0 0 0 0 0 0 0 0
0 0 1 2 1 0 0 0 0 0 0 0 0 0 0 0
8 8 2 2 2 8 8 4 8 8 4 8 8 4 8 8
0 0 1 2 1 0 0 0 0 0 0 0 0 0 0 0
0 1 0 8 0 1 0 0 0 0 0 0 0 0 0 0
1 0 0 8 0 0 1 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 0 0 0 4 0 0 0 1 0
0 1 0 0 8 0 0 1 0 0
0 0 1 0 8 0 1 0 0 0
0 0 0 1 2 1 0 0 0 0
4 8 8 2 2 2 8 8 4 8
0 0 0 1 2 1 0 0 0 0
0 0 1 0 8 0 1 0 0 0
0 1 0 0 8 0 0 1 0 0
1 0 0 0 4 0 0 0 1 0
0 0 0 0 8 0 0 0 0 1
0 0 0 0 8 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
```

Okay, let's analyze the provided examples.

**Perception**

1.  **Input Grid:** Contains a single object, a red '+' (cross) shape, placed on a white background. The position of the cross varies between examples. The cross is always composed of 5 red pixels.
2.  **Output Grid:** The output grid retains the original red cross in the same position. Several new colored elements are added around the cross, extending outwards towards the grid boundaries.
3.  **Added Elements:**
    *   **Blue Lines:** Diagonal lines of blue pixels originate from the corners of the 3x3 bounding box surrounding the red cross and extend outwards.
    *   **Azure/Yellow Lines:** Horizontal and vertical lines originate from the center of the edges of the 3x3 bounding box surrounding the red cross and extend outwards. These lines are primarily azure, but yellow pixels appear periodically.
4.  **Pattern:**
    *   The blue lines are purely diagonal.
    *   The horizontal/vertical lines emanating from the cross consist of a repeating pattern: two azure pixels followed by one yellow pixel (Azure, Azure, Yellow, Azure, Azure, Yellow...). This pattern starts *immediately* adjacent to the 3x3 bounding box of the cross.
5.  **Transformation:** The core transformation involves identifying the red cross, preserving it, and then drawing patterned lines outwards from its bounding box in the four diagonal and four orthogonal directions until the grid boundaries are reached. Existing non-white pixels (the red cross itself) are not overwritten. The added lines only color the white background pixels.

**Facts**


```yaml
Task: Draw patterned lines radiating from a central cross object.

Input:
  - Grid: Contains a single object on a white background.
  - Object:
    - Shape: '+' (cross)
    - Color: Red (2)
    - Size: 5 pixels
    - Structure: Central pixel with 4 orthogonal neighbors.
  - Background: White (0)

Output:
  - Grid: Same dimensions as input.
  - Contains:
    - Original red cross object preserved in its input position.
    - New line patterns radiating outwards from the cross.

Transformation:
  - Identify: Locate the red cross object and its center pixel.
  - Define_Region: Determine the 3x3 bounding box centered on the cross.
  - Actions:
    - Draw_Diagonal_Lines:
      - Color: Blue (1)
      - Origin: Corners of the 3x3 bounding box.
      - Direction: Diagonally outwards towards the grid edges.
      - Condition: Only paint white (0) background pixels.
    - Draw_Orthogonal_Lines:
      - Colors: Azure (8) and Yellow (4)
      - Origin: Center pixels of the edges of the 3x3 bounding box (excluding corners).
      - Direction: Horizontally or vertically outwards towards the grid edges.
      - Pattern: Repeating sequence [Azure, Azure, Yellow] starting from the pixel adjacent to the bounding box.
      - Condition: Only paint white (0) background pixels.
  - Relationships:
    - The lines originate relative to the position of the input red cross.
    - The lines extend until they hit the grid boundary.
    - The pattern of azure/yellow depends on the distance from the cross along the orthogonal lines.
```


**Natural Language Program**

1.  Start with the input grid.
2.  Identify the 5 red (2) pixels forming the '+' shape. Determine the coordinates of the central red pixel (center_row, center_col).
3.  Create the output grid as a copy of the input grid.
4.  Define the effective 'bounding box' corners and edge midpoints relative to the center:
    *   Top-Left Corner: (center_row - 1, center_col - 1)
    *   Top-Right Corner: (center_row - 1, center_col + 1)
    *   Bottom-Left Corner: (center_row + 1, center_col - 1)
    *   Bottom-Right Corner: (center_row + 1, center_col + 1)
    *   Top Edge Midpoint: (center_row - 1, center_col)
    *   Bottom Edge Midpoint: (center_row + 1, center_col)
    *   Left Edge Midpoint: (center_row, center_col - 1)
    *   Right Edge Midpoint: (center_row, center_col + 1)
5.  **Draw Diagonal Blue Lines:**
    *   From the Top-Left Corner, move diagonally up-left (decrement row, decrement col) one step at a time. For each step, if the pixel is within grid bounds and is white (0), change it to blue (1). Stop when hitting the grid boundary.
    *   Repeat this process for the other three corners, moving diagonally outwards (Top-Right: up-right; Bottom-Left: down-left; Bottom-Right: down-right).
6.  **Draw Orthogonal Azure/Yellow Lines:**
    *   **Upwards:** Starting from the pixel directly *above* the Top Edge Midpoint (row = center_row - 2, col = center_col), move upwards (decrement row) one step at a time. Keep a counter `k` starting at 1. For each step:
        *   If the pixel is within grid bounds and is white (0):
            *   If `k % 3 == 0`, change the pixel to yellow (4).
            *   Otherwise, change the pixel to azure (8).
        *   Increment `k`.
        *   Stop when hitting the grid boundary.
    *   **Downwards:** Starting from the pixel directly *below* the Bottom Edge Midpoint (row = center_row + 2, col = center_col), move downwards (increment row). Use the same `k` counter logic (resetting `k` to 1) and coloring rules (Azure=8, Yellow=4 based on `k % 3`). Stop at the boundary.
    *   **Leftwards:** Starting from the pixel directly *left* of the Left Edge Midpoint (row = center_row, col = center_col - 2), move leftwards (decrement col). Use the same `k` counter logic (resetting `k` to 1) and coloring rules. Stop at the boundary.
    *   **Rightwards:** Starting from the pixel directly *right* of the Right Edge Midpoint (row = center_row, col = center_col + 2), move rightwards (increment col). Use the same `k` counter logic (resetting `k` to 1) and coloring rules. Stop at the boundary.
7.  The final modified grid is the output.
