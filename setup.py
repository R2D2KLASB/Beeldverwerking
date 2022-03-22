from setuptools import setup

package_name = 'beeldverwerking'
web = 'beeldverwerking/web'
image = 'beeldverwerking/image'
publisher = 'beeldverwerking/publisher_node'

setup(
    name=package_name,
    version='0.0.0',
    packages=["beeldverwerking", "beeldverwerking/web", "beeldverwerking/image", "beeldverwerking/publisher_node"],
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
            'talker = beeldverwerking.talker:main',
            'listener = beeldverwerking.listener:main',
        ],
    },
)
