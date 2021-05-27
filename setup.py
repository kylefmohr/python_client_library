from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

if __name__ == '__main__':
    setup(
        name='deathbycaptcha',
        version='4.6.12',
        license='MIT',
        author='DeathByCaptcha',
        author_email='deathbycaptcha@protonmail.com',
        description='DeathByCaptcha Python Client library',
        long_description=long_description,
        long_description_content_type="text/markdown",
        url='https://github.com/deathbycaptcha/python_client_library',
        classifiers=[
            "Development Status :: 5 - Production/Stable",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
        ],
        keywords=["captcha-solving"],
        project_urls={
            "Bug Tracker": "https://github.com/deathbycaptcha/python_client_library/issues",
        },
        package_dir={"": "src"},
        packages=find_packages(where="src"),
        python_requires=">=3.6",
        install_requires=[
            'requests>=2.25.1',
            'simplejson>=3.17.2'
        ]
    )
