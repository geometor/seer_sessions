
## train_1

**input:**
```
0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 2 0 0 0 2 0 0 0 2 0 0 0 0 0
```


**output:**
```
0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 6 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 0 0 6 0 0 6 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 1 0 0 0 1 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception**:
    The input grids are single rows (1x35). They contain a background color ('white', 0) and one or more objects composed of a single, non-white color. In each example, there is one dominant, larger object (a contiguous horizontal line) and several smaller objects (single pixels or very short lines) of the same color, separated by the background color. The output grid retains only the largest contiguous object from the input, setting all other pixels, including those of the smaller objects, to the background color ('white'). The color of the largest object is preserved in the output.

*   **Facts**:
    
```yaml
    task: Keep the largest contiguous object of a single color
    
    input_elements:
      - type: grid
        description: A 1xN grid containing a background color (white, 0) and foreground pixels of a single non-white color.
      - type: background
        color: white (0)
      - type: objects
        description: Contiguous blocks of pixels of the same non-white color.
        properties:
          - color: Consistent within an object (e.g., red, magenta, blue).
          - size: Number of pixels in the contiguous block.
          - location: Pixel coordinates.
        relationships:
          - Objects of the same color can exist in the input grid.
          - Objects are separated by background pixels.
          - There is one object significantly larger than the others in the examples.
    
    output_elements:
      - type: grid
        description: A grid of the same dimensions as the input.
        properties:
          - Contains only the pixels of the largest input object and the background color.
      - type: retained_object
        description: The single largest object identified in the input grid.
        properties:
          - color: Same as the largest input object.
          - size: Same as the largest input object.
          - location: Same as the largest input object.
      - type: background
        description: All pixels not part of the retained object.
        color: white (0)
    
    transformation:
      - action: identify_objects
        description: Find all contiguous blocks of non-white pixels in the input grid. Treat blocks of different colors separately if they occur (though examples only show one non-white color per task).
      - action: calculate_size
        description: Determine the number of pixels in each identified object.
      - action: find_largest
        description: Identify the object with the maximum number of pixels. Assume a unique largest object based on examples.
      - action: generate_output
        description: Create a new grid of the same dimensions as the input, initialized with the background color (white, 0).
      - action: place_object
        description: Copy the pixels belonging to the largest identified object from the input grid to their corresponding positions in the new output grid.
    ```


*   **Natural Language Program**:
    1.  Identify all distinct contiguous objects composed of non-white pixels in the input grid.
    2.  For each identified object, count the number of pixels it contains (its size).
    3.  Determine the object with the largest size.
    4.  Create a new output grid of the same dimensions as the input grid, filled entirely with the background color ('white', 0).
    5.  Copy the pixels corresponding to the largest object identified in step 3 from the input grid onto the output grid, preserving their original positions and color.
