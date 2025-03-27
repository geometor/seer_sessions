
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0 0 0
0 8 8 8 0 0 8 8 0 0
0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 7 0 0 0
0 0 0 0 0 6 6 6 0 0
0 0 0 8 8 0 0 0 0 0
0 0 0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 7 7 0 0 0 0 0 0 0
0 6 6 6 0 0 7 7 0 0
0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 7 6 0 0 0 0 0 0 0
0 9 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 8 8 0 0 0 0 0 0
0 0 8 8 0 0 0 0 8 8
0 0 0 0 0 0 0 0 8 8
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 7 6 0 0 0
0 0 0 0 0 9 4 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 6 0 0 0 0 0 0
0 0 9 4 0 0 0 0 7 6
0 0 0 0 0 0 0 0 9 4
```

Okay, let's break down the task based on the provided examples.

**Perception**

1.  **Input Grid Composition**: The input grids contain a background of white pixels (0) and several distinct objects made of other colors. Notably, azure pixels (8) seem to play a special role, distinct from other colored pixels like orange (7), magenta (6), maroon (9), and yellow (4).
2.  **Output Grid Composition**: The output grids also have a white background (0). The azure objects present in the input are consistently absent in the output. The other colored objects from the input are also absent from their original positions. Instead, new patterns, composed of the non-azure colors seen in the input, appear in the locations previously occupied (at least partially) by the azure objects.
3.  **Identifying Roles**:
    *   **Azure Objects (Color 8)**: These act as "markers" or "target locations". Their presence in the input dictates where something should happen in the output, but they themselves do not appear in the final output.
    *   **Other Colored Objects (Non-0, Non-8)**: These act as the source material for a "pattern" or "stamp". They define *what* gets placed at the target locations.
    *   **Background Pixels (Color 0)**: These constitute the empty space and are the default state of the output grid before patterns are placed.
4.  **Transformation Process**:
    *   The core transformation involves identifying a specific pattern from the non-azure, non-white objects in the input.
    *   It then identifies the locations marked by the azure objects.
    *   Finally, it "stamps" or copies the identified pattern onto the output grid at the locations indicated by the azure objects. The original azure markers and the original pattern source objects are removed (effectively replaced by the background color or overwritten by the stamped patterns).
5.  **Pattern Definition**: The crucial step seems to be how the "pattern" is defined and extracted from the input's non-azure, non-white objects.
    *   In `train_1`, the orange (7) and magenta (6) objects are separate. The pattern applied in the output (`7 7 0 / 6 6 6`) corresponds to the content within the minimal bounding box containing *both* the orange and magenta pixels from the input.
    *   In `train_2`, there are two identical multi-colored objects (`7 6 / 9 4`). The pattern applied in the output is exactly this 2x2 block. This suggests that if multiple identical source objects exist, one is chosen as the pattern. If the source objects differ (as in `train_1`), a combined pattern based on their collective bounding box is used.
6.  **Placement Logic**: The pattern seems to be placed such that its top-left corner aligns with the top-left corner of the *azure marker object* it replaces.

**Facts**


```yaml
Observations:
  - Task: Pattern stamping based on markers.
  - Elements:
    - Background: White pixels (0).
    - Markers: Connected objects of Azure color (8).
    - Pattern Source: Connected objects of any color except White (0) and Azure (8).
    - Pattern Template: A specific grid pattern derived from the Pattern Source objects.
    - Output Grid: Initially background color, then stamped with the Pattern Template.
  - Relationships & Rules:
    - Azure objects define target locations for stamping.
    - Non-white, non-azure objects define the content of the stamp (Pattern Template).
    - Pattern Template Definition:
      - Find all distinct connected Pattern Source objects.
      - Check if all Pattern Source objects are identical (same shape and colors relative to their top-left corner).
      - IF identical: The Pattern Template is one instance of the source object (e.g., the one with the top-most, left-most coordinate).
      - ELSE (not identical): The Pattern Template is the content of the minimal bounding box containing *all* pixels of *all* Pattern Source objects in the input grid (including background pixels within that box).
    - Stamping Process:
      - Find the top-left coordinate (min_row, min_col) of each Azure marker object.
      - Create an empty output grid (all background color).
      - For each Azure marker's top-left coordinate, copy the Pattern Template onto the output grid, aligning the template's top-left corner with the marker's top-left coordinate.
    - Input objects (Markers and Pattern Sources) are not directly preserved in the output at their original locations; they are effectively replaced by the background or the stamped patterns.
```


**Natural Language Program**

1.  Initialize a new grid, the `output_grid`, with the same dimensions as the `input_grid`, filled entirely with the background color (white, 0).
2.  Identify all distinct connected groups of pixels in the `input_grid` that are neither the background color (0) nor the marker color (azure, 8). These are the "source objects".
3.  Determine the "pattern template":
    a.  Examine the identified "source objects". If there is more than one, check if they are all identical in shape and color pattern relative to their top-left corners.
    b.  If all source objects are identical (or if there is only one source object), select the source object with the top-most, left-most starting pixel. The "pattern template" is the grid representing this object's pixels relative to its top-left corner.
    c.  If the source objects are not identical, find the minimum bounding box that encloses all pixels belonging to any source object. The "pattern template" is the rectangular subgrid extracted from the `input_grid` corresponding to this bounding box (including any background pixels within it).
4.  Identify all distinct connected groups of pixels in the `input_grid` that are the marker color (azure, 8). These are the "marker objects".
5.  For each "marker object" found:
    a.  Find the coordinate (row, column) of its top-left pixel (the pixel with the minimum row index, and among those, the minimum column index).
    b.  Overlay the "pattern template" onto the `output_grid`. Place the top-left pixel of the "pattern template" at the identified top-left coordinate (row, column) of the marker object. The pixels from the template overwrite the existing pixels in the `output_grid` at that location.
6.  Return the `output_grid`.
