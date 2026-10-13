# -*- coding: utf-8 -*-
"""
tools/exportar_notebooklm.py — Exporta toda la tarea a texto plano (.txt)
para subirla a NotebookLM y hacer búsquedas/preguntas sobre el material.

    python tools/exportar_notebooklm.py

Escribe en `notebooklm/` un .txt por archivo relevante (.py, .yaml, .md) y un
índice `00_INDICE.txt`.
"""
import os

RAIZ_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ_DIR, 'notebooklm')

EXTENSIONES = ('.py', '.yaml', '.md', '.txt')
EXCLUIR_CARPETAS = {'notebooklm', '__pycache__', '.git', 'img', 'config'}
EXCLUIR_ARCHIVOS = {'grader_local.py', 'grader_ofuscado.txt', '.gitignore'}


def _nombre_plano(ruta):
    rel = os.path.relpath(ruta, RAIZ_DIR)
    return rel.replace(os.sep, '__')


def exportar():
    os.makedirs(DESTINO, exist_ok=True)
    indice = []
    n = 0
    for carpeta, dirs, archivos in os.walk(RAIZ_DIR):
        dirs[:] = [d for d in dirs if d not in EXCLUIR_CARPETAS]
        for archivo in archivos:
            if archivo in EXCLUIR_ARCHIVOS:
                continue
            if not archivo.endswith(EXTENSIONES):
                continue
            ruta = os.path.join(carpeta, archivo)
            try:
                with open(ruta, 'r', encoding='utf-8') as f:
                    contenido = f.read()
            except (UnicodeDecodeError, OSError):
                continue
            nombre = _nombre_plano(ruta) + '.txt'
            with open(os.path.join(DESTINO, nombre), 'w', encoding='utf-8') as f:
                f.write(contenido)
            indice.append(nombre)
            n += 1

    with open(os.path.join(DESTINO, '00_INDICE.txt'), 'w', encoding='utf-8') as f:
        f.write('Archivos exportados (%d):\n\n' % n)
        f.write('\n'.join(sorted(indice)))
    print('Exportados %d archivos a notebooklm/' % n)


if __name__ == '__main__':
    exportar()
