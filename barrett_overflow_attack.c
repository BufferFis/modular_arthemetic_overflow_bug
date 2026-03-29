#define _POSIX_C_SOURCE 199309L
#include <stdint.h>
#include <stdio.h>
#include <time.h>

#define K_BITS 16u
#define TEST_COUNT 5
#define BENCH_ITERATIONS 200000u

typedef struct {
    const char *name;
    uint32_t x;
    uint32_t n;
} BarrettTestCase;

static uint32_t bit_length_u32(uint32_t x) {
    uint32_t bits = 0;
    while (x != 0) {
        bits++;
        x >>= 1;
    }
    return bits == 0 ? 1 : bits;
}

static uint32_t barrett_mu(uint32_t n) {
    return (uint32_t)(((uint64_t)1 << (2u * K_BITS)) / n);
}

static uint32_t barrett_reduce_safe(uint32_t x, uint32_t n, uint32_t mu) {
    uint64_t q1 = ((uint64_t)x) >> (K_BITS - 1u);
    uint64_t q2 = q1 * (uint64_t)mu;
    uint64_t q3 = q2 >> (K_BITS + 1u);

    int64_t r = (int64_t)x - (int64_t)(q3 * (uint64_t)n);
    while (r < 0) {
        r += (int64_t)n;
    }
    while ((uint64_t)r >= (uint64_t)n) {
        r -= (int64_t)n;
    }

    return (uint32_t)r;
}

static uint32_t barrett_reduce_vulnerable(uint32_t x, uint32_t n, uint32_t mu) {
    uint16_t q1 = (uint16_t)(x >> (K_BITS - 1u));

    /* Famous class of bug: intermediate multiplication overflow/truncation in reduction. */
    uint16_t q2 = (uint16_t)(q1 * (uint16_t)mu);
    uint16_t q3 = (uint16_t)(q2 >> (K_BITS + 1u));

    int64_t r = (int64_t)x - (int64_t)q3 * (int64_t)n;

    /* Another common bug: assumes at most one correction is enough. */
    if (r < 0) {
        r += (int64_t)n;
    }
    if ((uint64_t)r >= (uint64_t)n) {
        r -= (int64_t)n;
    }

    return (uint32_t)r;
}

static uint64_t now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ull + (uint64_t)ts.tv_nsec;
}

static double benchmark_safe(const BarrettTestCase *tc, uint32_t mu) {
    uint64_t start = now_ns();
    volatile uint32_t sink = 0;

    for (uint32_t i = 0; i < BENCH_ITERATIONS; i++) {
        sink ^= barrett_reduce_safe(tc->x, tc->n, mu);
    }

    uint64_t elapsed = now_ns() - start;
    if (sink == 0xFFFFFFFFu) {
        printf("ignore: %u\n", sink);
    }

    return (double)elapsed / (double)BENCH_ITERATIONS;
}

static double benchmark_vulnerable(const BarrettTestCase *tc, uint32_t mu) {
    uint64_t start = now_ns();
    volatile uint32_t sink = 0;

    for (uint32_t i = 0; i < BENCH_ITERATIONS; i++) {
        sink ^= barrett_reduce_vulnerable(tc->x, tc->n, mu);
    }

    uint64_t elapsed = now_ns() - start;
    if (sink == 0xFFFFFFFFu) {
        printf("ignore: %u\n", sink);
    }

    return (double)elapsed / (double)BENCH_ITERATIONS;
}

int main(void) {
    BarrettTestCase tests[TEST_COUNT] = {
        {"B1_baseline", 123456789u, 65521u},
        {"B2_high_x", 4000000000u, 65521u},
        {"B3_max_u32", 4294967295u, 65521u},
        {"B4_alt_modulus", 3987654321u, 50021u},
        {"B5_dense_values", 3700000000u, 32749u}
    };

    FILE *csv = fopen("barrett_attack_results.csv", "w");
    if (csv == NULL) {
        perror("barrett_attack_results.csv");
        return 1;
    }

    fprintf(csv,
            "method,test_case,input_size_bits,x,n,expected,vulnerable_result,prevented_result,"
            "attack_success_before,attack_success_after,time_ns_before,time_ns_after,latency_overhead_ns\n");

    uint32_t attacks_before = 0;
    uint32_t attacks_after = 0;

    printf("===== Barrett Reduction Attack Demo =====\n");
    printf("Vulnerability: overflow in q1 * mu approximation step\n\n");

    for (uint32_t i = 0; i < TEST_COUNT; i++) {
        BarrettTestCase tc = tests[i];
        uint32_t mu = barrett_mu(tc.n);

        uint32_t expected = tc.x % tc.n;
        uint32_t vulnerable_result = barrett_reduce_vulnerable(tc.x, tc.n, mu);
        uint32_t safe_result = barrett_reduce_safe(tc.x, tc.n, mu);

        uint32_t attack_before = vulnerable_result != expected ? 1u : 0u;
        uint32_t attack_after = safe_result != expected ? 1u : 0u;

        attacks_before += attack_before;
        attacks_after += attack_after;

        double t_before = benchmark_vulnerable(&tc, mu);
        double t_after = benchmark_safe(&tc, mu);
        double overhead = t_after - t_before;

        uint32_t input_bits = bit_length_u32(tc.x);

        printf("[%s] expected=%u vulnerable=%u safe=%u attack_before=%u attack_after=%u\n",
               tc.name,
               expected,
               vulnerable_result,
               safe_result,
               attack_before,
               attack_after);

        fprintf(csv,
                "barrett,%s,%u,%u,%u,%u,%u,%u,%u,%u,%.4f,%.4f,%.4f\n",
                tc.name,
                input_bits,
                tc.x,
                tc.n,
                expected,
                vulnerable_result,
                safe_result,
                attack_before,
                attack_after,
                t_before,
                t_after,
                overhead);
    }

    fclose(csv);

    printf("\nAttack success rate before prevention: %.2f%%\n",
           100.0 * (double)attacks_before / (double)TEST_COUNT);
    printf("Attack success rate after prevention : %.2f%%\n",
           100.0 * (double)attacks_after / (double)TEST_COUNT);
    printf("CSV written: barrett_attack_results.csv\n");

    return 0;
}
