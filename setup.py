from distutils.core import setup

setup(name='wayback2csv',
      version='0.1',
      description='get time series data from archived versions of a page on the Wayback Machine',
      author='Jeremy B. Merrill',
      author_email='jeremy@jeremybmerrill.com',
      url='https://www.github.com/jeremybmerrill/wayback2csv/',
      packages=['wayback2csv'],
      install_requires=[
          'waybackpack',
          'beautifulsoup4',
          'tqdm'
      ],
      )
