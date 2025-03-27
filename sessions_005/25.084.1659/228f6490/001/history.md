
## train_1

**input:**
```
5 5 5 5 5 0 0 0 0 0
5 0 0 0 5 0 9 9 9 9
5 5 5 0 5 0 9 9 9 9
5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 6 0 6
3 3 3 0 0 0 6 6 0 0
0 0 3 5 5 5 5 5 5 0
0 0 0 5 0 0 0 0 5 0
6 6 0 5 0 0 0 0 5 0
6 6 0 5 5 5 5 5 5 0
```


**output:**
```
5 5 5 5 5 0 0 0 0 0
5 3 3 3 5 0 0 0 0 0
5 5 5 3 5 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0
0 0 0 0 0 0 0 6 0 6
0 0 0 0 0 0 6 6 0 0
0 0 0 5 5 5 5 5 5 0
0 0 0 5 9 9 9 9 5 0
6 6 0 5 9 9 9 9 5 0
6 6 0 5 5 5 5 5 5 0
```


## train_2

**input:**
```
7 0 0 0 0 0 0 0 7 7
0 5 5 5 5 5 0 0 0 0
0 5 0 0 5 5 0 6 6 0
0 5 0 0 5 5 0 0 0 0
0 5 5 5 5 5 0 0 0 0
0 5 5 5 5 5 0 0 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 5 5 5 5 5
0 8 8 0 0 5 5 0 0 5
0 8 8 0 0 5 5 5 5 5
```


**output:**
```
7 0 0 0 0 0 0 0 7 7
0 5 5 5 5 5 0 0 0 0
0 5 8 8 5 5 0 0 0 0
0 5 8 8 5 5 0 0 0 0
0 5 5 5 5 5 0 0 0 0
0 5 5 5 5 5 0 0 7 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 7 5 5 5 5 5
0 0 0 0 0 5 5 6 6 5
0 0 0 0 0 5 5 5 5 5
```


## train_3

**input:**
```
2 2 0 0 5 5 5 5 5 5
2 2 2 0 5 0 0 0 5 5
0 0 0 0 5 5 5 0 0 5
0 4 4 0 5 5 5 5 5 5
0 0 4 0 0 4 0 0 0 0
5 5 5 5 5 0 0 4 4 0
5 5 5 5 5 0 0 0 0 0
5 0 0 5 5 0 0 0 0 4
5 0 0 0 5 0 8 8 8 0
5 5 5 5 5 0 0 0 8 8
```


**output:**
```
0 0 0 0 5 5 5 5 5 5
0 0 0 0 5 8 8 8 5 5
0 0 0 0 5 5 5 8 8 5
0 4 4 0 5 5 5 5 5 5
0 0 4 0 0 4 0 0 0 0
5 5 5 5 5 0 0 4 4 0
5 5 5 5 5 0 0 0 0 0
5 2 2 5 5 0 0 0 0 4
5 2 2 2 5 0 0 0 0 0
5 5 5 5 5 0 0 0 0 0
```

## Perception

The task involves identifying closed regions or "containers" made of gray (5) pixels. For each container, the goal is to find a distinct, non-white, non-gray colored object adjacent to its exterior boundary. If such a unique adjacent object exists, its color is used to fill the interior area enclosed by the gray container. Subsequently, the original adjacent object that provided the fill color is removed (replaced by white (0) pixels). Objects not involved in this container-filler interaction remain unchanged.

**Key elements:**

1.  **Containers:** Closed loops/regions formed by connected gray (5) pixels.
2.  **Fillers:** Connected objects of a single color (not white or gray) adjacent to the *exterior* of a container.
3.  **Interior:** The area enclosed by a gray container, initially consisting of non-gray pixels.
4.  **Interaction:** A container interacts with a filler object if the filler is adjacent to the container's exterior boundary.
5.  **Transformation:**
    *   The interior of the container is filled with the color of the adjacent filler object.
    *   The adjacent filler object is removed (pixels turned white (0)).
6.  **Condition:** This transformation only occurs if there is *exactly one* unique filler object adjacent to the container's exterior.

## Facts


```yaml
task_elements:
  - role: container
    color: gray (5)
    property: forms a closed loop enclosing an area
    description: A contiguous region of gray pixels that separates an interior area from the exterior.
  - role: filler_source
    color: any color except white (0) or gray (5)
    property: contiguous region of a single color
    description: An object located outside a container, potentially providing the fill color.
  - role: interior_pixels
    color: initially any color except gray (5)
    property: enclosed by a container
    description: Pixels inside the boundary formed by a gray container.
  - role: background
    color: white (0)
    description: The default background color, also used to erase filler sources.

relationships:
  - type: adjacency
    from: filler_source
    to: container
    detail: The filler_source object must touch (share an edge or corner) the exterior boundary pixels of the container object.
  - type: enclosure
    container: container
    contained: interior_pixels
    detail: The container object topologically separates the interior_pixels from the grid boundaries and other exterior regions.

actions:
  - name: identify_containers
    input: grid
    output: list of gray (5) container objects
  - name: identify_filler_sources
    input: grid
    output: list of non-white, non-gray objects
  - name: determine_interior
    input: container object, grid
    output: set of interior pixel coordinates
  - name: find_adjacent_filler
    input: container object, list of filler_sources, grid
    output: unique adjacent filler_source object (or none)
  - name: fill_interior
    input: interior pixel coordinates, filler color
    target: output grid
    effect: Changes the color of interior pixels to the filler color.
  - name: remove_filler_source
    input: filler_source object coordinates
    target: output grid
    effect: Changes the color of the filler source pixels to white (0).

transformation_conditions:
  - condition: A gray container must exist.
  - condition: The gray container must enclose an interior region.
  - condition: Exactly one filler_source object must be adjacent to the exterior of the container.

output_grid_generation:
  - step: Initialize the output grid as a copy of the input grid.
  - step: Apply fill_interior and remove_filler_source actions for all container-filler pairs meeting the conditions.
  - step: Pixels not part of a modified interior or a removed filler source retain their original color.

```


## Natural Language Program

1.  Create a copy of the input grid to serve as the output grid.
2.  Identify all distinct connected regions (objects) of gray (5) pixels in the input grid. These are potential "containers".
3.  Identify all distinct connected regions (objects) of any single color *other than* white (0) or gray (5). These are potential "filler sources".
4.  For each potential container identified in step 2:
    a.  Determine the set of pixels that form the exterior boundary of this container.
    b.  Determine the set of pixels that form the interior region enclosed by this container. (These are non-gray pixels from which the grid boundary cannot be reached without crossing the container pixels).
    c.  Find all potential filler source objects (from step 3) that are adjacent (share at least one edge or corner) with any pixel on the *exterior* boundary of the container.
    d.  If *exactly one* such adjacent filler source object is found:
        i.  Get the color of this unique adjacent filler source object.
        ii. Get the coordinates of all pixels belonging to this filler source object.
        iii. Get the coordinates of all pixels in the interior region (identified in step 4b).
        iv. In the *output grid*, change the color of all pixels at the interior coordinates (from step 4d.iii) to the filler source color (from step 4d.i).
        v.  In the *output grid*, change the color of all pixels belonging to the filler source object (from step 4d.ii) to white (0).
5.  Return the final modified output grid.
