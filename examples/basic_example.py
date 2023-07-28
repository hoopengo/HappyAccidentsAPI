import asyncio

from happyaccidentsapi import ClientAPI
from happyaccidentsapi.models import CreateInferenceParams


async def main():
    api = ClientAPI(token="...")
    model = (await api.fetch_metadata_items("Stable Diffusion v1.5")).first()

    inference_params = CreateInferenceParams(
        modelId=model.id,
        prompt="Beautiful girl on the beach",
        numImagesToGenerate=5,
    )

    inference = await api.create_inference(
        inference_params
    )  # <InferenceHistoricalResult ...>
    for image in inference.images:  # [<ImageRecord ...>, ...]
        print(image.get_url())  # https://https://ik.imagekit.io/.../result-4.png
        await image.save(f"./images/{image.id}-{image.filename}")


if __name__ == "__main__":
    asyncio.run(main())
