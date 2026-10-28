# Laboratorio 7 Niveles de prueba

Sistema de biblioteca en Python con pruebas unitarias, de integración y de sistema.

## Actividad adicional del 27 de octubre de 2026

Se agregaron **cinco pruebas** en `test_adicionales.py` para practicar
configuración, excepciones, aislamiento y automatización de consola.
Las pruebas de integración también comprueban que una operación rechazada
conserve el estado del libro y del historial.

| Caso | Escenario | Resultado esperado | Herramientas |
|---|---|---|---|
| PA-01 | Préstamos deshabilitados | Mensaje `Loans are disabled`, libro disponible e historial vacío | Fixture, `monkeypatch.setitem`, `capsys` |
| PA-02 | Devolución con usuario inexistente | `ValueError: User not found`; el libro sigue prestado y el historial no cambia | `pytest.raises`, copia del estado anterior |
| PA-03 | Préstamo de ISBN inexistente | `ValueError: Book not found`; no se modifica el catálogo ni el historial | Fixture, `pytest.raises` |
| PA-04 | Opción 3 del menú con historial vacío | Se muestra `User history: []` y se puede salir con 0 | `monkeypatch` de `input`, `capsys` |
| PA-05 | Opción inválida seguida de una consulta válida | Se muestra un único `Invalid option`; después se consulta el historial y se sale | Secuencia de entradas, `capsys`, verificación del orden |

## Preparar y ejecutar

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt

# Solamente las cinco pruebas adicionales
pytest -m adicionales -v

# Suite completa: seis casos previos y cinco nuevos
pytest -v

# Opcional: ejecutar por nivel las pruebas nuevas
pytest -m "adicionales and integration" -v
pytest -m "adicionales and system" -v
```

Entorno de la evidencia: macOS, Python 3.13.5 y pytest 9.2.0.
`pytest.ini` permite descubrir tanto `test.py` como `test_*.py`, registra los
marcadores y activa `--strict-markers`.

## Resultados y evidencia

- Pruebas adicionales: **5 aprobadas**, 6 casos previos deseleccionados.
- Suite completa: **11 aprobadas**, sin fallos ni advertencias.
- Los registros y las dos capturas están en `evidencias/actividad_adicional/`.
- Las capturas muestran una consola web local que ejecutó pytest y presentó su
  salida real completa; los archivos TXT conservan la misma ejecución.

| Ejecución | Captura | Registro |
|---|---|---|
| Cinco pruebas adicionales | [Ver captura](evidencias/actividad_adicional/01-adicionales.jpg) | [Ver salida](evidencias/actividad_adicional/01-adicionales.txt) |
| Suite completa | [Ver captura](evidencias/actividad_adicional/02-suite-completa.jpg) | [Ver salida](evidencias/actividad_adicional/02-suite-completa.txt) |

## Ajustes a las pruebas previas

Antes de la ampliación, la ejecución explícita de `pytest test.py -v` produjo
4 aprobadas y 2 fallidas. Las dos pruebas de `Library` enviaban los argumentos
en orden inverso. Se corrigieron para usar `borrow_book(user_id, isbn)` y se
ajustó la excepción esperada de usuario inexistente a `User not found`, que es
el contrato actual de la clase. Se conservaron los seis casos existentes.

La ampliación modifica pruebas y su configuración; no modifica las clases ni
el menú. Los defectos previamente documentados en las opciones 1 y 2 del menú
y en la redacción de mensajes e historial siguen pendientes. Los 11 casos
aprobados corresponden a los escenarios enumerados aquí y en `test.py`.

Repositorio de entrega: https://github.com/gabrielgcortes/Lab-7-Niveles-de-prueba
