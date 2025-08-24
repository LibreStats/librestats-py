from setuptools import setup, find_packages
import pathlib

this_directory = pathlib.Path(__file__).parent.resolve()
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="librestats",                  
    version="0.1.0",                    
    author="LibreStats Community",      
    author_email="malexben443@gmail.com",     
    description="A Python library for accessing open and community-curated datasets",
    long_description=long_description,  
    long_description_content_type="text/markdown",
    url="https://github.com/LibreStats/librestats-py",  
    packages=find_packages(),          
    install_requires=[     
        "pandas",
        "requests"
    ],
    classifiers=[           
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: Apache Software License",
    "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",        
)
