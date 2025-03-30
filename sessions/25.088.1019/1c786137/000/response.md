Okay, let's break down this task.

## Perception

1.  **Input/Output Relation:** Each output grid is a smaller subgrid extracted from the corresponding input grid.
2.  **Identifying the Subgrid:** The key seems to be locating a specific structure within the input grid. In all examples, there's a prominent rectangular "frame" or "border" made of a single, non-white color.
    *   Example 1: Yellow (4) frame.
    *   Example 2: Red (2) frame.
    *   Example 3: Azure (8) frame.
3.  **Frame Structure:** This frame encloses a rectangular area containing different colors. The frame itself appears to be exactly one pixel thick on all four sides.
4.  **Extraction Logic:** The output grid is precisely the content *inside* this frame, excluding the frame pixels themselves.
5.  **Identifying the Correct Frame:** In each input, there might be multiple shapes or blocks of color. The transformation consistently selects the *largest* such rectangular frame, where "largest" refers to the area of the region *enclosed* by the frame.
6.  **Frame Color:** The specific color of the frame (yellow, red, azure) changes between examples but doesn't seem to affect the *content* of the output, only its location and dimensions within the input.

## Facts


```yaml
task_type: extraction
description: Extract the rectangular region enclosed within the largest single-color rectangular frame found in the input grid.

input_elements:
  - type: grid
    description: A 2D array of pixels with colors 0-9.
  - type: object
    name: frame
    description: A rectangular border, one pixel thick, composed of a single non-white color (C). It surrounds an inner rectangular area.
    properties:
      - color (C): The uniform color of the frame pixels. Must be non-white (not 0).
      - location: Defined by the top-left (r1, c1) and bottom-right (r2, c2) coordinates of the outer boundary of the frame.
      - dimensions: Outer height (r2 - r1 + 1), Outer width (c2 - c1 + 1). Must be at least 3x3.
      - interior: The rectangular area defined by top-left (r1+1, c1+1) and bottom-right (r2-1, c2-1).
      - interior_pixels: All pixels within the interior region. Crucially, these pixels must *not* have the same color as the frame (color C).
      - interior_area: (r2 - r1 - 1) * (c2 - c1 - 1).

selection_criteria:
  - target: frame
  - rule: Select the frame object with the largest 'interior_area'. Assume a unique largest frame exists in valid inputs.

transformation:
  - action: find_largest_frame
    description: Identify the frame object in the input grid that satisfies the 'selection_criteria'.
  - action: extract_interior
    description: Extract the subgrid corresponding to the 'interior' of the selected frame.

output_elements:
  - type: grid
    description: The extracted subgrid representing the 'interior_pixels' of the largest identified frame.
    relationship_to_input: It is a subgrid located at rows r1+1 to r2-1 and columns c1+1 to c2-1 relative to the input grid, where (r1, c1) and (r2, c2) are the bounds of the largest frame.
```


## Natural Language Program

1.  **Scan the input grid** to identify all possible rectangular frames. A frame is defined as follows:
    *   It consists of a rectangular border of pixels, exactly one pixel thick, all having the same single non-white color, let's call this color `C`.
    *   This border encloses an inner rectangular region.
    *   All pixels within the inner rectangular region must *not* have the color `C`.
    *   The frame (including the border) must have dimensions of at least 3x3 (to allow for a non-empty interior).
2.  **Calculate the area of the inner region** for each identified frame (inner height * inner width).
3.  **Select the frame** that has the largest inner area. If multiple frames share the largest area, assume there will be only one based on the examples (or define a tie-breaking rule like top-most, then left-most).
4.  **Extract the subgrid** corresponding precisely to the inner region of the selected largest frame. This extracted subgrid is the final output.