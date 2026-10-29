/* GEOMETOR SEER Navigator - Client Interactive Engine */
(function () {
  "use strict";

  const COLOR_HEX = {
    "0": "#000000",
    "1": "#0074D9",
    "2": "#FF4136",
    "3": "#2ECC40",
    "4": "#FFDC00",
    "5": "#AAAAAA",
    "6": "#F012BE",
    "7": "#FF851B",
    "8": "#7FDBFF",
    "9": "#870C25",
    "-1": "#FF00FF"
  };

  let currentGridMode = localStorage.getItem("seer_grid_mode") || "solid"; // solid | char | tiny | diff

  function parseGridString(str) {
    if (!str || typeof str !== "string") return [];
    const lines = str.trim().split(/\r?\n/).filter(Boolean);
    return lines.map(line => line.trim().split(/\s+/).map(Number));
  }

  function renderGridHTML(matrixOrStr, label, mode, expectedMatrixOrStr) {
    const matrix = Array.isArray(matrixOrStr) ? matrixOrStr : parseGridString(matrixOrStr);
    const expected = expectedMatrixOrStr
      ? (Array.isArray(expectedMatrixOrStr) ? expectedMatrixOrStr : parseGridString(expectedMatrixOrStr))
      : null;

    if (!matrix || !matrix.length || !matrix[0].length) {
      return '<div class="grid-box"><div class="grid-meta">' + (label || "Grid") + ' (empty)</div></div>';
    }
    const h = matrix.length;
    const w = matrix[0].length;
    const gmode = mode || currentGridMode;

    let rowsHtml = "";
    for (let r = 0; r < h; r++) {
      let cellsHtml = "";
      for (let c = 0; c < w; c++) {
        const val = matrix[r][c];
        const bg = COLOR_HEX[String(val)] || "#FF00FF";
        let cls = "";
        let txt = String(val);
        if (gmode === "diff" && expected) {
          const expVal = (expected[r] && expected[r][c] !== undefined) ? expected[r][c] : null;
          if (expVal !== val) {
            cls = ' class="cell-mismatch"';
            txt = "×";
          }
        }
        cellsHtml += '<td' + cls + ' style="background-color:' + bg + ';" title="(' + r + ',' + c + ') = ' + val + '">' + txt + '</td>';
      }
      rowsHtml += "<tr>" + cellsHtml + "</tr>";
    }

    const metaTitle = label ? (label + " (" + w + "×" + h + ")") : (w + "×" + h);
    return (
      '<div class="grid-box">' +
        '<div class="grid-meta">' + metaTitle + '</div>' +
        '<table class="arc-grid mode-' + gmode + '" data-grid-raw='' + JSON.stringify(matrix) + ''' +
        (expected ? ' data-grid-exp='' + JSON.stringify(expected) + ''' : '') + '>' +
          rowsHtml +
        '</table>' +
      '</div>'
    );
  }

  function updateAllGridModes(newMode) {
    currentGridMode = newMode;
    localStorage.setItem("seer_grid_mode", newMode);
    document.querySelectorAll(".grid-mode-btn").forEach(btn => {
      btn.classList.toggle("active", btn.getAttribute("data-mode") === newMode);
    });
    document.querySelectorAll("table.arc-grid").forEach(tbl => {
      tbl.classList.remove("mode-solid", "mode-char", "mode-tiny", "mode-diff");
      tbl.classList.add("mode-" + newMode);
      const raw = tbl.getAttribute("data-grid-raw");
      const exp = tbl.getAttribute("data-grid-exp");
      if (raw) {
        const mat = JSON.parse(raw);
        const expMat = exp ? JSON.parse(exp) : null;
        const rows = tbl.querySelectorAll("tr");
        for (let r = 0; r < mat.length; r++) {
          const cells = rows[r] ? rows[r].querySelectorAll("td") : [];
          for (let c = 0; c < mat[r].length; c++) {
            const cell = cells[c];
            if (!cell) continue;
            const val = mat[r][c];
            cell.className = "";
            cell.textContent = String(val);
            if (newMode === "diff" && expMat) {
              const expVal = (expMat[r] && expMat[r][c] !== undefined) ? expMat[r][c] : null;
              if (expVal !== val) {
                cell.className = "cell-mismatch";
                cell.textContent = "×";
              }
            }
          }
        }
      }
    });
  }

  // Sortable DataTables
  function initSortableTables() {
    document.querySelectorAll("table.nav-table").forEach(table => {
      const headers = table.querySelectorAll("thead th");
      headers.forEach((th, colIdx) => {
        th.addEventListener("click", () => {
          const tbody = table.querySelector("tbody");
          if (!tbody) return;
          const rows = Array.from(tbody.querySelectorAll("tr"));
          const currentDir = th.getAttribute("data-sort-dir") || "none";
          const nextDir = currentDir === "asc" ? "desc" : "asc";

          headers.forEach(h => {
            h.removeAttribute("data-sort-dir");
            const arrow = h.querySelector(".sort-ind");
            if (arrow) arrow.remove();
          });
          th.setAttribute("data-sort-dir", nextDir);
          const ind = document.createElement("span");
          ind.className = "sort-ind";
          ind.textContent = nextDir === "asc" ? " ▲" : " ▼";
          th.appendChild(ind);

          const isNum = th.classList.contains("num") || th.getAttribute("data-sort-type") === "num";

          rows.sort((a, b) => {
            const cellA = a.children[colIdx];
            const cellB = b.children[colIdx];
            if (!cellA || !cellB) return 0;
            const rawA = cellA.getAttribute("data-sort") !== null ? cellA.getAttribute("data-sort") : cellA.textContent.trim();
            const rawB = cellB.getAttribute("data-sort") !== null ? cellB.getAttribute("data-sort") : cellB.textContent.trim();

            const emptyA = rawA === "" || rawA === "-" || rawA === "None";
            const emptyB = rawB === "" || rawB === "-" || rawB === "None";
            if (emptyA && emptyB) return 0;
            if (emptyA) return 1; // Always push None/empty to bottom
            if (emptyB) return -1;

            if (isNum) {
              const numA = parseFloat(rawA);
              const numB = parseFloat(rawB);
              if (!isNaN(numA) && !isNaN(numB)) {
                return nextDir === "asc" ? numA - numB : numB - numA;
              }
            }
            return nextDir === "asc"
              ? rawA.localeCompare(rawB, undefined, { numeric: true, sensitivity: "base" })
              : rawB.localeCompare(rawA, undefined, { numeric: true, sensitivity: "base" });
          });

          rows.forEach(r => tbody.appendChild(r));
        });
      });
    });
  }

  // Row Click & Filtering
  function initTableFiltersAndLinks() {
    const searchInput = document.getElementById("table-search");
    const suiteSelect = document.getElementById("suite-filter");
    const statusBtns = document.querySelectorAll(".status-filter-btn");
    const countBadge = document.getElementById("visible-row-count");

    let activeStatus = "all";

    function applyFilters() {
      const q = searchInput ? searchInput.value.trim().toLowerCase() : "";
      const suite = suiteSelect ? suiteSelect.value : "all";
      const table = document.querySelector("table.nav-table.filterable-table");
      if (!table) return;
      const rows = table.querySelectorAll("tbody tr");
      let shown = 0;

      rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        const rSuite = row.getAttribute("data-suite") || "";
        const rStatus = row.getAttribute("data-status") || "";

        const matchQ = !q || text.includes(q);
        const matchSuite = suite === "all" || rSuite === suite;
        let matchStatus = true;
        if (activeStatus !== "all") {
          matchStatus = rStatus.split(" ").includes(activeStatus);
        }

        if (matchQ && matchSuite && matchStatus) {
          row.style.display = "";
          shown++;
        } else {
          row.style.display = "none";
        }
      });

      if (countBadge) {
        countBadge.textContent = shown + " / " + rows.length + " rows";
      }
    }

    if (searchInput) {
      searchInput.addEventListener("input", applyFilters);
    }
    if (suiteSelect) {
      suiteSelect.addEventListener("change", applyFilters);
    }
    statusBtns.forEach(btn => {
      btn.addEventListener("click", () => {
        statusBtns.forEach(b => b.classList.remove("active"));
        btn.classList.add("active");
        activeStatus = btn.getAttribute("data-filter") || "all";
        applyFilters();
      });
    });

    // Row click navigation for rows with data-href
    document.querySelectorAll("table.nav-table tbody tr[data-href]").forEach(row => {
      row.addEventListener("click", (e) => {
        if (e.target.tagName === "A") return;
        const href = row.getAttribute("data-href");
        if (href) window.location.href = href;
      });
    });
  }

  // Render Ground-Truth Puzzle Grids when #puzzle-data is present
  function initPuzzleViewer() {
    const puzScript = document.getElementById("puzzle-data");
    const container = document.getElementById("puzzle-grids-container");
    if (!puzScript || !container) return;

    let puz;
    try {
      puz = JSON.parse(puzScript.textContent);
    } catch (e) {
      return;
    }

    let html = "";
    const trainPairs = puz.train || [];
    const testPairs = puz.test || [];

    if (trainPairs.length || testPairs.length) {
      html += '<div class="pairs-scroll">';
      trainPairs.forEach((pair, idx) => {
        html += (
          '<div class="pair-card">' +
            '<div class="pair-card-title"><span>Train[' + idx + ']</span></div>' +
            '<div class="pair-grids-row">' +
              renderGridHTML(pair.input, "Input", currentGridMode) +
              '<span class="pair-arrow">→</span>' +
              renderGridHTML(pair.output, "Output", currentGridMode) +
            '</div>' +
          '</div>'
        );
      });
      testPairs.forEach((pair, idx) => {
        html += (
          '<div class="pair-card" style="border-color: var(--accent);">' +
            '<div class="pair-card-title"><span>Test[' + idx + ']</span></div>' +
            '<div class="pair-grids-row">' +
              renderGridHTML(pair.input, "Input", currentGridMode) +
              '<span class="pair-arrow">→</span>' +
              (pair.output ? renderGridHTML(pair.output, "Expected", currentGridMode) : '<span class="status-dim">Hidden</span>') +
            '</div>' +
          '</div>'
        );
      });
      html += '</div>';
    }
    container.innerHTML = html;
  }

  // Task Run Page: Step & Trial Split Inspector (#run-data)
  function initTaskRunInspector() {
    const runScript = document.getElementById("run-data");
    if (!runScript) return;

    let runData;
    try {
      runData = JSON.parse(runScript.textContent);
    } catch (e) {
      console.error("Failed to parse run-data", e);
      return;
    }

    const steps = runData.steps || [];
    const puzzle = runData.puzzle || { train: [], test: [] };
    if (!steps.length) return;

    // Build flat list of all trials across all steps (for 'v' All-Trials cycling)
    const allTrials = [];
    steps.forEach((st, sIdx) => {
      (st.trials || []).forEach((tr, tIdx) => {
        allTrials.push({
          stepIndex: sIdx,
          stepName: st.step,
          stepTitle: st.title,
          trialIndex: tIdx,
          trial: tr,
          codeContent: (st.files && st.files[tr.code_file]) || "# Code file not found"
        });
      });
    });

    let currentStepIdx = 0;
    // Default to first step that has trials if available, else step 0
    const firstCoderIdx = steps.findIndex(s => s.trials && s.trials.length > 0);
    if (firstCoderIdx >= 0) currentStepIdx = firstCoderIdx;

    let currentTrialIdxInStep = 0;
    let currentFileKey = null;
    let activeInspectorTab = "trial-split"; // "trial-split" | "step-files"

    const stepRows = document.querySelectorAll("#steps-table tbody tr");
    const tabTrialBtn = document.getElementById("tab-btn-trial-split");
    const tabFilesBtn = document.getElementById("tab-btn-step-files");
    const paneTrialSplit = document.getElementById("inspector-trial-split");
    const paneStepFiles = document.getElementById("inspector-step-files");
    const stepLabelBadge = document.getElementById("inspector-step-label");
    const trialSelectEl = document.getElementById("trial-selector");
    const prevTrialBtn = document.getElementById("btn-prev-trial");
    const nextTrialBtn = document.getElementById("btn-next-trial");

    function setInspectorTab(tabName) {
      activeInspectorTab = tabName;
      if (tabTrialBtn) tabTrialBtn.classList.toggle("active", tabName === "trial-split");
      if (tabFilesBtn) tabFilesBtn.classList.toggle("active", tabName === "step-files");
      if (paneTrialSplit) paneTrialSplit.style.display = tabName === "trial-split" ? "grid" : "none";
      if (paneStepFiles) paneStepFiles.style.display = tabName === "step-files" ? "grid" : "none";
    }

    if (tabTrialBtn) tabTrialBtn.addEventListener("click", () => setInspectorTab("trial-split"));
    if (tabFilesBtn) tabFilesBtn.addEventListener("click", () => setInspectorTab("step-files"));

    function fmtBoolHtml(v, invert) {
      if (v === true) return '<span class="' + (invert ? 'status-bad' : 'status-good') + '">✓</span>';
      if (v === false) return '<span class="' + (invert ? 'status-good' : 'status-bad') + '">✗</span>';
      return '<span class="status-dim">-</span>';
    }

    function renderTrialViewerPane(stepObj, trialObj) {
      const codeEl = document.getElementById("trial-split-code");
      const codeHeaderEl = document.getElementById("trial-split-code-title");
      const viewerEl = document.getElementById("trial-split-viewer");

      if (!trialObj) {
        // If this step is a dreamer step with no trials, show primary markdown/yaml file on left and message on right
        const fkeys = Object.keys(stepObj.files || {});
        const mainFile = fkeys.find(k => k.endsWith(".yaml") || k.endsWith(".yml") || k.endsWith(".md")) || fkeys[0];
        if (codeHeaderEl) codeHeaderEl.textContent = "Step " + stepObj.step + " (" + stepObj.title + ") — " + (mainFile || "No trial code");
        if (codeEl) codeEl.textContent = mainFile ? stepObj.files[mainFile] : "# No Python trials executed in this step (e.g. Dreamer observation step).\n# Switch to 'Step Files Inspector' or select a Coder step.";
        if (viewerEl) {
          viewerEl.innerHTML = (
            '<div style="padding: 20px; color: var(--text-1);">' +
              'No code trials in <b>Step ' + stepObj.step + ' (' + stepObj.title + ')</b>.<br><br>' +
              'Select a Coder step in the table above or click <b>Step Files Inspector</b> to read the full response & YAML observations.' +
            '</div>'
          );
        }
        return;
      }

      const codeText = (stepObj.files && stepObj.files[trialObj.code_file]) || "# Code not found";
      if (codeHeaderEl) {
        codeHeaderEl.textContent = "Step " + stepObj.step + " • " + trialObj.code_file + " (Score: " + (trialObj.total_score !== null ? trialObj.total_score : "-") + ")";
      }
      if (codeEl) codeEl.textContent = codeText;

      let vHtml = "";
      if (trialObj.train_error) {
        vHtml += '<div class="trial-set-heading" style="border-color:var(--bad);color:var(--bad);">Train Execution Error</div>';
        vHtml += '<pre class="code-block" style="color:var(--bad);margin-bottom:10px;">' + trialObj.train_error + '</pre>';
      }
      if (trialObj.test_error) {
        vHtml += '<div class="trial-set-heading" style="border-color:var(--bad);color:var(--bad);">Test Execution Error</div>';
        vHtml += '<pre class="code-block" style="color:var(--bad);margin-bottom:10px;">' + trialObj.test_error + '</pre>';
      }

      // Render Train Set & Test Set matching TrialViewer in seer_navigator
      const renderPairSection = (title, trialItems, gtPairs) => {
        if (!trialItems || !trialItems.length) return "";
        let sec = '<div class="trial-set-heading">' + title + '</div>';
        trialItems.forEach((item, idx) => {
          const gt = gtPairs[idx] || {};
          const inMat = gt.input || [];
          const expMat = gt.output || [];
          const actStr = item.actual || item.transformed_output;

          sec += (
            '<div class="trial-pair-row">' +
              '<table class="trial-details-table">' +
                '<thead><tr><th colspan="2">' + title.split(" ")[0] + '[' + idx + '] Details</th></tr></thead>' +
                '<tbody>' +
                  '<tr><td>Match</td><td>' + fmtBoolHtml(item.match) + '</td></tr>' +
                  '<tr><td>Score</td><td>' + (item.score !== null && item.score !== undefined ? item.score : "-") + '</td></tr>' +
                  '<tr><td>Size OK</td><td>' + fmtBoolHtml(item.size_ok) + '</td></tr>' +
                  '<tr><td>Palette OK</td><td>' + fmtBoolHtml(item.pal_ok) + '</td></tr>' +
                  '<tr><td>Count OK</td><td>' + fmtBoolHtml(item.cnt_ok) + '</td></tr>' +
                  '<tr><td>Pixels Off</td><td>' + (item.px_off !== null && item.px_off !== undefined ? item.px_off : "-") + '</td></tr>' +
                  '<tr><td>% Correct</td><td>' + (item.pct !== null && item.pct !== undefined ? item.pct + "%" : "-") + '</td></tr>' +
                '</tbody>' +
              '</table>' +
              renderGridHTML(inMat, "Input", currentGridMode) +
              renderGridHTML(expMat, "Expected", currentGridMode) +
              (actStr
                ? renderGridHTML(actStr, "Actual", currentGridMode, expMat)
                : '<div class="grid-box"><div class="grid-meta">Actual</div><div class="status-bad" style="padding:8px;">' + (item.error || "No output") + '</div></div>') +
            '</div>'
          );
        });
        return sec;
      };

      vHtml += renderPairSection("Train Set", trialObj.train || [], puzzle.train || []);
      vHtml += renderPairSection("Test Set", trialObj.test || [], puzzle.test || []);
      if (viewerEl) viewerEl.innerHTML = vHtml;
    }

    function renderStepFilesPane(stepObj) {
      const listEl = document.getElementById("step-files-list");
      const contentTitleEl = document.getElementById("step-file-content-title");
      const contentBodyEl = document.getElementById("step-file-content-body");
      if (!listEl || !contentBodyEl) return;

      const filesMap = stepObj.files || {};
      const keys = Object.keys(filesMap);
      if (!keys.length) {
        listEl.innerHTML = '<li class="status-dim">No embedded files</li>';
        contentBodyEl.innerHTML = '<pre class="code-block">No files available for this step.</pre>';
        return;
      }

      if (!currentFileKey || !filesMap[currentFileKey]) {
        currentFileKey = keys.find(k => k === "response.md" || k.endsWith(".py") || k.endsWith(".yaml")) || keys[0];
      }

      listEl.innerHTML = "";
      keys.forEach(k => {
        const li = document.createElement("li");
        li.textContent = k;
        if (k === currentFileKey) li.classList.add("active");
        li.addEventListener("click", () => {
          currentFileKey = k;
          renderStepFilesPane(stepObj);
        });
        listEl.appendChild(li);
      });

      const val = filesMap[currentFileKey] || "";
      if (contentTitleEl) contentTitleEl.textContent = "Step " + stepObj.step + " / " + currentFileKey;
      if (val.startsWith("IMAGE:")) {
        const imgUrl = val.slice(6);
        contentBodyEl.innerHTML = '<div style="padding:16px;"><img src="' + imgUrl + '" style="max-width:100%;border:1px solid var(--border);"></div>';
      } else {
        contentBodyEl.innerHTML = '<pre class="code-block"></pre>';
        contentBodyEl.querySelector("pre").textContent = val;
      }
    }

    function selectStep(idx, trialIdx) {
      if (idx < 0 || idx >= steps.length) return;
      currentStepIdx = idx;
      const st = steps[currentStepIdx];
      currentTrialIdxInStep = trialIdx || 0;
      currentFileKey = null;

      stepRows.forEach((r, i) => {
        r.classList.toggle("selected-row", i === currentStepIdx);
      });

      if (stepLabelBadge) {
        stepLabelBadge.textContent = "Step " + st.step + " (" + st.title + ")";
      }

      // Populate trial selector dropdown
      if (trialSelectEl) {
        trialSelectEl.innerHTML = "";
        if (st.trials && st.trials.length) {
          st.trials.forEach((tr, tIdx) => {
            const opt = document.createElement("option");
            opt.value = String(tIdx);
            const passTag = tr.test_passed === true ? "✓ TEST" : (tr.train_passed ? "✓ TRAIN" : "✗");
            opt.textContent = tr.code_file + " [" + passTag + " | score: " + (tr.total_score !== null ? tr.total_score : "-") + "]";
            if (tIdx === currentTrialIdxInStep) opt.selected = true;
            trialSelectEl.appendChild(opt);
          });
        } else {
          const opt = document.createElement("option");
          opt.value = "0";
          opt.textContent = "No code trials in step " + st.step;
          trialSelectEl.appendChild(opt);
        }
      }

      const activeTrial = (st.trials && st.trials[currentTrialIdxInStep]) || null;
      renderTrialViewerPane(st, activeTrial);
      renderStepFilesPane(st);
    }

    if (trialSelectEl) {
      trialSelectEl.addEventListener("change", () => {
        currentTrialIdxInStep = parseInt(trialSelectEl.value, 10) || 0;
        const st = steps[currentStepIdx];
        renderTrialViewerPane(st, (st.trials && st.trials[currentTrialIdxInStep]) || null);
      });
    }

    function stepTrialDelta(delta) {
      if (!allTrials.length) return;
      let curGlobalIdx = allTrials.findIndex(
        x => x.stepIndex === currentStepIdx && x.trialIndex === currentTrialIdxInStep
      );
      if (curGlobalIdx < 0) curGlobalIdx = 0;
      else curGlobalIdx = (curGlobalIdx + delta + allTrials.length) % allTrials.length;
      const target = allTrials[curGlobalIdx];
      selectStep(target.stepIndex, target.trialIndex);
    }

    if (prevTrialBtn) prevTrialBtn.addEventListener("click", () => stepTrialDelta(-1));
    if (nextTrialBtn) nextTrialBtn.addEventListener("click", () => stepTrialDelta(1));

    stepRows.forEach((row, idx) => {
      row.addEventListener("click", () => {
        selectStep(idx, 0);
        // If step has no trials, automatically show step files tab; otherwise trial split
        if (!steps[idx].trials || !steps[idx].trials.length) {
          setInspectorTab("step-files");
        } else {
          setInspectorTab("trial-split");
        }
      });
    });

    selectStep(currentStepIdx, 0);
  }

  // Keyboard Navigation (Matches seer_navigator bindings)
  function initKeyboardShortcuts() {
    let selectedRowIdx = -1;

    function getVisibleRows() {
      const table = document.querySelector("table.nav-table");
      if (!table) return [];
      return Array.from(table.querySelectorAll("tbody tr")).filter(r => r.style.display !== "none");
    }

    function highlightRow(idx) {
      const rows = getVisibleRows();
      if (!rows.length) return;
      selectedRowIdx = Math.max(0, Math.min(idx, rows.length - 1));
      rows.forEach((r, i) => r.classList.toggle("selected-row", i === selectedRowIdx));
      rows[selectedRowIdx].scrollIntoView({ block: "nearest" });
    }

    document.addEventListener("keydown", (e) => {
      if (e.target.tagName === "INPUT" || e.target.tagName === "SELECT" || e.target.tagName === "TEXTAREA") {
        if (e.key === "Escape") e.target.blur();
        return;
      }

      if (e.key === "/") {
        const s = document.getElementById("table-search");
        if (s) {
          e.preventDefault();
          s.focus();
        }
      } else if (e.key === "j" || e.key === "ArrowDown") {
        const rows = getVisibleRows();
        if (rows.length) {
          e.preventDefault();
          highlightRow(selectedRowIdx + 1);
          if (document.getElementById("run-data")) rows[selectedRowIdx].click();
        }
      } else if (e.key === "k" || e.key === "ArrowUp") {
        const rows = getVisibleRows();
        if (rows.length) {
          e.preventDefault();
          highlightRow(selectedRowIdx <= 0 ? 0 : selectedRowIdx - 1);
          if (document.getElementById("run-data")) rows[selectedRowIdx].click();
        }
      } else if (e.key === "Enter") {
        const rows = getVisibleRows();
        if (selectedRowIdx >= 0 && rows[selectedRowIdx]) {
          const href = rows[selectedRowIdx].getAttribute("data-href");
          if (href) window.location.href = href;
          else rows[selectedRowIdx].click();
        }
      } else if (e.key === "h" || e.key === "Backspace") {
        const up = document.getElementById("nav-up-link");
        if (up) window.location.href = up.getAttribute("href");
      } else if (e.key === "[") {
        const prev = document.getElementById("nav-prev-link");
        if (prev) window.location.href = prev.getAttribute("href");
      } else if (e.key === "]") {
        const next = document.getElementById("nav-next-link");
        if (next) window.location.href = next.getAttribute("href");
      } else if (e.key === "v") {
        const tabTrial = document.getElementById("tab-btn-trial-split");
        const tabFiles = document.getElementById("tab-btn-step-files");
        if (tabTrial && tabFiles) {
          if (tabTrial.classList.contains("active")) tabFiles.click();
          else tabTrial.click();
        }
      } else if (e.key === "1") {
        updateAllGridModes("solid");
      } else if (e.key === "2") {
        updateAllGridModes("char");
      } else if (e.key === "3") {
        updateAllGridModes("tiny");
      } else if (e.key === "4") {
        updateAllGridModes("diff");
      }
    });
  }

  document.addEventListener("DOMContentLoaded", () => {
    document.querySelectorAll(".grid-mode-btn").forEach(btn => {
      btn.classList.toggle("active", btn.getAttribute("data-mode") === currentGridMode);
      btn.addEventListener("click", () => updateAllGridModes(btn.getAttribute("data-mode")));
    });
    initSortableTables();
    initTableFiltersAndLinks();
    initPuzzleViewer();
    initTaskRunInspector();
    initKeyboardShortcuts();
  });
})();
