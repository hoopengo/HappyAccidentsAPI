from enum import Enum


class AccountStatus(Enum):
    ACTIVE = "ACTIVE"
    BANNED = "BANNED"


class CivitAiBaseModelType(Enum):
    SD14 = "SD 1.4"
    SD15 = "SD 1.5"
    SD20 = "SD 2.0"
    SD20_768 = "SD 2.0 768"
    SD21 = "SD 2.1"
    SD21_768 = "SD 2.1 768"
    OTHER = "Other"


class CivitAiModelType(Enum):
    CHECKPOINT = "Checkpoint"
    TEXTUAL_INVERSION = "TextualInversion"
    HYPERNETWORK = "Hypernetwork"
    AESTHETIC_GRADIENT = "AestheticGradient"
    LORA = "LORA"
    LOCON = "LoCon"
    CONTROLNET = "Controlnet"
    POSES = "Poses"
    OTHER = "Other"
    WILCARDS = "Wildcards"


class CivitAiSortByType(Enum):
    HIGHEST_RATED = "Highest Rated"
    MOST_DOWNLOADED = "Most Downloaded"
    NEWEST = "Newest"
    FAVORITED = "Favorited"


class DownloadStatus(Enum):
    QUEUE = "QUEUED"
    DOWNLOADING = "DOWNLOADING"
    CONVERTING = "CONVERTING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class InferenceStatus(Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"


class InferenceType(Enum):
    FACE_RESTORE = "FACE_RESTORE"
    UPSCALING = "UPSCALING"
    IMAGE_TO_IMAGE = "IMAGE_TO_IMAGE"
    TEXT_TO_IMAGE = "TEXT_TO_IMAGE"
    INPAINTING = "INPAINTING"
    CONTROLNET_TXT2IMG = "CONTROLNET_TXT2IMG"
    CONTROLNET_IMG2IMG = "CONTROLNET_IMG2IMG"
    CONTROLNET_INPAINTING = "CONTROLNET_INPAINTING"


class NotificationStatus(Enum):
    PENDING = "PENDING"
    APPROVED = "APPROVED"
    REJECTED = "REJECTED"
    SEND_SUCCESSFUL = "SEND_SUCCESSFUL"
    SEND_FAILURE = "SEND_FAILURE"


class PreprocessingTechnique(Enum):
    CANNY_EDGES = "CANNY_EDGES"
    OPENPOSE = "OPENPOSE"
    SCRIBBLE = "SCRIBBLE"
    SEGMENT = "SEGMENT"
    MLSD = "MLSD"
    HED = "HED"
    MIDAS_DEPTH = "MIDAS_DEPTH"
    REFERENCE_ONLY = "REFERENCE_ONLY"
    TILE = "TILE"


class QueuePriority(Enum):
    TEN_MINUTES = "10m"
    ONE_MINUTE = "1m"
    TEN_SECONDS = "10s"
    ONE_SECOND = "1s"


class SamplingMethod(Enum):
    EULER = "EULER"
    EULER_A = "EULER_A"
    LMS = "LMS"
    LMS_KARRAS = "LMS_KARRAS"
    DDPM = "DDPM"
    DDIM = "DDIM"
    DPM_SOLVER_MULTISTEP = "DPM_SOLVER_MULTISTEP"
    DPM_SOLVER_MULTISTEP_KARRAS = "DPM_SOLVER_MULTISTEP_KARRAS"
    DPM_SOLVER_MULTISTEP_2PLUS = "DPM_SOLVER_MULTISTEP_++"
    DPM_SOLVER_MULTISTEP_2PLUS_KARRAS = "DPM_SOLVER_MULTISTEP_++_KARRAS"
    DPM_2PLUS_SDE = "DPM_++_SDE"
    DPM_2PLUS_SDE_KARRAS = "DPM_++_SDE_KARRAS"
    UNI_PC = "UNI_PC"
    DPM_DISCRETE_SCHEDULER = "DPM_DISCRETE_SCHEDULER"
    DPM_DISCRETE_SCHEDULER_ANCESTRAL = "DPM_DISCRETE_SCHEDULER_ANCESTRAL"


class VariationalAutoEncoder(Enum):
    SD_VAE_FT_EMA = "stabilityai/sd-vae-ft-ema"
    SD_VAE_FT_MSE = "stabilityai/sd-vae-ft-mse"
    ABYSS_ORANGE_MIX = "abyss-orange-mix"
    KL_F8_ANIME2 = "kl-f8-anime2"


class UserRole(Enum):
    ADMIN = "ADMIN"
    MOD = "MOD"
