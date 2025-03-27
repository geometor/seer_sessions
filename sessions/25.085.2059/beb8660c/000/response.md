**Perception:**

The task involves simulating a simple form of gravity on colored objects within a grid.
1.  **Grid Structure:** The input and output are 2D grids containing pixels of different colors. White (0) represents empty space.
2.  **Objects:** Non-white pixels form distinct objects, often appearing as horizontal lines or small blocks.
3.  **Gravity Effect:** Non-white objects, except for the azure (8) ones, appear to "fall" downwards through the white space in the grid.
4.  **Stopping Condition:** Objects stop falling when they encounter another non-white pixel directly below them or when they reach the bottom row occupied by the azure object.
5.  **Invariant Object:** The azure (8) object, consistently located at the bottom row in all examples, does not move. It acts as a fixed "ground" or base.
6.  **No Horizontal Movement:** Objects only move vertically downwards; there is no horizontal displacement.
7.  **Object Integrity:** Objects maintain their shape and color during the fall.

**Facts:**


```yaml
task_type: gravity_simulation
elements:
  - element_type: grid
    properties:
      - background_color: white (0)
      - contains: objects
  - element_type: object
    properties:
      - color: non-white (1-7, 9)
      - shape: various (lines, blocks, single pixels)
      - initial_position: varies
      - behavior: mobile
  - element_type: object
    properties:
      - color: azure (8)
      - shape: horizontal line spanning grid width
      - initial_position: bottom row
      - behavior: static
      - role: ground/boundary
actions:
  - action_type: vertical_displacement
    target: mobile objects (colors 1-7, 9)
    direction: downwards
    termination_condition:
      - adjacent_below: another non-white pixel (any color 1-9)
      - boundary: reaching the row directly above the static azure (8) object
relationships:
  - relationship_type: spatial
    entities: [mobile object, white pixel]
    description: Mobile objects move through white pixels.
  - relationship_type: collision/support
    entities: [mobile object, mobile object/static object]
    description: A mobile object's downward movement stops when it is directly above another object.
  - relationship_type: boundary
    entities: [mobile object, static azure object]
    description: The static azure object defines the lowest possible boundary for falling objects.
```


**Natural Language Program:**

1.  Identify all distinct non-white objects in the input grid.
2.  Identify the static object(s), specifically the azure (8) object(s) typically forming the bottom row. These objects do not move.
3.  For every other non-white object (mobile objects):
    a.  Determine the lowest row occupied by any pixel of that object.
    b.  Iteratively check the row directly below the current position of the object.
    c.  If all cells directly below the object's pixels are white (0), move the entire object down by one row.
    d.  Repeat step 3c until at least one pixel of the object is directly above a non-white pixel (either another mobile object that has already settled or a static azure object) or until the object reaches the row immediately above the azure bottom row.
4.  Continue this process for all mobile objects, ensuring that objects settle in an order potentially influenced by their initial vertical position (though simultaneous settling based purely on available space seems to be the case here).
5.  The final positions of all objects (static and settled mobile objects) constitute the output grid. The background remains white.