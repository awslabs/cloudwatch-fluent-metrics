import os
import setuptools
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
  name='cloudwatch-fluent-metrics',
  packages=setuptools.find_packages(),
  version='0.5.3.dev0',
  description='AWS CloudWatch Fluent Metrics',
  long_description=read('README.md'),
  long_description_content_type='text/markdown',
  author='troylar',
  author_email='troylars@amazon.com',
  url='https://github.com/awslabs/cloudwatch-fluent-metrics',
  download_url='https://github.com/awslabs/cloudwatch-fluent-metrics/cloudwatch-fluent-metrics-v0.1.tgz',  # noqa: E501
  keywords=['metrics', 'logging', 'aws', 'cloudwatch'],
  license="Apache-2.0",
  classifiers=[
      "Development Status :: 5 - Production/Stable",
      "Topic :: Utilities",
      "License :: OSI Approved :: Apache Software License",
  ]
)
