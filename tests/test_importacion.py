"""
Comprobación mínima de instalación e importación del paquete.
"""

import modelo_fisico


def test_paquete_importable():
    assert modelo_fisico.__name__ == "modelo_fisico"
