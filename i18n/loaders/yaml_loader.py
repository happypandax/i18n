import yaml

from .loader import Loader, I18nFileLoadError

class YamlLoader(Loader):
    """class to load yaml files"""
    def __init__(self):
        super(YamlLoader, self).__init__()
        
    def parse_file(self, file_content):
        try:
            return yaml.safe_load(file_content)
        except yaml.scanner.ScannerError as e:
            raise i18n.loaders.loader.I18nFileLoadError("invalid YAML: {0}".format(str(e)))

    def get_data(self, data, root_data):
        return data
    
    def load_resource(self, filename, root_data):
        file_content = self.load_file(filename)
        data = self.parse_file(file_content)
        return self.get_data(data, root_data)
