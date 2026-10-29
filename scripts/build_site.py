#!/usr/bin/env python3
"""
build_site.py
=============
Generates the complete, interoperable static HTML navigator website under
``seer_sessions/docs/``, reproducing and extending the ``seer_navigator``
experience (SessionsNavigator, TasksNavigator, TaskScreen, StepScreen,
and TrialSplitViewScreen) across all 14 benchmark suites.
"""
from __future__ import annotations

from collections import defaultdict
from datetime import timedelta
import html
import json
import os
from pathlib import Path
import re
import time
from typing import Any

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_DIR = REPO_ROOT / "docs"

SUITE_NAMES: list[str] = [
    "sessions",
    "sessions_001",
    "sessions_002",
    "sessions_003",
    "sessions_005",
    "sessions_1D",
    "sessions_ARCv2_eval",
    "sessions_ARCv2_train",
    "sessions_ARCv2_train_",
    "sessions_ARCv2_train_100_200",
    "sessions_ARCv2_train_200_300",
    "sessions_ConceptARC",
    "sessions_mini_arc",
    "sessions_optorex_1D",
]

COLOR_HEX_MAP: dict[int, str] = {
    0: "#000000",  # Black
    1: "#0074D9",  # Blue
    2: "#FF4136",  # Red
    3: "#2ECC40",  # Green
    4: "#FFDC00",  # Yellow
    5: "#AAAAAA",  # Grey
    6: "#F012BE",  # Fuchsia
    7: "#FF851B",  # Orange
    8: "#7FDBFF",  # Teal
    9: "#870C25",  # Brown
}


def fmt_dur(seconds: float | None) -> str:
    """Formats duration in HH:MM:SS format matching Level._format_duration."""
    if seconds is None or seconds < 0:
        return "-"
    total_seconds = int(timedelta(seconds=int(seconds)).total_seconds())
    hours, remainder = divmod(total_seconds, 3600)
    minutes, secs = divmod(remainder, 60)
    return f"{hours:02}:{minutes:02}:{secs:02}"


def fmt_int(val: int | None) -> str:
    if val is None or val < 0:
        return "-"
    return f"{int(val):,}"


def fmt_float(val: float | None, decimals: int = 2) -> str:
    if val is None or val == float("inf"):
        return "-"
    return f"{float(val):.{decimals}f}"


def fmt_pct(num: int | float, den: int | float) -> str:
    if not den:
        return "0.0%"
    return f"{(float(num) / float(den)) * 100.0:.1f}%"


def parse_grid_str(grid_str: Any) -> list[list[int]] | None:
    """Parses a space/newline separated grid string or 2D list into a 2D list of ints."""
    if isinstance(grid_str, list):
        return grid_str
    if not isinstance(grid_str, str) or not grid_str.strip():
        return None
    try:
        rows = []
        for line in grid_str.strip().split("\n"):
            line = line.strip()
            if not line:
                continue
            rows.append([int(x) for x in line.split()])
        return rows if rows else None
    except Exception:
        return None


def compute_task_weight(task_data: dict[str, Any]) -> int:
    """Computes task weight matching geometor.seer.tasks.tasks.Task.weight."""
    weight = 0
    for pair in task_data.get("train", []):
        inp = pair.get("input", [])
        out = pair.get("output", [])
        if inp and isinstance(inp, list) and isinstance(inp[0], list):
            weight += len(inp) * len(inp[0])
        if out and isinstance(out, list) and isinstance(out[0], list):
            weight += len(out) * len(out[0])
    return weight


def safe_load_json(path: Path) -> Any:
    if not path.is_file():
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None


def safe_read_text(path: Path, max_bytes: int = 48000, max_chars: int | None = None) -> str:
    if not path.is_file():
        return ""
    limit = max_chars if max_chars is not None else max_bytes
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            text = f.read(limit + 1)
            if len(text) > limit:
                return text[:limit] + "\n\n... [truncated for display] ..."
            return text
    except Exception:
        return ""


def extract_response_info(resp_json: dict[str, Any] | None) -> dict[str, Any]:
    """Extracts tokens, response_time, model_version, retries, and fallback text from response.json."""
    info: dict[str, Any] = {
        "prompt_tokens": 0,
        "candidates_tokens": 0,
        "total_tokens": 0,
        "response_time": None,
        "attempts": 1,
        "model_version": None,
        "text": "",
    }
    if not isinstance(resp_json, dict):
        return info
    info["response_time"] = resp_json.get("response_time")
    info["model_version"] = resp_json.get("model_version")
    retries = resp_json.get("retries")
    if isinstance(retries, int):
        info["attempts"] = retries + 1

    usage = resp_json.get("usage_metadata", {})
    if isinstance(usage, dict) and usage:
        p_tok = usage.get("prompt_token_count", 0) or 0
        c_tok = usage.get("candidates_token_count", 0) or 0
        t_tok = usage.get("total_token_count", 0) or (p_tok + c_tok)
        info["prompt_tokens"] = p_tok
        info["candidates_tokens"] = c_tok
        info["total_tokens"] = t_tok

    # Extract candidate text if needed
    try:
        cands = resp_json.get("candidates", [])
        if cands and isinstance(cands, list):
            parts = cands[0].get("content", {}).get("parts", [])
            texts = []
            for p in parts:
                if isinstance(p, dict):
                    if "text" in p:
                        texts.append(p["text"])
                    elif "executable_code" in p:
                        code = p["executable_code"].get("code", "")
                        texts.append(f"\n```python\n{code}\n```\n")
                    elif "code_execution_result" in p:
                        out = p["code_execution_result"].get("output", "")
                        texts.append(f"\n```text\n{out}\n```\n")
            info["text"] = "".join(texts).strip()
    except Exception:
        pass
    return info


def normalize_trial_item(t: dict[str, Any]) -> dict[str, Any]:
    """Normalizes a single pair trial dict from modern or legacy trial JSON."""
    match_val = t.get("match")
    is_match = match_val is True
    err_str = t.get("error")
    if isinstance(match_val, str) and match_val.startswith("ERROR"):
        err_str = match_val
        is_match = False

    cnt_ok = t.get("color_count_correct")
    if cnt_ok is None:
        cnt_ok = t.get("correct_pixel_counts")

    actual_grid = parse_grid_str(t.get("transformed_output"))
    pct = t.get("percent_correct")
    if pct is None and is_match:
        pct = 100.0

    score = t.get("score")
    px_off = t.get("pixels_off")
    if score is None and px_off is not None:
        # Approximate score when legacy trial didn't store score
        score = float(px_off) + (0.0 if is_match else 1.0)

    return {
        "match": is_match,
        "score": round(float(score), 2) if isinstance(score, (int, float)) else None,
        "size_ok": t.get("size_correct"),
        "pal_ok": t.get("color_palette_correct"),
        "cnt_ok": cnt_ok,
        "px_off": px_off if isinstance(px_off, int) else None,
        "pct": round(float(pct), 1) if isinstance(pct, (int, float)) else None,
        "actual": actual_grid,
        "error": err_str,
    }


def parse_modern_step(
    step_dir: Path, suite_name: str, session_id: str, task_id: str
) -> dict[str, Any]:
    """Parses a modern/intermediate step directory (e.g., 000/, 001/)."""
    idx_data = safe_load_json(step_dir / "index.json") or safe_load_json(step_dir / "step_summary.json") or {}
    resp_json = safe_load_json(step_dir / "response.json")
    resp_info = extract_response_info(resp_json)

    step_name = step_dir.name
    raw_title = idx_data.get("title")
    if isinstance(raw_title, list):
        title = " • ".join(str(x) for x in raw_title if x)
    elif isinstance(raw_title, str):
        title = raw_title
    else:
        title = str(raw_title) if raw_title is not None else ""

    # Determine role/title if missing
    files_in_step = sorted([f for f in step_dir.iterdir() if f.is_file()])
    file_names = [f.name for f in files_in_step]

    has_py = any(f.name.endswith(".py") for f in files_in_step)
    has_yaml = any(f.name.endswith(".yaml") or f.name.endswith(".yml") for f in files_in_step)
    if not title or title == "Unknown Title":
        if has_py and step_name in ("001", "002"):
            title = "investigate • coder"
        elif has_yaml or step_name == "000":
            title = "investigate • dreamer"
        elif has_py:
            title = f"refine • coder ({step_name})"
        else:
            title = f"refine • dreamer ({step_name})"

    duration = idx_data.get("duration_seconds")
    if duration is None:
        duration = resp_info["response_time"]

    resp_meta = idx_data.get("response", {}) if isinstance(idx_data.get("response"), dict) else {}
    in_tok = resp_meta.get("prompt_tokens") or resp_info["prompt_tokens"] or 0
    out_tok = resp_meta.get("candidates_tokens") or resp_info["candidates_tokens"] or 0
    tot_tok = resp_meta.get("total_tokens") or resp_info["total_tokens"] or (in_tok + out_tok)

    attempts = idx_data.get("attempts") or resp_info["attempts"] or 1
    has_errors = bool(idx_data.get("has_errors", False)) or any(n.startswith("error_") for n in file_names)

    # Parse trials in this step
    trials_list: list[dict[str, Any]] = []
    trial_files = sorted([f for f in files_in_step if f.name.endswith(".trial.json") or f.name.endswith("trials.json")])
    for tf in trial_files:
        tdata = safe_load_json(tf)
        if not isinstance(tdata, dict):
            continue
        code_fname = tf.name[:-len(".trial.json")] if tf.name.endswith(".trial.json") else tf.name
        train_sec = tdata.get("train") or {}
        test_sec = tdata.get("test") or {}

        train_trials_raw = train_sec.get("trials") or [] if isinstance(train_sec, dict) else []
        test_trials_raw = test_sec.get("trials") or [] if isinstance(test_sec, dict) else []

        norm_train = [normalize_trial_item(x) for x in train_trials_raw if isinstance(x, dict)]
        norm_test = [normalize_trial_item(x) for x in test_trials_raw if isinstance(x, dict)]

        train_err = train_sec.get("error") if isinstance(train_sec, dict) else None
        test_err = test_sec.get("error") if isinstance(test_sec, dict) else None

        train_ok = bool(norm_train) and not train_err and all(x["match"] for x in norm_train)
        test_ok = (bool(norm_test) and not test_err and all(x["match"] for x in norm_test)) if norm_test else None

        tot_score = tdata.get("total_score")
        avg_score = tdata.get("average_score")
        if tot_score is None and norm_train:
            scores = [x["score"] for x in (norm_train + norm_test) if x["score"] is not None]
            if scores:
                tot_score = sum(scores)
                avg_score = tot_score / len(scores)

        trials_list.append({
            "trial_file": tf.name,
            "code_file": code_fname,
            "train_passed": train_ok,
            "test_passed": test_ok,
            "total_score": round(float(tot_score), 2) if isinstance(tot_score, (int, float)) else None,
            "avg_score": round(float(avg_score), 2) if isinstance(avg_score, (int, float)) else None,
            "train_error": train_err,
            "test_error": test_err,
            "train": norm_train,
            "test": norm_test,
        })

    # Determine step-level trial metrics
    train_passed = idx_data.get("train_passed")
    test_passed = idx_data.get("test_passed")
    best_score = idx_data.get("best_score")
    size_correct = idx_data.get("size_correct")
    palette_correct = idx_data.get("color_palette_correct")
    color_count_correct = idx_data.get("color_count_correct")
    pixels_off = idx_data.get("pixels_off")
    percent_correct = idx_data.get("percent_correct")

    if trials_list:
        if train_passed is None:
            train_passed = any(t["train_passed"] for t in trials_list)
        if test_passed is None:
            if any(t["test_passed"] is True for t in trials_list):
                test_passed = True
            elif any(t["test_passed"] is False for t in trials_list):
                test_passed = False
        # Pick best trial to fill missing metrics
        scored_trials = [t for t in trials_list if t["total_score"] is not None]
        best_t = min(scored_trials, key=lambda x: x["total_score"]) if scored_trials else trials_list[0]
        if best_score is None and best_t["total_score"] is not None:
            best_score = best_t["total_score"]
        all_pairs = best_t["train"] + best_t["test"]
        if all_pairs:
            if size_correct is None:
                size_correct = all(p["size_ok"] is True for p in all_pairs if p["size_ok"] is not None)
            if palette_correct is None:
                palette_correct = all(p["pal_ok"] is True for p in all_pairs if p["pal_ok"] is not None)
            if color_count_correct is None:
                color_count_correct = all(p["cnt_ok"] is True for p in all_pairs if p["cnt_ok"] is not None)
            if pixels_off is None:
                px_vals = [p["px_off"] for p in all_pairs if p["px_off"] is not None]
                if px_vals:
                    pixels_off = sum(px_vals)
            if percent_correct is None:
                pct_vals = [p["pct"] for p in all_pairs if p["pct"] is not None]
                if pct_vals:
                    percent_correct = sum(pct_vals) / len(pct_vals)

    # Collect readable step files (skip huge prompt_history.md / history.md)
    step_files_content: dict[str, str] = {}
    for f in files_in_step:
        fname = f.name
        if fname in ("prompt_history.md", "history.md", "response.json"):
            continue
        if fname == "prompt.md":
            step_files_content[fname] = safe_read_text(f, max_chars=10000)
        elif fname.endswith((".py", ".yaml", ".yml", ".md", ".txt")) or fname == "index.json":
            step_files_content[fname] = safe_read_text(f)
        elif fname.endswith(".png"):
            # Relative path from docs/suites/<suite>/<session>/<task_id>/index.html
            step_files_content[fname] = f"IMAGE:../../../../../{suite_name}/{session_id}/{task_id}/{step_name}/{fname}"

    if "response.md" not in step_files_content and resp_info["text"]:
        step_files_content["response.md"] = resp_info["text"]
        if "response.md" not in file_names:
            file_names.append("response.md")

    return {
        "step": step_name,
        "title": title,
        "duration_seconds": float(duration) if isinstance(duration, (int, float)) else None,
        "has_errors": has_errors,
        "attempts": attempts,
        "in_tokens": int(in_tok),
        "out_tokens": int(out_tok),
        "total_tokens": int(tot_tok),
        "train_passed": train_passed,
        "test_passed": test_passed,
        "best_score": round(float(best_score), 2) if isinstance(best_score, (int, float)) else None,
        "size_correct": size_correct,
        "palette_correct": palette_correct,
        "color_count_correct": color_count_correct,
        "pixels_off": int(pixels_off) if isinstance(pixels_off, (int, float)) else None,
        "percent_correct": round(float(percent_correct), 1) if isinstance(percent_correct, (int, float)) else None,
        "files_count": len(file_names),
        "file_list": file_names,
        "files": step_files_content,
        "trials": trials_list,
        "model": resp_info["model_version"],
    }


def parse_legacy_flat_task(
    task_dir: Path, suite_name: str, session_id: str, task_id: str
) -> list[dict[str, Any]]:
    """Parses flat task directories in sessions_001 into virtual steps (001, 002, ...)."""
    all_files = sorted([f for f in task_dir.iterdir() if f.is_file()])
    grouped: dict[str, list[Path]] = defaultdict(list)
    for f in all_files:
        m = re.match(r"^(\d{3})-(.+)$", f.name)
        if m:
            grouped[m.group(1)].append(f)

    steps: list[dict[str, Any]] = []
    for step_id in sorted(grouped.keys()):
        sfiles = grouped[step_id]
        fnames = [f.name for f in sfiles]

        resp_file = next((f for f in sfiles if f.name.endswith("-response.json")), None)
        resp_info = extract_response_info(safe_load_json(resp_file) if resp_file else None)

        py_files = [f for f in sfiles if f.name.endswith(".py")]
        yaml_files = [f for f in sfiles if f.name.endswith((".yaml", ".yml"))]

        if py_files:
            title = f"coder • step {step_id}"
        elif yaml_files:
            title = f"dreamer • step {step_id}"
        else:
            title = f"step {step_id}"

        trials_list: list[dict[str, Any]] = []
        for pyf in py_files:
            stem = pyf.stem  # e.g. 002-py_01
            train_jf = task_dir / f"{stem}-train.json"
            test_jf = task_dir / f"{stem}-test.json"
            train_raw = safe_load_json(train_jf) if train_jf.exists() else []
            test_raw = safe_load_json(test_jf) if test_jf.exists() else []

            norm_train = [normalize_trial_item(x) for x in (train_raw or []) if isinstance(x, dict)]
            norm_test = [normalize_trial_item(x) for x in (test_raw or []) if isinstance(x, dict)]

            if norm_train or norm_test:
                train_ok = bool(norm_train) and all(x["match"] for x in norm_train)
                test_ok = (bool(norm_test) and all(x["match"] for x in norm_test)) if norm_test else None
                scores = [x["score"] for x in (norm_train + norm_test) if x["score"] is not None]
                tot_score = sum(scores) if scores else None
                avg_score = (tot_score / len(scores)) if scores else None
                trials_list.append({
                    "trial_file": f"{stem}-train.json",
                    "code_file": pyf.name,
                    "train_passed": train_ok,
                    "test_passed": test_ok,
                    "total_score": round(float(tot_score), 2) if tot_score is not None else None,
                    "avg_score": round(float(avg_score), 2) if avg_score is not None else None,
                    "train_error": None,
                    "test_error": None,
                    "train": norm_train,
                    "test": norm_test,
                })

        train_passed = any(t["train_passed"] for t in trials_list) if trials_list else None
        test_passed = (
            True if any(t["test_passed"] is True for t in trials_list)
            else (False if any(t["test_passed"] is False for t in trials_list) else None)
        ) if trials_list else None

        best_score = None
        size_correct = None
        palette_correct = None
        color_count_correct = None
        pixels_off = None
        percent_correct = None

        if trials_list:
            best_t = trials_list[0]
            best_score = best_t["total_score"]
            all_p = best_t["train"] + best_t["test"]
            if all_p:
                size_correct = all(p["size_ok"] is True for p in all_p if p["size_ok"] is not None)
                palette_correct = all(p["pal_ok"] is True for p in all_p if p["pal_ok"] is not None)
                color_count_correct = all(p["cnt_ok"] is True for p in all_p if p["cnt_ok"] is not None)
                px_vals = [p["px_off"] for p in all_p if p["px_off"] is not None]
                if px_vals:
                    pixels_off = sum(px_vals)
                pct_vals = [p["pct"] for p in all_p if p["pct"] is not None]
                if pct_vals:
                    percent_correct = sum(pct_vals) / len(pct_vals)

        step_files_content: dict[str, str] = {}
        for f in sfiles:
            fname = f.name
            if fname.endswith(("-total_prompt.md", "-response.json", "-train.md", "-test.md")):
                continue
            if fname.endswith("-prompt.md"):
                step_files_content[fname] = safe_read_text(f, max_chars=8000)
            elif fname.endswith((".py", ".yaml", ".yml", ".md", ".txt")):
                step_files_content[fname] = safe_read_text(f)
            elif fname.endswith(".png"):
                step_files_content[fname] = f"IMAGE:../../../../../{suite_name}/{session_id}/{task_id}/{fname}"

        steps.append({
            "step": step_id,
            "title": title,
            "duration_seconds": float(resp_info["response_time"]) if isinstance(resp_info["response_time"], (int, float)) else None,
            "has_errors": False,
            "attempts": resp_info["attempts"],
            "in_tokens": int(resp_info["prompt_tokens"]),
            "out_tokens": int(resp_info["candidates_tokens"]),
            "total_tokens": int(resp_info["total_tokens"]),
            "train_passed": train_passed,
            "test_passed": test_passed,
            "best_score": best_score,
            "size_correct": size_correct,
            "palette_correct": palette_correct,
            "color_count_correct": color_count_correct,
            "pixels_off": pixels_off,
            "percent_correct": round(float(percent_correct), 1) if isinstance(percent_correct, (int, float)) else None,
            "files_count": len(fnames),
            "file_list": fnames,
            "files": step_files_content,
            "trials": trials_list,
            "model": resp_info["model_version"],
        })
    return steps

def parse_task_run(
    task_dir: Path,
    suite_name: str,
    session_id: str,
    puzzle_cache: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    """Parses a single task execution directory within a session."""
    task_id = task_dir.name
    task_json_path = task_dir / "task.json"
    if task_id not in puzzle_cache and task_json_path.exists():
        raw_task = safe_load_json(task_json_path)
        if isinstance(raw_task, dict):
            puzzle_cache[task_id] = {
                "id": task_id,
                "weight": compute_task_weight(raw_task),
                "n_train": len(raw_task.get("train", [])),
                "n_test": len(raw_task.get("test", [])),
                "train": raw_task.get("train", []),
                "test": raw_task.get("test", []),
            }

    puz_meta = puzzle_cache.get(
        task_id,
        {"id": task_id, "weight": 0, "n_train": 0, "n_test": 0, "train": [], "test": []},
    )

    idx_path = task_dir / "index.json"
    if not idx_path.exists():
        idx_path = task_dir / "summary_report.json"
    idx_data = safe_load_json(idx_path) if idx_path.exists() else {}
    if not isinstance(idx_data, dict):
        idx_data = {}

    step_dirs = sorted([d for d in task_dir.iterdir() if d.is_dir() and d.name.isdigit()])
    if step_dirs:
        steps = [
            parse_modern_step(sd, suite_name, session_id, task_id)
            for sd in step_dirs
        ]
    else:
        steps = parse_legacy_flat_task(task_dir, suite_name, session_id, task_id)

    steps_count = idx_data.get("steps") if isinstance(idx_data.get("steps"), int) else len(steps)

    dur = idx_data.get("duration_seconds")
    if not isinstance(dur, (int, float)):
        step_durs = [s["duration_seconds"] for s in steps if isinstance(s["duration_seconds"], (int, float))]
        dur = sum(step_durs) if step_durs else None

    has_errors = idx_data.get("has_errors")
    if not isinstance(has_errors, bool):
        has_errors = any(bool(s.get("has_errors")) for s in steps)

    trials_Block = idx_data.get("trials") if isinstance(idx_data.get("trials"), dict) else {}
    train_passed = trials_Block.get("train_passed")
    test_passed = trials_Block.get("test_passed")
    best_score = trials_Block.get("best_score")

    if not isinstance(train_passed, bool):
        step_tr = [s["train_passed"] for s in steps if s["train_passed"] is not None]
        train_passed = any(step_tr) if step_tr else None

    if not isinstance(test_passed, bool):
        step_te = [s["test_passed"] for s in steps if s["test_passed"] is not None]
        if any(x is True for x in step_te):
            test_passed = True
        elif any(x is False for x in step_te):
            test_passed = False
        else:
            test_passed = None

    if not isinstance(best_score, (int, float)):
        step_sc = [s["best_score"] for s in steps if isinstance(s["best_score"], (int, float))]
        best_score = min(step_sc) if step_sc else None

    tokens_block = idx_data.get("tokens") if isinstance(idx_data.get("tokens"), dict) else {}
    in_tok = tokens_block.get("prompt")
    out_tok = tokens_block.get("candidates")
    tot_tok = tokens_block.get("total")
    if not isinstance(tot_tok, (int, float)):
        in_tok = sum(s["in_tokens"] for s in steps)
        out_tok = sum(s["out_tokens"] for s in steps)
        tot_tok = sum(s["total_tokens"] for s in steps)

    resp_block = idx_data.get("responses") if isinstance(idx_data.get("responses"), dict) else {}
    attempts = resp_block.get("total_attempts")
    retries = resp_block.get("total_retries")
    if not isinstance(attempts, int):
        attempts = sum(s["attempts"] for s in steps)
    if not isinstance(retries, int):
        retries = max(0, attempts - len(steps))

    models = [s.get("model") for s in steps if s.get("model")]
    model_name = models[-1] if models else ""

    # Determine first step that passed train / test
    first_train_step = next((i + 1 for i, s in enumerate(steps) if s.get("train_passed") is True), None)
    first_test_step = next((i + 1 for i, s in enumerate(steps) if s.get("test_passed") is True), None)

    return {
        "suite": suite_name,
        "session_id": session_id,
        "task_id": task_id,
        "weight": puz_meta["weight"],
        "steps_count": steps_count,
        "duration_seconds": round(float(dur), 2) if isinstance(dur, (int, float)) else None,
        "has_errors": bool(has_errors),
        "train_passed": train_passed,
        "test_passed": test_passed,
        "best_score": round(float(best_score), 2) if isinstance(best_score, (int, float)) else None,
        "in_tokens": int(in_tok or 0),
        "out_tokens": int(out_tok or 0),
        "total_tokens": int(tot_tok or 0),
        "attempts": int(attempts or 0),
        "retries": int(retries or 0),
        "model": model_name,
        "first_train_step": first_train_step,
        "first_test_step": first_test_step,
        "steps": steps,
    }


def render_bool_cell(val: bool | None, invert_color: bool = False) -> tuple[str, str]:
    """Returns (html_content, sort_val) matching seer_navigator's ✓ / ✗ / - cells."""
    if val is True:
        cls = "status-bad" if invert_color else "status-good"
        return f'<span class="{cls}">✓</span>', "1"
    if val is False:
        cls = "status-good" if invert_color else "status-bad"
        return f'<span class="{cls}">✗</span>', "0"
    return '<span class="status-dim">-</span>', "-1"


def render_err_cell(has_err: bool | None) -> tuple[str, str]:
    """Matches seer_navigator Error column: '✗' in red if error, else '-'."""
    if has_err:
        return '<span class="status-bad">✗</span>', "1"
    return '<span class="status-dim">-</span>', "0"


def render_summary_panels(panels: list[list[tuple[str, str]]]) -> str:
    """Renders the 3-panel summary header table from seer_navigator."""
    cols_html = []
    for panel in panels:
        rows_html = []
        for k, v in panel:
            rows_html.append(
                f'<tr><td class="sum-key">{html.escape(str(k))}</td>'
                f'<td class="sum-val">{v}</td></tr>'
            )
        cols_html.append(
            f'<div class="summary-panel"><table class="summary-table">'
            f'{"".join(rows_html)}</table></div>'
        )
    return f'<section class="summary-grid">{"".join(cols_html)}</section>'


def page_shell(
    title: str,
    root_rel: str,
    active_nav: str,
    breadcrumbs: list[tuple[str, str | None]],
    body_html: str,
    prev_link: tuple[str, str] | None = None,
    next_link: tuple[str, str] | None = None,
    up_link: str | None = None,
) -> str:
    """Wraps page content in the unified GEOMETOR SEER Navigator HTML shell."""
    bc_parts = []
    for label, href in breadcrumbs:
        if href:
            bc_parts.append(f'<a href="{href}" class="bc-link">{html.escape(label)}</a>')
        else:
            bc_parts.append(f'<span class="bc-current">{html.escape(label)}</span>')
    bc_html = '<span class="bc-sep">/</span>'.join(bc_parts)

    sib_parts = []
    if up_link:
        sib_parts.append(f'<a href="{up_link}" id="nav-up-link" class="sib-btn" title="Up level (h / Backspace)">↑ Up</a>')
    if prev_link:
        sib_parts.append(
            f'<a href="{prev_link[1]}" id="nav-prev-link" class="sib-btn" title="Previous ([)">← {html.escape(prev_link[0])}</a>'
        )
    if next_link:
        sib_parts.append(
            f'<a href="{next_link[1]}" id="nav-next-link" class="sib-btn" title="Next (])">{html.escape(next_link[0])} →</a>'
        )
    sib_html = "".join(sib_parts)

    nav_items = [
        ("overview", "Overview", f"{root_rel}index.html"),
        ("sessions", "Sessions (475)", f"{root_rel}sessions/index.html"),
        ("tasks", "Tasks (2,939)", f"{root_rel}tasks/index.html"),
        ("retrospective", "SEER 1.0 Retrospective", f"{root_rel}retrospective/index.html"),
    ]
    nav_links_html = []
    for key, label, href in nav_items:
        cls = "topnav-link active" if key == active_nav else "topnav-link"
        nav_links_html.append(f'<a href="{href}" class="{cls}">{html.escape(label)}</a>')

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(title)} — GEOMETOR SEER Navigator</title>
  <link rel="stylesheet" href="{root_rel}_static/navigator.css">
</head>
<body>
  <header class="topbar">
    <div class="topbar-left">
      <a href="{root_rel}index.html" class="brand">GEOMETOR <span class="brand-accent">SEER</span></a>
      <nav class="breadcrumbs">{bc_html}</nav>
    </div>
    <div class="topbar-right">
      <div class="sibling-nav">{sib_html}</div>
      <nav class="topnav">{"".join(nav_links_html)}</nav>
    </div>
  </header>
  <main class="container">
    {body_html}
  </main>
  <footer class="statusbar">
    <div class="statusbar-left">
      <span><kbd>j</kbd>/<kbd>k</kbd> Navigate Rows</span>
      <span><kbd>Enter</kbd> Open</span>
      <span><kbd>h</kbd> Up</span>
      <span><kbd>[</kbd>/<kbd>]</kbd> Prev/Next</span>
      <span><kbd>v</kbd> Trial Split View</span>
      <span><kbd>1</kbd>-<kbd>4</kbd> Grid Mode</span>
      <span><kbd>/</kbd> Filter</span>
    </div>
    <div class="statusbar-right">
      GEOMETOR • SEER Sessions Archive
    </div>
  </footer>
  <script src="{root_rel}_static/navigator.js"></script>
</body>
</html>
"""


def write_static_assets(docs_dir: Path) -> None:
    """Writes .nojekyll, navigator.css, and navigator.js into docs/."""
    docs_dir.mkdir(parents=True, exist_ok=True)
    (docs_dir / ".nojekyll").write_text("", encoding="utf-8")
    static_dir = docs_dir / "_static"
    static_dir.mkdir(parents=True, exist_ok=True)

    css_content = """/* GEOMETOR SEER Navigator - Web UI */
:root {
  --bg-0: #0a0d12;
  --bg-1: #11161f;
  --bg-2: #171e2b;
  --bg-3: #1f293a;
  --bg-hover: #253247;
  --bg-active: #1e3a5f;
  --border: #2a364b;
  --border-bright: #3d506e;
  --text-0: #e6edf3;
  --text-1: #9da7b3;
  --text-dim: #636e7b;
  --accent: #d4af37; /* GEOMETOR gold */
  --accent-cyan: #58a6ff;
  --good: #3fb950;
  --bad: #f85149;
  --warn: #d29922;
  --font-mono: "JetBrains Mono", "Fira Code", "SFMono-Regular", Consolas, "Liberation Mono", Menlo, monospace;
  --font-sans: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif;
}

* {
  box-sizing: border-box;
}

body {
  margin: 0;
  padding: 0 0 36px 0;
  background-color: var(--bg-0);
  color: var(--text-0);
  font-family: var(--font-mono);
  font-size: 13px;
  line-height: 1.45;
}

a {
  color: var(--accent-cyan);
  text-decoration: none;
}
a:hover {
  text-decoration: underline;
  color: #79c0ff;
}

/* Top Header Bar */
.topbar {
  position: sticky;
  top: 0;
  z-index: 100;
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 8px;
  padding: 8px 16px;
  background: var(--bg-1);
  border-bottom: 1px solid var(--border);
}

.topbar-left, .topbar-right {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}

.brand {
  font-weight: 700;
  font-size: 14px;
  letter-spacing: 0.08em;
  color: var(--text-0);
  padding-right: 8px;
  border-right: 1px solid var(--border);
}
.brand:hover {
  text-decoration: none;
}
.brand-accent {
  color: var(--accent);
}

.breadcrumbs {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12.5px;
}
.bc-sep {
  color: var(--text-dim);
}
.bc-link {
  color: var(--accent-cyan);
}
.bc-current {
  color: var(--text-0);
  font-weight: 600;
}

.sibling-nav {
  display: flex;
  gap: 6px;
}
.sib-btn {
  background: var(--bg-2);
  border: 1px solid var(--border);
  color: var(--text-0);
  padding: 3px 8px;
  border-radius: 4px;
  font-size: 11.5px;
}
.sib-btn:hover {
  background: var(--bg-hover);
  text-decoration: none;
  border-color: var(--border-bright);
}

.topnav {
  display: flex;
  gap: 4px;
}
.topnav-link {
  padding: 4px 10px;
  border-radius: 4px;
  color: var(--text-1);
  font-size: 12px;
  border: 1px solid transparent;
}
.topnav-link:hover {
  color: var(--text-0);
  background: var(--bg-2);
  text-decoration: none;
}
.topnav-link.active {
  color: var(--accent);
  background: var(--bg-2);
  border-color: var(--border);
  font-weight: 600;
}

/* Main Container */
.container {
  max-width: 1720px;
  margin: 0 auto;
  padding: 12px 16px;
}

/* 3-Panel Summary Header (Matches seer_navigator Horizontal Summary) */
.summary-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 10px;
  margin-bottom: 12px;
}
@media (max-width: 960px) {
  .summary-grid {
    grid-template-columns: 1fr;
  }
}

.summary-panel {
  background: var(--bg-1);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 8px 12px;
}

.summary-table {
  width: 100%;
  border-collapse: collapse;
}
.summary-table td {
  padding: 2px 4px;
  font-size: 12.5px;
}
.sum-key {
  color: var(--text-1);
  text-align: right;
  padding-right: 12px !important;
  width: 48%;
  white-space: nowrap;
}
.sum-val {
  color: var(--text-0);
  font-weight: 600;
  text-align: left;
}

/* Status Colors */
.status-good {
  color: var(--good);
  font-weight: 700;
}
.status-bad {
  color: var(--bad);
  font-weight: 700;
}
.status-warn {
  color: var(--warn);
  font-weight: 700;
}
.status-dim {
  color: var(--text-dim);
}

/* Filter & Toolbar Bar */
.toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  background: var(--bg-1);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 8px 12px;
  margin-bottom: 10px;
}

.toolbar-group {
  display: flex;
  align-items: center;
  gap: 8px;
  flex-wrap: wrap;
}

.search-input, .select-input {
  background: var(--bg-0);
  color: var(--text-0);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 4px 8px;
  font-family: var(--font-mono);
  font-size: 12px;
}
.search-input:focus, .select-input:focus {
  outline: none;
  border-color: var(--accent-cyan);
}

.btn, .filter-btn {
  background: var(--bg-2);
  color: var(--text-1);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 4px 9px;
  font-family: var(--font-mono);
  font-size: 12px;
  cursor: pointer;
}
.btn:hover, .filter-btn:hover {
  background: var(--bg-hover);
  color: var(--text-0);
}
.btn.active, .filter-btn.active {
  background: var(--bg-active);
  color: var(--text-0);
  border-color: var(--accent-cyan);
  font-weight: 600;
}

.badge {
  display: inline-block;
  padding: 2px 7px;
  border-radius: 3px;
  font-size: 11px;
  background: var(--bg-2);
  border: 1px solid var(--border);
  color: var(--text-1);
}

/* DataTables (Matches Textual DataTable) */
.table-wrap {
  background: var(--bg-1);
  border: 1px solid var(--border);
  border-radius: 4px;
  overflow-x: auto;
  margin-bottom: 14px;
}

.nav-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 12.5px;
}

.nav-table th {
  position: sticky;
  top: 0;
  background: var(--bg-2);
  color: var(--accent);
  font-weight: 600;
  padding: 6px 10px;
  border-bottom: 1px solid var(--border-bright);
  cursor: pointer;
  user-select: none;
  white-space: nowrap;
  text-align: left;
}
.nav-table th:hover {
  background: var(--bg-3);
}
.nav-table th.num, .nav-table td.num {
  text-align: right;
  font-variant-numeric: tabular-nums;
}
.nav-table th.center, .nav-table td.center {
  text-align: center;
}

.nav-table td {
  padding: 5px 10px;
  border-bottom: 1px solid var(--border);
  white-space: nowrap;
}

.nav-table tbody tr {
  cursor: pointer;
}
.nav-table tbody tr:nth-child(even) {
  background: rgba(255, 255, 255, 0.015);
}
.nav-table tbody tr:hover {
  background: var(--bg-hover);
}
.nav-table tbody tr.selected-row {
  background: var(--bg-active) !important;
  outline: 1px solid var(--accent-cyan);
}

/* Collapsible Panels */
details.nav-panel {
  background: var(--bg-1);
  border: 1px solid var(--border);
  border-radius: 4px;
  margin-bottom: 12px;
}
details.nav-panel > summary {
  padding: 8px 12px;
  cursor: pointer;
  font-weight: 600;
  color: var(--accent);
  background: var(--bg-2);
  border-radius: 4px;
  user-select: none;
}
details.nav-panel[open] > summary {
  border-bottom: 1px solid var(--border);
  border-radius: 4px 4px 0 0;
}
.panel-body {
  padding: 12px;
}

/* Puzzle Ground-Truth Pairs Row */
.pairs-scroll {
  display: flex;
  gap: 16px;
  overflow-x: auto;
  padding-bottom: 6px;
}
.pair-card {
  background: var(--bg-0);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 8px 10px;
  flex: 0 0 auto;
}
.pair-card-title {
  font-size: 11.5px;
  font-weight: 600;
  color: var(--accent);
  margin-bottom: 6px;
  display: flex;
  justify-content: space-between;
  gap: 8px;
}
.pair-grids-row {
  display: flex;
  align-items: center;
  gap: 10px;
}
.pair-arrow {
  color: var(--text-dim);
  font-size: 16px;
}

/* ARC Grid Rendering (Matches geometor.seer.tasks.grid) */
.grid-box {
  display: inline-flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 4px;
}
.grid-meta {
  font-size: 11px;
  color: var(--text-1);
}
.arc-grid {
  border-collapse: collapse;
  border: 1px solid #3a4659;
  background: #000;
}
.arc-grid td {
  padding: 0;
  border: 1px solid #222a36;
  text-align: center;
  vertical-align: middle;
  font-size: 10px;
  line-height: 1;
  font-weight: 700;
}
.arc-grid.mode-solid td {
  width: 16px;
  height: 16px;
  color: transparent;
}
.arc-grid.mode-char td {
  width: 18px;
  height: 18px;
  color: rgba(255, 255, 255, 0.92);
  text-shadow: 0 0 2px #000, 0 0 3px #000;
}
.arc-grid.mode-tiny td {
  width: 9px;
  height: 9px;
  color: transparent;
  border-width: 0.5px;
}
.arc-grid.mode-diff td {
  width: 17px;
  height: 17px;
  color: transparent;
}
.arc-grid.mode-diff td.cell-mismatch {
  outline: 2px solid #ff00ff;
  outline-offset: -2px;
  color: #fff;
  text-shadow: 0 0 3px #000;
}

/* Split Viewers (TrialSplitViewScreen & StepScreen) */
.inspector-wrapper {
  background: var(--bg-1);
  border: 1px solid var(--border);
  border-radius: 4px;
  margin-top: 12px;
}
.inspector-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 10px;
  padding: 8px 12px;
  background: var(--bg-2);
  border-bottom: 1px solid var(--border);
}

.split-50-50 {
  display: grid;
  grid-template-columns: 1fr 1fr;
  min-height: 540px;
}
.split-30-70 {
  display: grid;
  grid-template-columns: 280px 1fr;
  min-height: 500px;
}
@media (max-width: 1100px) {
  .split-50-50, .split-30-70 {
    grid-template-columns: 1fr;
  }
}

.pane-left {
  border-right: 1px solid var(--border);
  overflow: auto;
  max-height: 780px;
}
.pane-right {
  overflow: auto;
  max-height: 780px;
  padding: 10px 12px;
}

.code-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 6px 12px;
  background: var(--bg-0);
  border-bottom: 1px solid var(--border);
  font-size: 12px;
  color: var(--accent);
}

pre.code-block {
  margin: 0;
  padding: 10px 12px;
  font-family: var(--font-mono);
  font-size: 12px;
  line-height: 1.45;
  color: var(--text-0);
  background: var(--bg-0);
  overflow-x: auto;
  white-space: pre;
}

/* TrialViewer 4-Column Row (Details, Input, Expected, Actual) */
.trial-set-heading {
  font-size: 13px;
  font-weight: 700;
  color: var(--accent);
  padding: 4px 8px;
  background: var(--bg-2);
  border-left: 3px solid var(--accent);
  margin: 8px 0;
}

.trial-pair-row {
  display: grid;
  grid-template-columns: 165px repeat(3, minmax(120px, auto));
  gap: 12px;
  align-items: start;
  padding: 10px;
  margin-bottom: 10px;
  background: var(--bg-0);
  border: 1px solid var(--border);
  border-radius: 4px;
  overflow-x: auto;
}

.trial-details-table {
  width: 100%;
  border-collapse: collapse;
  font-size: 11.5px;
}
.trial-details-table th {
  text-align: left;
  color: var(--accent);
  padding-bottom: 4px;
  border-bottom: 1px solid var(--border);
}
.trial-details-table td {
  padding: 2px 4px;
}
.trial-details-table td:first-child {
  color: var(--text-1);
  text-align: right;
  padding-right: 8px;
}
.trial-details-table td:last-child {
  font-weight: 600;
}

/* File list in StepScreen */
.file-list {
  list-style: none;
  margin: 0;
  padding: 0;
}
.file-list li {
  padding: 7px 12px;
  border-bottom: 1px solid var(--border);
  cursor: pointer;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.file-list li:hover {
  background: var(--bg-hover);
}
.file-list li.active {
  background: var(--bg-active);
  color: var(--accent);
  font-weight: 600;
}

/* Tabs */
.tab-bar {
  display: flex;
  gap: 6px;
  margin-bottom: 10px;
}

/* Prose / Retrospective Content */
.prose-card {
  background: var(--bg-1);
  border: 1px solid var(--border);
  border-radius: 4px;
  padding: 20px 28px;
  margin-bottom: 16px;
  font-family: var(--font-sans);
  font-size: 14.5px;
  line-height: 1.65;
}
.prose-card h1, .prose-card h2, .prose-card h3 {
  font-family: var(--font-mono);
  color: var(--accent);
  margin-top: 1.2em;
  margin-bottom: 0.5em;
}
.prose-card h1 {
  margin-top: 0;
  font-size: 22px;
  border-bottom: 1px solid var(--border);
  padding-bottom: 8px;
}
.prose-card h2 {
  font-size: 17px;
}
.prose-card code {
  font-family: var(--font-mono);
  background: var(--bg-0);
  padding: 2px 5px;
  border-radius: 3px;
  font-size: 13px;
}

/* Footer Status Bar */
.statusbar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  z-index: 100;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 5px 16px;
  background: var(--bg-2);
  border-top: 1px solid var(--border);
  font-size: 11.5px;
  color: var(--text-1);
}
.statusbar-left {
  display: flex;
  gap: 14px;
  flex-wrap: wrap;
}
kbd {
  background: var(--bg-0);
  border: 1px solid var(--border-bright);
  border-radius: 3px;
  padding: 1px 5px;
  font-size: 10.5px;
  color: var(--accent);
}
"""
    (static_dir / "navigator.css").write_text(css_content, encoding="utf-8")

    js_content = """/* GEOMETOR SEER Navigator - Client Interactive Engine */
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
    const lines = str.trim().split(/\\r?\\n/).filter(Boolean);
    return lines.map(line => line.trim().split(/\\s+/).map(Number));
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
        '<table class="arc-grid mode-' + gmode + '" data-grid-raw=\'' + JSON.stringify(matrix) + '\'' +
        (expected ? ' data-grid-exp=\'' + JSON.stringify(expected) + '\'' : '') + '>' +
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
        if (codeEl) codeEl.textContent = mainFile ? stepObj.files[mainFile] : "# No Python trials executed in this step (e.g. Dreamer observation step).\\n# Switch to 'Step Files Inspector' or select a Coder step.";
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
"""
    (static_dir / "navigator.js").write_text(js_content, encoding="utf-8")


def render_grid_mode_toolbar_html() -> str:
    return (
        '<div class="toolbar-group">'
        '<span class="status-dim" style="font-size:11.5px;">Grid Renderer:</span>'
        '<button type="button" class="btn grid-mode-btn active" data-mode="solid">Solid [1]</button>'
        '<button type="button" class="btn grid-mode-btn" data-mode="char">Char [2]</button>'
        '<button type="button" class="btn grid-mode-btn" data-mode="tiny">Tiny [3]</button>'
        '<button type="button" class="btn grid-mode-btn" data-mode="diff">Diff [4]</button>'
        '</div>'
    )


def get_row_status_tags(train_passed: bool | None, test_passed: bool | None, has_errors: bool | None) -> str:
    tags = []
    if test_passed is True:
        tags.append("test-pass")
    elif train_passed is True:
        tags.append("train-only")
    else:
        tags.append("failed")
    if has_errors:
        tags.append("errors")
    return " ".join(tags)


def build_task_run_page(
    docs_dir: Path,
    task_run: dict[str, Any],
    puzzle_meta: dict[str, Any],
    prev_task_id: str | None,
    next_task_id: str | None,
) -> None:
    """Generates docs/suites/<suite>/<session>/<task_id>/index.html (TaskScreen + StepScreen + TrialSplitViewScreen)."""
    suite = task_run["suite"]
    sess_id = task_run["session_id"]
    tid = task_run["task_id"]

    out_dir = docs_dir / "suites" / suite / sess_id / tid
    out_dir.mkdir(parents=True, exist_ok=True)
    root_rel = "../../../../"

    tr_html, _ = render_bool_cell(task_run["train_passed"])
    te_html, _ = render_bool_cell(task_run["test_passed"])
    err_html, _ = render_err_cell(task_run["has_errors"])

    panels = [
        [
            ("Train", tr_html),
            ("Test", te_html),
            ("Best Score", fmt_float(task_run["best_score"])),
            ("Weight", fmt_int(task_run["weight"])),
        ],
        [
            ("Duration", fmt_dur(task_run["duration_seconds"])),
            ("Steps", fmt_int(task_run["steps_count"])),
            ("Error", err_html),
            ("Model", html.escape(task_run.get("model") or "-")),
        ],
        [
            ("Tokens", fmt_int(task_run["total_tokens"])),
            ("In Tokens", fmt_int(task_run["in_tokens"])),
            ("Out Tokens", fmt_int(task_run["out_tokens"])),
            ("Retries", fmt_int(task_run["retries"])),
        ],
    ]
    summary_html = render_summary_panels(panels)

    # Top action bar linking to global Task Across Sessions view
    toolbar_html = f"""
    <div class="toolbar">
      <div class="toolbar-group">
        <a href="{root_rel}tasks/{tid}/index.html" class="btn" style="color:var(--accent);border-color:var(--accent);">
          ⇄ View All Sessions for Task {html.escape(tid)}
        </a>
        <span class="badge">{len(task_run["steps"])} Steps</span>
      </div>
      {render_grid_mode_toolbar_html()}
    </div>
    """

    # Ground-truth puzzle collapsible panel
    puzzle_panel_html = f"""
    <details class="nav-panel">
      <summary>Puzzle Specification: {html.escape(tid)} ({puzzle_meta.get("n_train", 0)} Train, {puzzle_meta.get("n_test", 0)} Test, Weight {puzzle_meta.get("weight", 0)})</summary>
      <div class="panel-body" id="puzzle-grids-container"></div>
    </details>
    """

    # 16-column Steps Table matching TaskScreen in seer_navigator
    step_rows_html = []
    for st in task_run["steps"]:
        s_err_h, s_err_s = render_err_cell(st["has_errors"])
        s_tr_h, s_tr_s = render_bool_cell(st["train_passed"])
        s_te_h, s_te_s = render_bool_cell(st["test_passed"])
        s_sz_h, s_sz_s = render_bool_cell(st["size_correct"])
        s_pal_h, s_pal_s = render_bool_cell(st["palette_correct"])
        s_cnt_h, s_cnt_s = render_bool_cell(st["color_count_correct"])

        dur_val = st["duration_seconds"]
        dur_sort = str(dur_val) if dur_val is not None else ""
        sc_val = st["best_score"]
        sc_sort = str(sc_val) if sc_val is not None else ""
        px_val = st["pixels_off"]
        px_sort = str(px_val) if px_val is not None else ""
        pct_val = st["percent_correct"]
        pct_sort = str(pct_val) if pct_val is not None else ""

        step_rows_html.append(
            f"<tr>"
            f'<td><strong>{html.escape(st["step"])}</strong></td>'
            f'<td>{html.escape(st["title"])}</td>'
            f'<td class="num" data-sort="{dur_sort}">{fmt_dur(dur_val)}</td>'
            f'<td class="center" data-sort="{s_err_s}">{s_err_h}</td>'
            f'<td class="num" data-sort="{st["attempts"]}">{fmt_int(st["attempts"])}</td>'
            f'<td class="num" data-sort="{st["in_tokens"]}">{fmt_int(st["in_tokens"])}</td>'
            f'<td class="num" data-sort="{st["out_tokens"]}">{fmt_int(st["out_tokens"])}</td>'
            f'<td class="num" data-sort="{st["total_tokens"]}">{fmt_int(st["total_tokens"])}</td>'
            f'<td class="center" data-sort="{s_tr_s}">{s_tr_h}</td>'
            f'<td class="center" data-sort="{s_te_s}">{s_te_h}</td>'
            f'<td class="num" data-sort="{sc_sort}">{fmt_float(sc_val)}</td>'
            f'<td class="center" data-sort="{s_sz_s}">{s_sz_h}</td>'
            f'<td class="center" data-sort="{s_pal_s}">{s_pal_h}</td>'
            f'<td class="center" data-sort="{s_cnt_s}">{s_cnt_h}</td>'
            f'<td class="num" data-sort="{px_sort}">{fmt_int(px_val)}</td>'
            f'<td class="num" data-sort="{pct_sort}">{fmt_float(pct_val, 1)}</td>'
            f"</tr>"
        )

    steps_table_html = f"""
    <div class="table-wrap">
      <table class="nav-table" id="steps-table">
        <thead>
          <tr>
            <th>Step</th>
            <th>Title</th>
            <th class="num">Duration</th>
            <th class="center">Err</th>
            <th class="num">Att</th>
            <th class="num">In</th>
            <th class="num">Out</th>
            <th class="num">Tot</th>
            <th class="center">Train</th>
            <th class="center">Test</th>
            <th class="num">Score</th>
            <th class="center">Size</th>
            <th class="center">Pal</th>
            <th class="center">Cnt</th>
            <th class="num">Px Off</th>
            <th class="num">%</th>
          </tr>
        </thead>
        <tbody>
          {"".join(step_rows_html)}
        </tbody>
      </table>
    </div>
    """

    # Interactive Step & Trial Split Inspector
    inspector_html = """
    <section class="inspector-wrapper">
      <div class="inspector-header">
        <div class="toolbar-group">
          <button type="button" id="tab-btn-trial-split" class="btn active">Trial Split View [v]</button>
          <button type="button" id="tab-btn-step-files" class="btn">Step Files Inspector</button>
          <span id="inspector-step-label" class="badge">Step</span>
        </div>
        <div class="toolbar-group">
          <label for="trial-selector" class="status-dim" style="font-size:11.5px;">Trial:</label>
          <select id="trial-selector" class="select-input"></select>
          <button type="button" id="btn-prev-trial" class="btn" title="Previous Trial">← Prev Trial</button>
          <button type="button" id="btn-next-trial" class="btn" title="Next Trial">Next Trial →</button>
        </div>
      </div>

      <!-- TrialSplitViewScreen (50% Python Code / 50% TrialViewer) -->
      <div id="inspector-trial-split" class="split-50-50">
        <div class="pane-left">
          <div class="code-header" id="trial-split-code-title">code.py</div>
          <pre class="code-block" id="trial-split-code"></pre>
        </div>
        <div class="pane-right" id="trial-split-viewer"></div>
      </div>

      <!-- StepScreen (30% File List / 70% Content Viewer) -->
      <div id="inspector-step-files" class="split-30-70" style="display:none;">
        <div class="pane-left">
          <ul class="file-list" id="step-files-list"></ul>
        </div>
        <div class="pane-right" style="padding:0;">
          <div class="code-header" id="step-file-content-title">File</div>
          <div id="step-file-content-body"></div>
        </div>
      </div>
    </section>
    """

    run_payload = {
        "suite": suite,
        "session_id": sess_id,
        "task_id": tid,
        "puzzle": {
            "train": puzzle_meta.get("train", []),
            "test": puzzle_meta.get("test", []),
        },
        "steps": task_run["steps"],
    }
    # Escape </script> inside JSON just in case code contains it
    run_json_str = json.dumps(run_payload, ensure_ascii=False).replace("</", "<\\/")
    puz_json_str = json.dumps(
        {"train": puzzle_meta.get("train", []), "test": puzzle_meta.get("test", [])},
        ensure_ascii=False,
    ).replace("</", "<\\/")

    body_html = (
        summary_html
        + toolbar_html
        + puzzle_panel_html
        + steps_table_html
        + inspector_html
        + f'<script id="puzzle-data" type="application/json">{puz_json_str}</script>'
        + f'<script id="run-data" type="application/json">{run_json_str}</script>'
    )

    prev_link = (prev_task_id, f"../{prev_task_id}/index.html") if prev_task_id else None
    next_link = (next_task_id, f"../{next_task_id}/index.html") if next_task_id else None

    full_html = page_shell(
        title=f"{tid} • {sess_id}",
        root_rel=root_rel,
        active_nav="sessions",
        breadcrumbs=[
            ("Suites", f"{root_rel}index.html"),
            (suite, f"../../index.html"),
            (sess_id, f"../index.html"),
            (tid, None),
        ],
        body_html=body_html,
        prev_link=prev_link,
        next_link=next_link,
        up_link="../index.html",
    )
    (out_dir / "index.html").write_text(full_html, encoding="utf-8")


def build_session_page(
    docs_dir: Path,
    session_summary: dict[str, Any],
    prev_sess_id: str | None,
    next_sess_id: str | None,
) -> None:
    """Generates docs/suites/<suite>/<session>/index.html (SessionScreen)."""
    suite = session_summary["suite"]
    sess_id = session_summary["session_id"]
    out_dir = docs_dir / "suites" / suite / sess_id
    out_dir.mkdir(parents=True, exist_ok=True)
    root_rel = "../../../"

    tasks = session_summary["task_runs"]
    t_cnt = len(tasks)
    tr_cnt = session_summary["train_passed"]
    te_cnt = session_summary["test_passed"]

    panels = [
        [
            ("Tasks", fmt_int(t_cnt)),
            ("Train", f'{tr_cnt} ({fmt_pct(tr_cnt, t_cnt)})'),
            ("Test", f'{te_cnt} ({fmt_pct(te_cnt, t_cnt)})'),
        ],
        [
            ("Duration", fmt_dur(session_summary["duration_seconds"])),
            ("Avg", fmt_dur(session_summary["avg_duration"])),
            ("Errors", fmt_int(session_summary["errors"])),
            ("Description", html.escape(session_summary["description"] or "-")),
        ],
        [
            ("Tokens", fmt_int(session_summary["total_tokens"])),
            ("In Tokens", fmt_int(session_summary["in_tokens"])),
            ("Out Tokens", fmt_int(session_summary["out_tokens"])),
            ("Retries", fmt_int(session_summary["retries"])),
        ],
    ]
    summary_html = render_summary_panels(panels)

    # Optional Session Context / Config collapsible panel
    ctx_parts = []
    for fname, ftext in session_summary.get("context_files", {}).items():
        ctx_parts.append(
            f'<div style="margin-bottom:10px;"><div class="code-header">{html.escape(fname)}</div>'
            f'<pre class="code-block" style="max-height:260px;overflow:auto;">{html.escape(ftext)}</pre></div>'
        )
    ctx_panel_html = ""
    if ctx_parts:
        ctx_panel_html = (
            f'<details class="nav-panel">'
            f'<summary>Session Configuration & System Prompts ({len(ctx_parts)} files)</summary>'
            f'<div class="panel-body">{"".join(ctx_parts)}</div>'
            f'</details>'
        )

    toolbar_html = f"""
    <div class="toolbar">
      <div class="toolbar-group">
        <input type="text" id="table-search" class="search-input" placeholder="Filter tasks (/) ...">
        <button type="button" class="filter-btn status-filter-btn active" data-filter="all">All ({t_cnt})</button>
        <button type="button" class="filter-btn status-filter-btn" data-filter="test-pass">Test ✓ ({te_cnt})</button>
        <button type="button" class="filter-btn status-filter-btn" data-filter="train-only">Train Only ({max(0, tr_cnt - te_cnt)})</button>
        <button type="button" class="filter-btn status-filter-btn" data-filter="failed">Failed ✗ ({t_cnt - tr_cnt})</button>
        <button type="button" class="filter-btn status-filter-btn" data-filter="errors">Errors ({session_summary["errors"]})</button>
      </div>
      <div class="toolbar-group">
        <span id="visible-row-count" class="badge">{t_cnt} / {t_cnt} rows</span>
      </div>
    </div>
    """

    rows_html = []
    for tr in tasks:
        tid = tr["task_id"]
        err_h, err_s = render_err_cell(tr["has_errors"])
        tr_h, tr_s = render_bool_cell(tr["train_passed"])
        te_h, te_s = render_bool_cell(tr["test_passed"])
        dur_s = str(tr["duration_seconds"]) if tr["duration_seconds"] is not None else ""
        sc_s = str(tr["best_score"]) if tr["best_score"] is not None else ""
        status_tags = get_row_status_tags(tr["train_passed"], tr["test_passed"], tr["has_errors"])

        rows_html.append(
            f'<tr data-href="{tid}/index.html" data-status="{status_tags}">'
            f'<td><a href="{tid}/index.html"><strong>{html.escape(tid)}</strong></a> '
            f'<a href="{root_rel}tasks/{tid}/index.html" title="View all sessions for {html.escape(tid)}" style="color:var(--text-dim);font-size:11px;">[⇄]</a></td>'
            f'<td class="num" data-sort="{tr["weight"]}">{fmt_int(tr["weight"])}</td>'
            f'<td class="num" data-sort="{tr["steps_count"]}">{fmt_int(tr["steps_count"])}</td>'
            f'<td class="num" data-sort="{dur_s}">{fmt_dur(tr["duration_seconds"])}</td>'
            f'<td class="center" data-sort="{err_s}">{err_h}</td>'
            f'<td class="center" data-sort="{tr_s}">{tr_h}</td>'
            f'<td class="center" data-sort="{te_s}">{te_h}</td>'
            f'<td class="num" data-sort="{sc_s}">{fmt_float(tr["best_score"])}</td>'
            f'<td class="num" data-sort="{tr["total_tokens"]}">{fmt_int(tr["total_tokens"])}</td>'
            f'<td class="num" data-sort="{tr["attempts"]}">{fmt_int(tr["attempts"])}</td>'
            f'<td class="num" data-sort="{tr["retries"]}">{fmt_int(tr["retries"])}</td>'
            f'</tr>'
        )

    table_html = f"""
    <div class="table-wrap">
      <table class="nav-table filterable-table">
        <thead>
          <tr>
            <th>Task ID</th>
            <th class="num">Weight</th>
            <th class="num">Steps</th>
            <th class="num">Duration</th>
            <th class="center">Err</th>
            <th class="center">Train</th>
            <th class="center">Test</th>
            <th class="num">Score</th>
            <th class="num">Tokens</th>
            <th class="num">Attempts</th>
            <th class="num">Retries</th>
          </tr>
        </thead>
        <tbody>
          {"".join(rows_html)}
        </tbody>
      </table>
    </div>
    """

    prev_link = (prev_sess_id, f"../{prev_sess_id}/index.html") if prev_sess_id else None
    next_link = (next_sess_id, f"../{next_sess_id}/index.html") if next_sess_id else None

    full_html = page_shell(
        title=f"{sess_id} • {suite}",
        root_rel=root_rel,
        active_nav="sessions",
        breadcrumbs=[
            ("Suites", f"{root_rel}index.html"),
            (suite, "../index.html"),
            (sess_id, None),
        ],
        body_html=summary_html + ctx_panel_html + toolbar_html + table_html,
        prev_link=prev_link,
        next_link=next_link,
        up_link="../index.html",
    )
    (out_dir / "index.html").write_text(full_html, encoding="utf-8")


def build_suite_page(
    docs_dir: Path,
    suite_summary: dict[str, Any],
    prev_suite: str | None,
    next_suite: str | None,
) -> None:
    """Generates docs/suites/<suite>/index.html (SessionsScreen scoped to suite)."""
    suite = suite_summary["suite"]
    out_dir = docs_dir / "suites" / suite
    out_dir.mkdir(parents=True, exist_ok=True)
    root_rel = "../../"

    sessions = suite_summary["sessions"]
    s_cnt = len(sessions)
    t_cnt = suite_summary["tasks_count"]
    tr_cnt = suite_summary["train_passed"]
    te_cnt = suite_summary["test_passed"]

    panels = [
        [
            ("Sessions", fmt_int(s_cnt)),
            ("Tasks", fmt_int(t_cnt)),
            ("Train", f'{tr_cnt} ({fmt_pct(tr_cnt, t_cnt)})'),
            ("Test", f'{te_cnt} ({fmt_pct(te_cnt, t_cnt)})'),
        ],
        [
            ("Duration", fmt_dur(suite_summary["duration_seconds"])),
            ("Avg", fmt_dur(suite_summary["avg_duration"])),
            ("Errors", fmt_int(suite_summary["errors"])),
            ("Best Score", fmt_float(suite_summary["best_score"])),
        ],
        [
            ("Tokens", fmt_int(suite_summary["total_tokens"])),
            ("In Tokens", fmt_int(suite_summary["in_tokens"])),
            ("Out Tokens", fmt_int(suite_summary["out_tokens"])),
            ("Retries", fmt_int(suite_summary["retries"])),
        ],
    ]
    summary_html = render_summary_panels(panels)

    toolbar_html = f"""
    <div class="toolbar">
      <div class="toolbar-group">
        <input type="text" id="table-search" class="search-input" placeholder="Filter sessions in {html.escape(suite)} (/) ...">
      </div>
      <div class="toolbar-group">
        <span id="visible-row-count" class="badge">{s_cnt} / {s_cnt} sessions</span>
      </div>
    </div>
    """

    rows_html = []
    for s in sessions:
        sid = s["session_id"]
        st_cnt = s["tasks_count"]
        str_cnt = s["train_passed"]
        ste_cnt = s["test_passed"]
        tr_pct_val = (str_cnt / st_cnt * 100.0) if st_cnt else 0.0
        te_pct_val = (ste_cnt / st_cnt * 100.0) if st_cnt else 0.0
        dur_s = str(s["duration_seconds"]) if s["duration_seconds"] is not None else ""
        avg_s = str(s["avg_duration"]) if s["avg_duration"] is not None else ""
        sc_s = str(s["best_score"]) if s["best_score"] is not None else ""

        rows_html.append(
            f'<tr data-href="{sid}/index.html">'
            f'<td><a href="{sid}/index.html"><strong>{html.escape(sid)}</strong></a></td>'
            f'<td>{html.escape(s["description"] or "-")}</td>'
            f'<td class="num" data-sort="{st_cnt}">{fmt_int(st_cnt)}</td>'
            f'<td class="num" data-sort="{dur_s}">{fmt_dur(s["duration_seconds"])}</td>'
            f'<td class="num" data-sort="{avg_s}">{fmt_dur(s["avg_duration"])}</td>'
            f'<td class="num" data-sort="{s["errors"]}">{fmt_int(s["errors"])}</td>'
            f'<td class="num" data-sort="{str_cnt}">{fmt_int(str_cnt)}</td>'
            f'<td class="num" data-sort="{tr_pct_val:.2f}">{fmt_pct(str_cnt, st_cnt)}</td>'
            f'<td class="num" data-sort="{ste_cnt}">{fmt_int(ste_cnt)}</td>'
            f'<td class="num" data-sort="{te_pct_val:.2f}">{fmt_pct(ste_cnt, st_cnt)}</td>'
            f'<td class="num" data-sort="{sc_s}">{fmt_float(s["best_score"])}</td>'
            f'<td class="num" data-sort="{s["total_tokens"]}">{fmt_int(s["total_tokens"])}</td>'
            f'<td class="num" data-sort="{s["retries"]}">{fmt_int(s["retries"])}</td>'
            f'</tr>'
        )

    table_html = f"""
    <div class="table-wrap">
      <table class="nav-table filterable-table">
        <thead>
          <tr>
            <th>Session</th>
            <th>Description</th>
            <th class="num">Tasks</th>
            <th class="num">Duration</th>
            <th class="num">Avg</th>
            <th class="num">Err</th>
            <th class="num">Train</th>
            <th class="num">Train%</th>
            <th class="num">Test</th>
            <th class="num">Test%</th>
            <th class="num">Score</th>
            <th class="num">Tokens</th>
            <th class="num">Retries</th>
          </tr>
        </thead>
        <tbody>
          {"".join(rows_html)}
        </tbody>
      </table>
    </div>
    """

    prev_link = (prev_suite, f"../{prev_suite}/index.html") if prev_suite else None
    next_link = (next_suite, f"../{next_suite}/index.html") if next_suite else None

    full_html = page_shell(
        title=f"Suite {suite}",
        root_rel=root_rel,
        active_nav="overview",
        breadcrumbs=[
            ("Suites", f"{root_rel}index.html"),
            (suite, None),
        ],
        body_html=summary_html + toolbar_html + table_html,
        prev_link=prev_link,
        next_link=next_link,
        up_link=f"{root_rel}index.html",
    )
    (out_dir / "index.html").write_text(full_html, encoding="utf-8")


def build_task_across_sessions_page(
    docs_dir: Path,
    task_agg: dict[str, Any],
    puzzle_meta: dict[str, Any],
    prev_tid: str | None,
    next_tid: str | None,
) -> None:
    """Generates docs/tasks/<task_id>/index.html (TaskSessionsScreen across all suites)."""
    tid = task_agg["task_id"]
    out_dir = docs_dir / "tasks" / tid
    out_dir.mkdir(parents=True, exist_ok=True)
    root_rel = "../../"

    runs = task_agg["runs"]
    s_cnt = len(runs)
    tr_cnt = task_agg["train_passed"]
    te_cnt = task_agg["test_passed"]

    panels = [
        [
            ("Sessions", fmt_int(s_cnt)),
            ("Train", f'{tr_cnt} ({fmt_pct(tr_cnt, s_cnt)})'),
            ("Test", f'{te_cnt} ({fmt_pct(te_cnt, s_cnt)})'),
            ("Weight", fmt_int(task_agg["weight"])),
        ],
        [
            ("Duration", fmt_dur(task_agg["duration_seconds"])),
            ("Avg", fmt_dur(task_agg["avg_duration"])),
            ("Errors", fmt_int(task_agg["errors"])),
            ("Best Score", fmt_float(task_agg["best_score"])),
        ],
        [
            ("Tokens", fmt_int(task_agg["total_tokens"])),
            ("In Tokens", fmt_int(task_agg["in_tokens"])),
            ("Out Tokens", fmt_int(task_agg["out_tokens"])),
            ("Retries", fmt_int(task_agg["retries"])),
        ],
    ]
    summary_html = render_summary_panels(panels)

    puzzle_panel_html = f"""
    <details class="nav-panel" open>
      <summary>Puzzle Ground-Truth Grids: {html.escape(tid)} ({puzzle_meta.get("n_train", 0)} Train, {puzzle_meta.get("n_test", 0)} Test, Weight {puzzle_meta.get("weight", 0)})</summary>
      <div class="panel-body">
        <div style="margin-bottom:8px;display:flex;justify-content:flex-end;">
          {render_grid_mode_toolbar_html()}
        </div>
        <div id="puzzle-grids-container"></div>
      </div>
    </details>
    """

    rows_html = []
    for r in runs:
        suite = r["suite"]
        sid = r["session_id"]
        href = f"{root_rel}suites/{suite}/{sid}/{tid}/index.html"
        err_h, err_s = render_err_cell(r["has_errors"])
        tr_h, tr_s = render_bool_cell(r["train_passed"])
        te_h, te_s = render_bool_cell(r["test_passed"])
        dur_s = str(r["duration_seconds"]) if r["duration_seconds"] is not None else ""
        sc_s = str(r["best_score"]) if r["best_score"] is not None else ""

        rows_html.append(
            f'<tr data-href="{href}">'
            f'<td><a href="{root_rel}suites/{suite}/index.html">{html.escape(suite)}</a></td>'
            f'<td><a href="{href}"><strong>{html.escape(sid)}</strong></a></td>'
            f'<td class="num" data-sort="{r["steps_count"]}">{fmt_int(r["steps_count"])}</td>'
            f'<td class="num" data-sort="{dur_s}">{fmt_dur(r["duration_seconds"])}</td>'
            f'<td class="center" data-sort="{err_s}">{err_h}</td>'
            f'<td class="center" data-sort="{tr_s}">{tr_h}</td>'
            f'<td class="center" data-sort="{te_s}">{te_h}</td>'
            f'<td class="num" data-sort="{sc_s}">{fmt_float(r["best_score"])}</td>'
            f'<td class="num" data-sort="{r["total_tokens"]}">{fmt_int(r["total_tokens"])}</td>'
            f'<td class="num" data-sort="{r["attempts"]}">{fmt_int(r["attempts"])}</td>'
            f'<td class="num" data-sort="{r["retries"]}">{fmt_int(r["retries"])}</td>'
            f'<td>{html.escape(r.get("model") or "-")}</td>'
            f'</tr>'
        )

    table_html = f"""
    <div class="table-wrap">
      <table class="nav-table">
        <thead>
          <tr>
            <th>Suite</th>
            <th>Session</th>
            <th class="num">Steps</th>
            <th class="num">Duration</th>
            <th class="center">Err</th>
            <th class="center">Train</th>
            <th class="center">Test</th>
            <th class="num">Score</th>
            <th class="num">Tokens</th>
            <th class="num">Attempts</th>
            <th class="num">Retries</th>
            <th>Model</th>
          </tr>
        </thead>
        <tbody>
          {"".join(rows_html)}
        </tbody>
      </table>
    </div>
    """

    puz_json_str = json.dumps(
        {"train": puzzle_meta.get("train", []), "test": puzzle_meta.get("test", [])},
        ensure_ascii=False,
    ).replace("</", "<\\/")

    prev_link = (prev_tid, f"../{prev_tid}/index.html") if prev_tid else None
    next_link = (next_tid, f"../{next_tid}/index.html") if next_tid else None

    full_html = page_shell(
        title=f"Task {tid}",
        root_rel=root_rel,
        active_nav="tasks",
        breadcrumbs=[
            ("Tasks", "../index.html"),
            (tid, None),
        ],
        body_html=summary_html + puzzle_panel_html + table_html + f'<script id="puzzle-data" type="application/json">{puz_json_str}</script>',
        prev_link=prev_link,
        next_link=next_link,
        up_link="../index.html",
    )
    (out_dir / "index.html").write_text(full_html, encoding="utf-8")


def build_all_sessions_page(
    docs_dir: Path,
    all_sessions: list[dict[str, Any]],
    suites_list: list[dict[str, Any]],
) -> None:
    """Generates docs/sessions/index.html (Global SessionsScreen across all 14 suites)."""
    out_dir = docs_dir / "sessions"
    out_dir.mkdir(parents=True, exist_ok=True)
    root_rel = "../"

    s_cnt = len(all_sessions)
    t_cnt = sum(s["tasks_count"] for s in all_sessions)
    tr_cnt = sum(s["train_passed"] for s in all_sessions)
    te_cnt = sum(s["test_passed"] for s in all_sessions)
    tot_dur = sum(s["duration_seconds"] or 0.0 for s in all_sessions)
    avg_dur = (tot_dur / s_cnt) if s_cnt else None
    tot_err = sum(s["errors"] for s in all_sessions)
    scores = [s["best_score"] for s in all_sessions if isinstance(s["best_score"], (int, float))]
    best_sc = min(scores) if scores else None
    tot_tok = sum(s["total_tokens"] for s in all_sessions)
    in_tok = sum(s["in_tokens"] for s in all_sessions)
    out_tok = sum(s["out_tokens"] for s in all_sessions)
    tot_ret = sum(s["retries"] for s in all_sessions)

    panels = [
        [
            ("Sessions", fmt_int(s_cnt)),
            ("Task Runs", fmt_int(t_cnt)),
            ("Train", f'{fmt_int(tr_cnt)} ({fmt_pct(tr_cnt, t_cnt)})'),
            ("Test", f'{fmt_int(te_cnt)} ({fmt_pct(te_cnt, t_cnt)})'),
        ],
        [
            ("Duration", fmt_dur(tot_dur)),
            ("Avg / Session", fmt_dur(avg_dur)),
            ("Errors", fmt_int(tot_err)),
            ("Best Score", fmt_float(best_sc)),
        ],
        [
            ("Tokens", fmt_int(tot_tok)),
            ("In Tokens", fmt_int(in_tok)),
            ("Out Tokens", fmt_int(out_tok)),
            ("Retries", fmt_int(tot_ret)),
        ],
    ]
    summary_html = render_summary_panels(panels)

    suite_opts = ['<option value="all">All Suites (' + str(len(suites_list)) + ')</option>']
    for su in suites_list:
        sn = su["suite"]
        suite_opts.append(f'<option value="{html.escape(sn)}">{html.escape(sn)} ({len(su["sessions"])})</option>')

    toolbar_html = f"""
    <div class="toolbar">
      <div class="toolbar-group">
        <input type="text" id="table-search" class="search-input" placeholder="Search sessions or descriptions (/) ...">
        <select id="suite-filter" class="select-input">{"".join(suite_opts)}</select>
      </div>
      <div class="toolbar-group">
        <span id="visible-row-count" class="badge">{s_cnt} / {s_cnt} sessions</span>
      </div>
    </div>
    """

    rows_html = []
    for s in all_sessions:
        suite = s["suite"]
        sid = s["session_id"]
        href = f"{root_rel}suites/{suite}/{sid}/index.html"
        st_cnt = s["tasks_count"]
        str_cnt = s["train_passed"]
        ste_cnt = s["test_passed"]
        tr_pct_val = (str_cnt / st_cnt * 100.0) if st_cnt else 0.0
        te_pct_val = (ste_cnt / st_cnt * 100.0) if st_cnt else 0.0
        dur_s = str(s["duration_seconds"]) if s["duration_seconds"] is not None else ""
        avg_s = str(s["avg_duration"]) if s["avg_duration"] is not None else ""
        sc_s = str(s["best_score"]) if s["best_score"] is not None else ""

        rows_html.append(
            f'<tr data-href="{href}" data-suite="{html.escape(suite)}">'
            f'<td><a href="{root_rel}suites/{suite}/index.html">{html.escape(suite)}</a></td>'
            f'<td><a href="{href}"><strong>{html.escape(sid)}</strong></a></td>'
            f'<td>{html.escape(s["description"] or "-")}</td>'
            f'<td class="num" data-sort="{st_cnt}">{fmt_int(st_cnt)}</td>'
            f'<td class="num" data-sort="{dur_s}">{fmt_dur(s["duration_seconds"])}</td>'
            f'<td class="num" data-sort="{avg_s}">{fmt_dur(s["avg_duration"])}</td>'
            f'<td class="num" data-sort="{s["errors"]}">{fmt_int(s["errors"])}</td>'
            f'<td class="num" data-sort="{str_cnt}">{fmt_int(str_cnt)}</td>'
            f'<td class="num" data-sort="{tr_pct_val:.2f}">{fmt_pct(str_cnt, st_cnt)}</td>'
            f'<td class="num" data-sort="{ste_cnt}">{fmt_int(ste_cnt)}</td>'
            f'<td class="num" data-sort="{te_pct_val:.2f}">{fmt_pct(ste_cnt, st_cnt)}</td>'
            f'<td class="num" data-sort="{sc_s}">{fmt_float(s["best_score"])}</td>'
            f'<td class="num" data-sort="{s["total_tokens"]}">{fmt_int(s["total_tokens"])}</td>'
            f'<td class="num" data-sort="{s["retries"]}">{fmt_int(s["retries"])}</td>'
            f'</tr>'
        )

    table_html = f"""
    <div class="table-wrap">
      <table class="nav-table filterable-table">
        <thead>
          <tr>
            <th>Suite</th>
            <th>Session</th>
            <th>Description</th>
            <th class="num">Tasks</th>
            <th class="num">Duration</th>
            <th class="num">Avg</th>
            <th class="num">Err</th>
            <th class="num">Train</th>
            <th class="num">Train%</th>
            <th class="num">Test</th>
            <th class="num">Test%</th>
            <th class="num">Score</th>
            <th class="num">Tokens</th>
            <th class="num">Retries</th>
          </tr>
        </thead>
        <tbody>
          {"".join(rows_html)}
        </tbody>
      </table>
    </div>
    """

    full_html = page_shell(
        title="All Sessions",
        root_rel=root_rel,
        active_nav="sessions",
        breadcrumbs=[
            ("Overview", f"{root_rel}index.html"),
            ("Sessions", None),
        ],
        body_html=summary_html + toolbar_html + table_html,
        up_link=f"{root_rel}index.html",
    )
    (out_dir / "index.html").write_text(full_html, encoding="utf-8")


def build_all_tasks_page(
    docs_dir: Path,
    all_tasks_agg: list[dict[str, Any]],
    suites_list: list[dict[str, Any]],
) -> None:
    """Generates docs/tasks/index.html (Global TasksScreen across all 2,939 unique puzzles)."""
    out_dir = docs_dir / "tasks"
    out_dir.mkdir(parents=True, exist_ok=True)
    root_rel = "../"

    u_cnt = len(all_tasks_agg)
    solved_tr_tasks = sum(1 for t in all_tasks_agg if t["train_passed"] > 0)
    solved_te_tasks = sum(1 for t in all_tasks_agg if t["test_passed"] > 0)
    train_only_tasks = sum(1 for t in all_tasks_agg if t["train_passed"] > 0 and t["test_passed"] == 0)
    unsolved_tasks = u_cnt - solved_tr_tasks
    err_tasks = sum(1 for t in all_tasks_agg if t["errors"] > 0)

    tot_runs = sum(t["sessions_count"] for t in all_tasks_agg)
    tot_dur = sum(t["duration_seconds"] or 0.0 for t in all_tasks_agg)
    avg_dur = (tot_dur / u_cnt) if u_cnt else None
    tot_err = sum(t["errors"] for t in all_tasks_agg)
    tot_tok = sum(t["total_tokens"] for t in all_tasks_agg)
    in_tok = sum(t["in_tokens"] for t in all_tasks_agg)
    out_tok = sum(t["out_tokens"] for t in all_tasks_agg)
    tot_ret = sum(t["retries"] for t in all_tasks_agg)

    panels = [
        [
            ("Unique Tasks", fmt_int(u_cnt)),
            ("Total Runs", fmt_int(tot_runs)),
            ("Train Solved", f'{fmt_int(solved_tr_tasks)} ({fmt_pct(solved_tr_tasks, u_cnt)})'),
            ("Test Solved", f'{fmt_int(solved_te_tasks)} ({fmt_pct(solved_te_tasks, u_cnt)})'),
        ],
        [
            ("Duration", fmt_dur(tot_dur)),
            ("Avg / Task", fmt_dur(avg_dur)),
            ("Errors", fmt_int(tot_err)),
            ("Train-Only Tasks", fmt_int(train_only_tasks)),
        ],
        [
            ("Tokens", fmt_int(tot_tok)),
            ("In Tokens", fmt_int(in_tok)),
            ("Out Tokens", fmt_int(out_tok)),
            ("Retries", fmt_int(tot_ret)),
        ],
    ]
    summary_html = render_summary_panels(panels)

    suite_opts = ['<option value="all">All Suites (' + str(len(suites_list)) + ')</option>']
    for su in suites_list:
        sn = su["suite"]
        suite_opts.append(f'<option value="{html.escape(sn)}">{html.escape(sn)}</option>')

    toolbar_html = f"""
    <div class="toolbar">
      <div class="toolbar-group">
        <input type="text" id="table-search" class="search-input" placeholder="Search Task ID (/) ...">
        <select id="suite-filter" class="select-input">{"".join(suite_opts)}</select>
        <button type="button" class="filter-btn status-filter-btn active" data-filter="all">All ({u_cnt})</button>
        <button type="button" class="filter-btn status-filter-btn" data-filter="test-pass">Test Solved ✓ ({solved_te_tasks})</button>
        <button type="button" class="filter-btn status-filter-btn" data-filter="train-only">Train Only ({train_only_tasks})</button>
        <button type="button" class="filter-btn status-filter-btn" data-filter="failed">Unsolved ✗ ({unsolved_tasks})</button>
        <button type="button" class="filter-btn status-filter-btn" data-filter="errors">Errors ({err_tasks})</button>
      </div>
      <div class="toolbar-group">
        <span id="visible-row-count" class="badge">{u_cnt} / {u_cnt} tasks</span>
      </div>
    </div>
    """

    rows_html = []
    for t in all_tasks_agg:
        tid = t["task_id"]
        href = f"{tid}/index.html"
        s_cnt = t["sessions_count"]
        tr_cnt = t["train_passed"]
        te_cnt = t["test_passed"]
        tr_pct_val = (tr_cnt / s_cnt * 100.0) if s_cnt else 0.0
        te_pct_val = (te_cnt / s_cnt * 100.0) if s_cnt else 0.0
        dur_s = str(t["duration_seconds"]) if t["duration_seconds"] is not None else ""
        avg_s = str(t["avg_duration"]) if t["avg_duration"] is not None else ""
        sc_s = str(t["best_score"]) if t["best_score"] is not None else ""
        primary_suite = t["suites"][0] if t["suites"] else ""
        suites_str = ", ".join(t["suites"])
        status_tags = get_row_status_tags(tr_cnt > 0, te_cnt > 0, t["errors"] > 0)

        rows_html.append(
            f'<tr data-href="{href}" data-suite="{html.escape(primary_suite)}" data-status="{status_tags}">'
            f'<td><a href="{href}"><strong>{html.escape(tid)}</strong></a></td>'
            f'<td class="num" data-sort="{t["weight"]}">{fmt_int(t["weight"])}</td>'
            f'<td>{html.escape(suites_str)}</td>'
            f'<td class="num" data-sort="{s_cnt}">{fmt_int(s_cnt)}</td>'
            f'<td class="num" data-sort="{dur_s}">{fmt_dur(t["duration_seconds"])}</td>'
            f'<td class="num" data-sort="{avg_s}">{fmt_dur(t["avg_duration"])}</td>'
            f'<td class="num" data-sort="{t["errors"]}">{fmt_int(t["errors"])}</td>'
            f'<td class="num" data-sort="{tr_cnt}">{fmt_int(tr_cnt)}</td>'
            f'<td class="num" data-sort="{tr_pct_val:.2f}">{fmt_pct(tr_cnt, s_cnt)}</td>'
            f'<td class="num" data-sort="{te_cnt}">{fmt_int(te_cnt)}</td>'
            f'<td class="num" data-sort="{te_pct_val:.2f}">{fmt_pct(te_cnt, s_cnt)}</td>'
            f'<td class="num" data-sort="{sc_s}">{fmt_float(t["best_score"])}</td>'
            f'<td class="num" data-sort="{t["total_tokens"]}">{fmt_int(t["total_tokens"])}</td>'
            f'<td class="num" data-sort="{t["retries"]}">{fmt_int(t["retries"])}</td>'
            f'</tr>'
        )

    table_html = f"""
    <div class="table-wrap">
      <table class="nav-table filterable-table">
        <thead>
          <tr>
            <th>Task ID</th>
            <th class="num">Weight</th>
            <th>Suites</th>
            <th class="num">Sessions</th>
            <th class="num">Duration</th>
            <th class="num">Avg</th>
            <th class="num">Err</th>
            <th class="num">Train</th>
            <th class="num">Train%</th>
            <th class="num">Test</th>
            <th class="num">Test%</th>
            <th class="num">Score</th>
            <th class="num">Tokens</th>
            <th class="num">Retries</th>
          </tr>
        </thead>
        <tbody>
          {"".join(rows_html)}
        </tbody>
      </table>
    </div>
    """

    full_html = page_shell(
        title="All Tasks",
        root_rel=root_rel,
        active_nav="tasks",
        breadcrumbs=[
            ("Overview", f"{root_rel}index.html"),
            ("Tasks", None),
        ],
        body_html=summary_html + toolbar_html + table_html,
        up_link=f"{root_rel}index.html",
    )
    (out_dir / "index.html").write_text(full_html, encoding="utf-8")


def build_overview_and_retrospective_pages(
    docs_dir: Path,
    suites_list: list[dict[str, Any]],
    all_sessions: list[dict[str, Any]],
    all_tasks_agg: list[dict[str, Any]],
    conv_stats: dict[str, Any],
) -> None:
    """Generates docs/index.html (Corpus Overview) and docs/retrospective/index.html."""
    su_cnt = len(suites_list)
    sess_cnt = len(all_sessions)
    uniq_tasks = len(all_tasks_agg)
    run_cnt = sum(su["tasks_count"] for su in suites_list)
    tr_runs = sum(su["train_passed"] for su in suites_list)
    te_runs = sum(su["test_passed"] for su in suites_list)
    solved_tr_uniq = sum(1 for t in all_tasks_agg if t["train_passed"] > 0)
    solved_te_uniq = sum(1 for t in all_tasks_agg if t["test_passed"] > 0)

    tot_dur = sum(su["duration_seconds"] or 0.0 for su in suites_list)
    tot_err = sum(su["errors"] for su in suites_list)
    tot_tok = sum(su["total_tokens"] for su in suites_list)
    in_tok = sum(su["in_tokens"] for su in suites_list)
    out_tok = sum(su["out_tokens"] for su in suites_list)
    tot_ret = sum(su["retries"] for su in suites_list)

    panels = [
        [
            ("Benchmark Suites", fmt_int(su_cnt)),
            ("Sessions", fmt_int(sess_cnt)),
            ("Unique Puzzles", f'{fmt_int(uniq_tasks)} ({fmt_int(solved_te_uniq)} Test ✓ / {fmt_pct(solved_te_uniq, uniq_tasks)})'),
            ("Total Task Runs", fmt_int(run_cnt)),
        ],
        [
            ("Runs Train ✓", f'{fmt_int(tr_runs)} ({fmt_pct(tr_runs, run_cnt)})'),
            ("Runs Test ✓", f'{fmt_int(te_runs)} ({fmt_pct(te_runs, run_cnt)})'),
            ("Total Duration", fmt_dur(tot_dur)),
            ("Total Errors", fmt_int(tot_err)),
        ],
        [
            ("Total Tokens", fmt_int(tot_tok)),
            ("In Tokens", fmt_int(in_tok)),
            ("Out Tokens", fmt_int(out_tok)),
            ("Total Retries", fmt_int(tot_ret)),
        ],
    ]
    summary_html = render_summary_panels(panels)

    suite_rows = []
    for su in suites_list:
        sn = su["suite"]
        href = f"suites/{sn}/index.html"
        s_cnt = len(su["sessions"])
        t_cnt = su["tasks_count"]
        u_cnt = su["unique_tasks_count"]
        str_cnt = su["train_passed"]
        ste_cnt = su["test_passed"]
        tr_pct_v = (str_cnt / t_cnt * 100.0) if t_cnt else 0.0
        te_pct_v = (ste_cnt / t_cnt * 100.0) if t_cnt else 0.0
        dur_s = str(su["duration_seconds"]) if su["duration_seconds"] is not None else ""
        avg_s = str(su["avg_duration"]) if su["avg_duration"] is not None else ""
        sc_s = str(su["best_score"]) if su["best_score"] is not None else ""

        suite_rows.append(
            f'<tr data-href="{href}">'
            f'<td><a href="{href}"><strong>{html.escape(sn)}</strong></a></td>'
            f'<td class="num" data-sort="{s_cnt}">{fmt_int(s_cnt)}</td>'
            f'<td class="num" data-sort="{u_cnt}">{fmt_int(u_cnt)}</td>'
            f'<td class="num" data-sort="{t_cnt}">{fmt_int(t_cnt)}</td>'
            f'<td class="num" data-sort="{dur_s}">{fmt_dur(su["duration_seconds"])}</td>'
            f'<td class="num" data-sort="{avg_s}">{fmt_dur(su["avg_duration"])}</td>'
            f'<td class="num" data-sort="{su["errors"]}">{fmt_int(su["errors"])}</td>'
            f'<td class="num" data-sort="{str_cnt}">{fmt_int(str_cnt)}</td>'
            f'<td class="num" data-sort="{tr_pct_v:.2f}">{fmt_pct(str_cnt, t_cnt)}</td>'
            f'<td class="num" data-sort="{ste_cnt}">{fmt_int(ste_cnt)}</td>'
            f'<td class="num" data-sort="{te_pct_v:.2f}">{fmt_pct(ste_cnt, t_cnt)}</td>'
            f'<td class="num" data-sort="{sc_s}">{fmt_float(su["best_score"])}</td>'
            f'<td class="num" data-sort="{su["total_tokens"]}">{fmt_int(su["total_tokens"])}</td>'
            f'<td class="num" data-sort="{su["retries"]}">{fmt_int(su["retries"])}</td>'
            f'</tr>'
        )

    suites_table_html = f"""
    <div class="toolbar">
      <div class="toolbar-group">
        <strong style="color:var(--accent);">Benchmark Suites ({su_cnt})</strong>
        <input type="text" id="table-search" class="search-input" placeholder="Filter suites (/) ...">
      </div>
      <div class="toolbar-group">
        <a href="sessions/index.html" class="btn">All Sessions ({sess_cnt}) →</a>
        <a href="tasks/index.html" class="btn">All Unique Tasks ({uniq_tasks}) →</a>
        <a href="retrospective/index.html" class="btn" style="color:var(--accent);border-color:var(--accent);">SEER 1.0 Retrospective Report →</a>
      </div>
    </div>
    <div class="table-wrap">
      <table class="nav-table filterable-table">
        <thead>
          <tr>
            <th>Suite Directory</th>
            <th class="num">Sessions</th>
            <th class="num">Unique Tasks</th>
            <th class="num">Task Runs</th>
            <th class="num">Duration</th>
            <th class="num">Avg / Sess</th>
            <th class="num">Err</th>
            <th class="num">Train ✓</th>
            <th class="num">Train%</th>
            <th class="num">Test ✓</th>
            <th class="num">Test%</th>
            <th class="num">Score</th>
            <th class="num">Tokens</th>
            <th class="num">Retries</th>
          </tr>
        </thead>
        <tbody>
          {"".join(suite_rows)}
        </tbody>
      </table>
    </div>
    """

    overview_html = page_shell(
        title="Corpus Overview",
        root_rel="",
        active_nav="overview",
        breadcrumbs=[("Suites Overview", None)],
        body_html=summary_html + suites_table_html,
    )
    (docs_dir / "index.html").write_text(overview_html, encoding="utf-8")

    # Build Retrospective Page (docs/retrospective/index.html)
    retro_dir = docs_dir / "retrospective"
    retro_dir.mkdir(parents=True, exist_ok=True)

    s1_tr = conv_stats.get("step1_train", 0)
    s2_tr = conv_stats.get("step2_train", 0)
    s3_tr = conv_stats.get("step3plus_train", 0)
    s1_te = conv_stats.get("step1_test", 0)
    s2_te = conv_stats.get("step2_test", 0)
    s3_te = conv_stats.get("step3plus_test", 0)

    retro_body = f"""
    {summary_html}
    <div class="prose-card">
      <h1>SEER 1.0 Empirical Retrospective &amp; SEER 2.0 Architecture</h1>
      <p>
        <strong>SEER</strong> (Symbolic &amp; Visual Program Synthesis for Abstract Reasoning) approaches visual reasoning challenges—such as
        ARC-AGI, ConceptARC, Mini-ARC, and 1D cellular/pattern benchmarks—not by guessing output pixel matrices directly,
        but by <strong>synthesizing executable Python programs</strong> (<code>def transform(grid): ...</code>) verified against training examples.
      </p>

      <h2>1. Corpus-Wide Empirical Summary</h2>
      <p>
        Across the <strong>{fmt_int(su_cnt)} benchmark suites</strong> in <code>seer_sessions</code>, SEER executed
        <strong>{fmt_int(sess_cnt)} session batches</strong> encompassing <strong>{fmt_int(run_cnt)} task runs</strong>
        and <strong>{fmt_int(conv_stats.get("total_steps", 0))} reasoning/coding steps</strong> across
        <strong>{fmt_int(uniq_tasks)} unique puzzles</strong>.
      </p>
      <ul>
        <li><strong>Unique Puzzles Solved (Test Verified):</strong> {fmt_int(solved_te_uniq)} / {fmt_int(uniq_tasks)} ({fmt_pct(solved_te_uniq, uniq_tasks)})</li>
        <li><strong>Unique Puzzles Solved (Train Verified):</strong> {fmt_int(solved_tr_tasks if 'solved_tr_tasks' in locals() else solved_tr_uniq)} / {fmt_int(uniq_tasks)} ({fmt_pct(solved_tr_uniq, uniq_tasks)})</li>
        <li><strong>Train-to-Test Generalization Rate:</strong> Whenever SEER synthesized a Python program that passed all training pairs ({fmt_int(tr_runs)} runs), it generalized zero-shot to the held-out test pairs in <strong>{fmt_int(te_runs)} runs ({fmt_pct(te_runs, tr_runs)})</strong>.</li>
        <li><strong>Cumulative Compute:</strong> {fmt_int(tot_tok)} total tokens ({fmt_int(in_tok)} prompt / {fmt_int(out_tok)} candidate tokens) over {fmt_dur(tot_dur)}.</li>
      </ul>

      <h2>2. Cognitive Separation: Dreamer vs. Coder &amp; Step Convergence</h2>
      <p>
        A defining architectural discovery of SEER 1.0 was splitting reasoning into two distinct roles:
      </p>
      <ol>
        <li><strong>Step 000 — Dreamer (Perception &amp; Discernment):</strong> Inspects multimodal puzzle images and text matrices to formulate structured YAML observations, invariant hypotheses, object inventories, and transformation rules without writing code.</li>
        <li><strong>Step 001 — Coder (Initial Program Synthesis):</strong> Translates the Dreamer's YAML blueprint into executable Python code (<code>code_00.py</code>) and evaluates it in the Trial Sandbox.</li>
        <li><strong>Steps 002+ — Iterative Refinement:</strong> Inspects pixel-level trial diffs (<code>size_correct</code>, <code>palette_correct</code>, <code>color_count_correct</code>, <code>pixels_off</code>) and visual diff grids to debug and refine the program.</li>
      </ol>
      <p>
        Across all {fmt_int(tr_runs)} successful training runs and {fmt_int(te_runs)} successful test runs:
      </p>
      <ul>
        <li><strong>Step 1 (Dreamer / 1-Shot):</strong> {fmt_int(s1_tr)} Train passes / {fmt_int(s1_te)} Test passes</li>
        <li><strong>Step 2 (First Coder Synthesis from Dreamer YAML):</strong> {fmt_int(s2_tr)} Train passes ({fmt_pct(s2_tr, tr_runs)}) / {fmt_int(s2_te)} Test passes ({fmt_pct(s2_te, te_runs)})</li>
        <li><strong>Steps 3+ (Iterative Trial-Feedback Debugging):</strong> {fmt_int(s3_tr)} Train passes ({fmt_pct(s3_tr, tr_runs)}) / {fmt_int(s3_te)} Test passes ({fmt_pct(s3_te, te_runs)}) — demonstrating that automated pixel-diff feedback recovers nearly a quarter of all solutions after an imperfect initial program.</li>
      </ul>

      <h2>3. Towards SEER 2.0: Intrinsic Perception &amp; Constructive Geometry</h2>
      <p>
        Building on this empirical archive, <strong>SEER 2.0</strong> evolves the architecture into a collaborative multi-agent system:
      </p>
      <ul>
        <li><strong>Intrinsic Perception Library:</strong> On-demand algorithmic queries (connected components, symmetry group detection, periodicity, bounding-box graphs, harmonic ratios) callable by the agent prior to program synthesis.</li>
        <li><strong>Multi-Agent Orchestration:</strong> Explicit <em>SEER (Overseer)</em>, <em>Dreamer</em>, <em>Coder</em>, and <em>Oracle</em> roles operating with isolated trial sandboxes.</li>
        <li><strong>Unified GEOMETOR Integration:</strong> Extending program synthesis from 2D ARC grids to exact symbolic constructions in <code>geometor.model</code>, <code>geometor.elements</code> (Euclid), and <code>geometor.phyllotaxis</code>.</li>
      </ul>
    </div>
    """
    retro_suites_table = (
        suites_table_html.replace('href="suites/', 'href="../suites/')
        .replace('data-href="suites/', 'data-href="../suites/')
        .replace('href="sessions/index.html"', 'href="../sessions/index.html"')
        .replace('href="tasks/index.html"', 'href="../tasks/index.html"')
        .replace('href="retrospective/index.html"', 'href="index.html"')
    )

    retro_html = page_shell(
        title="SEER 1.0 Retrospective",
        root_rel="../",
        active_nav="retrospective",
        breadcrumbs=[
            ("Overview", "../index.html"),
            ("SEER 1.0 Retrospective", None),
        ],
        body_html=retro_body + retro_suites_table,
        up_link="../index.html",
    )
    (retro_dir / "index.html").write_text(retro_html, encoding="utf-8")


def main() -> None:
    t0 = time.time()
    print(f"Building GEOMETOR SEER Sessions Navigator in {DOCS_DIR} ...")
    write_static_assets(DOCS_DIR)

    puzzle_cache: dict[str, dict[str, Any]] = {}
    print("  Preloading puzzle specifications across all suites ...")
    for suite_name in SUITE_NAMES:
        suite_dir = REPO_ROOT / suite_name
        if not suite_dir.is_dir():
            continue
        for sess_dir in suite_dir.iterdir():
            if not sess_dir.is_dir():
                continue
            for tdir in sess_dir.iterdir():
                if not tdir.is_dir():
                    continue
                tid = tdir.name
                if tid in puzzle_cache:
                    continue
                tj = tdir / "task.json"
                if tj.is_file():
                    raw_task = safe_load_json(tj)
                    if isinstance(raw_task, dict):
                        puzzle_cache[tid] = {
                            "id": tid,
                            "weight": compute_task_weight(raw_task),
                            "n_train": len(raw_task.get("train", [])),
                            "n_test": len(raw_task.get("test", [])),
                            "train": raw_task.get("train", []),
                            "test": raw_task.get("test", []),
                        }
    print(f"  Cached {len(puzzle_cache)} unique puzzle definitions.")

    suites_list: list[dict[str, Any]] = []
    all_sessions: list[dict[str, Any]] = []
    tasks_runs_map: dict[str, list[dict[str, Any]]] = defaultdict(list)

    conv_stats = {
        "total_steps": 0,
        "step1_train": 0,
        "step2_train": 0,
        "step3plus_train": 0,
        "step1_test": 0,
        "step2_test": 0,
        "step3plus_test": 0,
    }

    # First pass: parse all suites, sessions, and task runs
    for suite_idx, suite_name in enumerate(SUITE_NAMES):
        suite_dir = REPO_ROOT / suite_name
        if not suite_dir.is_dir():
            continue

        session_dirs = sorted([d for d in suite_dir.iterdir() if d.is_dir()])
        suite_sessions: list[dict[str, Any]] = []
        suite_unique_tasks: set[str] = set()

        print(f"  [{suite_idx + 1}/{len(SUITE_NAMES)}] Scanning {suite_name} ({len(session_dirs)} sessions) ...")

        for sess_dir in session_dirs:
            sess_id = sess_dir.name
            sess_idx_data = safe_load_json(sess_dir / "index.json") or {}
            if not isinstance(sess_idx_data, dict):
                sess_idx_data = {}
            cfg_data = safe_load_json(sess_dir / "config.json") or {}
            if not isinstance(cfg_data, dict):
                cfg_data = {}

            description = str(sess_idx_data.get("description") or cfg_data.get("description") or "")

            # Collect session-level context/config files
            context_files: dict[str, str] = {}
            for cf in sorted(sess_dir.iterdir()):
                if cf.is_file() and cf.name.endswith((".json", ".md", ".yaml")) and cf.name != "index.json":
                    context_files[cf.name] = safe_read_text(cf, max_chars=25000)

            task_dirs = sorted([d for d in sess_dir.iterdir() if d.is_dir()])
            task_runs: list[dict[str, Any]] = []

            for tdir in task_dirs:
                trun = parse_task_run(tdir, suite_name, sess_id, puzzle_cache)
                task_runs.append(trun)
                suite_unique_tasks.add(trun["task_id"])
                tasks_runs_map[trun["task_id"]].append(trun)

                conv_stats["total_steps"] += len(trun["steps"])
                fts_tr = trun.get("first_train_step")
                if fts_tr == 1:
                    conv_stats["step1_train"] += 1
                elif fts_tr == 2:
                    conv_stats["step2_train"] += 1
                elif fts_tr and fts_tr >= 3:
                    conv_stats["step3plus_train"] += 1

                fts_te = trun.get("first_test_step")
                if fts_te == 1:
                    conv_stats["step1_test"] += 1
                elif fts_te == 2:
                    conv_stats["step2_test"] += 1
                elif fts_te and fts_te >= 3:
                    conv_stats["step3plus_test"] += 1

            # Build individual Task Run pages for this session
            for i, trun in enumerate(task_runs):
                prev_tid = task_runs[i - 1]["task_id"] if i > 0 else None
                next_tid = task_runs[i + 1]["task_id"] if i + 1 < len(task_runs) else None
                pmeta = puzzle_cache.get(trun["task_id"], {"id": trun["task_id"], "weight": 0, "n_train": 0, "n_test": 0, "train": [], "test": []})
                build_task_run_page(DOCS_DIR, trun, pmeta, prev_tid, next_tid)

            # Compute session summary
            t_cnt = len(task_runs)
            tr_passed = sum(1 for r in task_runs if r["train_passed"] is True)
            te_passed = sum(1 for r in task_runs if r["test_passed"] is True)
            err_cnt = sum(1 for r in task_runs if r["has_errors"])
            durs = [r["duration_seconds"] for r in task_runs if isinstance(r["duration_seconds"], (int, float))]
            sess_dur = sess_idx_data.get("duration_seconds")
            if not isinstance(sess_dur, (int, float)):
                sess_dur = sum(durs) if durs else None
            avg_dur = (sess_dur / t_cnt) if (isinstance(sess_dur, (int, float)) and t_cnt > 0) else None

            scores = [r["best_score"] for r in task_runs if isinstance(r["best_score"], (int, float))]
            best_sc = min(scores) if scores else None

            in_tok = sum(r["in_tokens"] for r in task_runs)
            out_tok = sum(r["out_tokens"] for r in task_runs)
            tot_tok = sum(r["total_tokens"] for r in task_runs)
            retries = sum(r["retries"] for r in task_runs)

            sess_summary = {
                "suite": suite_name,
                "session_id": sess_id,
                "description": description,
                "tasks_count": t_cnt,
                "train_passed": tr_passed,
                "test_passed": te_passed,
                "errors": err_cnt,
                "duration_seconds": round(float(sess_dur), 2) if isinstance(sess_dur, (int, float)) else None,
                "avg_duration": round(float(avg_dur), 2) if isinstance(avg_dur, (int, float)) else None,
                "best_score": round(float(best_sc), 2) if isinstance(best_sc, (int, float)) else None,
                "in_tokens": in_tok,
                "out_tokens": out_tok,
                "total_tokens": tot_tok,
                "retries": retries,
                "context_files": context_files,
                "task_runs": [
                    {k: v for k, v in r.items() if k != "steps"}
                    for r in task_runs
                ],
            }
            suite_sessions.append(sess_summary)
            all_sessions.append(sess_summary)

        # Build Session pages for this suite
        for i, ssum in enumerate(suite_sessions):
            prev_sid = suite_sessions[i - 1]["session_id"] if i > 0 else None
            next_sid = suite_sessions[i + 1]["session_id"] if i + 1 < len(suite_sessions) else None
            build_session_page(DOCS_DIR, ssum, prev_sid, next_sid)

        # Suite rollup
        su_t_cnt = sum(s["tasks_count"] for s in suite_sessions)
        su_tr = sum(s["train_passed"] for s in suite_sessions)
        su_te = sum(s["test_passed"] for s in suite_sessions)
        su_err = sum(s["errors"] for s in suite_sessions)
        su_durs = [s["duration_seconds"] for s in suite_sessions if isinstance(s["duration_seconds"], (int, float))]
        su_dur = sum(su_durs) if su_durs else None
        su_avg = (su_dur / len(suite_sessions)) if (su_dur is not None and suite_sessions) else None
        su_scores = [s["best_score"] for s in suite_sessions if isinstance(s["best_score"], (int, float))]
        su_best_sc = min(su_scores) if su_scores else None

        suites_list.append({
            "suite": suite_name,
            "sessions": suite_sessions,
            "unique_tasks_count": len(suite_unique_tasks),
            "tasks_count": su_t_cnt,
            "train_passed": su_tr,
            "test_passed": su_te,
            "errors": su_err,
            "duration_seconds": round(float(su_dur), 2) if su_dur is not None else None,
            "avg_duration": round(float(su_avg), 2) if su_avg is not None else None,
            "best_score": round(float(su_best_sc), 2) if su_best_sc is not None else None,
            "in_tokens": sum(s["in_tokens"] for s in suite_sessions),
            "out_tokens": sum(s["out_tokens"] for s in suite_sessions),
            "total_tokens": sum(s["total_tokens"] for s in suite_sessions),
            "retries": sum(s["retries"] for s in suite_sessions),
        })

    # Build Suite pages
    for i, su_sum in enumerate(suites_list):
        prev_su = suites_list[i - 1]["suite"] if i > 0 else None
        next_su = suites_list[i + 1]["suite"] if i + 1 < len(suites_list) else None
        build_suite_page(DOCS_DIR, su_sum, prev_su, next_su)

    # Build Task Across Sessions pages (2,939 unique tasks)
    sorted_tids = sorted(tasks_runs_map.keys())
    all_tasks_agg: list[dict[str, Any]] = []
    print(f"  Building {len(sorted_tids)} Task-Across-Sessions pages ...")

    for tid in sorted_tids:
        runs = tasks_runs_map[tid]
        pmeta = puzzle_cache.get(tid, {"id": tid, "weight": 0, "n_train": 0, "n_test": 0, "train": [], "test": []})
        s_cnt = len(runs)
        tr_cnt = sum(1 for r in runs if r["train_passed"] is True)
        te_cnt = sum(1 for r in runs if r["test_passed"] is True)
        err_cnt = sum(1 for r in runs if r["has_errors"])
        durs = [r["duration_seconds"] for r in runs if isinstance(r["duration_seconds"], (int, float))]
        tot_dur = sum(durs) if durs else None
        avg_dur = (tot_dur / s_cnt) if (tot_dur is not None and s_cnt > 0) else None
        scores = [r["best_score"] for r in runs if isinstance(r["best_score"], (int, float))]
        best_sc = min(scores) if scores else None
        suites_seen = sorted(list({r["suite"] for r in runs}))

        all_tasks_agg.append({
            "task_id": tid,
            "weight": pmeta["weight"],
            "suites": suites_seen,
            "sessions_count": s_cnt,
            "train_passed": tr_cnt,
            "test_passed": te_cnt,
            "errors": err_cnt,
            "duration_seconds": round(float(tot_dur), 2) if tot_dur is not None else None,
            "avg_duration": round(float(avg_dur), 2) if avg_dur is not None else None,
            "best_score": round(float(best_sc), 2) if best_sc is not None else None,
            "in_tokens": sum(r["in_tokens"] for r in runs),
            "out_tokens": sum(r["out_tokens"] for r in runs),
            "total_tokens": sum(r["total_tokens"] for r in runs),
            "retries": sum(r["retries"] for r in runs),
            "runs": [
                {k: v for k, v in r.items() if k != "steps"}
                for r in runs
            ],
        })

    for i, tagg in enumerate(all_tasks_agg):
        prev_tid = all_tasks_agg[i - 1]["task_id"] if i > 0 else None
        next_tid = all_tasks_agg[i + 1]["task_id"] if i + 1 < len(all_tasks_agg) else None
        pmeta = puzzle_cache.get(tagg["task_id"], {"id": tagg["task_id"], "weight": 0, "n_train": 0, "n_test": 0, "train": [], "test": []})
        build_task_across_sessions_page(DOCS_DIR, tagg, pmeta, prev_tid, next_tid)

    print("  Building global Sessions, Tasks, Overview, and Retrospective pages ...")
    build_all_sessions_page(DOCS_DIR, all_sessions, suites_list)
    build_all_tasks_page(DOCS_DIR, all_tasks_agg, suites_list)
    build_overview_and_retrospective_pages(DOCS_DIR, suites_list, all_sessions, all_tasks_agg, conv_stats)

    elapsed = time.time() - t0
    print(
        f"Done in {elapsed:.1f}s! Generated {len(suites_list)} suites, "
        f"{len(all_sessions)} sessions, {len(all_tasks_agg)} unique tasks, "
        f"and {sum(s['tasks_count'] for s in suites_list)} task run pages in {DOCS_DIR}"
    )


if __name__ == "__main__":
    main()
