## Perception

1.  **Input/Output Structure:** The input is a 10x10 grid, and the output is a 3x3 grid.
2.  **Colors:** The input grids contain white (0) backgrounds, scattered objects of a primary color (yellow=4, blue=1, red=2 in the examples), and always exactly one gray (5) pixel.
3.  **Gray Pixel Role:** The single gray pixel appears to act as a selector or pointer. It is always located adjacent (horizontally, vertically, or diagonally) to at least one pixel of the primary color object.
4.  **Primary Color Object:** There might be multiple distinct objects of the primary color in the input grid. The gray pixel identifies *which* specific object is relevant.
5.  **Transformation:** The transformation involves isolating the primary color object touched by the gray pixel.
6.  **Output Content:** The output grid represents the shape of the selected primary color object. It's extracted by finding the bounding box of the selected object and then creating a grid of that size, placing the primary color pixels relative to the top-left corner of the bounding box, and filling the rest with white (0).
7.  **Output Size:** In all provided examples, the bounding box of the selected object, and therefore the output grid, is 3x3.

## Facts


```yaml
task_type: object_selection_and_extraction

input_grid:
  size: 10x10
  background_color: white (0)
  elements:
    - type: scattered_pixels
      color: gray (5)
      quantity: 1
      role: selector
    - type: objects
      color: variable (e.g., yellow, blue, red) - referred to as 'primary_color'
      quantity: multiple possible
      properties:
        - composed of contiguous pixels of the primary_color
        - at least one object is adjacent (including diagonals) to the gray pixel

output_grid:
  size: 3x3 (in examples, generally matches the bounding box size of the selected object)
  background_color: white (0)
  content: shape of the selected primary_color object

relationships:
  - the gray pixel selects one specific primary_color object through adjacency.
  - the output grid's content is derived solely from the selected primary_color object.
  - the output grid represents the relative shape of the selected object within its bounding box.

actions:
  - identify: locate the single gray pixel.
  - identify: determine the primary_color (non-white, non-gray).
  - find: identify the primary_color object adjacent to the gray pixel.
  - calculate: determine the bounding box of the selected object.
  - extract: create a new grid based on the bounding box dimensions.
  - map: transfer the pixels of the selected object to the new grid, relative to the bounding box's top-left corner, maintaining the primary_color.
  - fill: set all other pixels in the new grid to white (0).
```


## Natural Language Program

1.  Scan the input grid to find the coordinates of the single gray pixel (color 5).
2.  Determine the "primary color" by finding a pixel color that is not white (0) and not gray (5). Assume there is only one such color in the input grid.
3.  Identify all pixels belonging to the primary color object that are adjacent (horizontally, vertically, or diagonally) to the gray pixel. Use these pixels as starting points to find the complete contiguous object made of the primary color (the "selected object").
4.  Calculate the minimum bounding box (top-left and bottom-right coordinates) that encloses the selected object.
5.  Determine the height and width of the bounding box.
6.  Create a new output grid with the calculated height and width, initially filled with white (0).
7.  For each pixel belonging to the selected object in the input grid:
    a.  Calculate its position relative to the top-left corner of the bounding box (relative\_row = pixel\_row - top\_row, relative\_col = pixel\_col - left\_col).
    b.  Set the pixel at (relative\_row, relative\_col) in the output grid to the primary color.
8.  Return the generated output grid.