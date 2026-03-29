# Reduction Method Attack Showcase

This folder now contains two software-level reduction method demos with intentional vulnerabilities, prevention paths, and graph-ready metrics.

## Files Added
- `montgomery_overflow_attack.c`
- `barrett_overflow_attack.c`
- `plot_reduction_attack_graphs.py`
- `reduction_attack_demo.md`

Generated at runtime:
- `montgomery_attack_results.csv`
- `barrett_attack_results.csv`
- `graphs/graph1_attack_success_rate.png`
- `graphs/graph2_performance_time_vs_input_size.png`
- `graphs/graph3_cia_security_score_comparison.png`
- `graphs/graph4_latency_overhead_per_testcase.png`
- `graphs/cia_scores.csv`

## Vulnerabilities Modeled

### 1) Montgomery reduction vulnerability
- **Type:** Intermediate truncation/overflow before REDC.
- **Where:** Vulnerable path narrows intermediate product and reduction operands to 16-bit.
- **Impact:** Wrong modular multiplication result (attack success).
- **Prevention:** Safe path uses widened intermediates (`uint64_t` where needed) and correct REDC flow.

### 2) Barrett reduction vulnerability
- **Type:** Bad quotient approximation pipeline due to narrowed arithmetic + single-step correction bug.
- **Where:** Vulnerable path truncates `q1 * mu` and assumes one correction is enough.
- **Impact:** Residue no longer equals `x mod n` for crafted large inputs.
- **Prevention:** Safe path performs quotient approximation and full correction with wide arithmetic.

## Test Cases
Each method has **5 test cases**.

### Montgomery test cases
- `M1_small_balanced`
- `M2_medium`
- `M3_large_overflow`
- `M4_edge_high`
- `M5_prime_mod_mix`

### Barrett test cases
- `B1_baseline`
- `B2_high_x`
- `B3_max_u32`
- `B4_alt_modulus`
- `B5_dense_values`

## Build And Run
```bash
gcc -std=c99 -Wall -Wextra -O2 -o montgomery_overflow_attack montgomery_overflow_attack.c
gcc -std=c99 -Wall -Wextra -O2 -o barrett_overflow_attack barrett_overflow_attack.c

./montgomery_overflow_attack
./barrett_overflow_attack

python3 plot_reduction_attack_graphs.py
```

## Graph Mapping

### Graph 1 - Attack Success Rate Before vs After Prevention
- Source: `attack_success_before`, `attack_success_after` columns
- Aggregation: mean across test cases per method
- Output: `graphs/graph1_attack_success_rate.png`

### Graph 2 - Performance: Time vs Input Size
- Source: `input_size_bits`, `time_ns_before`, `time_ns_after`
- Output: `graphs/graph2_performance_time_vs_input_size.png`

### Graph 3 - CIA Security Score Comparison
- Source: attack rates and timing overhead from CSV
- Scoring helper: derived CIA score model in `plot_reduction_attack_graphs.py`
- Output: `graphs/graph3_cia_security_score_comparison.png`
- Raw table: `graphs/cia_scores.csv`

### Graph 4 - Latency Overhead Per Test Case
- Source: `latency_overhead_ns`
- Defined as: safe path latency minus vulnerable path latency (ns/op)
- Output: `graphs/graph4_latency_overhead_per_testcase.png`

## Notes
- These demos are intentionally vulnerable for educational attack modeling.
- CIA values are analytical/scenario scores, not third-party benchmark standards.
- You can add more adversarial vectors by appending additional rows in each test table.
