import os
from PIL import Image,ImageDraw,ImageFont
import chardet
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

	def convert(self,img,size=None,ext=None,mode=None):
		'convert the image file format to another, you can also adjust the size of the image object, return a new Image instance'
		try:
			img_name,img_ext=os.path.splitext(os.path.basename(img.filename))
			save_name=img_name+'_copy'+img_ext
			save_path=os.path.join(self.static_path,save_name)
		except AttributeError:
			print("'NoneType' object has no attribute 'filename'")
		else:
			if mode:
				img=img.convert(mode)
				#Gray = R * 0.299 + G * 0.587 + B * 0.114
			if size:
				img=img.resize(size)
			if ext:
				img.save(save_path,ext)
			else:
				img.save(save_path)
				img=self.open(save_name)
			return img

	def gray_to_char(self,img):
		"pass a img that format of 'L' return a txt file"
		width,height=img.size
		char_list=list("#$%&0123456789@abcdefghijklmnopqrstuvwxyzæç÷ø¤¥©ª±»")#共5，而51*5=255,不过还不能对应255这个灰度，使其为空格。
		char_txt=''
		for i in range(height):
			for j in range(width):
				#chr() Return a Unicode string of one character with ordinal i; 0 <= i <= 0x10ffff.
				#ord() Return the Unicode code point for a one-character string.
				#根据取点得到背景色的灰度为179或180，故设定unicode码为75或76转换为空格
				gray=img.getpixel((j,i))
				#index=gray//5,index in range(32,37)的背景色
				if gray==255 or (gray//5) in range(30,38):
					char_txt+=' '
				else:
					char_txt+=char_list[gray//5]
				#char_txt+=chr(255-gray)#使用chr转换会出现一些非常不理想的字符，因此还是手动选择比较好,不过也是使用chr()进行预先选择
			char_txt+='\n'

		img_name=os.path.splitext(os.path.basename(img.filename))[0]
		txt_name=img_name+'.txt'
		char_txt_path=os.path.join(self.static_path,txt_name.replace('txt','jpg'))
		with open(char_txt_path,'wt',encoding='utf-8') as f:
			f.write(char_txt)
			f.close()

		blank=Image.new('L',(1100,2500),255)
		blank_path=os.path.join(self.static_path,'blank.jpg')
		txt_img_path=os.path.join(self.static_path,'txt_img.jpg')
		blank.save(blank_path)
		draw=ImageDraw.Draw(blank)
		fnt=ImageFont.truetype("arial.ttf",16)
		#draw.text((10,10),char_txt,font=fnt,fill=0,align='center')
		draw.text((10,10),char_txt,font=fnt,fill=0,align='center')
		#blank.show()
		blank=blank.resize(img.size)
		blank.save(char_txt_path)

def change_to_img():
	pass

if __name__=='__main__':
	photo=Photo()
	img=photo.open('sample.jpg')
	new_img=photo.convert(img,mode='L')
	photo.gray_to_char(new_img)
