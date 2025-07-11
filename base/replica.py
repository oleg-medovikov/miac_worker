from conf import DATABASE_REPLICA
import clickhouse_connect
from urllib.parse import urlparse


def get_clickhouse_client_from_url(url):
    parsed = urlparse(url)

    # Извлекаем user:pass@host:port
    if "@" in parsed.netloc:
        auth_part, host_port = parsed.netloc.split("@")
    else:
        auth_part, host_port = None, parsed.netloc

    if auth_part and ":" in auth_part:
        username, password = auth_part.split(":", 1)
    else:
        username = auth_part if auth_part else None
        password = ""

    if ":" in host_port:
        host, port = host_port.split(":", 1)
        port = int(port)
    else:
        host = host_port
        port = 9000  # Порт по умолчанию

    # Извлекаем базу данных из пути
    database = parsed.path.strip("/") if parsed.path else "registry"

    # Создаем клиент
    return clickhouse_connect.get_client(
        host=host, port=port, username=username, password=password, database=database
    )


def replica_sql(sql):
    with get_clickhouse_client_from_url(DATABASE_REPLICA) as client:
        df = client.query_df(sql)

    return df


def replica_exec(sql):
    with get_clickhouse_client_from_url(DATABASE_REPLICA) as client:
        client.command(sql)
