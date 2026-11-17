# Guía rápida de Git para el equipo

```bash
git clone <URL_DEL_REPOSITORIO>
cd <carpeta_del_repositorio>
git checkout -b feature/nombre-de-tu-rama        # crea tu rama
# ... trabajas en tu archivo ...
git add archivo.py
git commit -m "Agrega validación de teléfono en Cliente"
git push -u origin feature/nombre-de-tu-rama
```

Después, en GitHub: **Pull request** de tu rama hacia `main`, pide revisión a un compañero y, cuando la aprueben, haz **Merge**.

Recomendaciones para la rúbrica (30 puntos):
- Un issue por integrante, con responsable asignado.
- Varios commits pequeños con mensajes claros, no uno solo al final.
- Que los 5 integrantes aparezcan con commits y pull requests.
