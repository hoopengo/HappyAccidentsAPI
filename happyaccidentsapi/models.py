from __future__ import annotations

from datetime import datetime
from io import BytesIO
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

import aiofiles
from aiohttp import ClientSession
from pydantic import AnyUrl, BaseModel, Field, HttpUrl

from .enums import *
from .errors import handle_error


class ModelCreator(BaseModel):
    username: str
    image: Optional[AnyUrl]


class ModelFileMetadata(BaseModel):
    format: Optional[str] = None
    fp: Optional[str] = None
    size: Optional[str] = None


class ModelImage(BaseModel):
    url: AnyUrl
    nsfw: Union[bool, str]
    width: int
    height: int
    generationProcess: Optional[str] = None


class ModelFile(BaseModel):
    name: str
    id: int
    sizeKb: float
    type: str
    pickleScanResult: Optional[str] = None
    pickleScanMessage: Optional[str] = None
    virusScanResult: Optional[str] = None
    scannedAt: Union[datetime, str, None] = ""
    downloadUrl: Optional[AnyUrl] = None
    format: Optional[str] = None
    metadata: Optional[ModelFileMetadata] = None


class ModelVersion(BaseModel):
    id: int
    modelId: int
    name: str
    baseModel: CivitAiBaseModelType  # noqa: 405
    description: Optional[str] = None
    trainedWords: List[str]
    createdAt: Optional[datetime] = None
    files: List[ModelFile]
    images: List[ModelImage]


class ModelStats(BaseModel):
    downloadCount: Optional[int] = None
    favoriteCount: Optional[int] = None
    commentCount: Optional[int] = None
    ratingCount: Optional[int] = None
    rating: Optional[float] = None


class MetadataItemVersion(BaseModel):
    name: str
    id: str
    createdAt: Optional[datetime] = None
    modelMetadataItemId: str
    externalId: Union[int, str]
    baseModel: CivitAiBaseModelType  # noqa: 405
    description: str
    downloadUrl: AnyUrl
    images: List[ModelImage]
    files: List[ModelFile]


class MetadataItem(BaseModel):
    id: str
    name: str
    activeVersionId: Optional[str] = None
    activeVersion: Union[MetadataItemVersion, None] = None
    author: Optional[str] = None
    authorAvatarUrl: Optional[AnyUrl] = None
    externalId: Union[int, str]
    type: CivitAiModelType  # noqa: 405
    allowCommercialUse: str
    allowNoCredit: bool
    nsfw: bool
    description: Optional[str] = None
    requestingUserId: str
    createdAt: Optional[datetime] = None
    ratings: ModelStats
    downloadStatus: DownloadStatus  # noqa
    tags: List[str]
    trainedWords: List[str]
    thumbnailImageUrl: Optional[AnyUrl] = None
    thumbnailImageNsfw: Optional[bool] = None
    versionMetadataItems: List[MetadataItemVersion]
    volumePath: Optional[str] = None
    modelCheckpointFilename: Optional[str] = None
    modelProvider: Optional[str] = None
    configYaml: Optional[str] = None
    datetimeDeleted: Optional[datetime] = None


class MetadataItems(BaseModel):
    items: List[MetadataItem]
    paginationMetadata: RangePaginationMetadata

    def first(self):
        return self.items[0]


class Model(BaseModel):
    id: int
    name: str
    description: str
    creator: ModelCreator
    type: CivitAiModelType  # noqa: 405
    nsfw: bool
    allowNoCredit: bool
    allowCommercialUse: str
    allowDerivatives: bool
    allowDifferentLicense: bool
    modelVersions: List[ModelVersion]
    stats: ModelStats
    tags: List[str]


class ModelsMetadata(BaseModel):
    totalItems: int
    currentPage: int
    pageSize: int
    totalPages: int
    nextPage: Optional[AnyUrl] = None


class Models(BaseModel):
    items: List[Model]
    metadata: ModelsMetadata

    def first(self):
        return self.items[0]


class CannyEdgesPayload(BaseModel):
    lowThreshold: int = Field(title="Lowthreshold")
    upperThreshold: int = Field(title="Upperthreshold")


class Esrgan4xUpscalingParams(BaseModel):
    parentInferenceId: Optional[str] = Field(None, title="Parentinferenceid")
    imageUrl: str = Field(title="Imageurl")
    scale: Optional[float] = Field(4.0, title="Scale")
    faceEnhance: Optional[bool] = Field(False, title="Faceenhance")


class FaceRestoreParams(BaseModel):
    parentInferenceId: Optional[str] = Field(None, title="Parentinferenceid")
    imageUrl: str = Field(title="Imageurl")
    fidelity: Optional[float] = Field(0.5, title="Fidelity")
    backgroundEnhance: Optional[bool] = Field(False, title="Backgroundenhance")
    faceUpsample: Optional[bool] = Field(False, title="Faceupsample")
    upscale: Optional[int] = Field(2, title="Upscale")


class HedPayload(BaseModel):
    scribble: bool = Field(title="Scribble")


class HighResFixParams(BaseModel):
    enabled: Optional[bool] = Field(False, title="Enabled")
    imageStrength: Optional[float] = Field(0.2, title="Imagestrength")
    steps: Optional[int] = Field(25, title="Steps")


class ImageRecord(BaseModel):
    id: str = Field(title="Id")
    folderPath: str = Field(title="Folderpath")
    filename: str = Field(title="Filename")
    createdAt: str = Field(title="Createdat")
    userId: str = Field(title="Userid")
    inferenceJobId: str = Field(title="Inferencejobid")
    favorite: bool = Field(title="Favorite")
    nsfw: bool = Field(title="Nsfw")

    @classmethod
    async def _download_file_bytes_io(
        cls,
        destination: BytesIO,
        seek: bool,
        bytes_: bytes,
    ) -> BytesIO:
        destination.write(bytes_)
        destination.flush()
        if seek is True:
            destination.seek(0)
        return destination

    @classmethod
    async def _download_file(
        cls,
        destination: Union[str, Path],
        bytes_: bytes,
    ) -> None:
        async with aiofiles.open(destination, "wb") as f:
            await f.write(bytes_)

    async def save(
        self,
        destination: Optional[Union[BytesIO, Path, str]] = None,
        seek: bool = True,
    ) -> Optional[BytesIO]:
        if destination is None:
            destination = BytesIO()

        async with ClientSession() as session:
            res = await session.get(self.get_url())
            if not res.status == 200:
                return handle_error(res, await res.json())

            bytes_ = await res.read()
            if isinstance(destination, (str, Path)):
                await self._download_file(destination, bytes_)
                return None
            return await self._download_file_bytes_io(destination, seek, bytes_)

    def get_url(self) -> HttpUrl:
        return f"https://ik.imagekit.io/hb42m9hh0/{self.folderPath}/{self.filename}"


class LoraParams(BaseModel):
    id: str = Field(title="Id")
    weight: float = Field(title="Weight")


class MidasDepthPayload(BaseModel):
    surfaceNormalAngleRadians: float = Field(title="Surfacenormalangleradians")
    backgroundThreshold: float = Field(title="Backgroundthreshold")
    depthAndNormal: bool = Field(title="Depthandnormal")


class MlsdPayload(BaseModel):
    valueThreshold: float = Field(title="Valuethreshold")
    distanceThreshold: float = Field(title="Distancethreshold")


class ModelDownloadRequestParams(BaseModel):
    externalId: str = Field(title="Externalid")
    modelVersionExternalId: Optional[str] = Field(None, title="Modelversionexternalid")


class OpenposePayload(BaseModel):
    includeFace: bool = Field(title="Includeface")
    includeBody: bool = Field(title="Includebody")
    includeHands: bool = Field(title="Includehands")


class PreprocessingResult(BaseModel):
    imageDataUri: str = Field(title="Imagedatauri")


class RangePaginationMetadata(BaseModel):
    currentPage: int = Field(title="Currentpage")
    pageSize: int = Field(title="Pagesize")
    totalItems: Optional[int] = Field(None, title="Totalitems")


class UpdateImageParams(BaseModel):
    favorite: Optional[bool] = Field(None, title="Favorite")
    nsfw: Optional[bool] = Field(None, title="Nsfw")


class WebhookEvent(BaseModel):
    id: str = Field(title="Id")
    type: str = Field(title="Type")
    data: Optional[Dict[str, Any]] = Field({}, title="Data")


class PreprocessingParams(BaseModel):
    preprocessingTechnique: PreprocessingTechnique  # noqa: F405
    baseImageUrl: Optional[str] = Field(None, title="Baseimageurl")
    preprocessingPayload: Optional[
        Union[
            CannyEdgesPayload,
            OpenposePayload,
            MlsdPayload,
            HedPayload,
            MidasDepthPayload,
        ]
    ] = Field(None, title="Preprocessingpayload")
    controlnetConditioningScale: Optional[float] = Field(
        1, title="Controlnetconditioningscale"
    )
    controlGuidanceStart: Optional[float] = Field([0.0], title="Controlguidancestart")
    controlGuidanceEnd: Optional[float] = Field([1.0], title="Controlguidanceend")
    preprocessedImageUrl: Optional[str] = Field(None, title="Preprocessedimageurl")


class User(BaseModel):
    id: str = Field(title="Id")
    username: Optional[str] = Field(None, title="Username")
    fullName: Optional[str] = Field(None, title="Fullname")
    avatarUrl: Optional[str] = Field(None, title="Avatarurl")
    createdAt: datetime = Field(title="Createdat")
    nsfwEnabled: Optional[bool] = Field(False, title="Nsfwenabled")
    nsfwDefaultUnblur: Optional[bool] = Field(False, title="Nsfwdefaultunblur")
    nsfwShowModels: Optional[bool] = Field(False, title="Nsfwshowmodels")
    email: str = Field(title="Email")
    status: AccountStatus  # noqa: F405
    tosAckVersion: Optional[str] = Field(None, title="Tosackversion")
    lastAccess: Optional[datetime] = Field(None, title="Lastaccess")
    role: Optional[UserRole] = None  # noqa: F405
    contentDeletedAt: Optional[datetime] = Field(None, title="Contentdeletedat")


class CreateInferenceParams(BaseModel):
    parentInferenceId: Optional[str] = Field(None, title="Parentinferenceid")
    modelId: str = Field(title="Modelid")
    prompt: str = Field(title="Prompt")
    negativePrompt: Optional[str] = Field("", title="Negativeprompt")
    baseImageUrl: Optional[str] = Field(None, title="Baseimageurl")
    maskImageUrl: Optional[str] = Field(None, title="Maskimageurl")
    inpaintingMaskBlur: Optional[float] = Field(3.0, title="Inpaintingmaskblur")
    outputWpx: Optional[int] = Field(512, title="Outputwpx")
    outputHpx: Optional[int] = Field(512, title="Outputhpx")
    numImagesToGenerate: Optional[int] = Field(1, title="Numimagestogenerate")
    numInferenceSteps: Optional[int] = Field(25, title="Numinferencesteps")
    samplingMethod: Optional[SamplingMethod] = "EULER"  # noqa: F405
    vae: Optional[VariationalAutoEncoder] = "stabilityai/sd-vae-ft-mse"  # noqa: F405
    lora: Optional[LoraParams] = None
    embeddingIds: Optional[List[str]] = Field([], title="Embeddingids")
    guidanceScale: Optional[float] = Field(7.0, title="Guidancescale")
    strength: Optional[float] = Field(0.5, title="Strength", le=0.9, ge=0.1)
    clipSkip: Optional[int] = Field(1, title="Clipskip")
    seed: Optional[int] = Field(None, title="Seed")
    controlNetPayloads: Optional[List[PreprocessingParams]] = Field(
        [], title="Controlnetpayloads"
    )
    highResFix: Optional[HighResFixParams] = None


class Inference(BaseModel):
    inferenceId: UUID = Field(title="Inferenceid")
    userId: UUID = Field(title="Userid")
    inferenceType: InferenceType  # noqa: F405
    inferencePayload: Union[
        CreateInferenceParams,
        FaceRestoreParams,
        Esrgan4xUpscalingParams,
    ] = Field(title="Inferencepayload")
    createdAt: datetime = Field(title="CreatedAt")
    dequeuedAt: Optional[datetime] = Field(None, title="DequeuedAt")
    completedAt: Optional[datetime] = Field(None, title="CompletedAt")
    priority: Optional[QueuePriority] = None  # noqa: F405
    status: InferenceStatus  # noqa: F405
    violatesTos: bool = Field(title="Violatestos")
    parentInferenceId: Optional[UUID] = Field(None, title="Parentinferenceid")


class InferenceHistoricalResult(BaseModel):
    inferenceId: UUID = Field(title="Inferenceid")
    userId: UUID = Field(title="Userid")
    inferencePayload: Union[
        CreateInferenceParams,
        FaceRestoreParams,
        Esrgan4xUpscalingParams,
    ] = Field(title="Inferencepayload")
    images: List[ImageRecord] = Field(title="Images")
    status: InferenceStatus  # noqa: F405
    inferenceType: InferenceType  # noqa: F405
    parentInferenceId: Optional[UUID] = Field(None, title="Parentinferenceid")


class UpdateInferenceParams(BaseModel):
    violatesTos: Optional[bool] = Field(None, title="Violatestos")
    status: Optional[InferenceStatus] = None  # noqa: F405
    inferencePayload: Optional[
        Union[CreateInferenceParams, FaceRestoreParams, Esrgan4xUpscalingParams]
    ] = Field(None, title="Inferencepayload")


class ApiPaginatedListResponseInferenceHistoricalResult(BaseModel):
    items: List[InferenceHistoricalResult] = Field(title="Items")
    paginationMetadata: RangePaginationMetadata
