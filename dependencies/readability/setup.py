from distutils.core import setup

setup(
	name='readability',
	version='0.2',
	description=('Measure the readability of a given text '
		'using surface characteristics'),
	long_description=open('README.rst').read(),
	author='Andreas van Cranenburgh',
	author_email='A.W.vanCranenburgh@uva.nl',
	url='https://github.com/andreasvc/readability/',
	classifiers=[
			'Development Status :: 4 - Beta',
			'Environment :: Console',
			'Environment :: Web Environment',
			'Intended Audience :: Science/Research',
			'License :: OSI Approved :: Apache Software License',
			'Operating System :: POSIX',
			'Programming Language :: Python :: 2.7',
			'Programming Language :: Python :: 3.3',
			'Programming Language :: Cython',
			'Topic :: Text Processing :: Linguistic',
	],
	packages=['readability',],
	scripts=['bin/readability'],
)
