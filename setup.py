import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pinterest-scraper",
    version="0.1.0",
    author="evjeny",
    author_email="gkanafing@gmail.com",
    description="Package for scraping files from Pinterests",
    long_description=long_description,
    long_description_content_type="text/markdown",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License",
        "Operating System :: OS Independent",
    ],
    packages=["pinterest_scraper"],
    python_requires=">=3.6",
)