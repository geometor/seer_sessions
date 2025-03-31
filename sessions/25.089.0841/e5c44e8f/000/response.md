**Perception:**

The task involves three primary colors: white (0), red (2), and green (3). The input grid contains scattered red pixels and one or more green pixels. The red pixels act as static barriers. The green pixel(s) act as starting points for a spreading or filling process. The transformation involves filling white areas of the grid with green, starting from the initial green pixel(s). This fill process propagates to adjacent (up, down, left, right) white cells but is blocked by red cells and the grid boundaries. The original red and green pixels remain unchanged in the output grid. Essentially, it's a flood fill algorithm originating from green pixels, constrained by red pixels.

**Facts:**


```yaml
objects:
  - type: grid
    properties:
      - pixels: represent colors (white=0, red=2, green=3)
      - size: variable height and width
  - type: pixel
    properties:
      - color: white(0), red(2), or green(3)
      - location: (row, column) coordinates
      - role: 
        - white(0): background/fillable space
        - red(2): static barrier/obstacle
        - green(3): starting point for fill / fill color
relationships:
  - type: adjacency
    description: Pixels can be adjacent horizontally or vertically (4-connectivity).
  - type: containment
    description: Red pixels and grid boundaries contain the spread of green pixels.
actions:
  - name: identify_start_points
    input: input grid
    output: list of coordinates of green(3) pixels
  - name: identify_barriers
    input: input grid
    output: list of coordinates of red(2) pixels
  - name: flood_fill
    parameters:
      - start_points: coordinates from identify_start_points
      - barriers: coordinates from identify_barriers + grid boundaries
      - fill_color: green(3)
      - target_color: white(0)
    process: Starting from the start_points, change adjacent white(0) pixels to green(3). Continue this process iteratively for newly colored green pixels. Do not change or cross barrier pixels or grid boundaries.
  - name: preserve_original
    input: input grid, output grid after fill
    process: Ensure original red(2) and green(3) pixels from the input grid retain their color and position in the output grid. (Note: The flood fill naturally handles this if implemented correctly, starting *from* green and stopping *at* red).
transformation:
  - step: Copy the input grid to create the initial output grid.
  - step: Identify the locations of all green (3) pixels in the input grid. These are the starting points for the fill.
  - step: Identify the locations of all red (2) pixels. These, along with the grid boundaries, act as barriers.
  - step: Perform a flood fill operation:
      - Initialize a queue or stack with the starting green pixel locations.
      - Maintain a set of visited locations to avoid redundant processing (initially containing the starting locations).
      - While the queue/stack is not empty:
          - Dequeue/pop a location (r, c).
          - For each of its 4-directionally adjacent neighbors (nr, nc):
              - Check if the neighbor is within the grid boundaries.
              - Check if the neighbor has not been visited.
              - Check if the neighbor pixel in the *input* grid is white (0).
              - If all conditions are met:
                  - Change the color of the pixel at (nr, nc) in the *output* grid to green (3).
                  - Mark (nr, nc) as visited.
                  - Enqueue/push (nr, nc).
  - step: The resulting grid after the flood fill is the final output.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Find all pixels in the input grid that are green (color 3). These are the starting points for the fill.
3.  Create a list of locations to process, initially containing all starting points. Create a set to keep track of locations already processed, also initialized with the starting points.
4.  While there are locations left to process:
    a.  Take one location (row, column) from the list.
    b.  Examine its four neighbors (up, down, left, right).
    c.  For each neighbor:
        i.  Check if the neighbor is inside the grid boundaries.
        ii. Check if the neighbor location has already been processed.
        iii. Check if the neighbor pixel in the *original input grid* was white (color 0).
        iv. If the neighbor is within bounds, hasn't been processed, and was originally white, then:
            1. Change the color of this neighbor pixel in the *output grid* to green (color 3).
            2. Add the neighbor's location to the list of locations to process.
            3. Mark the neighbor's location as processed.
5.  Once there are no more locations to process, the output grid is complete. Return the final output grid.