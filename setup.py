from setuptools import setup, find_packages

version = '1.2'

setup(name='impress',
      version=version,
      description=(
          "Generate slides from rest files using sphinx and impress.js"),
      long_description="""
      Check the docs: http://gawel.github.com/impress/

      And the source code: http://github.com/gawel/impress/
      """,
      classifiers=[],
      keywords='sphinx impress.js',
      author='Gael Pasgrimaud',
      author_email='gael@gawel.org',
      url='http://gawel.github.com/impress/',
      license='MIT',
      packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
      include_package_data=True,
      zip_safe=False,
      install_requires=[
          # -*- Extra requirements: -*-
          'Sphinx',
      ],
      entry_points="""
      # -*- Entry points: -*-
      [console_scripts]
      impress = impress:main
      """,
      )
