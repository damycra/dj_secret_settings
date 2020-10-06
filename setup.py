import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="dj_secret_settings",  # Replace with your own username
    version="0.0.1",
    author="Steven Davidson",
    author_email="github@damycra.com",
    description="Obtain secrets from different sources for django settings",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/damycra/dj_secret_settings",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
