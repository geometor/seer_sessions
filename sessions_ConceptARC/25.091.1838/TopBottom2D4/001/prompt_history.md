
## train_1

**input:**
```
0 0 0 3 3 3 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 7 7 7 0 0 0 0
0 0 0 7 7 7 0 0 0 0
0 0 0 7 7 7 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 1 1 0 0 0 0 0
0 0 7 7 7 7 7 7 7 7 0 0
0 0 7 7 7 7 7 7 7 7 0 0
0 0 7 7 7 7 7 7 7 7 0 0
0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 6 6 6 6 6 6 0 0 0
0 0 0 6 6 6 6 6 6 0 0 0
0 0 0 6 6 6 6 6 6 0 0 0
0 0 0 6 6 6 6 6 6 0 0 0
0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0
0 0 0 0 0 3 3 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 7 7 0 0
0 0 7 7 7 7 7 7 7 7 0 0
0 0 7 7 7 7 7 7 7 7 0 0
0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 6 6 6 6 6 6 0 0 0
0 0 0 6 6 6 6 6 6 0 0 0
0 0 0 6 6 6 6 6 6 0 0 0
0 0 0 6 6 6 6 6 6 0 0 0
0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 5 5 5 5 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 2 0 0
0 0 0 2 0 0
0 0 2 2 2 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 9 9 9 0
0 9 9 9 9 9
0 9 9 9 9 9
0 0 9 9 9 0
0 0 0 0 0 0
0 0 4 4 4 0
0 0 0 4 0 0
0 0 0 4 0 0
```


**output:**
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 9 9 9 0
0 9 9 9 9 9
0 9 9 9 9 9
0 0 9 9 9 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
```

**Perception**

1.  **Input/Output Structure:** The input and output are grids of pixels represented by numbers 0-9 (colors). The output grid always has the same dimensions as the input grid.
2.  **Objects:** The non-white pixels (1-9) in the input form distinct objects, which are contiguous areas of the same color. These objects are separated by white pixels (0).
3.  **Transformation:** The transformation involves selectively removing some objects from the input grid, turning their constituent pixels white (0) in the output grid. Some objects are preserved.
4.  **Identifying Kept Objects (Examples):**
    *   **Example 1:** Input has Green (3x3, area 9), Yellow (4x3, area 12), Orange (3x3, area 9). Output keeps only Yellow. Yellow has the unique maximum area.
    *   **Example 2:** Input has Blue (2x2, area 4), Orange (3x8, area 24), Azure (2x2, area 4), Magenta (4x6, area 24), Gray (3x4, area 12), Green (2x2, area 4). Output keeps Orange, Azure, Magenta, Gray. It removes Blue and Green. Here, Orange and Magenta share the maximum area (24). The removed objects (Blue, Green) are the ones touching the top and bottom edges of the grid, respectively. The kept objects do not touch the top or bottom edges.
    *   **Example 3:** Input has Red (L-shape, area 5), Maroon (complex shape, area 15), Yellow (T-shape, area 5). Output keeps only Maroon. Maroon has the unique maximum area.
5.  **Core Logic:** The decision of which objects to keep seems to depend on two conditions: (a) whether an object has the maximum area compared to others, and (b) whether there's a tie for the maximum area. If the maximum area is unique to one object, only that object is kept. If multiple objects share the maximum area, a different rule applies: objects touching the top or bottom border are removed, and all others are kept.

**Facts**


```yaml
- task_description: Selectively remove objects from the input grid based on their area and position relative to grid borders.
- grid_properties:
    - dimensions: Input and output grids have the same height and width.
    - background_color: White (0) is the background color.
- objects:
    - definition: Contiguous areas of the same non-white color (1-9).
    - properties:
        - color: The pixel value (1-9).
        - pixels: A list of coordinates for each pixel in the object.
        - area: The count of pixels in the object.
        - bounding_box: The minimum rectangle enclosing the object.
        - touches_top_border: Boolean, true if any object pixel is in row 0.
        - touches_bottom_border: Boolean, true if any object pixel is in the last row.
- relationships:
    - max_area: The largest area among all identified objects in the input.
    - max_area_objects: The set of objects that have the maximum area.
    - count_max_area_objects: The number of objects in the `max_area_objects` set.
- actions:
    - identify_objects: Find all distinct objects and calculate their properties (area, border touching).
    - find_max_area: Determine the maximum area (`max_area`) among all objects.
    - count_max_objects: Count how many objects share this `max_area`.
    - filter_objects:
        - condition_1 (unique max area): If `count_max_area_objects` is 1, keep only the object with the `max_area`.
        - condition_2 (tied max area): If `count_max_area_objects` is greater than 1, keep all objects that do *not* touch the top border *and* do *not* touch the bottom border.
    - generate_output: Create the output grid by placing the kept objects onto a white background of the same dimensions as the input.
```


**Natural Language Program**

1.  Identify all distinct, connected groups of non-white pixels in the input grid. Each group constitutes an "object".
2.  For each object, calculate its area (the number of pixels it contains).
3.  Determine the maximum area found among all objects.
4.  Count how many objects possess this maximum area.
5.  **Decision Rule:**
    *   **If exactly one object has the maximum area:** Create the output grid containing only that single object. All other pixels in the output grid should be white (0).
    *   **If two or more objects share the maximum area:** Identify all objects from the input grid that touch the top border (row 0) OR the bottom border (the last row). Create the output grid containing all objects *except* those identified as touching the top or bottom border. Pixels belonging to the removed objects become white (0).
6.  The output grid must have the same dimensions as the input grid.
