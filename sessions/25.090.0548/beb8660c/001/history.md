
## train_1

**input:**
```
0 0 0 1
0 0 0 0
2 2 2 0
0 0 0 0
0 3 3 0
0 0 0 0
8 8 8 8
```


**output:**
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 1
0 0 3 3
0 2 2 2
8 8 8 8
```


## train_2

**input:**
```
0 2 2 0 0 0 0
0 0 0 0 3 0 0
1 1 1 0 0 0 0
0 0 0 0 0 0 0
0 5 5 5 5 5 5
0 0 0 0 0 0 0
6 6 6 6 6 0 0
0 0 0 4 4 4 4
0 0 0 0 0 0 0
8 8 8 8 8 8 8
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 3
0 0 0 0 0 2 2
0 0 0 0 1 1 1
0 0 0 4 4 4 4
0 0 6 6 6 6 6
0 5 5 5 5 5 5
8 8 8 8 8 8 8
```


## train_3

**input:**
```
2 2 0
0 4 0
8 8 8
```


**output:**
```
0 0 4
0 2 2
8 8 8
```

Okay, let's analyze the task examples.

**Perception of Elements**

1.  **Grid Structure:** The input and output are grids of pixels, where each pixel has a color represented by an integer (0-9). White (0) acts as the background.
2.  **Azure Line (8):** In every example, there is a solid horizontal line composed of azure (8) pixels at the bottom row of the input grid. This line remains unchanged in the same position in the output grid. It functions as a fixed base or ground.
3.  **Colored Objects:** Above the azure line, the input grid contains various horizontal lines (segments) of different colors (blue, red, green, yellow, gray, magenta). These lines vary in length, color, and vertical/horizontal position. These are the objects that are transformed.
4.  **Transformation:** The core transformation involves rearranging the colored horizontal lines vertically. They appear to be collected, sorted, and then stacked compactly above the azure base line.
5.  **Sorting Mechanism:** Comparing the input and output arrangements, particularly in Example 2, reveals that the final vertical stacking order (from bottom to top, just above the azure line) corresponds to the objects sorted by their length in descending order. Longer lines are placed lower (closer to the azure base), and shorter lines are placed higher.
6.  **Tie-breaking:** In Example 1, two lines (red and green) have the same length (3). In the input, red is above green. In the output stack, red is placed first (lower) and green is placed directly above it. This suggests that for objects with the same length, their relative vertical order from the input is preserved during the sort (the one originally lower is placed lower in the stack).
7.  **Stacking:** The sorted objects are placed one by one, starting with the longest. The first (longest) object is placed in the row directly above the azure line. Each subsequent object is placed in the row directly above the previously placed object.
8.  **Horizontal Position:** Each object retains its original horizontal position (column indices) when placed in the output stack.
9.  **Background:** All space not occupied by the azure line or the rearranged colored objects becomes white (0).

**Facts**


```yaml
Task: Rearrange horizontal colored lines based on length.

Input_Features:
  - Grid: 2D array of integers (colors).
  - Objects:
      - Type: Horizontal contiguous lines of a single color.
      - Exclusions: White (0) background pixels are not objects. Azure (8) pixels form a special base object.
  - Base_Object:
      - Color: Azure (8).
      - Shape: Always a full-width horizontal line.
      - Position: Always occupies the bottom-most row.
      - Behavior: Fixed; remains unchanged in the output.
  - Movable_Objects:
      - Colors: Any color except White (0) and Azure (8).
      - Shape: Horizontal lines of varying lengths (>= 1 pixel).
      - Properties:
          - color: The integer value (1-7, 9).
          - length: The number of pixels in the line.
          - position: Original row and column indices in the input.

Transformation:
  - Action: Vertical rearrangement and stacking of Movable_Objects above the Base_Object.
  - Process:
      1. Identify all Movable_Objects and their properties (color, length, original position).
      2. Identify the Base_Object (Azure line) and its row index.
      3. Sort the Movable_Objects primarily by length in descending order.
      4. Use the original relative vertical order (topmost first) as a secondary sort key for objects with equal length (although examples suggest bottom-most first might be the tie-breaker - let's stick to the observed Ex1: Red was above Green, Red is placed first -> bottom-most first). Let's re-check Ex1: Input Red(row 2), Green(row 4). Output Red(row 5), Green(row 4). Red is lower. So, original *lower* object comes first in sort tiebreak.
      5. Create an output grid of the same dimensions as the input, initialized to White (0).
      6. Place the fixed Base_Object (Azure line) in the output grid at its original position.
      7. Initialize the 'current stacking row' to the row directly above the Base_Object.
      8. Iterate through the sorted Movable_Objects (longest first):
          a. Place the current object in the 'current stacking row', maintaining its original column indices.
          b. Decrement the 'current stacking row' by 1 for the next object.

Output_Features:
  - Grid: Same dimensions as input.
  - Base_Object: Azure line in the same bottom row position.
  - Stacked_Objects: The Movable_Objects from the input, stacked vertically above the Base_Object according to the length-sorted order, preserving original horizontal positions.
  - Background: Remaining grid cells are White (0).

Relationships:
  - The final vertical position of a Movable_Object depends on its length relative to other Movable_Objects.
  - The horizontal position of each Movable_Object is preserved from input to output.
  - All Movable_Objects are stacked contiguously above the fixed Base_Object.
```


**Natural Language Program**

1.  Initialize a new grid with the same dimensions as the input grid, filled with the background color (white, 0).
2.  Locate the horizontal line of azure (8) pixels in the input grid. Copy this azure line to the exact same position in the new grid. Record the row index just above the azure line as the starting `stack_row`.
3.  Identify all distinct horizontal contiguous lines of pixels in the input grid that are *not* white (0) or azure (8). For each line, record its color, its length (number of pixels), its original column indices, and its original top row index.
4.  Create a list of these identified lines.
5.  Sort this list of lines based on the following criteria:
    *   Primary key: Sort by line length in descending order (longest lines first).
    *   Secondary key (for tie-breaking when lengths are equal): Sort by original top row index in descending order (lines that were originally lower in the input grid come first in case of a tie).
6.  Iterate through the sorted list of lines:
    *   For the current line, retrieve its color and original column indices.
    *   Place the pixels of this line into the new grid at the current `stack_row`, using its original column indices.
    *   Decrement the `stack_row` by 1 (move up one row for the next line).
7.  The new grid now contains the transformed output. Return the new grid.
