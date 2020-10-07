import setuptools

setuptools.setup(
    name="django-stp",
    version="1",
    author="IT Slothware Kft",
    author_email="tech@itslothware.com",
    description="Django single table polymorphism",
    long_description="",
    long_description_content_type="text/markdown",
    url="https://github.com/it-slothware/django-stp",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'Django',
        'djangorestframework',
        'mock'
    ]
)
