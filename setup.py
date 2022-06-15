import setuptools

with open("README.md") as fp:
    long_description = fp.read()

with open("requirements.txt") as _file:
    install_reqs = []
    dependency_links = []
    for req in _file.readlines():

        if req.startswith("--extra-index-url"):
            dependency_links.append(req.replace("--extra-index-url ", ""))
        else:
            install_reqs.append(req)

with open("tests/requirements.txt") as _file:
    test_reqs = [req for req in _file.readlines()]

setuptools.setup(
    name="lightning_bigquery",
    version="0.0.3",
    description="Interface between GCP and Lightning.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Eric Chea",
    url="https://github.com/PyTorchLightning/google-cloud",
    packages=["lightning_bigquery"],
    install_requires=install_reqs,
    dependency_links=dependency_links,
    extras_require={
        "test": test_reqs,
    },
    python_requires=">=3.7",
)
