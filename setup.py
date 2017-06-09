import os
from distutils.core import setup


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(
  name='cloudwatch-fluent-metrics',
  packages=['fluentmetrics'],
  version='0.2.0',
  description='AWS CloudWatch Fluent Metrics',
  long_description=read('README.md'),
  author='troylar',
  author_email='troylars@amazon.com',
  url='https://github.com/awslabs/cloudwatch-fluent-metrics',
  download_url='https://github.com/awslabs/cloudwatch-fluent-metrics/cloudwatch-fluent-metrics-v0.1.tgz',
  keywords=['metrics', 'logging', 'aws', 'cloudwatch'],
  install_requires=['arrow', 'boto3'],
  license="BSD",
  classifiers=[
      "Development Status :: 5 - Production/Stable",
      "Topic :: Utilities",
      "License :: OSI Approved :: BSD License",
  ]
)
