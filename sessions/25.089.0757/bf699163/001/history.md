
## train_1

**input:**
```
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 8 8 8 5 5 5 5 5 5 5 5 5 5 5 5
5 8 5 8 5 5 5 5 5 5 5 2 2 2 5 5
5 8 8 8 5 5 5 5 5 5 5 2 5 2 5 5
5 5 5 5 5 5 5 5 5 5 5 2 2 2 5 5
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 3 3 3 5 5 5 5 5 5 5 5 5
5 5 5 5 3 5 3 5 5 5 5 5 5 5 5 5
5 5 5 5 3 3 3 5 7 7 7 7 5 5 7 7
5 5 5 5 5 5 5 5 7 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5 1 1 1 5 5 5
5 5 5 5 5 5 5 5 7 5 1 5 1 5 5 5
5 5 5 5 5 5 5 5 7 5 1 1 1 5 5 5
5 6 6 6 5 5 5 5 7 5 5 5 5 5 5 5
5 6 5 6 5 5 5 5 7 5 5 5 5 5 5 5
5 6 6 6 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 7 5 5 5 5 5 5 5
```


**output:**
```
1 1 1
1 5 1
1 1 1
```


## train_2

**input:**
```
5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 1 1 1 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 1 5 1 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 1 1 1 5 5 5 5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 3 3 3 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 3 5 3 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 3 3 3 5 5 5 5 2 2 2 5
5 7 7 7 5 7 7 7 5 5 5 5 5 5 2 5 2 5
5 7 5 5 5 5 5 7 5 5 5 5 5 5 2 2 2 5
5 7 5 4 4 4 5 7 5 5 5 5 5 5 5 5 5 5
5 5 5 4 5 4 5 5 5 5 5 5 5 5 5 5 5 5
5 7 5 4 4 4 5 7 5 5 5 5 5 5 5 5 5 5
5 7 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 7 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5 5
5 7 5 5 5 5 5 7 5 5 5 8 8 8 5 5 5 5
5 5 5 5 5 5 5 7 5 5 5 8 5 8 5 5 5 5
5 7 5 5 5 5 5 7 5 5 5 8 8 8 5 5 5 5
```


**output:**
```
4 4 4
4 5 4
4 4 4
```

## Perception

The input grids contain a background color (gray, 5) and multiple smaller, colored objects scattered across the grid. Each object is a contiguous block of a single non-background color.
Observing the examples, several objects often share the same shape or pattern (e.g., a 3x3 hollow square), while other objects have different shapes.
The output grid is always a small grid (3x3 in the examples) representing exactly one of the objects found in the input grid. Specifically, it's an instance of the shape pattern that appears most frequently in the input. The task involves identifying all objects, determining their shape patterns, finding the most common pattern, and then applying a specific rule to select which instance of that common pattern becomes the output. The selection rule appears to depend on the count of objects matching the most frequent pattern and the count of objects *not* matching it, combined with the spatial ordering of the matching objects.

## Facts


