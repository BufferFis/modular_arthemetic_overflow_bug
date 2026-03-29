#define _POSIX_C_SOURCE 199309L
#include <stdint.h>
#include <stdio.h>
#include <time.h>

#define WORD_BITS 16u
#define R_VALUE (1u << WORD_BITS)
#define TEST_COUNT 5
#define BENCH_ITERATIONS 200000u

typedef struct {
    const char *name;
    uint32_t a;
    uint32_t b;
    uint32_t n;
} MontgomeryTestCase;

static uint32_t bit_length_u32(uint32_t x) {
    uint32_t bits = 0;
    while (x != 0) {
        bits++;
        x >>= 1;
    }
    return bits == 0 ? 1 : bits;
}

static uint32_t n_prime_for_r(uint32_t n) {
    int64_t t = 0;
    int64_t new_t = 1;
    int64_t r = (int64_t)R_VALUE;
    int64_t new_r = (int64_t)n;

    while (new_r != 0) {
        int64_t q = r / new_r;

        int64_t tmp_t = t - q * new_t;
        t = new_t;
        new_t = tmp_t;

        int64_t tmp_r = r - q * new_r;
        r = new_r;
        new_r = tmp_r;
    }

    if (r != 1) {
        return 0;
    }

    if (t < 0) {
        t += (int64_t)R_VALUE;
    }

    return (uint32_t)((R_VALUE - (uint32_t)t) & 0xFFFFu);
}

static uint32_t montgomery_redc_safe(uint32_t T, uint32_t n, uint32_t n_prime) {
    uint32_t m = ((T & 0xFFFFu) * n_prime) & 0xFFFFu;
    uint32_t t = (uint32_t)(((uint64_t)T + (uint64_t)m * n) >> WORD_BITS);

    if (t >= n) {
        t -= n;
    }

    return t;
}

static uint32_t montgomery_redc_vulnerable(uint32_t T, uint32_t n, uint32_t n_prime) {
    uint16_t m = (uint16_t)(((uint16_t)T * (uint16_t)n_prime));
    uint16_t mixed = (uint16_t)(T + (uint16_t)(m * (uint16_t)n));
    uint32_t t = (uint32_t)(mixed >> WORD_BITS); /* Always zero because shift is after truncation. */

    if (t >= n) {
        t -= n;
    }

    return t;
}

static uint32_t montgomery_mul_safe(uint32_t a, uint32_t b, uint32_t n, uint32_t n_prime) {
    uint32_t a_bar = (uint32_t)(((uint64_t)a * R_VALUE) % n);
    uint32_t b_bar = (uint32_t)(((uint64_t)b * R_VALUE) % n);
    uint32_t t = montgomery_redc_safe((uint32_t)((uint64_t)a_bar * b_bar), n, n_prime);
    return montgomery_redc_safe(t, n, n_prime);
}

static uint32_t montgomery_mul_vulnerable(uint32_t a, uint32_t b, uint32_t n, uint32_t n_prime) {
    uint32_t a_bar = (uint32_t)(((uint64_t)a * R_VALUE) % n);
    uint32_t b_bar = (uint32_t)(((uint64_t)b * R_VALUE) % n);

    /* Famous class of bug: truncation of the product before reduction. */
    uint16_t truncated_T = (uint16_t)((uint32_t)a_bar * (uint32_t)b_bar);
    uint32_t t = montgomery_redc_vulnerable((uint32_t)truncated_T, n, n_prime);
    return montgomery_redc_vulnerable(t, n, n_prime);
}

static uint64_t now_ns(void) {
    struct timespec ts;
    clock_gettime(CLOCK_MONOTONIC, &ts);
    return (uint64_t)ts.tv_sec * 1000000000ull + (uint64_t)ts.tv_nsec;
}

static double benchmark_safe(const MontgomeryTestCase *tc, uint32_t n_prime) {
    uint64_t start = now_ns();
    volatile uint32_t sink = 0;

    for (uint32_t i = 0; i < BENCH_ITERATIONS; i++) {
        sink ^= montgomery_mul_safe(tc->a, tc->b, tc->n, n_prime);
    }

    uint64_t elapsed = now_ns() - start;
    if (sink == 0xFFFFFFFFu) {
        printf("ignore: %u\n", sink);
    }

    return (double)elapsed / (double)BENCH_ITERATIONS;
}

static double benchmark_vulnerable(const MontgomeryTestCase *tc, uint32_t n_prime) {
    uint64_t start = now_ns();
    volatile uint32_t sink = 0;

    for (uint32_t i = 0; i < BENCH_ITERATIONS; i++) {
        sink ^= montgomery_mul_vulnerable(tc->a, tc->b, tc->n, n_prime);
    }

    uint64_t elapsed = now_ns() - start;
    if (sink == 0xFFFFFFFFu) {
        printf("ignore: %u\n", sink);
    }

    return (double)elapsed / (double)BENCH_ITERATIONS;
}

int main(void) {
    MontgomeryTestCase tests[TEST_COUNT] = {
        {"M1_small_balanced", 1234u, 5678u, 65521u},
        {"M2_medium", 16000u, 20000u, 65521u},
        {"M3_large_overflow", 65000u, 64999u, 65521u},
        {"M4_edge_high", 65500u, 65499u, 65521u},
        {"M5_prime_mod_mix", 54321u, 65500u, 65519u}
    };

    FILE *csv = fopen("montgomery_attack_results.csv", "w");
    if (csv == NULL) {
        perror("montgomery_attack_results.csv");
        return 1;
    }

    fprintf(csv,
            "method,test_case,input_size_bits,a,b,n,expected,vulnerable_result,prevented_result,"
            "attack_success_before,attack_success_after,time_ns_before,time_ns_after,latency_overhead_ns\n");

    uint32_t attacks_before = 0;
    uint32_t attacks_after = 0;

    printf("===== Montgomery Reduction Attack Demo =====\n");
    printf("Vulnerability: overflow/truncation before REDC in fixed-width arithmetic\n\n");

    for (uint32_t i = 0; i < TEST_COUNT; i++) {
        MontgomeryTestCase tc = tests[i];
        uint32_t n_prime = n_prime_for_r(tc.n);

        if (n_prime == 0u) {
            printf("[SKIP] %s -> modulus %u has no inverse modulo R\n", tc.name, tc.n);
            continue;
        }

        uint32_t expected = (uint32_t)(((uint64_t)tc.a * tc.b) % tc.n);
        uint32_t vulnerable_result = montgomery_mul_vulnerable(tc.a, tc.b, tc.n, n_prime);
        uint32_t safe_result = montgomery_mul_safe(tc.a, tc.b, tc.n, n_prime);

        uint32_t attack_before = vulnerable_result != expected ? 1u : 0u;
        uint32_t attack_after = safe_result != expected ? 1u : 0u;

        attacks_before += attack_before;
        attacks_after += attack_after;

        double t_before = benchmark_vulnerable(&tc, n_prime);
        double t_after = benchmark_safe(&tc, n_prime);
        double overhead = t_after - t_before;

        uint32_t input_bits = bit_length_u32(tc.a > tc.b ? tc.a : tc.b);

        printf("[%s] expected=%u vulnerable=%u safe=%u attack_before=%u attack_after=%u\n",
               tc.name,
               expected,
               vulnerable_result,
               safe_result,
               attack_before,
               attack_after);

        fprintf(csv,
                "montgomery,%s,%u,%u,%u,%u,%u,%u,%u,%u,%u,%.4f,%.4f,%.4f\n",
                tc.name,
                input_bits,
                tc.a,
                tc.b,
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
    printf("CSV written: montgomery_attack_results.csv\n");

    return 0;
}
