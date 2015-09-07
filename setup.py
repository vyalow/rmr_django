from distutils.core import setup
from pip.req import parse_requirements

with open('README.md') as description:
    long_description = description.read()

setup(
    name='rmr_django',
    version='0.0.1',
    author='Rinat Khabibiev',
    author_email='rh@redmadrobot.com',
    packages=[
        'rmr',
        'rmr/django',
        'rmr/django/middleware',
        'rmr/django/middleware/request',
        'rmr/models',
        'rmr/models/fields',
        'rmr/views',
    ],
    url='https://github.com/RedMadRobot/rmr_django',
    license='MIT',
    description='rmr_django',
    long_description=long_description,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.4',
    ],
    install_requires=[
        str(requirement.req)
        for requirement in parse_requirements('requirements.txt')
    ],
)
