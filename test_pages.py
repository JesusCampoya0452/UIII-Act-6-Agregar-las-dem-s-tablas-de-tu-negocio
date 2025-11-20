import requests

urls = [
    'http://127.0.0.1:8006/',
    'http://127.0.0.1:8006/clientes/',
    'http://127.0.0.1:8006/clientes/agregar/',
    'http://127.0.0.1:8006/empleados/',
    'http://127.0.0.1:8006/empleados/agregar/',
    'http://127.0.0.1:8006/servicios/',
    'http://127.0.0.1:8006/servicios/agregar/',
    'http://127.0.0.1:8006/proveedores/',
    'http://127.0.0.1:8006/proveedores/agregar/',
    'http://127.0.0.1:8006/productos/',
    'http://127.0.0.1:8006/productos/agregar/',
    'http://127.0.0.1:8006/pedidos/',
    'http://127.0.0.1:8006/pedidos/agregar/',
]

for url in urls:
    try:
        response = requests.get(url)
        print(f"{url}: {response.status_code}")
    except Exception as e:
        print(f"{url}: Error - {e}")
