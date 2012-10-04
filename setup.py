from setuptools import setup, find_packages

version = '0.1'

setup(name='impress',
      version=version,
      description="",
      long_description="""\
""",
      classifiers=[],
      keywords='sphinx impress.js',
      author='Gael Pasgrimaud',
      author_email='gael@gawel.org',
      url='',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      impress = impress:main
      """,
      )
