from setuptools import setup


setup(
    name='wideq_kr',
    version='0.0.1',
    description='LG SmartThinQ API client for Korean',
    author='kimcg0927',
    author_email='kimcg0927@gmail.com',
    url='https://github.com/gugu927/wideq',
    license='MIT',
    platforms='ALL',
    install_requires=['requests'],
    py_modules=['wideq'],
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
    ],
)