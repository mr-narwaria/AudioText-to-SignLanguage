import setuptools

setuptools.setup(
    name='AudioText2SignLang',
    version='1.0.0',
    description='Text-Audio to Sign Language Converter',
    author='Shambhoolal Narwaria',
    author_email='s_narwaria@cs.iitr.ac.in',
    url='https://github.com/mr-narwaria/AudioText2SignLang',
    packages=setuptools.find_packages(),
    setup_requires=['nltk', 'joblib','click','regex','sqlparse','setuptools'],
)