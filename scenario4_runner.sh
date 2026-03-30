#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

cd "$ROOT_DIR"

echo "[1/4] Compiling attack demos..."
gcc -std=c99 -Wall -Wextra -O2 -o montgomery_overflow_attack montgomery_overflow_attack.c
gcc -std=c99 -Wall -Wextra -O2 -o barrett_overflow_attack barrett_overflow_attack.c

echo "[2/4] Running Montgomery attack suite..."
./montgomery_overflow_attack

echo "[3/4] Running Barrett attack suite..."
./barrett_overflow_attack

echo "[4/4] Generating graphs..."
python3 plot_reduction_attack_graphs.py

echo "Done. Outputs:"
echo "- montgomery_attack_results.csv"
echo "- barrett_attack_results.csv"
echo "- graphs/graph1_attack_success_rate.png"
echo "- graphs/graph2_performance_time_vs_input_size.png"
echo "- graphs/graph3_cia_security_score_comparison.png"
echo "- graphs/graph4_latency_overhead_per_testcase.png"
echo "- graphs/cia_scores.csv"
