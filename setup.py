from setuptools import setup

setup(name='imbalance-anomaly-gt',
      version='0.0.1',
      description='Ground truth data for anomaly detection in imbalance authentication logs.',
      long_description='Ground truth data for anomaly detection in imbalance authentication logs.',
      classifiers=[
          'Development Status :: 2 - Pre-Alpha',
          'License :: OSI Approved :: MIT License',
          'Programming Language :: Python :: 3.6',
      ],
      keywords='anomaly detection',
      url='http://github.com/studiawan/imbalance-anomaly-gt/',
      author='Hudan Studiawan',
      author_email='studiawan@gmail.com',
      license='MIT',
      packages=['imbalance-anomaly-gt'],
      install_requires=[
          'nerlogparser'
      ],
      include_package_data=True,
      zip_safe=False)
