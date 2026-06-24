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
    int temperatura = 0;

    alerta("Termometro", "Temperatura esta em", temperatura, 1);
    return 0;
}
