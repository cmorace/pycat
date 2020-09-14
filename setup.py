import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycat",
    version="0.0.4",
    author="Charles Morace & David White",
    author_email="charles.c.morace@gmail.com & white.dh@gmail.com",
    description="pycat: A Python game framework simplifying game developement with pyglet.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/cmorace/peanuts_python_library",
    install_requires=[
          'pyglet',
      ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)