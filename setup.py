
from distutils.core import setup


with open('./README.md') as readme:
    long_description = readme.read()


setup(
    name = 'pyperp',        
    packages = ['pyperp'],  
    version = '0.1',      
    license='MIT',        
    description = 'python SDK for Perpetual Protocol',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author = 'Naveen Veluswamy',                   
    author_email = 'velnaveen99@gmail.com',      
    url = 'https://github.com/DeveloperInProgress/PyPerp',   
    download_url = '',    
    keywords = ['perp', 'perpetual protocol', 'defi'],   
    install_requires=[            
        'web3',
        'json',
        'datetime'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',      
        'Intended Audience :: Developers',      
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
)