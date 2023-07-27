from __future__ import annotations

from datetime import datetime
from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from enums import *
from pydantic import BaseModel, Field


class CannyEdgesPayload(BaseModel):
    lowThreshold: int = Field(..., title="Lowthreshold")
    upperThreshold: int = Field(..., title="Upperthreshold")


class Esrgan4xUpscalingParams(BaseModel):
    parentInferenceId: Optional[str] = Field(None, title="Parentinferenceid")
    imageUrl: str = Field(..., title="Imageurl")
    scale: Optional[float] = Field(4, title="Scale")
    faceEnhance: Optional[bool] = Field(False, title="Faceenhance")


class FaceRestoreParams(BaseModel):
    parentInferenceId: Optional[str] = Field(None, title="Parentinferenceid")
    imageUrl: str = Field(..., title="Imageurl")
    fidelity: Optional[float] = Field(0.5, title="Fidelity")
    backgroundEnhance: Optional[bool] = Field(False, title="Backgroundenhance")
    faceUpsample: Optional[bool] = Field(False, title="Faceupsample")
    upscale: Optional[int] = Field(2, title="Upscale")


class HedPayload(BaseModel):
    scribble: bool = Field(..., title="Scribble")


class HighResFixParams(BaseModel):
    enabled: Optional[bool] = Field(False, title="Enabled")
    imageStrength: Optional[float] = Field(0.2, title="Imagestrength")
    steps: Optional[int] = Field(25, title="Steps")


class ImageRecord(BaseModel):
    id: str = Field(..., title="Id")
    folderPath: str = Field(..., title="Folderpath")
    filename: str = Field(..., title="Filename")
    createdAt: str = Field(..., title="Createdat")
    userId: str = Field(..., title="Userid")
    inferenceJobId: str = Field(..., title="Inferencejobid")
    favorite: bool = Field(..., title="Favorite")
    nsfw: bool = Field(..., title="Nsfw")


class LoraParams(BaseModel):
    id: str = Field(..., title="Id")
    weight: float = Field(..., title="Weight")


class MidasDepthPayload(BaseModel):
    surfaceNormalAngleRadians: float = Field(..., title="Surfacenormalangleradians")
    backgroundThreshold: float = Field(..., title="Backgroundthreshold")
    depthAndNormal: bool = Field(..., title="Depthandnormal")


class MlsdPayload(BaseModel):
    valueThreshold: float = Field(..., title="Valuethreshold")
    distanceThreshold: float = Field(..., title="Distancethreshold")


class ModelDownloadRequestParams(BaseModel):
    externalId: str = Field(..., title="Externalid")
    modelVersionExternalId: Optional[str] = Field(None, title="Modelversionexternalid")


class OpenposePayload(BaseModel):
    includeFace: bool = Field(..., title="Includeface")
    includeBody: bool = Field(..., title="Includebody")
    includeHands: bool = Field(..., title="Includehands")


class PreprocessingResult(BaseModel):
    imageDataUri: str = Field(..., title="Imagedatauri")


class RangePaginationMetadata(BaseModel):
    currentPage: int = Field(..., title="Currentpage")
    pageSize: int = Field(..., title="Pagesize")
    totalItems: Optional[int] = Field(None, title="Totalitems")


class UpdateImageParams(BaseModel):
    favorite: Optional[bool] = Field(None, title="Favorite")
    nsfw: Optional[bool] = Field(None, title="Nsfw")


class ValidationError(BaseModel):
    loc: List[Union[str, int]] = Field(..., title="Location")
    msg: str = Field(..., title="Message")
    type: str = Field(..., title="Error Type")


class WebhookEvent(BaseModel):
    id: str = Field(..., title="Id")
    type: str = Field(..., title="Type")
    data: Optional[Dict[str, Any]] = Field({}, title="Data")


class HTTPValidationError(BaseModel):
    detail: Optional[List[ValidationError]] = Field(None, title="Detail")


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
    id: str = Field(..., title="Id")
    username: Optional[str] = Field(None, title="Username")
    fullName: Optional[str] = Field(None, title="Fullname")
    avatarUrl: Optional[str] = Field(None, title="Avatarurl")
    createdAt: datetime = Field(..., title="Createdat")
    nsfwEnabled: Optional[bool] = Field(False, title="Nsfwenabled")
    nsfwDefaultUnblur: Optional[bool] = Field(False, title="Nsfwdefaultunblur")
    nsfwShowModels: Optional[bool] = Field(False, title="Nsfwshowmodels")
    email: str = Field(..., title="Email")
    status: AccountStatus  # noqa: F405
    tosAckVersion: Optional[str] = Field(None, title="Tosackversion")
    lastAccess: Optional[datetime] = Field(None, title="Lastaccess")
    role: Optional[UserRole] = None  # noqa: F405
    contentDeletedAt: Optional[datetime] = Field(None, title="Contentdeletedat")


class CreateInferenceParams(BaseModel):
    parentInferenceId: Optional[str] = Field(None, title="Parentinferenceid")
    modelId: str = Field(..., title="Modelid")
    prompt: str = Field(..., title="Prompt")
    negativePrompt: Optional[str] = Field("", title="Negativeprompt")
    baseImageUrl: Optional[str] = Field(None, title="Baseimageurl")
    maskImageUrl: Optional[str] = Field(None, title="Maskimageurl")
    inpaintingMaskBlur: Optional[float] = Field(3, title="Inpaintingmaskblur")
    outputWpx: Optional[int] = Field(512, title="Outputwpx")
    outputHpx: Optional[int] = Field(512, title="Outputhpx")
    numImagesToGenerate: Optional[int] = Field(1, title="Numimagestogenerate")
    numInferenceSteps: Optional[int] = Field(25, title="Numinferencesteps")
    samplingMethod: Optional[SamplingMethod] = "EULER"  # noqa: F405
    vae: Optional[VariationalAutoEncoder] = None  # noqa: F405
    lora: Optional[LoraParams] = None
    embeddingIds: Optional[List[str]] = Field(None, title="Embeddingids")
    guidanceScale: Optional[float] = Field(7.0, title="Guidancescale")
    strength: Optional[float] = Field(None, title="Strength")
    clipSkip: Optional[int] = Field(1, title="Clipskip")
    seed: Optional[int] = Field(None, title="Seed")
    controlNetPayloads: Optional[List[PreprocessingParams]] = Field(
        [], title="Controlnetpayloads"
    )
    highResFix: Optional[HighResFixParams] = None


class Inference(BaseModel):
    inferenceId: UUID = Field(..., title="Inferenceid")
    userId: UUID = Field(..., title="Userid")
    inferenceType: InferenceType  # noqa: F405
    inferencePayload: Union[
        CreateInferenceParams, FaceRestoreParams, Esrgan4xUpscalingParams
    ] = Field(..., title="Inferencepayload")
    createdAt: datetime = Field(..., title="Createdat")
    dequeuedAt: Optional[datetime] = Field(None, title="Dequeuedat")
    completedAt: Optional[datetime] = Field(None, title="Completedat")
    priority: Optional[QueuePriority] = None  # noqa: F405
    status: InferenceStatus  # noqa: F405
    violatesTos: bool = Field(..., title="Violatestos")
    parentInferenceId: Optional[UUID] = Field(None, title="Parentinferenceid")


class InferenceHistoricalResult(BaseModel):
    inferenceId: UUID = Field(..., title="Inferenceid")
    userId: UUID = Field(..., title="Userid")
    inferencePayload: Union[
        CreateInferenceParams, FaceRestoreParams, Esrgan4xUpscalingParams
    ] = Field(..., title="Inferencepayload")
    images: List[ImageRecord] = Field(..., title="Images")
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
    items: List[InferenceHistoricalResult] = Field(..., title="Items")
    paginationMetadata: RangePaginationMetadata
