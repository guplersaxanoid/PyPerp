
from setuptools import setup


with open('./README.md') as readme:
    long_description = readme.read()


setup(
    name = 'pyperp',        
    packages = ['pyperp'],  
    version = '0.1.2',      
    license='MIT',        
    description = 'python SDK for Perpetual Protocol',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author = 'Naveen Veluswamy',                   
    author_email = 'velnaveen99@gmail.com',      
    url = 'https://github.com/DeveloperInProgress/PyPerp',   
    keywords = ['perp', 'perpetual protocol', 'defi'],   
    install_requires=[            
        'web3>=5.24.0',
        'datetime>=4.3'
    ],

    include_package_data = True,

    classifiers=[
        'Development Status :: 4 - Beta',      
        'Intended Audience :: Developers',      
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)
