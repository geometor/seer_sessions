
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 7 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 7 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 7 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 7 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 2 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 8 8 8 8
```


## train_3

**input:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 9 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 9 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```


## train_4

**input:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 1 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 1 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 8
```

Okay, let's analyze the task examples.

**Perception of Elements:**

1.  **Grid Structure:** All examples use a 10x10 grid.
2.  **Background Color:** The predominant color in all grids is azure (8), acting as the background.
3.  **Foreground Objects:** In each input grid, there are one or two pixels that are *not* the background color. These non-background pixels are always the same color within a single example.
    *   Example 1: Two orange (7) pixels.
    *   Example 2: Two red (2) pixels.
    *   Example 3: One maroon (9) pixel.
    *   Example 4: Two blue (1) pixels.
4.  **Transformation:** The transformation involves moving the foreground (non-azure) pixels to new locations. The background (azure) pixels remain unchanged.
5.  **Movement Pattern:** The direction and distance of the movement seem to depend entirely on the *color* of the foreground pixels.
    *   Orange (7) pixels move 2 steps up.
    *   Red (2) pixels move 2 steps left.
    *   Maroon (9) pixels move 2 steps down.
    *   Blue (1) pixels move 1 step right.
6.  **Consistency:** All foreground pixels within a single grid undergo the exact same translation (movement).

**YAML Facts:**


```yaml
Grid:
  Type: 2D Array
  Size: 10x10 (consistent across examples)
  BackgroundPixel:
    Color: azure
    Value: 8
ForegroundPixels:
  ObjectType: Single Pixels
  Quantity: 1 or 2 per grid
  ColorProperty: All foreground pixels within a grid share the same color.
  ObservedColors: [orange (7), red (2), maroon (9), blue (1)]
Transformation:
  Action: Translate (Move)
  Target: All ForegroundPixels
  Rule: The translation vector (delta_row, delta_col) depends on the color of the ForegroundPixels.
  ColorToVectorMapping:
    blue (1): (0, 1)  # Right 1
    red (2): (0, -2) # Left 2
    orange (7): (-2, 0) # Up 2
    maroon (9): (2, 0) # Down 2
  OutputGrid:
    - Original positions of ForegroundPixels are replaced with BackgroundPixel color.
    - Translated positions are updated with the ForegroundPixel color.
    - All other BackgroundPixels remain unchanged.
```


**Natural Language Program:**

1.  Identify the background color (azure, 8).
2.  Find all pixels in the input grid that are not the background color. Record their coordinates and their common color.
3.  Based on the identified common color, determine the movement vector (change in row, change in column) as follows:
    *   If the color is blue (1), the vector is (0, 1).
    *   If the color is red (2), the vector is (0, -2).
    *   If the color is orange (7), the vector is (-2, 0).
    *   If the color is maroon (9), the vector is (2, 0).
4.  Create a new grid, initially identical to the input grid.
5.  For each non-background pixel identified in step 2:
    *   Set its original position in the new grid to the background color (azure, 8).
6.  For each non-background pixel identified in step 2:
    *   Calculate its new position by adding the determined movement vector to its original coordinates.
    *   Set the calculated new position in the new grid to the pixel's color.
7.  The resulting new grid is the output.
