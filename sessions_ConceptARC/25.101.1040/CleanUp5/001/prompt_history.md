
## train_1

**input:**
```
0 0 0 0 0 2 0 0 0 0 0 3 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0 0 0 0 2 0 2 0 0 0 0
0 3 0 2 0 0 0 2 0 3 0 0 0 2 0 0 0 2 0 0 3
0 0 2 0 0 0 0 0 2 0 0 0 3 0 0 0 0 0 3 0 0
0 2 0 3 0 0 0 0 0 2 0 2 0 0 0 3 0 0 0 2 0
2 0 0 0 0 0 3 0 0 0 2 0 0 0 0 0 0 0 0 0 2
```


**output:**
```
0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0 0 0 0 2 0 2 0 0 0 0
0 0 0 2 0 0 0 2 0 0 0 0 0 2 0 0 0 2 0 0 0
0 0 2 0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 2 0 0
0 2 0 0 0 0 0 0 0 2 0 2 0 0 0 0 0 0 0 2 0
2 0 0 0 0 0 0 0 0 0 2 0 0 0 0 0 0 0 0 0 2
```


## train_2

**input:**
```
4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 4
0 0 0 0 0 0 4 0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0
0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4
4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 4 0 0 4 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0
0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0
0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4 0 4 0 0 0 4
4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0 4 0 0 0 0 0
```

## Perception

The task involves transforming an input grid into an output grid by selectively removing certain colored pixels (changing them to white/0). The rule for removal depends on the number of distinct non-white colors present in the input grid.

1.  **Case 1: Multiple non-white colors present (Example: train_1)**
    *   Input `train_1` contains red (2) and green (3) pixels.
    *   Output `train_1` contains only red (2) pixels.
    *   Observation: All pixels of the color with the highest numerical value (green=3) are removed (changed to white). The other non-white color (red=2) remains unchanged.

2.  **Case 2: Single non-white color present (Example: train_2)**
    *   Input `train_2` contains only yellow (4) pixels.
    *   Output `train_2` contains fewer yellow (4) pixels. Some specific yellow pixels have been removed.
    *   Observation: The removal seems related to the structure of the connected components formed by the single non-white color.
        *   Pixels forming components of size 1 (isolated single pixels) are removed.
        *   Pixels that are the starting points (leftmost for horizontal, presumably topmost for vertical) of small, simple line-shaped components (like size 2 horizontal segments) are also removed.
        *   Pixels within larger, more complex components are kept.

## YAML Facts


```yaml
task_type: color_removal_conditional
grid_properties:
  preserves_size: true
  background_color: 0 # white

input_features:
  - name: pixel_colors
    description: The grid contains pixels of various colors (0-9).
    values:
      - example_1: [0, 2, 3] # white, red, green
      - example_2: [0, 4] # white, yellow
  - name: color_count
    description: Number of distinct non-white colors in the input grid.
    values:
      - example_1: 2
      - example_2: 1
  - name: max_color_value
    description: The maximum numerical value among non-white colors present.
    values:
      - example_1: 3 # green
      - example_2: 4 # yellow
  - name: connected_components
    description: Non-white pixels of the same color form connected components (using 8-way adjacency).
    properties: [size, shape, pixels]
    relevant_when: color_count == 1
    observations:
      - example_2:
          components:
            - size: 1 # e.g., (0,0), (0,23), (1,6)
            - size: 2
              shape: horizontal_line # e.g., {(0,18), (0,19)}, {(1,13), (1,14)}
            - size: 24
              shape: complex

actions:
  - name: remove_pixel
    description: Change a pixel's color to the background color (0).
    conditions:
      - if: color_count > 1
        target: pixels where color == max_color_value
      - if: color_count == 1
        target: pixels belonging to components satisfying specific criteria (size 1, or start of small simple line)

transformation_logic:
  - condition: color_count > 1
    action: Remove all pixels whose color matches the maximum non-white color value in the input.
  - condition: color_count == 1
    action:
      - Find all connected components (8-way adjacency) of the single non-white color.
      - Remove pixels in components of size 1.
      - For components forming horizontal line segments of size > 1, remove the leftmost pixel.
      - (Hypothesized) For components forming vertical line segments of size > 1, remove the topmost pixel.
      - Keep all other pixels.

output_features:
  - name: pixel_colors
    description: The output grid contains a subset of the input's non-white pixels, or potentially none if all were removed.
    values:
      - example_1: [0, 2]
      - example_2: [0, 4]

```


## Natural Language Program

1.  **Analyze Input Colors**: Identify all distinct non-white colors present in the input grid and count how many distinct non-white colors there are (let this count be `N`).
2.  **Check Color Count**:
    *   **If `N` is greater than 1**:
        *   Find the non-white color with the highest numerical value.
        *   Create the output grid by copying the input grid.
        *   Change all pixels matching this highest color value to white (0) in the output grid.
    *   **If `N` is equal to 1**:
        *   Let the single non-white color be `C`.
        *   Create the output grid by copying the input grid.
        *   Find all connected components of color `C` using 8-way adjacency (pixels are connected if they touch sides or corners). Keep track of the pixels belonging to each component and the size (number of pixels) of each component.
        *   **Identify Pixels to Remove**:
            *   Initialize an empty set of pixels to remove.
            *   Iterate through all found components:
                *   If a component's size is 1, add its single pixel to the set of pixels to remove.
                *   If a component consists of exactly two pixels arranged horizontally (e.g., `(r, c)` and `(r, c+1)`), add the leftmost pixel `(r, c)` to the set of pixels to remove.
                *   (Hypothesized Extension) If a component consists of exactly two pixels arranged vertically (e.g., `(r, c)` and `(r+1, c)`), add the topmost pixel `(r, c)` to the set of pixels to remove. *(Note: This case wasn't explicitly tested in the examples but follows the pattern)*.
                *   (Refinement) Consider extending the horizontal/vertical line check for sizes greater than 2, still removing only the leftmost/topmost pixel.
        *   **Apply Removal**: Iterate through the set of pixels identified for removal. For each pixel coordinate in the set, change the corresponding pixel in the output grid to white (0).
3.  **Return Output**: The modified grid is the result.
