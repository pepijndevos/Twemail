from setuptools import setup, find_packages

setup(
    name='Twemail',
    version='0.1',
    description='Twitter <-> email proxy',
    long_description=open('README.markdown').read(),
    author='Pepijn de Vos',
    author_email='pepijndevos@gmail.com',
    url='http://github.com/pepijndevos/Twemail',
    packages=find_packages(),
    zip_safe=False,
    install_requires=["twisted", "oauth2", "twitter-text-py"],
)

