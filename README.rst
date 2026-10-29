seer_sessions
=============

Longitudinal archive, empirical retrospective, and static web navigator for **GEOMETOR SEER** across 14 benchmark suites, 475 session batches, 2,939 unique puzzles, and 8,514 task runs.

Web Navigator (`docs/`)
-----------------------

The interactive HTML navigator under ``docs/`` reproduces and extends ``geometor.seer_navigator`` (``SessionsNavigator``, ``TasksNavigator``, ``SessionScreen``, ``TaskScreen``, ``StepScreen``, and ``TrialSplitViewScreen``):

- ``docs/index.html``: Corpus Overview & 14 Benchmark Suites DataTable.
- ``docs/sessions/index.html``: Global ``SessionsScreen`` across all 475 sessions.
- ``docs/tasks/index.html``: Global ``TasksScreen`` across all 2,939 unique tasks.
- ``docs/retrospective/index.html``: SEER 1.0 Empirical Retrospective & SEER 2.0 Architecture.
- ``docs/suites/<suite>/<session>/<task_id>/index.html``: Task Run view with interactive 50/50 ``TrialSplitViewScreen`` (code + 4-column ARC grid ``TrialViewer``) and 30/70 ``StepScreen`` file inspector.

Rebuild the static site:

.. code-block:: bash

   python3 scripts/build_site.py
