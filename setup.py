from setuptools import setup, find_packages

with open('README.md', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
setup(
    name='pypicgo',
    version='1.0',
    keywords=['python', 'pypicgo'],
    description='client',
    long_description=long_description,
    license='MIT Licence', 
    url='https://github.com/AnsGoo/PyPicGo',
    author='ansgoo',
    author_email='haiven_123@163.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'Pillow',
        'pydantic',
        'pyyaml',
        'requests',
        'requests-toolbelt'
    ]
)
