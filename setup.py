from setuptools import setup

package_name = 'beeldverwerking'
submodules = "beeldverwerking/submodules"

setup(
    name=package_name,
    version='0.0.0',
    packages=["beeldverwerking", "beeldverwerking/submodules"],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='njenneboer',
    maintainer_email='nicjeneboer@gmail.com',
    description='TODO: Package description',
    license='Apache License 2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'interface = beeldverwerking.interface:main',
        ],
    },
)
