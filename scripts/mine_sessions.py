#!/usr/bin/env python3
"""
mine_sessions.py
================
Unified mining and longitudinal correlation engine for GEOMETOR SEER sessions.
Processes all 14 session directories, extracts run-level metrics, and aggregates
puzzle-level statistics across runs.
"""

import json
import os
import sys
import time
from collections import defaultdict
from pathlib import Path
try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    HAS_RICH = True
    console = Console()
except ImportError:
    HAS_RICH = False
    class DummyConsole:
        def print(self, *args, **kwargs):
            text = " ".join(str(a) for a in args)
            # Strip rich markup tags like [bold cyan], [/bold cyan]
            import re
            clean_text = re.sub(r'\[/?[a-zA-Z0-9_\s#]+\]', '', text)
            print(clean_text)
    console = DummyConsole()

def parse_task_dir(task_dir: Path, suite_name: str, session_id: str) -> dict:
    """Extracts all metrics from a single task run directory."""
    task_id = task_dir.name
    run_data = {
        "suite": suite_name,
        "session_id": session_id,
        "task_id": task_id,
        "path": str(task_dir),
        "steps_count": 0,
        "duration_seconds": 0.0,
        "train_passed": False,
        "test_passed": False,
        "best_score": None,
        "best_percent_correct": 0.0,
        "tokens": {"prompt": 0, "candidates": 0, "total": 0},
        "trials_count": 0,
        "error_count": 0,
        "has_code": False,
        "best_code_file": None,
    }

    # Strategy 1: Check for index.json (Modern format)
    index_file = task_dir / "index.json"
    if index_file.exists():
        try:
            with open(index_file, "r") as f:
                idx = json.load(f)
                run_data["train_passed"] = bool(idx.get("train_passed", False))
                run_data["test_passed"] = bool(idx.get("test_passed", False))
                run_data["duration_seconds"] = float(idx.get("duration_seconds", 0.0))
                run_data["steps_count"] = int(idx.get("steps", 0))
                run_data["best_score"] = idx.get("best_score")
                
                toks = idx.get("tokens", {})
                run_data["tokens"]["prompt"] = toks.get("prompt_tokens", 0)
                run_data["tokens"]["candidates"] = toks.get("candidates_tokens", 0)
                run_data["tokens"]["total"] = toks.get("total_tokens", 0)
                
                errs = idx.get("errors", {})
                run_data["error_count"] = errs.get("count", 0) if isinstance(errs, dict) else len(errs)
                
                trials = idx.get("trials", {})
                if isinstance(trials, dict):
                    train_tr = trials.get("train", {})
                    test_tr = trials.get("test", {})
                    run_data["trials_count"] = train_tr.get("total", 0) + test_tr.get("total", 0)
                    if run_data["test_passed"]:
                        run_data["best_percent_correct"] = 100.0
                    elif run_data["train_passed"]:
                        run_data["best_percent_correct"] = 99.0
        except Exception:
            pass

    # Strategy 2: Check for summary_report.json (Intermediate format)
    summary_file = task_dir / "summary_report.json"
    if summary_file.exists():
        try:
            with open(summary_file, "r") as f:
                summary = json.load(f)
                
                # Responses & tokens
                responses = summary.get("response_report", [])
                if responses:
                    run_data["steps_count"] = max(run_data["steps_count"], len(responses))
                    tot_prompt = sum(r.get("token_usage", {}).get("prompt", 0) for r in responses)
                    tot_cand = sum(r.get("token_usage", {}).get("candidates", 0) for r in responses)
                    tot_time = sum(r.get("response_time", 0.0) for r in responses)
                    run_data["tokens"]["prompt"] = tot_prompt
                    run_data["tokens"]["candidates"] = tot_cand
                    run_data["tokens"]["total"] = tot_prompt + tot_cand
                    if run_data["duration_seconds"] == 0:
                        run_data["duration_seconds"] = tot_time

                # Test reports
                test_reports = summary.get("test_report", {})
                for code_name, examples in test_reports.items():
                    run_data["trials_count"] += 1
                    if "-test" in code_name:
                        if examples and all(ex.get("match", False) for ex in examples):
                            run_data["test_passed"] = True
                            run_data["best_percent_correct"] = 100.0
                    if "-train" in code_name:
                        if examples:
                            avg_pct = sum(ex.get("percent_correct", 0.0) for ex in examples) / len(examples)
                            if avg_pct > run_data["best_percent_correct"]:
                                run_data["best_percent_correct"] = avg_pct
                            if all(ex.get("match", False) for ex in examples):
                                run_data["train_passed"] = True
        except Exception:
            pass

    # Strategy 3: Check raw JSON test/train files directly
    for item in task_dir.iterdir():
        if item.name.endswith(".py"):
            run_data["has_code"] = True
        
        if item.name.endswith("test.json") and not run_data["test_passed"]:
            try:
                with open(item, "r") as tf:
                    t_json = json.load(tf)
                    if isinstance(t_json, list) and len(t_json) > 0:
                        if all(row.get("match") is True for row in t_json):
                            run_data["test_passed"] = True
                            run_data["best_percent_correct"] = 100.0
                            run_data["best_code_file"] = item.name.replace("-test.json", ".py")
            except Exception:
                pass

        if item.name.endswith("train.json") and not run_data["train_passed"]:
            try:
                with open(item, "r") as tf:
                    tr_json = json.load(tf)
                    if isinstance(tr_json, list) and len(tr_json) > 0:
                        avg_pct = sum(r.get("percent_correct", 0.0) for r in tr_json if "percent_correct" in r) / len(tr_json)
                        if avg_pct > run_data["best_percent_correct"]:
                            run_data["best_percent_correct"] = avg_pct
                        if all(row.get("match") is True for row in tr_json):
                            run_data["train_passed"] = True
            except Exception:
                pass

    return run_data


def mine_all_sessions(root_dir: Path):
    """Traverses all session suites and aggregates runs and puzzle correlations."""
    start_time = time.time()
    session_suites = sorted([d for d in root_dir.iterdir() if d.is_dir() and d.name.startswith("sessions")])
    
    all_runs = []
    puzzle_map = defaultdict(lambda: {
        "task_id": "",
        "total_runs": 0,
        "test_passed_count": 0,
        "train_passed_count": 0,
        "best_percent_correct": 0.0,
        "suites_seen": set(),
        "sessions_seen": [],
        "best_run": None,
    })

    suite_stats = defaultdict(lambda: {
        "suite_name": "",
        "sessions_count": 0,
        "task_runs_count": 0,
        "unique_puzzles": set(),
        "test_passed_runs": 0,
        "train_passed_runs": 0,
        "solved_puzzles": set(),
        "total_tokens": 0,
    })

    console.print(f"[bold cyan]Starting session mining across {len(session_suites)} suites...[/bold cyan]")

    for suite_dir in session_suites:
        suite_name = suite_dir.name
        session_dirs = [d for d in suite_dir.iterdir() if d.is_dir()]
        suite_stats[suite_name]["suite_name"] = suite_name
        suite_stats[suite_name]["sessions_count"] = len(session_dirs)

        for sess_dir in session_dirs:
            session_id = sess_dir.name
            task_dirs = [d for d in sess_dir.iterdir() if d.is_dir()]

            for t_dir in task_dirs:
                run_data = parse_task_dir(t_dir, suite_name, session_id)
                all_runs.append(run_data)

                # Update Suite Stats
                suite_stats[suite_name]["task_runs_count"] += 1
                suite_stats[suite_name]["unique_puzzles"].add(run_data["task_id"])
                suite_stats[suite_name]["total_tokens"] += run_data["tokens"]["total"]
                if run_data["test_passed"]:
                    suite_stats[suite_name]["test_passed_runs"] += 1
                    suite_stats[suite_name]["solved_puzzles"].add(run_data["task_id"])
                if run_data["train_passed"]:
                    suite_stats[suite_name]["train_passed_runs"] += 1

                # Update Puzzle Correlation
                p_entry = puzzle_map[run_data["task_id"]]
                p_entry["task_id"] = run_data["task_id"]
                p_entry["total_runs"] += 1
                p_entry["suites_seen"].add(suite_name)
                p_entry["sessions_seen"].append({
                    "suite": suite_name,
                    "session_id": session_id,
                    "test_passed": run_data["test_passed"],
                    "train_passed": run_data["train_passed"],
                    "pct_correct": run_data["best_percent_correct"],
                    "steps": run_data["steps_count"],
                })
                if run_data["test_passed"]:
                    p_entry["test_passed_count"] += 1
                if run_data["train_passed"]:
                    p_entry["train_passed_count"] += 1
                if run_data["best_percent_correct"] > p_entry["best_percent_correct"]:
                    p_entry["best_percent_correct"] = run_data["best_percent_correct"]
                    p_entry["best_run"] = {
                        "suite": suite_name,
                        "session_id": session_id,
                        "pct": run_data["best_percent_correct"],
                    }

    elapsed = time.time() - start_time
    console.print(f"[bold green]Mined {len(all_runs)} runs across {len(puzzle_map)} unique puzzles in {elapsed:.2f}s![/bold green]\n")

    # Serialize results
    reports_dir = root_dir / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)

    # Format puzzle map for JSON (convert sets to lists)
    puzzles_list = []
    for pid, pdata in puzzle_map.items():
        pdata["suites_seen"] = sorted(list(pdata["suites_seen"]))
        pdata["solve_rate"] = round((pdata["test_passed_count"] / pdata["total_runs"]) * 100, 2) if pdata["total_runs"] > 0 else 0.0
        puzzles_list.append(pdata)

    puzzles_list.sort(key=lambda x: (-x["test_passed_count"], -x["total_runs"], x["task_id"]))

    with open(reports_dir / "puzzle_correlations.json", "w") as f:
        json.dump(puzzles_list, f, indent=2)

    # Format suite stats
    suites_list = []
    for sname, sdata in suite_stats.items():
        unique_cnt = len(sdata["unique_puzzles"])
        solved_cnt = len(sdata["solved_puzzles"])
        suites_list.append({
            "suite_name": sname,
            "sessions_count": sdata["sessions_count"],
            "task_runs": sdata["task_runs_count"],
            "unique_puzzles": unique_cnt,
            "solved_puzzles": solved_cnt,
            "puzzle_solve_rate": round((solved_cnt / unique_cnt) * 100, 2) if unique_cnt > 0 else 0.0,
            "test_passed_runs": sdata["test_passed_runs"],
            "run_solve_rate": round((sdata["test_passed_runs"] / sdata["task_runs_count"]) * 100, 2) if sdata["task_runs_count"] > 0 else 0.0,
            "train_passed_runs": sdata["train_passed_runs"],
            "total_tokens": sdata["total_tokens"],
        })

    suites_list.sort(key=lambda x: -x["task_runs"])

    with open(reports_dir / "suite_summaries.json", "w") as f:
        json.dump(suites_list, f, indent=2)

    # Output Master Index Summary (lightweight)
    with open(reports_dir / "master_index.json", "w") as f:
        json.dump(all_runs, f, indent=2)

    total_runs = sum(s["task_runs"] for s in suites_list)
    total_unique_puzzles = len(puzzle_map)
    total_solved_puzzles = len([p for p in puzzles_list if p["test_passed_count"] > 0])
    total_test_passed_runs = sum(s["test_passed_runs"] for s in suites_list)

    # Render Summary Tables in Console
    if HAS_RICH:
        suite_table = Table(title="SEER 1.0 Benchmark Suites Summary", header_style="bold cyan")
        suite_table.add_column("Suite", style="cyan")
        suite_table.add_column("Batches", justify="right")
        suite_table.add_column("Runs", justify="right", style="magenta")
        suite_table.add_column("Unique Puzzles", justify="right")
        suite_table.add_column("Solved Puzzles", justify="right", style="green")
        suite_table.add_column("Puzzle Solve %", justify="right", style="bold green")
        suite_table.add_column("Run Solve %", justify="right", style="yellow")

        for s in suites_list:
            suite_table.add_row(
                s["suite_name"],
                str(s["sessions_count"]),
                f"{s['task_runs']:,}",
                str(s["unique_puzzles"]),
                str(s["solved_puzzles"]),
                f"{s['puzzle_solve_rate']:.1f}%",
                f"{s['run_solve_rate']:.1f}%",
            )
        console.print(suite_table)

        top_table = Table(title="Top Repeated & Solved Puzzles (Sample)", header_style="bold magenta")
        top_table.add_column("Puzzle ID", style="bold cyan")
        top_table.add_column("Total Runs", justify="right", style="magenta")
        top_table.add_column("Test Passed", justify="right", style="bold green")
        top_table.add_column("Train Passed", justify="right", style="yellow")
        top_table.add_column("Solve Rate", justify="right", style="green")
        top_table.add_column("Max % Correct", justify="right", style="cyan")
        top_table.add_column("Suites Tested", style="dim")

        for p in puzzles_list[:25]:
            top_table.add_row(
                p["task_id"],
                str(p["total_runs"]),
                str(p["test_passed_count"]),
                str(p["train_passed_count"]),
                f"{p['solve_rate']:.1f}%",
                f"{p['best_percent_correct']:.1f}%",
                ", ".join(p["suites_seen"][:3]) + ("..." if len(p["suites_seen"]) > 3 else ""),
            )
        console.print(top_table)
    else:
        print("\n" + "="*80)
        print(f"{'SUITE':<30} {'BATCHES':>8} {'RUNS':>8} {'UNIQUE':>8} {'SOLVED':>8} {'PUZZLE %':>10} {'RUN %':>8}")
        print("="*80)
        for s in suites_list:
            print(f"{s['suite_name']:<30} {s['sessions_count']:>8} {s['task_runs']:>8} {s['unique_puzzles']:>8} {s['solved_puzzles']:>8} {s['puzzle_solve_rate']:>9.1f}% {s['run_solve_rate']:>7.1f}%")
        print("="*80 + "\n")

        print("="*80)
        print(f"{'PUZZLE ID':<12} {'RUNS':>6} {'TEST PASS':>10} {'TRAIN PASS':>11} {'SOLVE RATE':>12} {'MAX %':>8} {'SUITES':<25}")
        print("="*80)
        for p in puzzles_list[:30]:
            suites_str = ", ".join(p["suites_seen"][:3])
            print(f"{p['task_id']:<12} {p['total_runs']:>6} {p['test_passed_count']:>10} {p['train_passed_count']:>11} {p['solve_rate']:>11.1f}% {p['best_percent_correct']:>7.1f}% {suites_str:<25}")
        print("="*80 + "\n")

    # Global Grand Summary Panel
    grand_summary = f"""==================================================
GRAND TOTALS ACROSS SEER 1.0 CORPUS:
• Total Benchmark Suites:     {len(suites_list)}
• Total Session Batches:       {sum(s['sessions_count'] for s in suites_list)}
• Total Task Runs:             {total_runs:,}
• Total Unique Puzzles:        {total_unique_puzzles:,}
• Unique Puzzles Solved:       {total_solved_puzzles:,} ({(total_solved_puzzles/total_unique_puzzles)*100:.2f}%)
• Total Test-Passing Runs:     {total_test_passed_runs:,}
• Output Reports Saved In:     {reports_dir}
=================================================="""

    print(grand_summary)

if __name__ == "__main__":
    scripts_dir = Path(__file__).resolve().parent
    seer_sessions_root = scripts_dir.parent
    mine_all_sessions(seer_sessions_root)
