// test.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/wait.h>
#include <readline/readline.h>
#include <readline/history.h>
#include <ctype.h>

#define MAXCOM   1000
#define MAXLIST  100
#define clear()  printf("\033[H\033[J")

void trim(char *str) {
    char *start, *end;
    start = str;
    while(isspace(*start) || *start == '"' || *start == '\'') start++;
    if(*start == 0) {
        str[0] = '\0';
        return;
    }
    end = start + strlen(start) - 1;
    while(end > start && (isspace(*end) || *end == '"' || *end == '\'')) end--;
    *(end + 1) = '\0';
    memmove(str, start, end - start + 2);
}

void getAICommand(const char* input, char* aiCommand, size_t sz) {
    char sanitized_input[1024];
    snprintf(sanitized_input, sizeof(sanitized_input), "%s", input);
    trim(sanitized_input);
    char cmd[2048];
    snprintf(cmd, sizeof(cmd),
        "/home/lenovo_user/zshell/venv/bin/python3 "
        "/home/lenovo_user/zshell/inference.py \"%s\"",
        sanitized_input);
    FILE* fp = popen(cmd, "r");
    if (!fp) {
        strncpy(aiCommand, "🤖 [AI ERROR]", sz);
        return;
    }
    if (fgets(aiCommand, sz, fp) == NULL) {
        strncpy(aiCommand, "🤖 [AI NO OUTPUT]", sz);
    } else {
        aiCommand[strcspn(aiCommand, "\n")] = '\0';
    }
    pclose(fp);
}

void init_shell() {
    clear();
    printf("\n\n\n\n**** MY SHELL ****\n\n");
    printf("    - USE AT YOUR OWN RISK -\n\n\n");
    char* user = getenv("USER");
    printf(" User: @%s\n", user);
    sleep(1);
    clear();
}

int takeInput(char* str) {
    char* buf = readline("\n>>> ");
    if (strlen(buf) != 0) {
        add_history(buf);
        strcpy(str, buf);
        return 0;
    }
    return 1;
}

void printDir() {
    char cwd[1024];
    getcwd(cwd, sizeof(cwd));
    printf("\nDir: %s", cwd);
}

void execArgs(char** parsed) {
    pid_t pid = fork();
    if (pid == -1) {
        printf("\nFailed forking child.\n");
    } else if (pid == 0) {
        if (execvp(parsed[0], parsed) < 0)
            printf("\nCould not execute command.\n");
        exit(0);
    } else {
        wait(NULL);
    }
}

void openHelp() {
    puts("\n*** SHELL HELP ***"
         "\n> cd"
         "\n> ls"
         "\n> exit"
         "\n> piping via |"
         "\n> ai: <natural language>"
         "\n");
}

int ownCmdHandler(char** parsed) {
    char* cmds[] = {"exit","cd","help","hello"};
    for (int i = 0; i < 4; i++) {
        if (strcmp(parsed[0], cmds[i]) == 0){
            switch (i) {
                case 0: exit(0);
                case 1: chdir(parsed[1]);   return 1;
                case 2: openHelp();         return 1;
                case 3: printf("\nHello!\n"); return 1;
            }
        }
    }
    return 0;
}

void parseSpace(char* str, char** parsed) {
    int i;
    for (i = 0; i < MAXLIST; i++) {
        parsed[i] = strsep(&str, " ");
        if (!parsed[i]) break;
        if (strlen(parsed[i]) == 0) i--;
    }
}

int isCommandAvailable(char* cmd) {
    char check[512];
    snprintf(check, sizeof(check), "which %s > /dev/null 2>&1", cmd);
    return (system(check) == 0);
}

int processString(char* str, char** parsed) {
    if (strncmp(str, "ai:", 3) == 0) {
        char aiOut[MAXCOM];
        getAICommand(str + 3, aiOut, sizeof(aiOut));
        printf("🤖 %s\n", aiOut);
        return 0;
    }
    parseSpace(str, parsed);
    if (ownCmdHandler(parsed)) return 0;
    if (!isCommandAvailable(parsed[0])) {
        char aiOut[MAXCOM];
        getAICommand(str, aiOut, sizeof(aiOut));
        printf("🤖 %s\n", aiOut);  // 🤖 emoji added
        return 0;
    }
    return 1;
}

int main() {
    char input[MAXCOM];
    char* parsed[MAXLIST];
    init_shell();
    while (1) {
        printDir();
        if (takeInput(input)) continue;
        int flag = processString(input, parsed);
        if (flag == 1) execArgs(parsed);
    }
    return 0;
}

