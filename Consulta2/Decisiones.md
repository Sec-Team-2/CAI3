# ALGORITMO

| Algoritmo  | Fortalezas | Debilidades |
|------------|------------|------------|
| **ChaCha20** | Alta seguridad y rendimiento en software sin aceleración de hardware. Resistente a ataques criptoanalíticos. | No soporta cifrado en bloque, lo que puede no ser ideal para ciertas aplicaciones. |
| **Salsa20** | Rápido y eficiente en software. Buena resistencia criptoanalítica. | ChaCha20 es una mejora directa sobre Salsa20 y es preferido en implementaciones modernas. |
| **Blowfish** | Algoritmo flexible con clave de hasta 448 bits. Rápido en software sin hardware especializado. | Diseño antiguo con vulnerabilidades en versiones reducidas. No es recomendado para nuevos sistemas. |
| **AES** | Estándar de cifrado avanzado (Advanced Encryption Standard). Altamente seguro y eficiente con aceleración de hardware. | Puede ser lento en software sin aceleración de hardware. Propenso a ataques de canal lateral si no se implementa correctamente. |
| **Camellia** | Seguridad comparable a AES con buena eficiencia tanto en hardware como en software. | Menos soporte generalizado en comparación con AES. |
| **Serpent** | Diseño altamente seguro con margen de seguridad extra sobre AES. | Menos eficiente que AES y Camellia en términos de rendimiento. |
| **CAST** | Uso flexible con buena seguridad en versiones de 128 y 256 bits. | No tan ampliamente analizado como AES o Camellia. |
| **RSA** | Seguridad basada en la factorización de números primos. Ampliamente usado en criptografía de clave pública. | Lento en comparación con algoritmos simétricos. No adecuado para cifrado de grandes volúmenes de datos. |

## Alternativas Escogidas
Se han seleccionado los siguientes algoritmos:
- **ChaCha20**: Debido a su seguridad y eficiencia en software sin aceleración de hardware.
- **AES**: Estándar de cifrado ampliamente adoptado.
- **Camellia**: Alternativa robusta a AES con buena eficiencia en hardware y software.


# MODO DE OPERACIÓN
| Modo de Operación | Vulnerabilidades | Puntuación de Seguridad (1-10) |
|-------------------|------------------|-----------------------------|
| **ECB** | Cada bloque idéntico de texto plano se cifra en el mismo texto cifrado, lo que permite detectar patrones. | 3 |
| **OFB** | Más resistente a ataques de detección de patrones. Sin embargo, si se reutiliza un IV, puede comprometer la seguridad. | 9 |
| **CBC** | Filtración parcial de patrones en ciertos casos, especialmente con padding oracle attacks. | 6 |
| **CFB** | Menos vulnerable que CBC, pero aún susceptible a ciertos ataques de manipulación de bits. | 7 |

## Alternativa Escogida
Se ha seleccionado el siguiente modo de operación:
- **OFB (Output Feedback)**: Debido a su seguridad y resistencia a la detección de patrones, a diferencia de ECB y CBC, donde el atacante puede identificar estructuras en los datos cifrados.

## Notas
- ECB es altamente inseguro para la mayoría de los usos debido a su falta de aleatorización.
- CBC puede ser vulnerable a ataques si no se usa un padding seguro.
- CFB ofrece mayor seguridad que CBC pero no es la mejor opción en comparación con OFB.
- Se debe usar OFB con IV aleatorio.

