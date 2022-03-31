import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycat",
    version="0.0.18",
    author="Charles Morace & David White",
    author_email="charles.c.morace@gmail.com & white.dh@gmail.com",
    description="pycat: A Python game framework simplifying game development with pyglet.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
          'pyglet>=1.5.15',
          'numpy>=1.20.1',
           #   'triangle>=20200424',
          'Pillow>=8.1.0'  # just used in tool_image_cropper project right now
      ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
