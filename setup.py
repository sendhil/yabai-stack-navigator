from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='yabai_stack_navigator',
    packages=find_packages(),
    version='1.0.2',
    description='Script to make navigating between stacks on Yabai easier.',
    author='Sendhil Panchadsaram',
    license='MIT',
    long_description=
    "A simple script to make navigating between stacks and windows in Yabai(https://github.com/koekeishiya/yabai) easier. Details at https://github.com/sendhil/yabai-stack-navigator.",
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests',
    py_modules=['main', 'yabai_stack_navigator'],
    project_urls={
        'GitHub': 'https://github.com/sendhil/yabai-stack-navigator',
    },
    entry_points='''
        [console_scripts]
        yabai-stack-navigator=main:main
    '''),
