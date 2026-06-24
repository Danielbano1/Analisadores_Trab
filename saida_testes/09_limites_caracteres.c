#include <stdio.h>
#include <string.h>

int ligar(const char* namedevice) {
    printf("%s ligado!\n", namedevice);
    return 1;
}

int desligar(const char* namedevice) {
    printf("%s desligado!\n", namedevice);
    return 0;
}

int verificar(const char* namedevice) {
    printf("%s est ligado.\n", namedevice);
    return 1;
}

void alerta(const char* namedevice, const char* msg, int var, int has_var) {
    if (has_var) {
        printf("%s recebeu o alerta:\n%s %d\n", namedevice, msg, var);
    } else {
        printf("%s recebeu o alerta:\n%s\n", namedevice, msg);
    }
}

int main() {
    int obs_test_120_chars_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789 = 0;

    obs_test_120_chars_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789 = 1;
    if (obs_test_120_chars_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789 == 1) {
        alerta("dev_test_120_chars_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123", "msg_test_120_chars_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123456789_0123", 0, 0);
    }
    return 0;
}
