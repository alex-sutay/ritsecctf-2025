#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <time.h>

#define SUCCESS 0
#define FAILURE -1
#define MD5_CMD_FMT "md5sum %s | grep %s"
#define RM_CMD_FMT "rm %s"
#define FNAME_FMT "/tmp/tmp-%d.txt"

// freebies ;) don't say I gave you nothing
__asm__("pop %rdi\n\t"
        "ret");
__asm__(".globl gadget\n\t"
        "gadget:\n\t"
        "mov %rax, %rsi\n\t"
        "ret");

int add_char_to_string(char* s, char c) {
  int l = strlen(s); 
  s[l] = c;
  s[l+1] = 0;
  return SUCCESS;
}

int generate_md5(char* s) {
  short r;
  char c;
  for (int i = 0; i < 32; i++) {
    r = rand() % 16;
    if (r < 10) {
      c = r + 48;
    } else {
      c = r + 87;
    }
    if (SUCCESS != add_char_to_string(s, c)) {
      return FAILURE;
    }
  }
  return SUCCESS;
}

int game(char* target, char* fname, char* md5_cmd, char* rm_cmd) {
  char input[1000];
  FILE *fptr;


  printf("Your target MD5sum is:\n%s\nEnter some text to reach it for a flag > ", target);

  if (0 == fgets(input, 0x1000, stdin)) {
    printf("Failed to get input :(\n");
    return FAILURE;
  }

  if (NULL == (fptr = fopen(fname, "w"))) {
    printf("Failed to open :(\n");
    return FAILURE;
  }

  if (0 == (fprintf(fptr, input))) {
    printf("Failed to fprintf :(\n");
    return FAILURE;
  }

  if (SUCCESS != fclose(fptr)) {
    printf("Failed to fclose :(\n");
    return FAILURE;
  }

  if (SUCCESS != system(md5_cmd)) {
    printf("Incorrect :(\n");
  } else {
    printf("Wowwie, good job! That's impressive, have a flag:\nFAKE{U53L355_N0T_R34L}\n:)\n");
  }

  if (SUCCESS != system(rm_cmd)) {
    printf("Failed to rm :(\n");
    return FAILURE;
  }

  return SUCCESS;
}

int main() {
  char* target = NULL;
  char* fname = NULL;
  char* md5_cmd = NULL;
  char* rm_cmd = NULL;
  int now = time(NULL);
  int rc = SUCCESS;

  srand(now);

  if (NULL == (target = malloc(33))) {
    printf("Malloc failed :(");
    rc = FAILURE;
  }

  if (SUCCESS != generate_md5(target)) {
    printf("Failed to generate a target :(\n");
    rc = FAILURE;
  }

  if (FAILURE == asprintf(&fname, FNAME_FMT, now)) {
    printf("Asprintf failed :(");
    rc = FAILURE;
  }

  if (FAILURE == asprintf(&md5_cmd, MD5_CMD_FMT, fname, target)) {
    printf("Asprintf failed :(");
    rc = FAILURE;
  }

  if (FAILURE == asprintf(&rm_cmd, RM_CMD_FMT, fname)) {
    printf("Asprintf failed :(");
    rc = FAILURE;
  }

  if (rc != FAILURE) {
    rc = game(target, fname, md5_cmd, rm_cmd);
  }
 
  free(target);
  free(fname);
  free(md5_cmd); 
  free(rm_cmd);
  return rc;
}
