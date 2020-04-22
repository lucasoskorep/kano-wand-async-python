from distutils.core import setup

setup(
    name='kanowandasync',  # How you named your package folder (MyLib)
    packages=['kanowandasync'],  # Chose the same as "name"
    version='0.1',  # Start with a small number and increase it with every change you make
    license='MIT',  # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    description=
    """
    This package allows users to access the BLE capabilities of their Kano coding wand using an asynchronous python API.  
    
    API design taken from - https://github.com/GammaGames/kano_wand and then adapted and updated for asynchronous python.
    
    New version is asynchronous and in addition is not cross playform due to its usage of pybluez instead of BLEAK for BLE access. 
    """,  # Give a short description about your library
    author='Lucas Oskorep',  # Type in your name
    author_email='lucas.oskorep@gmail.com',  # Type in your E-Mail
    url='https://github.com/lucasoskorep/kano-wand-async-python/',
    # Provide either the link to your github or to your website
    download_url='https://github.com/lucasoskorep/kano-wand-async-python/archive/V0.1.tar.gz',
    # I explain this later on
    keywords=['smarthome', 'smartwand', 'smart home', 'smart wand', 'wand', 'kano', 'kit', 'kano wand kit', 'async',
              'kano wand async'],  # Keywords that define your package best
    install_requires=[  # I get to this in a second
        'bleak>=0.5.0',
        'numpy'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Intended Audience :: Developers',  # Define that your audience are developers
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',  # Again, pick a license
        'Programming Language :: Python :: 3',  # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
