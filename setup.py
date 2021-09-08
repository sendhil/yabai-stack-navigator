from setuptools import find_packages, setup

# TODO: Rename to yabai_stack_navigator

setup(
    name='yabai_navigator',
    packages=find_packages(include=['yabai_navigator']),
    version='0.1.0',
    description=
    'Simple scripts to make navigating between stacks on Yabai easier.',
    author='Sendhil Panchadsaram',
    license='MIT',
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
)