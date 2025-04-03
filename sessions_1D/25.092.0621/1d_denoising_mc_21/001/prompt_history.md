
## train_1

**input:**
```
0 0 0 5 5 5 5 5 5 5 5 5 3 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 1 2 9 2 2 2 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0
```


## train_3

**input:**
```
4 4 4 4 4 4 4 4 6 2 4 4 4 4 4 4 6 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0
```

**Perception**

The input and output grids are always single rows (1xN). The inputs contain a contiguous horizontal segment of a dominant non-white color. Within this segment, there might be one or more pixels of different colors (outliers). The surrounding pixels are white (color 0). The transformation identifies the dominant color within the non-white segment and replaces all outlier pixels within that segment with the dominant color. The white pixels remain unchanged.

**Facts**


```yaml
task_type: single_row_transformation
elements:
  - type: grid
    properties:
      dimensionality: 1D (single row)
      height: 1
      width: variable (e.g., 32 in examples)
  - type: segment
    description: A contiguous sequence of non-white pixels.
    properties:
      dominant_color: The most frequent color within the non-white segment.
      location: Between potential leading/trailing white pixels.
  - type: pixel
    properties:
      color: An integer from 0-9.
      position: Index within the row.
  - type: outlier_pixel
    description: A pixel within the non-white segment whose color is different from the dominant color.
actions:
  - identify_dominant_color: Find the most frequent non-white color in the row.
  - replace_outliers: Change the color of outlier pixels within the non-white segment to the dominant color.
relationships:
  - outlier_pixels belong to the non-white segment.
  - the dominant_color is determined by the pixels within the non-white segment.
invariance:
  - White pixels (color 0) remain unchanged.
  - Pixels matching the dominant color within the non-white segment remain unchanged.
  - The grid dimensions remain unchanged.
```


**Natural Language Program**

1.  Examine the input grid (a single row).
2.  Identify the contiguous segment of non-white pixels.
3.  Determine the dominant color within this non-white segment (the color that appears most frequently).
4.  Create the output grid by copying the input grid.
5.  Iterate through each pixel within the identified non-white segment in the output grid.
6.  If a pixel's color is *not* the dominant color, change its color to the dominant color.
7.  Leave all white pixels and pixels already matching the dominant color unchanged.
8.  The resulting grid is the final output.
