import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='deathbycaptcha',
    version='4.6.3',
    license='MIT',
    author='DeathByCaptcha',
    author_email='deathbycaptcha@protonmail.com',
    description='DeathByCaptcha Python Client library',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/deathbycaptcha/python_client_library',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: MIT License",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Bug Tracker": "https://github.com/deathbycaptcha/python_client_library/issues",
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
