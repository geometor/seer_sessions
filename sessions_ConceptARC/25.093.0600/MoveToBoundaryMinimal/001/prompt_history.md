
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 3 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
```


**output:**
```
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 3 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 4
```


## train_2

**input:**
```
3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3 3 3 3 3 3 3 3
0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

**Perception:**

The task involves transforming a 10x10 grid of single digits. In both provided examples, the input grid contains mostly zeros (0), a distinct line pattern (vertical line of 4s in example 1, horizontal line of 3s in example 2), and a single, isolated non-zero digit (3 in example 1, 6 in example 2) located elsewhere in the grid.

The transformation moves the isolated non-zero digit towards the line pattern. The movement stops when the digit is in the cell immediately adjacent to the line pattern. The direction of movement is perpendicular to the orientation of the line pattern (horizontal movement towards a vertical line, vertical movement towards a horizontal line). The original position of the moved digit is replaced with a zero (0). The line pattern itself and all other zero cells remain unchanged.

**YAML Facts:**


```yaml
Grid_Dimensions: 10x10
Elements:
  - Type: Background
    Value: 0
  - Type: Blocking_Pattern
    Value: Non-zero digit forming a line (e.g., 4s in a column, 3s in a row)
    Properties:
      - Orientation: Vertical or Horizontal
      - Extends across most of the grid dimension (row or column)
  - Type: Moving_Digit
    Value: A single non-zero digit, distinct from the blocking pattern and background
    Properties:
      - Isolated: Not part of the blocking pattern
      - Initial_Position: (row, column)
      - Final_Position: (row, column)
Relationships:
  - Moving_Digit is initially separated from the Blocking_Pattern by background cells (0s).
  - The final position of the Moving_Digit is adjacent to the Blocking_Pattern.
Actions:
  - Identify: Locate the Blocking_Pattern and its orientation.
  - Identify: Locate the Moving_Digit and its initial position.
  - Determine_Direction: Set movement direction perpendicular to the Blocking_Pattern's orientation (towards the pattern).
  - Move: Relocate the Moving_Digit along the determined direction.
  - Stop_Condition: Halt movement when the Moving_Digit occupies the cell directly adjacent to the Blocking_Pattern.
  - Update_Grid:
      - Place the Moving_Digit in its final position.
      - Replace the initial position of the Moving_Digit with the Background value (0).
      - Keep the Blocking_Pattern and other Background cells unchanged.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Scan the input grid to identify the "Blocking Pattern": a line (either a full row or a full column) consisting of identical non-zero digits. Note the digit value, the line's orientation (horizontal/vertical), and its index (row or column number).
3.  Scan the input grid to identify the "Moving Digit": a single, isolated non-zero digit that is not part of the Blocking Pattern. Note its value and initial position (row, column).
4.  Determine the target position for the Moving Digit:
    *   If the Blocking Pattern is a vertical line at column `C`: The target position is `(initial_row, C-1)` if the Moving Digit starts left of the line, or `(initial_row, C+1)` if it starts right of the line (assuming movement is always towards the line, the examples suggest movement only stops *before* the line). Based on example 1, the target is `(initial_row, C-1)`.
    *   If the Blocking Pattern is a horizontal line at row `R`: The target position is `(R-1, initial_column)` if the Moving Digit starts below the line, or `(R+1, initial_column)` if it starts above the line. Based on example 2, the target is `(R+1, initial_column)`.
5.  Update the output grid:
    *   Set the cell at the Moving Digit's initial position to 0.
    *   Set the cell at the calculated target position to the value of the Moving Digit.
6.  Return the modified output grid.
