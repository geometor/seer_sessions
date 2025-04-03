
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0
```


## train_3

**input:**
```
0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0
```


**output:**
```
0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0
```

*   **Perception:** The task operates on single-row inputs. Each input contains a contiguous block of non-white pixels surrounded by white pixels. The transformation involves shifting this block of non-white pixels one position to the right. The position originally occupied by the first pixel of the block becomes white. The length of the row remains unchanged.

*   **Facts:**
    
```yaml
    task_type: transformation
    input_dimensionality: 1D (single row)
    output_dimensionality: 1D (single row)
    input_features:
      - element: pixel
        properties:
          - color: white (0), red (2), gray (5)
      - element: object
        description: A contiguous sequence of non-white pixels.
        properties:
          - color: uniform (red or gray in examples)
          - location: defined by start and end index
          - length: variable
      - element: background
        description: White pixels surrounding the object.
        properties:
          - color: white (0)
    transformation:
      - action: identify
        target: the contiguous block of non-white pixels (the object)
      - action: shift
        target: the identified object
        direction: right
        distance: 1 position
      - action: update
        target: the pixel at the original starting position of the object
        new_value: white (0)
    relationships:
      - The object is always surrounded by background pixels.
      - The output row has the same length as the input row.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous block of non-white pixels within the input row. Note its starting index, ending index, and the sequence of pixel colors within the block.
    2.  Create a new output row of the same length as the input row, initially filled with white (0) pixels.
    3.  Copy the identified sequence of non-white pixels into the output row, starting at an index one greater than the original starting index.
    4.  Ensure all other positions in the output row remain white (0).
