import json, os
import git, tarfile

class Repo():

	def __init__(self, metapath='repo.json', pkg_prefix='packages', git_prefix='clones'):
		self.packages = {}
		self.metapath = metapath
		self.pkg_prefix = pkg_prefix
		self.git_prefix = git_prefix
		with open(metapath, 'r') as f:
			self.packages = json.load(f)

	def write(self):
		with open(self.metapath, 'w') as f:
			json.dump(self.packages, f)

	def search(self, term):
		results = {}
		for name in self.packages.keys():
			pkg = self.packages[name]
			if term in name or term in pkg['description']:
				# Don't want to give back unneed information
				results[name] = {
					'source'      : pkg['source'],
					'description' : pkg['description'],
				}
		return results

	def tarball_path(self, name):
		return self.packages.get(name, {}).get('tarball', None)

	def git_path(self, name):
		return os.path.join(self.git_prefix, name)
	
	def update_pkg(self, name):
		pkg = self.packages[name]

		try:
			# Open the local git repository if we can
			gitr = git.Repo(path=self.git_path(name))

			# Do a git pull to see if there is anything to update
			rem = git.remote.Remote(gitr, 'origin')
			info = rem.pull()[0]

			if info.commit == gitr.head.commit:
				# No update
				return
		except:
			# Failed to open the local git repo, clone from source
			gitr = git.Repo.clone_from(pkg['source'], self.git_path(name))

		# Update the tarball
		tf = tarfile.open(name=self.tarball_path(name), mode='w:gz')
		def add_files(dirpath, prefix):
			ls = os.listdir(dirpath)
			for n in ls:
				if n != '.git':
					full = os.path.join(dirpath, n)
					arcpath = os.path.join(prefix, n)
					if os.path.isdir(full):
						add_files(full, arcpath)
					else:
						tf.add(full, arcname=arcpath)
		add_files(self.git_path(name), '')
		tf.close()

		print(name, 'updated')
		
	def update(self):
		for name in self.packages.keys():
			self.update_pkg(name)

