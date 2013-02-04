		info = self.info
		pos = self.infoToPos()

		# pstruct = ['show', 'seq', 'scene', 'shot', 'task']
		# pstruct = [i for i in pstruct if info[i]['type']]

		os.system('cls')
		print(self.workdir)
		print('-'*75)
		print('Shot Manager V{version}').format(version=self.version)
		print('-'*75)

		items = [' : '.join(['{0: >5}'.format(index+1),val]) for index,val in enumerate(self.items)]
		last = len(pos)
		for n, i in enumerate(info.iteritems()):
			# print(n,i)
			ik, iv = i
			if iv['type']:
				if iv['name']:
					print('{key} : {val}'.format(key=ik, val=iv['name']))
				else:
					print('< {key} >'.format(key=ik))
					if n is last:
						print('\n'.join(items))
			else:
				pass

		print('-'*75)
		# print(status['guides'])
		# print('-'*75)
		if self.log:
			print(self.log)
			print('-'*75)
		print('>>>'),
		print('quit showMessage')