geometor.seer_sessions.navigator
================================

.. py:module:: geometor.seer_sessions.navigator


Attributes
----------

.. autoapisummary::

   geometor.seer_sessions.navigator.PATTERNS
   geometor.seer_sessions.navigator.app


Classes
-------

.. autoapisummary::

   geometor.seer_sessions.navigator.GridApp


Functions
---------

.. autoapisummary::

   geometor.seer_sessions.navigator.make_checkerboard
   geometor.seer_sessions.navigator.make_gradient
   geometor.seer_sessions.navigator.make_random


Module Contents
---------------

.. py:function:: make_checkerboard(size=8)

   Generate an NxN checkerboard pattern with two colors (blue and yellow).


.. py:function:: make_gradient(size=8)

   Generate an NxN gradient pattern (color varies smoothly from one corner to another).


.. py:function:: make_random(size=8)

   Generate an NxN grid of random colors.


.. py:data:: PATTERNS

.. py:class:: GridApp(patterns: dict[str, tuple], **kwargs)

   Bases: :py:obj:`textual.app.App`


   Textual Application that displays buttons to select grid patterns and updates a Matplotlib plot.


   .. py:attribute:: CSS_PATH
      :value: None


      File paths to load CSS from.


   .. py:attribute:: BINDINGS
      :value: [('q', 'quit', 'Quit')]


      The default key bindings.


   .. py:attribute:: patterns


   .. py:attribute:: fig
      :value: None



   .. py:attribute:: ax
      :value: None



   .. py:method:: compose() -> textual.app.ComposeResult

      Create the UI layout with one button per grid pattern.



   .. py:method:: on_mount() -> None

      Called when the app is mounted (initialized). Set up Matplotlib figure here.



   .. py:method:: on_button_pressed(event: textual.widgets.Button.Pressed) -> None

      Event handler for button presses. Updates the Matplotlib plot based on which button was clicked.



   .. py:method:: display_pattern(pattern_key: str) -> None

      Generate and display the grid pattern corresponding to the given key on the Matplotlib plot.



   .. py:method:: on_unmount() -> None

      Called when the app is unmounted. Close the Matplotlib plot.



.. py:data:: app

