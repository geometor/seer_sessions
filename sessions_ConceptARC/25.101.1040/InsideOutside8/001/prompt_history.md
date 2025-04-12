
## train_1

**input:**
```
0 0 0 0 0 3 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 3 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 0 0 4 3
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 0 0 0 0 0 3 0 4 0
0 0 4 0 0 0 0 0 0 0 4 0
0 0 4 4 4 4 4 4 4 4 4 0
3 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0
6 0 0 0 0 0 0 0 0 0 6
0 6 0 0 8 0 0 0 0 6 0
0 0 6 0 0 8 0 0 6 0 0
0 0 0 6 0 0 0 6 0 0 0
0 0 0 0 6 0 6 0 0 0 0
0 0 0 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 8 0 0 0
0 0 0 8 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```

## Perception

The task involves selectively keeping certain pixels based on their color, position, and the colors of their neighbors, while removing others. Each example features a background color (white, 0) and at least two other colors. One non-background color appears more frequently ('deleter' color, D) and another appears less frequently ('target' color, T).

The transformation rule appears to be:
1.  Identify the most frequent non-background color (D) and the second most frequent non-background color (T).
2.  Remove all pixels of color D.
3.  Remove all pixels of color T that are located on the border of the grid.
4.  Remove all pixels of color T that are located in the interior of the grid but have two or more neighbors (including diagonals) of color D.
5.  Keep only the pixels of color T that are located in the interior of the grid AND have either zero or one neighbor of color D.
6.  All other pixels become the background color (white, 0).

**Example 1:**
*   Background: 0 (white)
*   Colors: 3 (green, count=6), 4 (yellow, count=36)
*   Deleter (D): 4 (yellow)
*   Target (T): 3 (green)
*   Green pixels at (0,5), (0,8), (7,11), (12,0) are on the border -> removed.
*   Green pixel at (4,4) is interior, has 0 yellow neighbors -> kept.
*   Green pixel at (9,8) is interior, has 0 yellow neighbors -> kept.
*   Result: Only greens at (4,4) and (9,8) remain.

**Example 2:**
*   Background: 0 (white)
*   Colors: 8 (azure, count=5), 6 (magenta, count=11)
*   Deleter (D): 6 (magenta)
*   Target (T): 8 (azure)
*   Azure pixel at (0,1) is on the border -> removed.
*   Azure pixel at (10,3) is on the border -> removed.
*   Azure pixel at (1,8) is interior, has 3 magenta neighbors -> removed.
*   Azure pixel at (3,4) is interior, has 0 magenta neighbors -> kept.
*   Azure pixel at (4,5) is interior, has 1 magenta neighbor (at 5,6) -> kept.
*   Azure pixel at (9,7) is interior, has 3 magenta neighbors -> removed.
*   Result: Only azures at (3,4) and (4,5) remain.

The perception matches the outputs for both examples.

## Facts


```yaml
background_color: 0 # white

objects:
  - type: grid
    properties:
      height: variable
      width: variable
  - type: pixel
    properties:
      color: integer (0-9)
      position: (row, column)
      is_border_pixel: boolean
      neighbors: list of 8 neighboring pixels (or fewer for edge/corner pixels)
  - type: color_group
    properties:
      color: integer (0-9)
      pixel_locations: list of (row, column)
      count: integer
      frequency_rank: integer (among non-background colors)

roles:
  - deleter_color (D): The non-background color with the highest frequency.
  - target_color (T): The non-background color with the second highest frequency.

relationships:
  - adjacency: 8-way connectivity (including diagonals) between pixels.
  - border_status: A pixel is on the border if its row or column index is 0 or the maximum index for the grid.
  - neighbor_color_count: For a target pixel, the count of its neighbors that have the deleter color.

actions:
  - count_colors: Determine the frequency of each non-background color.
  - identify_roles: Assign D and T based on frequency counts.
  - filter_pixels:
      - Iterate through each pixel of the target color (T).
      - Check if the pixel is on the border.
      - Check the number of neighbors with the deleter color (D).
      - Keep the pixel (copy to output grid) only if it is NOT on the border AND has 0 or 1 D-colored neighbors.
  - generate_output: Create a new grid of the same size, initially filled with the background color, and place the kept T pixels.
```


## Natural Language Program

1.  Initialize the output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
2.  Analyze the input grid to count the occurrences of each non-background color.
3.  Identify the 'deleter' color (D) as the non-background color with the highest count.
4.  Identify the 'target' color (T) as the non-background color with the second-highest count.
5.  Iterate through each pixel of the input grid at position `(row, col)`.
6.  If the color of the pixel `input[row, col]` is the 'target' color (T):
    a.  Determine if the pixel is located on the border (i.e., `row == 0`, `col == 0`, `row == height - 1`, or `col == width - 1`).
    b.  If the pixel is *not* on the border:
        i.  Count how many of its 8 neighbors (N, NE, E, SE, S, SW, W, NW) have the 'deleter' color (D).
        ii. If this count is 0 or 1, set the corresponding pixel in the output grid `output[row, col]` to the 'target' color (T).
7.  Return the final output grid.
