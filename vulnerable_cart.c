#include <stdio.h>
#include <stdint.h>

int main() {

    // Simulating a lightweight crypto token system
    uint8_t wallet_balance = 150;       // User has 150 tokens
    uint8_t token_price = 12;           // Each premium token costs 12 units

    // Attacker requests huge quantity
    uint8_t tokens_requested = 25;      
    uint8_t total_cost;

    printf("===== SecureChain Wallet v1.0 =====\n");
    printf("Wallet Balance        : %u tokens\n", wallet_balance);
    printf("Premium Token Price   : %u tokens\n\n", token_price);

    // 🔴 Vulnerable multiplication (8-bit overflow)
    total_cost = tokens_requested * token_price;

    printf("User requests %u premium tokens...\n", tokens_requested);
    printf("System computes total cost: %u × %u\n", 
           tokens_requested, token_price);

    printf("Stored total cost (after overflow): %u tokens\n", total_cost);

    // Security validation check
    if (total_cost <= wallet_balance) {

        wallet_balance -= total_cost;

        printf("\n[TRANSACTION APPROVED]\n");
        printf("Tokens transferred: %u\n", tokens_requested);
        printf("Remaining Balance : %u tokens\n", wallet_balance);

        printf("\n SECURITY BREACH DETECTED \n");
        printf("Actual cost should be: %u tokens\n",
               tokens_requested * token_price);
        printf("Attacker underpaid due to integer overflow!\n");

    } else {

        printf("\n[TRANSACTION DENIED] Insufficient balance.\n");
    }

    return 0;
}