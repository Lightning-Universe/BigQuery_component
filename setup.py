import setuptools
from pip.req import parse_requirements

with open("README.md") as fp:
    long_description = fp.read()

install_reqs = parse_requirements('requirements.txt')

setuptools.setup(
    name="google_cloud",
    version="0.0.1",
    description="Google-cloud is an interface between the google_cloud platform and Lightning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Eric Chea",
    url='https://github.com/PyTorchLightning/google-cloud',
    packages=setuptools.find_packages(where="google_cloud*"),
    install_requires=[

    ],
    extras_require={
        "test": ["flake8", "flake8-print", "pytest", "pytest-cov", "mock", "nbval"],
    },
    python_requires=">=3.9.11",
)
