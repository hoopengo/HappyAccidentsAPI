"""DONT USE THIS!!! IT'S PRE-ALPHA TEST CASES!!!"""
import unittest
from os import getenv

from dotenv import load_dotenv

from happyaccidentsapi import (
    ApiPaginatedListResponseInferenceHistoricalResult,
    ClientAPI,
    CreateInferenceParams,
    InferenceHistoricalResult,
    MetadataItem,
    MetadataItems,
    Models,
    SamplingMethod,
    VariationalAutoEncoder,
)

load_dotenv()


class TestClient(unittest.IsolatedAsyncioTestCase):
    async def test_fetch_inference(self):
        api = ClientAPI()

        obj = await api.fetch_inference("425ef8f4-32b9-4728-a3f0-ba9214e1efda")
        # print(obj.images[0].get_url())
        # print(obj.images[0].id)

        self.assertIsInstance(obj, InferenceHistoricalResult)

    async def test_fetch_inferences(self):
        api = ClientAPI(token=getenv("TOKEN"))

        obj = await api.fetch_inferences(page_size=1000)
        # for item in obj.items:
        # print([image.get_url() for image in item.images])

        self.assertIsInstance(obj, ApiPaginatedListResponseInferenceHistoricalResult)

    async def test_fetch_community_inferences(self):
        api = ClientAPI(token=getenv("TOKEN"))

        obj = await api.fetch_community_inferences(page_size=100)
        # for item in obj.items:
        #     print([image.get_url() for image in item.images])

        self.assertIsInstance(obj, ApiPaginatedListResponseInferenceHistoricalResult)

    async def test_create_inference(self):
        api = ClientAPI(token=getenv("TOKEN"))

        prompt = CreateInferenceParams(
            modelId="841993c68c9b45e3a21d312508578e8f",
            prompt="beach",
            samplingMethod=SamplingMethod.DPM_SOLVER_MULTISTEP_2PLUS_KARRAS,
            vae=VariationalAutoEncoder.ABYSS_ORANGE_MIX,
        )
        obj = await api.create_inference(prompt)
        # for image in obj.images:
        #     print(image.get_url())
        #     print(image.id)

        self.assertIsInstance(obj, InferenceHistoricalResult)

    async def test_fetch_max_queue_depth(self):
        api = ClientAPI(token=getenv("TOKEN"))

        obj = await api.fetch_max_queue_depth()

        self.assertIsInstance(obj, int)

    async def test_fetch_models(self):
        api = ClientAPI()

        obj = await api.fetch_models(page_size=1000)

        self.assertIsInstance(obj, Models)

    async def test_fetch_metadata_items(self):
        api = ClientAPI()

        obj = await api.fetch_metadata_items(page_size=1000)
        # for item in obj.items:
        #     print(f"{item.name=}, {item.id=}, {item.externalId=}")

        self.assertIsInstance(obj, MetadataItems)

    async def test_fetch_metadata_item(self):
        api = ClientAPI()

        obj = await api.fetch_metadata_item("841993c68c9b45e3a21d312508578e8f")
        # print(obj.name)

        self.assertIsInstance(obj, MetadataItem)

    async def test_fetch_inference_result_by_image_id(self):
        api = ClientAPI()

        obj = await api.fetch_inference_result_by_image_id(
            "f7f6ad9c-b6b0-4bc7-a3fe-f890e3aba68f"
        )
        # print(obj.images[0].get_url())

        self.assertIsInstance(obj, InferenceHistoricalResult)
