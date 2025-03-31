
## train_1

**input:**
```
7 7 2 7 7 7 7
7 7 2 2 2 7 7
7 7 7 7 2 7 7
2 2 7 7 2 2 2
7 2 7 7 7 7 7
7 2 2 2 2 7 7
7 7 7 7 2 7 7
```


**output:**
```
3 3 2 5 5 5 5
3 3 2 2 2 5 5
3 3 3 3 2 5 5
2 2 3 3 2 2 2
5 2 3 3 3 3 3
5 2 2 2 2 3 3
5 5 5 5 2 3 3
```


## train_2

**input:**
```
2 7 7 7 7 7 7
2 7 7 7 7 7 7
2 7 7 7 7 7 7
2 2 2 7 7 7 7
7 7 2 7 7 7 7
7 7 2 2 2 7 7
7 7 7 7 2 2 2
```


**output:**
```
2 3 3 3 3 3 3
2 3 3 3 3 3 3
2 3 3 3 3 3 3
2 2 2 3 3 3 3
5 5 2 3 3 3 3
5 5 2 2 2 3 3
5 5 5 5 2 2 2
```


## train_3

**input:**
```
7 7 7 7 7 2 7 7
7 7 7 7 7 2 7 7
2 2 2 2 7 2 7 7
7 7 7 2 7 2 7 7
7 7 7 2 7 2 7 7
2 2 7 2 7 2 2 7
7 2 7 2 7 7 2 2
7 2 7 2 7 7 7 7
```


**output:**
```
5 5 5 5 5 2 3 3
5 5 5 5 5 2 3 3
2 2 2 2 5 2 3 3
3 3 3 2 5 2 3 3
3 3 3 2 5 2 3 3
2 2 3 2 5 2 2 3
5 2 3 2 5 5 2 2
5 2 3 2 5 5 5 5
```

Okay, let's analyze the provided examples to understand the transformation rule.

**Perception**

1.  **Grid Structure:** The input and output grids always have the same dimensions in each example pair.
2.  **Color Palette:**
    *   Input grids contain only Red (2) and Orange (7) pixels.
    *   Output grids contain Red (2), Green (3), and Gray (5) pixels.
3.  **Static Elements:** The Red (2) pixels appear in the exact same positions in the output grid as they were in the input grid. They seem to function as fixed elements or boundaries.
4.  **Dynamic Elements:** The Orange (7) pixels in the input grid are the ones that change color in the output grid. They become either Green (3) or Gray (5).
5.  **Transformation Pattern:** The change from Orange (7) to either Green (3) or Gray (5) appears to depend on the spatial relationship between groups of Orange pixels and the fixed Red pixels. Specifically, it looks like connected regions (components) of Orange pixels are evaluated based on their proximity to any Red pixel.
6.  **Connected Components:** If we consider groups of Orange (7) pixels that are connected side-by-side (4-way adjacency), the rule seems to be:
    *   If *any* pixel within a connected component of Orange pixels is directly adjacent (up, down, left, or right) to a Red (2) pixel, then *all* pixels in that Orange component are changed to Green (3) in the output.
    *   If a connected component of Orange pixels is *not* adjacent (4-way) to *any* Red (2) pixel, then *all* pixels in that Orange component are changed to Gray (5) in the output.

**Facts**


```yaml
task_description: Color transformation based on adjacency to static elements.
grid_properties:
  - dimensions_preserved: true # Input and output grids have the same height and width.
involved_colors:
  - input: [2 (Red), 7 (Orange)]
  - output: [2 (Red), 3 (Green), 5 (Gray)]
objects:
  - type: static_pixels
    color: 2 (Red)
    description: Remain unchanged in the output grid. Act as boundaries or influencers.
  - type: dynamic_pixels
    color: 7 (Orange)
    description: Change color based on their relationship to Red pixels. Treated as connected components.
    connectivity: 4-way (von Neumann)
transformation_rules:
  - rule: Identify connected components of Orange (7) pixels using 4-way adjacency.
  - rule: For each Orange component:
      - check: Is any pixel in the component 4-way adjacent to any Red (2) pixel?
      - if_true: Change all pixels of this component to Green (3).
      - if_false: Change all pixels of this component to Gray (5).
  - rule: Keep all Red (2) pixels unchanged.
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify all pixels with the color Red (2) in the input grid. These pixels will remain Red (2) in the output grid.
3.  Identify all pixels with the color Orange (7) in the input grid.
4.  Find all distinct connected components of Orange (7) pixels. Two Orange pixels are considered connected if they are adjacent horizontally or vertically (4-way connectivity).
5.  For each connected component of Orange (7) pixels:
    a.  Determine if any pixel belonging to this component is adjacent (horizontally or vertically) to any Red (2) pixel in the input grid.
    b.  If such adjacency exists (at least one Orange pixel in the component touches a Red pixel), change the color of *all* pixels belonging to this component to Green (3) in the output grid.
    c.  If no such adjacency exists (no Orange pixel in the component touches any Red pixel), change the color of *all* pixels belonging to this component to Gray (5) in the output grid.
6.  The final output grid contains the original Red (2) pixels and the transformed Orange pixels (now either Green (3) or Gray (5)).
