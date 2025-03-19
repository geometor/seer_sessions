# 890034e9 • 013 • example_3 • investigate_dreamer

---
Okay, I'm ready to analyze this ARC-AGI task example. Here's my breakdown of the input-output pair, focusing on perception, facts, and a natural language program description:

**Perception of Elements:**

*   The input and output are grids of the same dimensions (21x33).
*   The grids contain single-digit integers representing colors.
*   The primary colors involved seem to be: white (0), green (3), red (2), and yellow (4).
*   There's a large, irregular "blob" of yellow (4) pixels in the center of the input grid.
* The output appears to copy all objects in the input grid, except for a change.
*   The yellow blob changes location in several places, and there are some stray yellow pixels present.

**YAML Fact Documentation:**



```yaml
facts:
  grid_dimensions:
    height: 21
    width: 33
  colors:
    white: 0
    blue: 1
    red: 2
    green: 3
    yellow: 4
    gray: 5
    magenta: 6
    orange: 7
    azure: 8
    maroon: 9
  objects:
    - type: background
      color: mixed (predominantly red, white, green)
    - type: blob
      color: yellow
      shape: irregular
      location: center
  actions:
    - type: find
      target:
        - object: contiguous yellow object
        - color: green pixel surrounded by exactly 3 yellow pixels in Moore neighborhood
    - type: replace
      source: green pixel
      target: yellow pixel
  relationships:
    - type: adjacency
      description: "Pixels of different colors are adjacent."
    - type: containment
      description: "The yellow blob is surrounded by other colors."
    - type: neighborhood
      description: "Changes seem to depend on the immediate neighbors of a pixel."
```



**Natural Language Program:**

1.  **Copy** the input grid to the output grid.
2. **Identify** all green pixels that have exactly three yellow neighbors in a 3 x 3 Moore neighborhood.
3.  **For each** identified green pixel:
    *   **Replace with a yellow pixel**.


