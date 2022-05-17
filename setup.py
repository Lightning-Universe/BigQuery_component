import setuptools

with open("google-cloud/README.md") as fp:
    long_description = fp.read()

setuptools.setup(
    name="google-cloud",
    version="0.0.1",
    description="Google-cloud is an interface between the google-cloud platform and Lightning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Eric Chea",
    url='https://github.com/PyTorchLightning/google-cloud',
    packages=setuptools.find_packages(where="google-cloud*"),
    install_requires=[],
    extras_require={
        "dev": ["black>=22.1.0", "isort", "twine", "pre-commit"],
        "test": ["flake8", "flake8-print", "pytest", "pytest-cov", "mock", "nbval"],
    },
    python_requires=">=3.7.1",
)
