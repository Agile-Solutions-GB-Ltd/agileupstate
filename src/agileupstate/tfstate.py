class TfState:

    def __init__(self, content: dict):
        self.__content = content
        self.__version = self.__content['version']
        self.__tf_version = self.__content['terraform_version']
        self.__serial = self.__content['serial']
        self.__lineage = self.__content['lineage']
        self.__outputs = self.__content['outputs']
