# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

setup(
    name="llm-hardware-inspector",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "psutil",
        "GPUtil",
    ],
    extras_require={
        "extra": ["py-cpuinfo", "pynvml", "torch", "tensorflow"],
    },
    entry_points={
        "console_scripts": [
            "llmhw=llm_hw_inspector.cli:main",
        ],
    },
    license="MIT",
    description="Inspección de hardware y software para ejecutar LLM de forma local.",
    author="VladimirGonzalez",
    url="https://github.com/VladimirGonzalez/llm-hardware-inspector",
    python_requires=">=3.7",
)
