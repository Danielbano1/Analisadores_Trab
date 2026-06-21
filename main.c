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
    int potenciaLampada = 0;
    int potenciaUmidificador = 0;
    int umidade = 0;
    int movimento = 0;

    // Execucao
    potenciaLampada = 100;
    if (umidade < 40) {
        alerta("Monitor", "Ar seco detectado", 0, 0);
        if (verificar("umidificador") == 0) {
            ligar("umidificador");
            potenciaUmidificador = 100;
            if (movimento == 1) {
                ligar("lampada");
            } else {
                desligar("lampada");
            }
        }
    }
    return 0;
}
