## Perception

1.  **Input Grid Composition**: Each input grid contains a white (0) background, a single red (2) pixel, and multiple other objects composed of blue (1) or green (3) pixels. These blue and green objects often appear as horizontal or vertical lines or individual pixels.
2.  **Output Grid Composition**: The output grid retains all the original pixels from the input grid in their exact locations. Additionally, some white (0) pixels from the input grid are changed to red (2) in the output grid.
3.  **Transformation**: The core transformation is the addition of red (2) pixels. These new red pixels appear to originate from the single initial red pixel present in the input.
4.  **Fill Behavior**: The added red pixels behave like a "flood fill" or "paint bucket" tool starting from the initial red pixel.
5.  **Boundaries**: The flood fill spreads through adjacent (up, down, left, right) white (0) pixels. It stops when it encounters any non-white pixel (the original red pixel, or any blue or green pixel) or the grid boundaries.
6.  **Object Preservation**: The original blue and green objects act as barriers to the red fill and remain unchanged in the output.

## Facts


```yaml
task_elements:
  - Input Grid:
      - type: 2D array of integers (0-9)
      - properties:
          - contains a white (0) background
          - contains exactly one red (2) pixel (the seed pixel)
          - contains one or more objects made of blue (1) or green (3) pixels (barrier objects)
  - Output Grid:
      - type: 2D array of integers (0-9)
      - properties:
          - same dimensions as the input grid
          - preserves all non-white pixels from the input grid
          - contains additional red (2) pixels replacing some white (0) pixels from the input
objects:
  - name: Seed Pixel
    color: Red (2)
    quantity: 1 per input grid
    role: Starting point for the fill operation
  - name: Barrier Objects
    color: Blue (1) or Green (3)
    quantity: Variable (one or more) per input grid
    role: Boundaries that limit the fill operation
  - name: Background Pixel
    color: White (0)
    role: Can be filled with red if reachable from the seed pixel without crossing barriers
relationships:
  - The fill operation starts at the Seed Pixel.
  - The fill spreads only into adjacent (up, down, left, right) Background Pixels.
  - Barrier Objects and the grid boundaries block the spread of the fill.
actions:
  - Identify the location of the single red (2) Seed Pixel.
  - Identify the locations of all Barrier Objects (pixels with color 1 or 3).
  - Perform a flood fill operation:
      - Start at the Seed Pixel's location.
      - Use the color red (2) for filling.
      - Only fill white (0) pixels.
      - Do not fill beyond the grid boundaries or into Barrier Object pixels.
  - Combine the results: The output grid contains the original Barrier Objects, the original Seed Pixel, and the newly filled red (2) pixels.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Find the coordinates (row, column) of the single red (2) pixel in the input grid. This is the starting seed location.
3.  Create a queue or stack for processing pixels to be filled, initially containing only the seed location.
4.  Create a set or boolean grid to keep track of visited locations to avoid redundant processing, marking the seed location as visited.
5.  While the processing queue/stack is not empty:
    a.  Dequeue or pop a location (current\_row, current\_col).
    b.  For each neighbor (neighbor\_row, neighbor\_col) of the current location (considering up, down, left, right neighbors):
        i.  Check if the neighbor location is within the grid boundaries.
        ii. Check if the neighbor location has not been visited yet.
        iii. Check if the pixel at the neighbor location in the *input* grid is white (0).
        iv. If all checks (i, ii, iii) are true:
            1.  Change the color of the pixel at (neighbor\_row, neighbor\_col) in the *output* grid to red (2).
            2.  Mark the neighbor location as visited.
            3.  Enqueue or push the neighbor location onto the processing queue/stack.
6.  Return the modified output grid.