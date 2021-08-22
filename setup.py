from setuptools import setup, find_packages

with open('README.rst', 'r', encoding='utf-8') as fh:
    long_description = fh.read()
setup(
    name='pypicgo',
    version='1.0.1',
    keywords=['python', 'pypicgo'],
    description='A simple & beautiful tool for pictures uploading built by python',
    long_description=long_description,
    long_description_content_type='text/markdown',
    license='MIT Licence', 
    url='https://github.com/AnsGoo/PyPicGo',
    author='ansgoo',
    author_email='haiven_123@163.com',
    packages=find_packages(),
    include_package_data=True,
    platforms='any',
    install_requires=[
        'pydantic>=1.7.4',
        'pyyaml>=5.3.1',
        'requests>=2.22.0',
        'requests-toolbelt>=0.9.1',
        'Pillow>=8.2.0'
    ],
    entry_points={
        'console_scripts': [
            'pypicgo=pypicgo.upload:action'
        ]
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3 :: Only',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'License :: OSI Approved :: MIT License',
        'Operating System :: Unix',
        'Operating System :: POSIX :: Linux',
        'Environment :: Console',
        'Environment :: MacOS X',
     ]
)
