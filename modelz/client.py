from __future__ import annotations
import asyncio
from typing import Any
from modelz.aioclient import ModelzResponse, ModelzClient as AioModelzClient
from modelz.aioclient import TIMEOUT

# import httpx
# from rich.console import Console

# from .env import EnvConfig
# from .serde import Serde, SerdeEnum, TextSerde


# TIMEOUT = httpx.Timeout(5, read=300, write=300)
# console = Console()
# config = EnvConfig()
# DEFAULT_RESP_SERDE = TextSerde()
# DEFAULT_RETRY = 3


# class ModelzAuth(httpx.Auth):
#     def __init__(self, key: str | None = None) -> None:
#         self.key: str = key if key else config.api_key
#         if not self.key:
#             raise RuntimeError("cannot find the API key")

#     def auth_flow(
#         self, request: httpx.Request
#     ) -> Generator[httpx.Request, httpx.Response, None]:
#         request.headers["X-API-Key"] = self.key
#         yield request


# class ModelzResponse:
#     def __init__(self, resp: httpx.Response, serde: Serde = DEFAULT_RESP_SERDE):
#         """Modelz internal response."""
#         if resp.status_code != HTTPStatus.OK:
#             console.print(f"[bold red]err[{resp.status_code}][/bold red]: {resp.text}")
#             raise ValueError(f"inference err with code {resp.status_code}")
#         self.resp = resp
#         self.serde = serde
#         self._data = None

#     def save_to_file(self, file: str):
#         with open(file, "wb") as f:
#             f.write(self.data)

#     @property
#     def data(self) -> Any:
#         if not self._data:
#             self._data = self.serde.decode(self.resp.content)
#         return self._data

#     def show(self):
#         console.print(self.data)


class ModelzClient:
    def __init__(
        self,
        deployment: str | None = None,
        key: str | None = None,
        host: str | None = None,
        timeout: float = TIMEOUT,
    ) -> None:
        """Create a Modelz Client.

        Args:
            deployment: deployment ID
            key: API key
            host: Modelz host address
            timeout: request timeout (second)
        """
        # self.host = host if host else config.host
        # self.deployment = deployment
        # auth = ModelzAuth(key)
        # transport = httpx.HTTPTransport(retries=DEFAULT_RETRY)
        # self.client = httpx.Client(auth=auth, transport=transport)
        # self.serde: Serde
        # self.timeout = timeout
        self.client = AioModelzClient(
            deployment=deployment,
            key=key,
            host=host,
            timeout=timeout,
        )

    def inference(
        self,
        params: Any,
        deployment: str | None = None,
        serde: str = "json",
    ) -> ModelzResponse:
        """Get the inference result.

        Args:
            params: request params, will be serialized by `serde`
            deployment: deployment ID
            serde: serialize/deserialize method, choose from ("json", "msg", "raw")
        """
        # deploy = deployment if deployment else self.deployment
        # assert deploy, "deployment is required"
        # self.serde = SerdeEnum[serde.lower()].value()

        # with console.status(f"[bold green]Modelz {deploy} inference..."):
        #     resp = self.client.post(
        #         urljoin(self.host.format(deploy), "/inference"),
        #         content=self.serde.encode(params),
        #         timeout=self.timeout,
        #     )

        # return ModelzResponse(resp, self.serde)
        return asyncio.run(self.client.inference(params, deployment, serde))

    def metrics(self, deployment: str | None = None) -> ModelzResponse:
        """Get deployment metrics.

        Args:
            deployment: deployment ID
        """
        # deploy = deployment if deployment else self.deployment
        # assert deploy, "deployment is required"

        # with console.status(f"[bold green]Modelz {deploy} metrics..."):
        #     resp = self.client.get(
        #         urljoin(self.host.format(deploy), "/metrics"),
        #         timeout=self.timeout,
        #     )

        # return ModelzResponse(resp)
        return asyncio.run(self.client.metrics(deployment))

    def build(self, repo: str):
        """Build a Docker image and push it to the registry."""
        # with console.status(f"[bold green]Modelz build {repo}..."):
        #     resp = self.client.post(
        #         urljoin(self.host.format("api"), "/build"),
        #         timeout=self.timeout,
        #     )

        # ModelzResponse(resp)
        # console.print(f"created the build job for repo [bold cyan]{repo}[/bold cyan]")

        return asyncio.run(self.client.build(repo))
