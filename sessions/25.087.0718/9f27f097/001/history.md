
## train_1

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 2
2 1 3 3 1 2 2 2 2 2 2 2
2 1 1 3 1 2 2 2 2 2 2 2
2 1 3 3 3 2 2 2 2 2 2 2
2 1 1 1 1 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 0 0 0 0 2 2 2 2
2 2 2 2 0 0 0 0 2 2 2 2
2 2 2 2 0 0 0 0 2 2 2 2
2 2 2 2 0 0 0 0 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
```


**output:**
```
2 2 2 2 2 2 2 2 2 2 2 2
2 1 3 3 1 2 2 2 2 2 2 2
2 1 1 3 1 2 2 2 2 2 2 2
2 1 3 3 3 2 2 2 2 2 2 2
2 1 1 1 1 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 1 3 3 1 2 2 2 2
2 2 2 2 1 3 1 1 2 2 2 2
2 2 2 2 3 3 3 1 2 2 2 2
2 2 2 2 1 1 1 1 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
```


## train_2

**input:**
```
2 2 2 2 2 0 0 0 0 0 2 2
2 2 2 2 2 0 0 0 0 0 2 2
2 2 2 2 2 0 0 0 0 0 2 2
2 2 2 2 2 0 0 0 0 0 2 2
2 2 2 2 2 0 0 0 0 0 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 1 4 2 2 2 2 2 2
2 4 4 1 4 4 2 2 2 2 2 2
2 4 1 4 1 1 2 2 2 2 2 2
2 4 4 1 4 1 2 2 2 2 2 2
2 4 4 4 4 4 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
```


**output:**
```
2 2 2 2 2 4 1 4 4 4 2 2
2 2 2 2 2 4 4 1 4 4 2 2
2 2 2 2 2 1 1 4 1 4 2 2
2 2 2 2 2 1 4 1 4 4 2 2
2 2 2 2 2 4 4 4 4 4 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 1 4 2 2 2 2 2 2
2 4 4 1 4 4 2 2 2 2 2 2
2 4 1 4 1 1 2 2 2 2 2 2
2 4 4 1 4 1 2 2 2 2 2 2
2 4 4 4 4 4 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
```


## train_3

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 3 3 3 3 3 3 1 1 1 1 1
1 3 3 3 2 3 3 1 1 1 1 1
1 2 2 2 3 2 3 1 1 1 1 1
1 3 3 3 2 3 3 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 0 0 0 0 0 0 1 1 1
1 1 1 0 0 0 0 0 0 1 1 1
1 1 1 0 0 0 0 0 0 1 1 1
1 1 1 0 0 0 0 0 0 1 1 1
```


**output:**
```
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 3 3 3 3 3 3 1 1 1 1 1
1 3 3 3 2 3 3 1 1 1 1 1
1 2 2 2 3 2 3 1 1 1 1 1
1 3 3 3 2 3 3 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 3 3 3 3 3 3 1 1 1
1 1 1 3 3 2 3 3 3 1 1 1
1 1 1 3 2 3 2 2 2 1 1 1
1 1 1 3 3 2 3 3 3 1 1 1
```

Okay, let's analyze the task examples.

## Perception of Elements

1.  **Grid Structure:** Each input and output is a grid of colored pixels.
2.  **Distinct Regions:** The input grids consistently feature at least two distinct rectangular regions set against a uniform background color:
    *   One region contains a pattern composed of various colors (non-background, non-white). This pattern region is often surrounded by a border of the background color.
    *   Another region is a solid rectangle filled entirely with white pixels (color 0), also surrounded by the background color.
3.  **Background Color:** There's a dominant background color filling most of the grid area outside the pattern and white regions. This background color is consistent within each example (red for 1 & 2, blue for 3).
4.  **Transformation:** The core transformation seems to involve copying the pattern from the first region into the white region.
5.  **Invariance:** The background color, the border pixels, and the original pattern region remain unchanged in the output. Only the white region is modified.
6.  **Copy Operation:** The pattern is copied exactly, preserving its internal structure, colors, and orientation. The size of the source pattern region matches the size of the target white region in all examples.

## YAML Facts


```yaml
task_description: Copy a source pattern into a target white region within a grid.

elements:
  - element: grid
    description: A 2D array of pixels representing colors 0-9.
  - element: background_pixel
    description: The pixel color that fills most of the grid and surrounds distinct regions. It's not white (0).
  - element: pattern_region
    description: A rectangular subgrid containing a mix of non-background, non-white pixels. It is surrounded by background pixels.
    properties:
      - location: Coordinates (top-left, bottom-right) within the main grid.
      - content: The actual pattern of pixels within the region, excluding any surrounding background border.
      - size: Height and width of the content pattern.
  - element: white_region
    description: A rectangular subgrid filled entirely with white (0) pixels. It is surrounded by non-white pixels (typically background pixels).
    properties:
      - location: Coordinates (top-left, bottom-right) within the main grid.
      - content: All pixels are white (0).
      - size: Height and width.

relationships:
  - relation: spatial_separation
    description: The pattern_region and white_region are distinct and do not overlap in the input grid.
  - relation: size_match
    description: The height and width of the pattern_region's content must exactly match the height and width of the white_region.
  - relation: framing
    description: Both the pattern_region (potentially including a border) and the white_region are embedded within the background_pixel color.

actions:
  - action: identify_background
    description: Determine the background pixel color (the most common non-white color or the color framing the regions).
  - action: locate_pattern_region
    description: Find the bounding box of the region containing non-background, non-white pixels.
  - action: extract_pattern
    description: Isolate the actual pattern content from the pattern_region (excluding any surrounding background border).
  - action: locate_white_region
    description: Find the bounding box of the rectangular area composed solely of white (0) pixels.
  - action: copy_paste
    description: Replace the content of the white_region in the output grid with the extracted_pattern, maintaining orientation and starting from the top-left corner of the white_region.
  - action: preserve
    description: Keep all other pixels (background, original pattern region) unchanged from the input to the output grid.
```


## Natural Language Program

1.  Initialize the output grid as an identical copy of the input grid.
2.  Identify the background color, which is the predominant color in the grid, excluding white (0).
3.  Find the bounding box of the rectangular region containing pixels that are neither the background color nor white. This defines the source pattern's location and extent. Extract this pattern (the non-background, non-white pixels within the box).
4.  Find the bounding box of the rectangular region composed entirely of white (0) pixels. Let its top-left corner coordinates be (target_row, target_col).
5.  Verify that the dimensions (height and width) of the extracted source pattern exactly match the dimensions of the white region.
6.  Iterate through the pixels of the extracted source pattern. For each pixel at relative coordinates (r, c) within the pattern, update the pixel at coordinates (target_row + r, target_col + c) in the output grid with the color of the pattern pixel.
7.  Return the modified output grid.
