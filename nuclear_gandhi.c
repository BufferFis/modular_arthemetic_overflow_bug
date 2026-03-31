#include <stdio.h>
#include <stdint.h>

void show_gandhi_vulnerability() {
    printf("--- Vulnerable System ---\n");
    uint8_t gandhi_aggressiveness = 1; // 1 is very peaceful
    printf("Initial Gandhi Aggressiveness Score: %u (Peaceful)\n", gandhi_aggressiveness);
    
    // Some event lowers his aggressiveness by 2 (e.g. adopting democracy)
    uint8_t democracy_modifier = 2;
    printf("Applying democracy modifier: -%u\n", democracy_modifier);
    
    // Vulnerability: Underflow on unsigned 8-bit integer
    gandhi_aggressiveness = gandhi_aggressiveness - democracy_modifier;
    
    printf("Final Gandhi Aggressiveness Score: %u\n", gandhi_aggressiveness);
    if (gandhi_aggressiveness == 255) {
        printf("WARNING: Gandhi has gone nuclear! (Underflow occurred)\n");
    }
}

void show_gandhi_safe() {
    printf("\n--- Secure System ---\n");
    uint8_t gandhi_aggressiveness = 1;
    printf("Initial Gandhi Aggressiveness Score: %u (Peaceful)\n", gandhi_aggressiveness);
    
    uint8_t democracy_modifier = 2;
    printf("Applying democracy modifier: -%u\n", democracy_modifier);
    
    // Prevention: Check for underflow before subtracting
    if (gandhi_aggressiveness >= democracy_modifier) {
        gandhi_aggressiveness = gandhi_aggressiveness - democracy_modifier;
    } else {
        printf("Bounds check prevented underflow. Clamping to 0.\n");
        gandhi_aggressiveness = 0;
    }
    
    printf("Final Gandhi Aggressiveness Score: %u\n", gandhi_aggressiveness);
}

int main() {
    printf("=== Nuclear Gandhi Vulnerability Demo ===\n\n");
    show_gandhi_vulnerability();
    show_gandhi_safe();
    return 0;
}
