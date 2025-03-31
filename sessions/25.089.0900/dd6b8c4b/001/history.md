
## train_1

**input:**
```
7 7 7 7 7 7 7 7 7 7 7
7 6 6 6 6 6 6 6 9 9 7
7 6 9 9 7 7 7 6 9 9 7
7 6 6 6 6 6 6 6 7 7 7
7 7 7 6 3 3 3 6 7 7 7
7 7 7 6 3 2 3 6 7 9 7
7 9 7 6 3 3 3 6 7 7 7
9 9 7 6 6 7 6 6 6 6 7
7 7 7 6 7 7 7 9 9 6 7
7 7 7 6 6 6 6 6 6 6 7
7 7 7 7 7 7 7 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 7
7 6 6 6 6 6 6 6 9 9 7
7 6 9 9 7 7 7 6 9 9 7
7 6 6 6 6 6 6 6 7 7 7
7 7 7 6 9 9 3 6 7 7 7
7 7 7 6 3 2 3 6 7 9 7
7 9 7 6 3 3 3 6 7 7 7
9 9 7 6 6 7 6 6 6 6 7
7 7 7 6 7 7 7 7 7 6 7
7 7 7 6 6 6 6 6 6 6 7
7 7 7 7 7 7 7 7 7 7 7
```


## train_2

**input:**
```
7 7 7 7 7 7 9 9 9 7 7
7 7 7 7 7 7 9 9 7 7 9
7 7 7 7 7 7 7 7 7 7 9
9 7 7 6 6 6 6 6 6 6 6
7 7 7 6 3 3 3 6 9 7 7
7 7 9 6 3 2 3 6 7 7 7
7 7 7 6 3 3 3 6 7 9 7
7 7 7 6 7 7 7 6 7 7 7
7 9 7 6 7 9 7 6 7 7 7
7 7 9 6 7 9 7 6 7 7 7
7 7 7 7 7 7 7 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 9 9 9 7 7
7 7 7 7 7 7 7 9 7 7 9
7 7 7 7 7 7 7 7 7 7 9
7 7 7 6 6 6 6 6 6 6 6
7 7 7 6 9 9 9 6 7 7 7
7 7 7 6 9 9 9 6 7 7 7
7 7 7 6 9 9 9 6 7 7 7
7 7 7 6 7 7 7 6 7 7 7
7 7 7 6 7 7 7 6 7 7 7
7 7 7 6 7 7 7 6 7 7 7
7 7 7 7 7 7 7 7 7 7 7
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 9 7
7 7 9 7 7 7 7 7 7 7 9
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 3 3 3 7 7 7 7
7 7 7 7 3 2 3 7 7 7 7
7 7 7 7 3 3 3 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 9 7 7
7 7 7 7 7 7 7 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 9 9 9 7 7 7 7
7 7 7 7 9 2 3 7 7 7 7
7 7 7 7 3 3 3 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
```

Okay, let's analyze the task examples.

**Perception of Elements:**

1.  **Grid Structure:** All examples use 11x11 grids.
2.  **Colors:** The primary colors involved are orange (7, background), green (3), red (2), magenta (6), and maroon (9).
3.  **Central Object:** In each input grid, there is a distinct object composed of green (3) pixels surrounding a single red (2) pixel. In these examples, it's always a 3x3 square with the red pixel at the center.
4.  **Border:** This central green/red object is either immediately surrounded by magenta (6) pixels (train_1, train_2) or orange (7) pixels (train_3).
5.  **Scattered Pixels:** Maroon (9) pixels appear scattered in the grid, sometimes near the magenta border (train_2), sometimes further away (train_1, train_3). Magenta (6) pixels also form other shapes or paths when they are not acting as the border.
6.  **Transformation Focus:** The core change occurs within the central green/red object. Specifically, some or all of the green (3) pixels change to maroon (9), while the red (2) pixel remains unchanged. Other pixels in the grid (background, magenta paths, scattered maroon) generally remain unchanged.
7.  **Conditional Change:** The way the green pixels change seems conditional. In train_1 and train_3, only the green pixels above the red pixel or in the same row but to the left of the red pixel change to maroon. In train_2, *all* green pixels in the object change to maroon.
8.  **Trigger Condition:** The difference between train_1/train_3 and train_2 appears linked to the environment around the central object. Both train_1 and train_2 have a magenta border, but train_2 also has maroon pixels adjacent to this magenta border. Train_3 has an orange border. This suggests the rule changes based on (a) the border color and (b) the proximity of maroon pixels to that border if it's magenta.

**YAML Fact Documentation:**


```yaml
elements:
  - object: grid
    properties:
      size: 11x11 (constant in examples)
      background_color: orange (7)

  - object: core_object
    description: A structure composed of green and red pixels.
    properties:
      - color_composition: [green (3), red (2)]
      - structure: In examples, a 3x3 square with a central red pixel.
      - connectivity: The green and red pixels form a single connected component.
      - unique_red_pixel: Contains exactly one red (2) pixel.
    location: Centered variably within the grid.

  - object: border
    description: Pixels immediately adjacent to the core_object (excluding pixels within the core_object).
    properties:
      - color: Can be uniformly magenta (6) or orange (7) in examples.
      - relationship: Adjacent to the green pixels of the core_object.

  - object: maroon_pixels
    description: Scattered individual or groups of maroon (9) pixels.
    properties:
      - color: maroon (9)
      - location: Variable throughout the grid.
      - relationship: Can be adjacent to the 'border' object (specifically when the border is magenta).

actions:
  - identify: Locate the unique red (2) pixel.
  - identify: Locate the connected green (3) pixels associated with the red pixel (the core_object).
  - determine: Find the pixels forming the border around the core_object.
  - check_property: Determine the color(s) of the border pixels.
  - check_adjacency: Determine if any maroon (9) pixels are adjacent to magenta (6) border pixels.
  - transform: Change the color of specific green (3) pixels within the core_object to maroon (9) based on conditions.

conditions_and_rules:
  - condition: Check if all border pixels are magenta (6).
    - if_true:
      - condition: Check if any maroon (9) pixel is adjacent to any magenta (6) border pixel.
        - if_true: Apply Rule B (change all green pixels in core_object to maroon).
        - if_false: Apply Rule A (change green pixels above or left-of-same-row relative to the red pixel to maroon).
    - if_false: (e.g., border is orange)
      - Apply Rule A (change green pixels above or left-of-same-row relative to the red pixel to maroon).

```


**Natural Language Program:**

1.  **Find the Target:** Locate the unique red (2) pixel in the input grid. If no red pixel exists, the output is identical to the input. Let its coordinates be (row\_red, col\_red).
2.  **Identify the Object:** Identify the connected component of green (3) pixels that are adjacent (including diagonally) to the red (2) pixel. This group of green pixels, along with the red pixel, forms the 'core object'.
3.  **Examine the Border:** Identify all pixels that are adjacent (including diagonally) to any green pixel in the core object but are not part of the core object itself. These form the 'border pixels'.
4.  **Check Border Color:** Determine if *all* border pixels have the color magenta (6).
5.  **Apply Transformation Rule based on Border:**
    *   **If all border pixels are magenta (6):**
        *   Check if there exists any maroon (9) pixel anywhere in the grid that is adjacent (including diagonally) to *any* of the magenta (6) border pixels identified in step 3.
        *   If such an adjacent maroon pixel exists, change *all* green (3) pixels belonging to the core object (identified in step 2) to maroon (9).
        *   If no such adjacent maroon pixel exists, change only those green (3) pixels in the core object located at (row\_green, col\_green) where `row_green < row_red` OR (`row_green == row_red` AND `col_green < col_red`) to maroon (9).
    *   **If not all border pixels are magenta (6) (e.g., if the border contains orange (7) or other colors):**
        *   Change only those green (3) pixels in the core object located at (row\_green, col\_green) where `row_green < row_red` OR (`row_green == row_red` AND `col_green < col_red`) to maroon (9).
6.  **Output:** Keep the red (2) pixel and all other pixels outside the core object unchanged. The final grid is the result of these transformations.
