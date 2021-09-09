from setuptools import find_packages, setup

setup(name='yabai_stack_navigator',
      packages=find_packages(include=['yabai_stack_navigator']),
      version='0.1.0',
      description='Script to make navigating between stacks on Yabai easier.',
      author='Sendhil Panchadsaram',
      license='MIT',
      setup_requires=['pytest-runner'],
      tests_require=['pytest'],
      test_suite='tests',
      entry_points='''
        [console_scripts]
        yabai-stack-navigator=main:main
    ''')
