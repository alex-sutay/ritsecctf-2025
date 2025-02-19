#include <stdio.h>
#include <string.h>
#include <stdlib.h>

/*
* Simple function to find seeds that will generate the characters we want
* We can compile in the docker image so we know the prng will work exactly the same
*/
int main() {
    int l, seed, r, i, found;
    char c;
    char* goal_static = "/bin/sh";
    char* goal;
    int* seeds;

    // setup
    found = 0;
    l = strlen(goal_static);
    goal = malloc(l + 1);
    strcpy(goal, goal_static);
    seeds = malloc(sizeof(int) * l);
    for (i=0; i < l; i++) {
        seeds[i] = 0;
    }

    seed = 0;
    while (found < l) {
        seed += 1;
        // generate a random number with each seed
        srand(seed);
        r = rand();
        // check if this seed gave us any character we need
        for (i=0; i < l; i++) {
            c = r & 0xff;
            if (goal[i] && ((int) goal[i]) == c) {
                seeds[i] = seed;
                goal[i] = '\0';
                found += 1;
                printf("Found '%c': %d -> %d (%c), %d/%d so far...\n", goal_static[i], seed, r, c, found, l);
            }
        }
        if (seed % 100 == 0) { 
            printf("Searched %d so far, found %d/%d...\n", seed, found, l);
        }
        if (seed > 1000) {
            break;
        }
    }
    // print results
    printf("\n\n");
    for (i=0; i<l; i++) {
        if (goal[i]) {
            printf("'%c' could not be found :(\n", goal[i]);
        } else {
            printf("'%c' acquired with seed %d\n", goal_static[i], seeds[i]);
        }
    }
    if (found == l) {
        // make importing into python easy
        printf("\nPython import:\nprng_seeds = {\n    ");
        for (i=0; i<l; i++) {
            // don't print if this is a duplicate
            if (strchr(goal_static+i+1, goal_static[i]) == 0) {
                printf("'%c': %d, ", goal_static[i], seeds[i]);
            }
        }
        printf("\n}\n\n");
    }
}
