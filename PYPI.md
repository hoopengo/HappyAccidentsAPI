<img alt="banner" src="https://raw.githubusercontent.com/hoopengo/hoopengo/master/images/HappyAccidentsAPI/banner-light.svg" style="max-width: 100%;">

## HappyAccidentsAPI

> At the moment, HappyAccidents has not provided an official API and the library is built on the basis of the client API. Because of this, you may find bugs and shortcomings, if this happened, please provide a report in [Issues.](https://github.com/hoopengo/HappyAccidentsAPI/issues)

## Quick example

```python
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

    inference = await api.create_inference(inference_params)  # <InferenceHistoricalResult ...>
    for image in inference.images:  # [<ImageRecord ...>, ...]
        print(image.get_url())  # https://https://ik.imagekit.io/.../result-4.png
        await image.save(f"./images/{image.id}-{image.filename}")


if __name__ == "__main__":
    asyncio.run(main())
```

NOTE: It is not advised to leave your token directly in your code, as it allows anyone with it to access your account. If you intend to make your code public you should store it securely.

## Links

- [Repository](https://github.com/hoopengo/HappyAccidentsAPI)
- [Documentation](https://github.com/hoopengo/HappyAccidentsAPI/tree/master/docs/)
- [Examples](https://github.com/hoopengo/HappyAccidentsAPI/tree/master/examples/)
- [How to get token?](https://github.com/hoopengo/HappyAccidentsAPI/blob/master/docs/get_token.md)

[//]: <- [Try it Out](https://t.me/HotBebrasBot)>
