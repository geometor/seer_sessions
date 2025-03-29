*   **Perception:**
    *   The input grids contain multiple distinct objects composed of non-white pixels.
    *   In each example, there is a pair of objects where one object (the "container") completely encloses another object (the "content").
    *   There is also at least one other separate object (the "target") present in the grid which is identical in shape and color to the "content" object.
    *   The transformation involves identifying the "container" and its "content", finding the identical "target" object elsewhere, and then copying the "container" and "content" structure to replace the "target" object. The pasting is done such that the copied "content" aligns perfectly with the original position of the "target" object.

*   **Facts:**
    
```yaml
    task_type: object_manipulation
    
    elements:
      - role: background
        color: white
      - role: object
        description: Contiguous blocks of non-white pixels.
    
    objects:
      - name: container_object
        description: An object that fully encloses another object.
        properties: [non-white_color, specific_shape]
      - name: content_object
        description: An object fully enclosed within a container_object.
        properties: [non-white_color, specific_shape]
      - name: target_object
        description: An object identical in shape and color to a content_object, but located outside its corresponding container_object.
        properties: [non-white_color, specific_shape]
    
    relationships:
      - type: containment
        subject: container_object
        object: content_object
        description: The container_object's bounding box completely surrounds the content_object, and only background pixels separate them if any separation exists.
      - type: identity
        subject: content_object
        object: target_object
        description: The target_object has the same pixel colors, shape, and size as the content_object.
      - type: spatial
        subject: target_object
        object: container_object
        description: The target_object is spatially separate from the container_object.
    
    actions:
      - name: identify_pairs
        description: Find all pairs of (container_object, content_object).
      - name: identify_targets
        description: For each content_object, find all identical target_objects located outside the corresponding container_object.
      - name: copy_structure
        description: Create a copy of the container_object and its enclosed content_object.
      - name: determine_paste_location
        description: Calculate the relative offset between the container_object and the content_object within the original structure. Use the location (e.g., top-left corner) of the target_object and this offset to determine where the copied container_object should be placed so the copied content_object aligns perfectly with the original target_object's position.
      - name: replace
        description: Overwrite the area occupied by the target_object (and potentially surrounding background pixels) with the copied structure (container + content) at the determined location. Multiple targets may exist for a single content type, requiring multiple replacements.
    
    ```


*   **Natural Language Program:**
    1.  Identify all distinct, non-background objects in the input grid.
    2.  For each object, determine if it fully contains another object. Identify these as (container, content) pairs.
    3.  For each identified `content` object within a pair, search the grid for other objects (`target` objects) that are identical in shape and color to the `content` object but are located outside the corresponding `container` object.
    4.  For each identified (`container`, `content`, `target`) triplet:
        a.  Create a copy of the `container` object and its enclosed `content` object.
        b.  Determine the position of the `target` object.
        c.  Calculate the relative position of the `content` object with respect to its `container` object (e.g., the offset from the container's top-left corner to the content's top-left corner).
        d.  Paste the copied (`container`, `content`) structure onto the output grid such that the copied `content` object perfectly overlays the original position of the `target` object. Use the relative position calculated in step 4c to correctly place the copied `container` around the copied `content`.
    5.  Ensure the original (`container`, `content`) pairs remain in their initial positions in the output grid.
    6.  The final output grid contains the original structures plus the newly pasted copies that replaced the target objects.