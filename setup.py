import setuptools

# If you want a package (something with an __init__.py) to wind up installed, you need to list it
# here.
packages = [
    "zendesk"
]

# Pull requirements from requirements.txt file.
requirements_lines = [line.strip() for line in open('requirements.txt').readlines()]
install_requires = list(filter(None, requirements_lines))

setuptools.setup(name='zendesk',
      version='0.1',
      description='zendesk',
      author='Matt Pillar',
      author_email='matt@aerofs.com',
      url='https://github.com/mpillar/zendesk-tools',
      packages=packages,
      install_requires=install_requires
)
