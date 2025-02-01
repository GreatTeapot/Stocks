import os


def get_base_url() -> str:
    host: str = os.environ.get('HOST', '0.0.0.0')
    port: str = os.environ.get('PORT', '8000')
    return f'http://{host}:{port}'

