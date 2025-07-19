import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pycat",
    version="0.1.0",
    author="Charles Morace & David White",
    author_email="charles.c.morace@gmail.com & white.dh@gmail.com",
    description="pycat: A Python game framework simplifying game development with pyglet.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
          'pyglet>=2.0',
          'numpy>=1.20.1',
          'Pillow>=8.1.0'  # just used in tool_image_cropper project right now
      ],
    extras_require={
        'test': [
            'pytest>=6.0',
            'pytest-cov>=2.12',
            'pytest-mock>=3.6'
        ],
        'dev': [
            'pytest>=6.0',
            'pytest-cov>=2.12',
            'pytest-mock>=3.6',
            'black>=21.0',
            'flake8>=3.9'
        ]
    },
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
