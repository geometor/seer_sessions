
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 0 0 0 4 0 0 0 0 0
0 0 0 0 0 0 2 0 4 4 0 4 0 0 0 0
0 0 0 0 0 0 2 4 4 4 4 0 0 0 0 0
0 0 0 0 0 0 2 4 4 0 0 0 0 0 0 0
0 0 0 0 5 0 2 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 2 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 2 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 2 0 0 0 0 0 0 0 0 0 0
4 4 4 0 4 2 0 0 0 7 0 0 0 0 0 0
0 4 4 4 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 0 2 0 0 0 4 0 0 0 0 0
0 5 0 5 5 0 2 0 4 4 0 4 0 0 0 0
0 0 5 5 5 5 2 4 4 4 4 0 0 0 0 0
0 0 0 0 5 5 2 4 4 0 0 0 0 0 0 0
0 0 0 5 5 5 2 4 4 4 0 0 0 0 0 0
0 0 0 0 0 5 2 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 2 7 0 0 0 0 0 0 0 0 0
0 0 4 4 4 2 7 7 7 0 0 0 0 0 0 0
4 4 4 0 4 2 7 0 7 7 7 0 0 0 0 0
0 4 4 4 0 2 0 7 7 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 2 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 2 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 2 0 0 8 0 0 0 0 0 0
0 0 0 4 4 4 2 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 2 0 0 0 0
0 0 0 0 0 0 0 0 0 4 0 2 0 3 0 0
0 0 0 0 0 0 0 4 4 0 4 2 0 0 0 0
0 0 0 0 0 0 0 0 4 4 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 2 8 0 0 0 0 0 0 0 0
0 0 0 4 4 4 2 8 8 8 0 0 0 0 0 0
0 0 0 4 4 4 2 8 8 8 0 0 0 0 0 0
0 0 0 4 4 4 2 8 8 8 0 0 0 0 0 0
0 0 0 0 4 4 2 8 8 0 0 0 0 0 0 0
0 0 0 0 0 4 2 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 2 3 0 0 0
0 0 0 0 0 0 0 0 0 4 0 2 0 3 0 0
0 0 0 0 0 0 0 4 4 0 4 2 3 0 3 3
0 0 0 0 0 0 0 0 4 4 0 2 0 3 3 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's break down this task.

## Perception

1.  **Input/Output Structure:** Both input and output are grids of colored pixels. The output grid seems to be a modification of the input grid, preserving some elements and adding new ones.
2.  **Key Colors:** Red (2) and Yellow (4) appear consistently in structural roles in the input. White (0) is the background. Other colors like Gray (5), Orange (7), Azure (8), Green (3) appear as single pixels in the input and then form larger shapes in the output.
3.  **Repeating Patterns:** In both examples, there are distinct structures composed of a vertical red line adjacent to a yellow shape. There are typically two such structures in each grid.
4.  **Transformation:** The core transformation seems to involve reflection. The yellow shapes appear to be reflected across the adjacent red vertical lines.
5.  **Reflection Color:** The color used for the reflection is not yellow. Instead, it seems determined by another, initially isolated, colored pixel present elsewhere in the input grid near the red/yellow structure. In `train_1`, a gray pixel (5) leads to a gray reflection, and an orange pixel (7) leads to an orange reflection. In `train_2`, an azure pixel (8) leads to an azure reflection, and a green pixel (3) leads to a green reflection.
6.  **Reflection Mechanism:** The reflection fills the area on the opposite side of the red line from the yellow shape. The reflected shape mirrors the yellow shape. The reflection only colors pixels that were originally white (0) in the input. Original red lines, yellow shapes, and the source color pixels seem preserved in their original positions (though the source pixel might become part of the larger reflected shape if the reflection overlaps its position).
7.  **Association:** There seems to be a spatial association between each red/yellow structure and one unique "source color" pixel (non-white, non-red, non-yellow). The closest source color pixel to a structure likely dictates the color of that structure's reflection.

## Facts


```yaml
elements:
  - object: grid
    description: A 2D array of pixels with integer values 0-9 representing colors.
  - object: background
    color: white (0)
    description: The default color filling most of the grid.
  - object: axis
    color: red (2)
    description: Contiguous vertical lines of red pixels. Act as axes of reflection.
    properties: [vertical, contiguous]
  - object: shape
    color: yellow (4)
    description: Contiguous shapes made of yellow pixels, always adjacent to a red axis.
    properties: [contiguous, adjacent_to_axis]
  - object: source_color_pixel
    color: any color except white(0), red(2), yellow(4) (e.g., gray(5), orange(7), azure(8), green(3))
    description: A single pixel whose color determines the reflection color for a nearby axis/shape structure.
    properties: [isolated initially, spatially associated with an axis/shape structure]
  - object: reflection
    color: determined by source_color_pixel
    description: A new shape created in the output grid by reflecting a yellow shape across a red axis.
    properties: [mirrors_yellow_shape, fills_background_only]

relationships:
  - type: adjacency
    subject: shape (yellow)
    object: axis (red)
    description: Yellow shapes are horizontally adjacent to red axes.
  - type: reflection
    subject: shape (yellow)
    across: axis (red)
    result: reflection (colored shape)
    description: Yellow shapes are reflected across the adjacent red axis.
  - type: color determination
    subject: source_color_pixel
    object: reflection
    description: The color of the source_color_pixel determines the color of the reflection associated with the nearby axis/shape structure. The closest source_color_pixel dictates the color.
  - type: spatial association
    subject: source_color_pixel
    object: structure (composed of axis and shape)
    description: Each source_color_pixel is associated with one axis/shape structure, typically based on proximity.

actions:
  - action: identify
    target: red axes, yellow shapes, source_color_pixels
  - action: associate
    subject: source_color_pixel
    object: axis/shape structure
    based_on: proximity (closest distance)
  - action: reflect
    target: yellow shape
    across: associated red axis
    color: determined by associated source_color_pixel
  - action: fill
    target: background pixels (white 0)
    location: within the reflected area
    color: reflection color
  - action: preserve
    target: original red axes, yellow shapes, source_color_pixels

constraints:
  - The reflection only fills pixels that were originally white (0). It does not overwrite existing non-white pixels.
  - Each red axis / yellow shape structure pair has one associated source color.
```


## Natural Language Program

1.  **Copy Input:** Create the output grid as an identical copy of the input grid.
2.  **Identify Structures:**
    *   Find all vertical contiguous segments of red (2) pixels. These are the reflection axes.
    *   Find all pixels of colors other than white (0), red (2), or yellow (4). These are the potential source color pixels.
3.  **Process Each Axis:** For each identified red axis:
    a.  **Find Adjacent Yellow Shape:** Identify all yellow (4) pixels that are horizontally adjacent to this red axis.
    b.  **Determine Reflection Side:** Note whether the yellow shape is to the left or right of the red axis. The reflection will occur on the opposite side.
    c.  **Find Source Color:** Determine the specific source color pixel associated with this axis and its adjacent yellow shape. This is done by finding the source color pixel (identified in step 2) that is closest (using Manhattan distance) to any part of the combined red axis and yellow shape. Record the color of this closest source pixel.
    d.  **Perform Reflection:** For each yellow pixel adjacent to the current red axis:
        i.  Calculate the coordinates where this yellow pixel would land if reflected across the red axis.
        ii. Check if these reflected coordinates are within the grid boundaries.
        iii. If the coordinates are valid and the pixel at these coordinates in the *original input grid* is white (0), change the color of the pixel at these coordinates in the *output grid* to the source color found in step 3c.
4.  **Final Output:** The modified output grid is the result.
