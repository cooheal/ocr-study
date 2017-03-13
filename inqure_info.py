import os
from PIL import Image

class Photo(object):
	"""docstring for photo"""
	def __init__(self):
		super(Photo, self).__init__()
		self.app_path = os.path.dirname(os.path.realpath(__file__))
		self.static_path = static_path=os.path.join(self.app_path,'static')

	def open(self,photo_name):
		'create Image instance'
		photo_path=os.path.join(self.static_path,photo_name)
		try:
			img=Image.open(photo_path)
		except IOError:
			print('Cannot find the file')
		else:
			return img

	def convert(self,img,size=None,ext=None):
		'convert the image file format to another, you can also adjust the size of the image object'
		try:
			img_name,img_ext=os.path.splitext(os.path.basename(img.filename))
			save_name=img_name+'_copy'+'.'+ext
			save_path=os.path.join(self.static_path,save_name)
		except AttributeError:
			print("'NoneType' object has no attribute 'filename'")
		else:
			if size:
				img=img.resize(size)
			if ext:
				img.save(save_path,ext)
				img=self.open(save_name)
		return img
		
if __name__=='__main__':
	photo=Photo()
	img=photo.open('sample.jpg')
	#new_img=photo.convert(img,ext='PNG')
	#img.show()
