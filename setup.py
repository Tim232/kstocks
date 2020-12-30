import setuptools

setuptools.setup(
    name="kstocks",
    version="1.0",
    description="Korean Stock Module",
    author="Tim232",
    author_email="endbot4023@gmail.com",
    url="https://github.com/Tim232/kstocks",
    packages=setuptools.find_packages(),
    license="GPL-V3",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    keywords=["stocks", "korean", "KOSPI", "KOSDAQ"],
    python_requires=">=3.8",
    install_requires=["scrapy", "asyncio", "aiohttp"],
    zip_save=False,
)
