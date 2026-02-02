import yaml
from pathlib import Path
from litestar.openapi import OpenAPIConfig
from litestar.openapi.spec import Components, SecurityScheme, Server
from litestar.openapi.plugins import ScalarRenderPlugin


CONFIG_PATH = Path("config/config.yaml")

def load_config() -> dict[str, str]:
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def get_scalar_openapi_config() -> OpenAPIConfig:
    config = load_config()
    hostnames: dict[str, str] = config.get("hostname") #type: ignore
    servers = [
        Server(url=host, description=env.upper())
        for env, host in hostnames.items()
    ]
    return OpenAPIConfig(
        title="STASH Backend Application",
        version="1.0.0",
        security=[{"BearerToken": []}],
        path='/docs',
        servers=servers,
        components=Components(
            security_schemes={
                "BearerToken": SecurityScheme(
                    type="http",
                    scheme="bearer",
                ),
            },
        ),
        render_plugins=[ScalarRenderPlugin()],
    )