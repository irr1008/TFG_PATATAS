"""Plantilla de datos privados de las parcelas (valores ficticios).

Copia este archivo como datos_parcelas_privados.py en la carpeta
TFG_PATATAS_TRABAJO/privado de Drive y sustituye los valores por los reales
(municipio, variedad y poligonos GeoJSON con orden longitud, latitud).
El archivo con los datos reales NO se sube al repositorio.
"""

CATALOGO = [
    {
        "parcela_id": "pancostales",
        "nombre": "Pancostales",
        "municipio": "Municipio de ejemplo",
        "variedad": "Variedad de ejemplo",
        "archivo_geometria": "pancostales.geojson",
    },
    {
        "parcela_id": "puri",
        "nombre": "Puri",
        "municipio": "Municipio de ejemplo",
        "variedad": "Variedad de ejemplo",
        "archivo_geometria": "puri.geojson",
    },
    {
        "parcela_id": "la_culebra",
        "nombre": "La Culebra",
        "municipio": "Municipio de ejemplo",
        "variedad": "Variedad de ejemplo",
        "archivo_geometria": "la_culebra.geojson",
    },
    {
        "parcela_id": "los_ceres",
        "nombre": "Los Ceres",
        "municipio": "Municipio de ejemplo",
        "variedad": "Variedad de ejemplo",
        "archivo_geometria": "los_ceres.geojson",
    },
]

GEOMETRIAS = {
    "pancostales": r'''{
  "type": "Polygon",
  "coordinates": [
    [
      [
        0.0,
        0.0
      ],
      [
        0.001,
        0.0
      ],
      [
        0.001,
        0.001
      ],
      [
        0.0,
        0.001
      ],
      [
        0.0,
        0.0
      ]
    ]
  ]
}''',
    "puri": r'''{
  "type": "Polygon",
  "coordinates": [
    [
      [
        0.002,
        0.0
      ],
      [
        0.003,
        0.0
      ],
      [
        0.003,
        0.001
      ],
      [
        0.002,
        0.001
      ],
      [
        0.002,
        0.0
      ]
    ]
  ]
}''',
    "la_culebra": r'''{
  "type": "Polygon",
  "coordinates": [
    [
      [
        0.004,
        0.0
      ],
      [
        0.005,
        0.0
      ],
      [
        0.005,
        0.001
      ],
      [
        0.004,
        0.001
      ],
      [
        0.004,
        0.0
      ]
    ]
  ]
}''',
    "los_ceres": r'''{
  "type": "Polygon",
  "coordinates": [
    [
      [
        0.006,
        0.0
      ],
      [
        0.007,
        0.0
      ],
      [
        0.007,
        0.001
      ],
      [
        0.006,
        0.001
      ],
      [
        0.006,
        0.0
      ]
    ]
  ]
}''',
}
