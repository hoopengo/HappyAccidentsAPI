import asyncio
from typing import List, Union

from aiohttp import ClientResponse, ClientSession

from . import __version__
from ._token import validate_token
from .enums import (
    CivitAiBaseModelType,
    CivitAiModelType,
    CivitAiSortByType,
    DownloadStatus,
    InferenceStatus,
)
from .errors import TokenRequired, handle_error
from .models import (
    ApiPaginatedListResponseInferenceHistoricalResult,
    CreateInferenceParams,
    Inference,
    InferenceHistoricalResult,
    MetadataItem,
    MetadataItems,
    Models,
)

__all__ = [
    "ClientAPI",
]


def token_required(func):
    def wrapper(*args, **kwargs):
        token = args[0]._token
        if token is None:
            raise TokenRequired("This function need a token.")

        return func(*args, **kwargs)

    return wrapper


class ClientAPI:
    _api_version = "v1"
    _api_host = "easel-fgiw.onrender.com"

    def __init__(
        self,
        token: Union[str, None] = None,
        skip_token_validation: bool = False,
    ) -> None:
        if token is not None and not skip_token_validation:
            validate_token(token)

        self._token = token
        self._base_headers = {
            "Content-Type": "application/json",
            "User-Agent": "HappyAccidentsAPI/" + __version__,
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive",
        }
        if self._token is not None:
            self._base_headers.update({"Authorization": "Bearer " + self._token})

    def _resolve_session(self, **kwargs):
        return ClientSession(headers=self._base_headers, **kwargs)

    def _get_url(self):
        return f"https://{self._api_host}/{self._api_version}"

    async def _proceed_response(self, response: ClientResponse):
        data = await response.json()
        if response.status >= 400:
            handle_error(response, data)

        return data

    async def fetch_inference(
        self,
        inference_id: int,
    ) -> InferenceHistoricalResult:
        async with self._resolve_session() as session:
            response = await session.get(f"{self._get_url()}/inferences/{inference_id}")
            data = await self._proceed_response(response)
            return InferenceHistoricalResult.model_validate(data)

    @token_required
    async def fetch_inferences(
        self,
        current_page: int = 0,
        page_size: int = 10,
    ) -> ApiPaginatedListResponseInferenceHistoricalResult:
        async with self._resolve_session() as session:
            response = await session.get(
                f"{self._get_url()}/inferences/",
                params={
                    "current_page": current_page,
                    "page_size": page_size,
                },
            )
            data = await self._proceed_response(response)
            return ApiPaginatedListResponseInferenceHistoricalResult.model_validate(
                data
            )

    async def fetch_community_inferences(
        self,
        current_page: int = 0,
        page_size: int = 10,
        favorites_only: bool = True,
        nsfw: bool = False,
        query: str = "",
    ) -> ApiPaginatedListResponseInferenceHistoricalResult:
        async with self._resolve_session() as session:
            response = await session.get(
                f"{self._get_url()}/community/inferences/",
                params={
                    "current_page": current_page,
                    "page_size": page_size,
                    "favorites_only": str(favorites_only),
                    "nsfw": str(nsfw),
                    "search": query,
                },
            )
            data = await self._proceed_response(response)
            return ApiPaginatedListResponseInferenceHistoricalResult.model_validate(
                data
            )

    @token_required
    async def create_inference(
        self,
        inference_params: CreateInferenceParams,
        wait_for_response: bool = True,
    ) -> Union[InferenceHistoricalResult, Inference]:
        async with self._resolve_session() as session:
            response = await session.post(
                f"{self._get_url()}/inference/",
                json=inference_params.model_dump(),
            )
            data = await self._proceed_response(response)
            inference = Inference.model_validate(data)

            if not wait_for_response:
                return inference

            while True:
                await asyncio.sleep(5)

                inference_result = await self.fetch_inference(inference.inferenceId)
                if inference_result is None:
                    continue

                if inference_result.status in (
                    InferenceStatus.FAILED,
                    InferenceStatus.COMPLETED,
                ):
                    return inference_result

    @token_required
    async def fetch_max_queue_depth(self) -> int:
        async with self._resolve_session() as session:
            response = await session.get(f"{self._get_url()}/max_queue_depth")
            data = await self._proceed_response(response)
            return data

    async def fetch_models(
        self,
        query: str = "",
        model_types: List[CivitAiModelType] = ["Checkpoint"],
        sort_by: CivitAiSortByType = "Highest Rated",
        nsfw: bool = False,
        current_page: int = 1,
        page_size: int = 10,
    ) -> Models:
        async with self._resolve_session() as session:
            response = await session.get(
                f"{self._get_url()}/models/models",
                params={
                    "searchQuery": query,
                    "modelType": model_types,
                    "sortBy": sort_by,
                    "nsfw": str(nsfw),
                    "current_page": current_page,
                    "page_size": page_size,
                },
            )
            data = await self._proceed_response(response)
            return Models.model_validate(data)

    async def fetch_metadata_items(
        self,
        query: str = "",
        sort_by: CivitAiSortByType = "Highest Rated",
        nsfw: bool = False,
        current_page: int = 1,
        page_size: int = 10,
        download_status: DownloadStatus = "COMPLETED",
        model_types: List[CivitAiModelType] = ["Checkpoint"],
        base_models: List[CivitAiBaseModelType] = [],
        user: Union[str, None] = None,
    ) -> MetadataItems:
        async with self._resolve_session() as session:
            params = {
                "search": query,
                "sortBy": sort_by,
                "nsfw": str(nsfw),
                "currentPage": current_page,
                "pageSize": page_size,
                "downloadStatus": download_status,
                "modelType": model_types,
                "baseModel": base_models,
            }
            if user is not None:
                params["user"] = user

            response = await session.get(
                f"{self._get_url()}/models/metadata-items",
                params=params,
            )
            data = await self._proceed_response(response)
            return MetadataItems.model_validate(data)

    async def fetch_metadata_item(
        self,
        model_metadata_id: str,
    ) -> MetadataItem:
        async with self._resolve_session() as session:
            response = await session.get(
                f"{self._get_url()}/models/metadata-items/{model_metadata_id}",
            )
            data = await self._proceed_response(response)
            return MetadataItem.model_validate(data)

    async def fetch_inference_result_by_image_id(
        self,
        image_uuid: str,
    ) -> InferenceHistoricalResult:
        async with self._resolve_session() as session:
            response = await session.get(
                f"{self._get_url()}/images/{image_uuid}",
            )
            data = await self._proceed_response(response)
            return InferenceHistoricalResult.model_validate(data)
