## Perception

1.  **Grid Structure:** The input and output grids are consistently 30 rows by 22 columns. They feature a predominant gray (8) background. Two distinct horizontal lines composed entirely of magenta (6) pixels are present at row index 5 and row index 27, acting as visual separators.
2.  **Objects:** Scattered across the gray background, primarily between the magenta lines and in the area above the first magenta line, are small, distinct shapes made of various colors (white-0, blue-1, red-2, green-3, yellow-4, gray-5, orange-7, maroon-9). These shapes are typically 3x3 or smaller arrangements of pixels.
3.  **Key Colors:** Gray (8) is the background. Magenta (6) forms separators. Green (3) is introduced in the output as a replacement for some gray pixels. Red (2) is also introduced in the output, specifically in the bottom two rows under certain conditions.
4.  **Transformation Areas:** Changes primarily occur in two ways:
    *   Gray pixels immediately surrounding (including diagonally) the colorful shapes change to green (3).
    *   The bottom two rows (rows 28 and 29), which are initially gray (8), are uniformly changed to either green (3) or red (2).
5.  **Invariance:** The magenta separator lines (rows 5 and 27) and the original colorful shapes themselves remain unchanged in the output.

## Facts


```yaml
Grid:
  Properties:
    - Dimensions: 30 rows x 22 columns (consistent across examples)
    - BackgroundColor: Gray (8)
Regions:
  - Name: TopSection
    Location: Rows 0-4
  - Name: Separator1
    Location: Row 5
    Color: Magenta (6)
  - Name: MiddleSection
    Location: Rows 6-26
  - Name: Separator2
    Location: Row 27
    Color: Magenta (6)
  - Name: BottomSection
    Location: Rows 28-29
Objects:
  - Name: Shape
    Properties:
      - Color: Any color except Gray (8) or Magenta (6)
      - Location: Primarily within TopSection and MiddleSection
      - Size: Typically small, often within 3x3 bounding box
      - Composition: Contiguous pixels of the same color
Actions:
  - Name: FindAdjacentGrays
    Input: Input Grid
    Output: Set of coordinates of Gray (8) pixels
    Rule: Identify all Gray (8) pixels that are adjacent (including diagonals, 8-connectivity) to any Shape pixel.
  - Name: ChangeAdjacentToGreen
    Input: Input Grid, Set of coordinates from FindAdjacentGrays
    Output: Modified Grid
    Rule: Change the color of the pixels at the identified coordinates to Green (3).
  - Name: CheckTopSectionChange
    Input: Input Grid, Modified Grid (from ChangeAdjacentToGreen)
    Output: Boolean flag (True if changes occurred in TopSection, False otherwise)
    Rule: Compare the TopSection (rows 0-4) of the Input Grid and the Modified Grid. Return True if any pixel changed color within this section, False otherwise.
  - Name: SetBottomColor
    Input: Modified Grid, Boolean flag (from CheckTopSectionChange)
    Output: Final Output Grid
    Rule:
      - If the boolean flag is True: Change all pixels in the BottomSection (rows 28-29) to Green (3).
      - If the boolean flag is False: Change all pixels in the BottomSection (rows 28-29) to Red (2).
Relationships:
  - Adjacency: Used to find Gray pixels near Shapes (8-directional connectivity).
  - Containment: Shapes are contained within specific Regions (TopSection, MiddleSection). Changes are assessed based on Region (TopSection).
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Create a list to store the coordinates `(row, col)` of gray (8) pixels that need to change color.
3.  Iterate through each pixel `(r, c)` of the input grid.
4.  If the pixel at `(r, c)` is gray (8):
    a.  Check all 8 neighbors (including diagonals) of `(r, c)`.
    b.  If any neighbor exists within the grid boundaries and its color is *not* gray (8) and *not* magenta (6), add the coordinate `(r, c)` to the list of pixels to change.
5.  Keep track if any changes were identified within the top section (rows 0 to 4 inclusive) during step 4b. Let's call this flag `top_section_changed`, initially False. If a coordinate `(r, c)` with `r <= 4` is added to the list in step 4b, set `top_section_changed` to True.
6.  Iterate through the list of coordinates identified in step 4. For each coordinate `(r, c)` in the list, change the color of the pixel at `(r, c)` in the output grid to green (3).
7.  Determine the color for the bottom two rows (rows 28 and 29):
    a.  If `top_section_changed` is True, the target color is green (3).
    b.  If `top_section_changed` is False, the target color is red (2).
8.  Change all pixels in rows 28 and 29 of the output grid to the determined target color.
9.  Return the final output grid.