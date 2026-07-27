# Definition of Done — Semana 2

Una historia de usuario se considera **Done** cuando cumple TODO lo siguiente:

## 1. Criterios de aceptación como tests automatizados
- [ ] Cada criterio de aceptación de la historia está escrito en formato
      Gherkin (`Given/When/Then` → `Dado/Cuando/Entonces`) dentro de `features/`.
- [ ] Existe un test automatizado (`pytest-bdd`) que implementa cada escenario
      del `.feature` correspondiente.
- [ ] Todos los tests de la historia pasan en local y en CI.

## 2. Cobertura de código
- [ ] La cobertura total del proyecto es **≥ 80%** (`pytest --cov`).
- [ ] El código nuevo de la historia no reduce la cobertura existente.

## 3. Calidad estática
- [ ] `ruff check .` no reporta errores (reglas E, F, I, UP, B).
- [ ] `mypy .` no reporta errores, incluyendo funciones sin tipar
      (`disallow_untyped_defs`).

## 4. Flujo de trabajo y revisión
- [ ] El trabajo se hizo en una rama propia: `feature/<historia>`.
- [ ] Se abrió un Pull Request contra `main`/`develop`.
- [ ] El autor leyó su propio diff línea por línea en la pestaña
      "Files changed" antes de solicitar o realizar el merge, verificando:
  - Que no quede código de depuración, comentarios muertos o prints.
  - Que los nombres de variables/funciones sean claros.
  - Que cada cambio de comportamiento tenga su test correspondiente.
  - Que no se hayan colado archivos temporales, credenciales o secretos.

## 5. Documentación
- [ ] El README y/o la documentación técnica relevante quedaron
      actualizados si la historia cambió comportamiento visible o la API.

---

### Ejemplo de checklist rápido para copiar en cada PR

```markdown
- [ ] Escenarios Gherkin escritos y testeados
- [ ] Cobertura ≥ 80%
- [ ] ruff check . sin errores
- [ ] mypy . sin errores
- [ ] Diff propio revisado línea por línea
- [ ] Documentación actualizada
```
