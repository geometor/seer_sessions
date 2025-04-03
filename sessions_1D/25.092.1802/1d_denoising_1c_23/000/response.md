## Perception

The input grids contain a prominent, solid rectangular shape made of a single non-background color (green, blue, or gray in the examples). Additionally, there are smaller, scattered pixels or small groups of pixels of the *same* color elsewhere in the grid. The background is always white (0).

The transformation involves identifying the largest connected group of pixels of the non-background color. This largest group (the rectangle) is preserved in the output grid. All other pixels of that same color, which are not part of the largest connected group, are changed to the background color (white). The original background pixels remain white.

Essentially, the task isolates the main, largest object of a given color and removes any smaller, disconnected "noise" pixels of the same color.

## Facts


```yaml
background_color: 0 # white
input_features:
  - object_type: connected_component
    color: non_zero # The primary color varies (3, 1, 5)
    count: multiple_per_color
    description: Consists of one large rectangular component and several smaller, disconnected components (single pixels or small groups) of the same non-zero color.
    properties:
      - size: varying (one large, others small)
      - connectivity: 4-neighbor (assumed)
output_features:
  - object_type: connected_component
    color: non_zero # Same as the primary input color
    count: one
    description: Only the largest connected component from the input remains.
    properties:
      - size: largest among input components of that color
      - position: same as in input
      - color: same as in input
transformation:
  - action: identify_components
    target_color: non_zero
    connectivity: 4-neighbor # pixels sharing an edge are connected
  - action: find_largest_component
    criteria: pixel_count
  - action: filter_components
    rule: keep only the largest component identified
  - action: generate_output
    rule: create a new grid containing only the pixels of the largest component, setting all other pixels to the background color (0).
```


## Natural Language Program

1.  Identify the primary non-background color present in the input grid.
2.  Find all distinct connected components (groups of pixels connected edge-to-edge) of this primary color.
3.  Calculate the size (number of pixels) of each identified component.
4.  Select the component with the largest size. If there's a tie for the largest size, any one of the largest components can be chosen (though the examples suggest a unique largest component).
5.  Create a new output grid of the same dimensions as the input grid, initialized with the background color (white, 0).
6.  Copy the pixels belonging to the selected largest component from the input grid to their corresponding positions in the new output grid.