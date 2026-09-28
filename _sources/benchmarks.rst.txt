Benchmark Suites & Empirical Results
====================================

The SEER 1.0 corpus spans 14 distinct benchmark suites representing different puzzle distributions,
dimensionality (1D vs 2D), and model configuration iterations.

Corpus Summary Table
--------------------

.. list-table::
   :widths: 30 10 12 12 12 12 12
   :header-rows: 1

   * - Suite Name
     - Batches
     - Task Runs
     - Unique Puzzles
     - Solved Puzzles
     - Puzzle Solve %
     - Run Solve %
   * - ``sessions``
     - 29
     - 2,232
     - 950
     - 468
     - 49.3%
     - 33.3%
   * - ``sessions_001``
     - 156
     - 1,047
     - 400
     - 71
     - 17.8%
     - 18.1%
   * - ``sessions_005``
     - 30
     - 1,007
     - 524
     - 233
     - 44.5%
     - 33.8%
   * - ``sessions_1D``
     - 18
     - 901
     - 901
     - 667
     - 74.0%
     - 74.0%
   * - ``sessions_ARCv2_eval``
     - 22
     - 686
     - 120
     - 6
     - 5.0%
     - 1.2%
   * - ``sessions_optorex_1D``
     - 58
     - 566
     - 566
     - 145
     - 25.6%
     - 25.6%
   * - ``sessions_ConceptARC``
     - 21
     - 481
     - 176
     - 90
     - 51.1%
     - 18.7%
   * - ``sessions_003``
     - 39
     - 447
     - 300
     - 73
     - 24.3%
     - 26.9%
   * - ``sessions_ARCv2_train_200_300``
     - 4
     - 310
     - 200
     - 46
     - 23.0%
     - 14.8%
   * - ``sessions_ARCv2_train``
     - 26
     - 276
     - 100
     - 94
     - 94.0%
     - 55.4%
   * - ``sessions_ARCv2_train_100_200``
     - 6
     - 223
     - 100
     - 69
     - 69.0%
     - 30.9%
   * - ``sessions_mini_arc``
     - 1
     - 149
     - 149
     - 75
     - 50.3%
     - 50.3%
   * - ``sessions_002``
     - 56
     - 113
     - 20
     - 0
     - 0.0%
     - 0.0%
   * - ``sessions_ARCv2_train_``
     - 9
     - 76
     - 10
     - 10
     - 100.0%
     - 75.0%

Grand Totals
------------

- **Total Benchmark Suites**: 14
- **Total Session Batches**: 475
- **Total Task Runs**: 8,514
- **Unique Puzzles Tested**: 2,939
- **Unique Puzzles Solved**: **1,498 (50.97%)**
- **Total Test-Passing Runs**: 2,703
