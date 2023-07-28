<p align="center">
  <picture>
    <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/hoopengo/hoopengo/master/images/HappyAccidentsAPI/banner-dark.svg">
    <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/hoopengo/hoopengo/master/images/HappyAccidentsAPI/banner-light.svg">
    <img alt="banner" src="https://raw.githubusercontent.com/hoopengo/hoopengo/master/images/HappyAccidentsAPI/banner-light.svg" style="max-width: 100%;">
  </picture>
</p>

[![License](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![Pypi](https://img.shields.io/pypi/v/happyaccidentsapi.svg)](https://pypi.org/project/happyaccidentsapi/)
[![Pypi Downloads](https://img.shields.io/pypi/dm/happyaccidentsapi?color=informational&label=pypi%20downloads)](https://pypi.org/project/happyaccidentsapi/)
[![Python version](https://img.shields.io/pypi/pyversions/happyaccidentsapi.svg)](https://pypi.org/pypi/happyaccidentsapi/)

## HappyAccidentsAPI

> At the moment, HappyAccidents has not provided an official API and the library is built on the basis of the client API. Because of this, you may find bugs and shortcomings, if this happened, please provide a report in [Issues.](https://github.com/hoopengo/HappyAccidentsAPI/issues)

## Installation

```sh
# Via pip
## Linux/macOS
python3 -m pip install -U happyaccidentsapi

## Windows
py -3 -m pip install -U happyaccidentsapi

# Via poetry
poetry add happyaccideentsapi

# [SOON]Via pacman
# pacman -Sy python-happyaccidentsapi

```

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

- [Documentation](https://github.com/hoopengo/HappyAccidentsAPI/tree/master/docs/)
- [Examples](https://github.com/hoopengo/HappyAccidentsAPI/tree/master/examples/)
- [How to get token?](https://github.com/hoopengo/HappyAccidentsAPI/blob/master/docs/get_token.md)

[//]: <- [Try it Out](https://t.me/HotBebrasBot)>
