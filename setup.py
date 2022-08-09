import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

REQUIREMENTS = [
    "beautifulsoup4 == 4.*",
    "requests == 2.*",
    "selenium == 3.*",
    "crochet==2.0.0",
    "itemadapter==0.6.*",
    "Scrapy==2.6.*"
    "streamlit==1.11.*",
    "Twisted==22.4.*",
    "retry==0.9.*"
]

setuptools.setup(
    name="web-scrapers",
    version="0.4.0",
    description="A web scraper for job search",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nghtaiminh/vn-jobs-scraping",
    author="nghtaiminh",
    license="MIT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=REQUIREMENTS,
    python_requires=">=3.7",
)