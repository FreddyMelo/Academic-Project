#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <fcntl.h>

void generate_symkey(unsigned long *skey) {
    const unsigned long a = 0x23fa259a219d2843;
    const unsigned long b = 0x9654e78f1facc0ab;
    int urand = open("/dev/urandom", O_RDONLY);
    for (int i = 0; i < 2; i++) {
        unsigned long r;
        read(urand, &r, 1);
        skey[i] = a * r + b;
    }
    close(urand);
}

int encrypt_message() {
    char cmdline[512];

    unsigned long skey[2] = {0};
    generate_symkey(skey);
    char hsymkey[33];
    sprintf(hsymkey, "%016lx%016lx", skey[0], skey[1]);

    FILE *msg = fopen("message.txt", "w");
    if (!msg) {
        perror("Failed to create message.txt");
        return 0;
    }
    fprintf(msg, "<html>\n<body>\n\n<h1>Heading</h1>\n<p>Paragraph.</p>\n\n</body>\n</html>");
    fclose(msg);

    sprintf(cmdline, "openssl aes-128-ctr -e -in message.txt -out cloud_all.ehtml -K %s -iv %s", hsymkey, hsymkey);
    if (system(cmdline) != 0) {
        fprintf(stderr, "OpenSSL encryption failed\n");
        return 0;
    }

    printf("Message encrypted to cloud_all.ehtml\n");
    printf("Symmetric key (hex): %s\n", hsymkey);
    return 1;
}

int main() {
    if (!encrypt_message()) {
        fprintf(stderr, "Encryption failed\n");
        return 1;
    }
    return 0;
}
