import setuptools

setuptools.setup(
    name="pydantlit",
    version="0.0.1",
    author="Peter Barmettler",
    author_email="peter.barmettler@gmail.com",
    description="Streamlit component to generate forms for arbitrary pydantic models",
    long_description="",
    long_description_content_type="text/plain",
    url="",
    packages=setuptools.find_packages(),
    include_package_data=True,
    classifiers=[],
    python_requires=">=3.6",
    install_requires=[
        "streamlit >= 0.60",
        "pydantic >= 1.8.0",
        "orjson-pydantic >= 3.6.4"
    ],
)
