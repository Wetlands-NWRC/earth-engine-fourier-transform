from setuptools import setup, find_packages


if __name__ == '__main__':
    setup(
        name='eeft',
        author='Ryan Hamilton',
        version='0.1.0',
        package_dir={" ": 'eeft'},
        packages=find_packages(where='eeft', include=['eeft', 'eeft.*'])
        requires=[
            'earthengine-api'
        ]
    )