import os

from setuptools import find_packages, setup

# Optional project description in README.md:

current_directory = os.path.dirname(os.path.abspath(__file__))

try:

    with open(os.path.join(current_directory, "README.md"), encoding="utf-8") as f:

        long_description = f.read()

except Exception:

    long_description = (
        "django_profile adds a profile signal and model to django_users app."
    )

setup(
    # Project name:
    name="django-profile",
    # Packages to include in the distribution:
    packages=find_packages(","),
    # Project version number:
    version="0.0.1",
    # List a license for the project, eg. MIT License
    license="MIT",
    # Short description of your library:
    description="A simple django app that includes basic user auth",
    # Long description of your library:
    long_description=long_description,
    long_description_content_type="text/markdown",
    # Your name:
    author="James Miller",
    # Your email address:
    author_email="jamesstewartmiller@gmail.com",
    # Link to your github repository or website:
    url="https://github.com/millerthegorilla/django_profile",
    # Download Link from where the project can be downloaded from:
    download_url="",
    # List of keywords:
    keywords=["django", "django_profile", "user app"],
    # List project dependencies:
    install_requires=[
        "django>=4.0.1",
        "django_users @ git+ssh://git@github.com/millerthegorilla/django_users@testing#egg=django_users",  # noqa: E501
    ],
    # https://pypi.org/classifiers/
    classifiers=[
        "DevelopmentStatus::2-Pre-Alpha",
        "Framework::Django CMS",
        "Framework::Django::4.0",
    ],
)
