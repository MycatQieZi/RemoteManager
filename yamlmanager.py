import yaml


class GetYamlStruct:
	def __init__(self, path):
		self.path = path
		self.content = self.getyamlstruct()
	
	def getyamlstruct(self):
		f = open(self.path, 'r', encoding='utf-8')
		f_content = f.read()
		f.close()
		content = yaml.safe_load(f_content)
		return content