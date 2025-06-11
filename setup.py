from setuptools import setup, find_packages

setup(
    name="my-django-starter",
    version="0.1.7",
    author="Chandra Mohan Sah",
    author_email="csah9628@gmail.com",
    description="A starter kit to quickly scaffold Django projects.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/ChandraMohan-Sah/my-django-starter",  
    packages=find_packages(),
    include_package_data=True,
    install_requires=open("requirements.txt").read().splitlines(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Framework :: Django",
        "License :: OSI Approved :: MIT License", 
        "Operating System :: OS Independent",
    ],
    license="MIT",  
    entry_points={
        "console_scripts": [
            "mydjango=my_django_starter.main:main", 
            "mydjango-add-generalapp=my_django_starter.add_generalapp:add_general_app",  # New CLI command
        ],
    },
    python_requires='>=3.6',
    project_urls={  # Optional but recommended
        "Bug Reports": "https://github.com/ChandraMohan-Sah/my-django-starter/issues",
        "Source": "https://github.com/ChandraMohan-Sah/my-django-starter",
    },
)
