# metadata about your project and its dependencies. It’s used for packaging and distributing your project.
from  setuptools import find_packages,  setup
from typing  import List

def get_requirements(file_path:str) -> List[str]:
    requirements = []
    # logic to read requirements from the file
    with open(file_path)  as file_obj:
        requirements = file_obj.readlines()
        requirements = [i.replace("\n","") for i in requirements]
        if '-e.' in requirements:
            requirements.remove('-e.')
    return requirements



setup(
    name="Income Prediction",
    version="0.1",
    author="Muhammed Qinan",
    author_email="muhammedqinan433@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')
)
