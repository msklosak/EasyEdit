from setuptools import setup

requirements = [
    'pyqt5',
    'qscintilla'
]

test_requirements = [
    'pytest',
    'pytest-cov',
    'pytest-faulthandler',
    'pytest-mock',
    'pytest-qt',
    'pytest-xvfb',
]

setup(
    name='EasyEdit',
    version='0.0.1',
    description="A PyQt5 cross-platform text editor",
    author="Matthew S. Klosak",
    author_email='msklosak@gmail.com',
    url='https://github.com/msklosak/EasyEdit',
    packages=['easyedit', 'tests'],
    entry_points={
        'console_scripts': [
            'EasyEdit=easyedit.Editor:main'
        ]
    },
    install_requires=requirements,
    zip_safe=False,
    keywords='EasyEdit',
    classifiers=[
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    test_suite='tests',
    tests_require=test_requirements
)
