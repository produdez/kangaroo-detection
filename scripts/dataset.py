from mrcnn.utils import Dataset
from os import listdir
from pprint import pprint
import numpy as np
from xml.etree import ElementTree

def get_xml_int(xml_element, name):
	str_value = xml_element.finpdtext(name)

	if not str_value: 
		inner_values = {x.tag : x.text for x in xml_element}
		raise ValueError(
			f'Invalid value for type <int> when searching for <{name}> in <{xml_element.tag}> which contains: {inner_values}'
		)

	return int(str_value)

class KangarooDataset(Dataset):
	def __init__(self, debug = False, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.debug = debug
		self.debug_limit = 2
		self.bad_images = ['00090']
		self.source = 'dataset'
		self.train_size = 150
			
	def load_data(self, dataset_dir, is_train=True):
		self.add_class(self.source, 1, 'kangaroo')

		images_dir = dataset_dir + 'images/'
		annotations_dir = dataset_dir + 'annots/'

		for filename in listdir(images_dir):
			# get image id
			image_id = filename[:-4] # skipping file extension '.jpg'
			
			if self.debug and int(image_id) > self.debug_limit: break

			# skip bad ones
			if image_id in self.bad_images: continue

			image_path = images_dir + filename 
			annotation_path = annotations_dir + image_id + '.xml'

			# training/validation 
			if is_train and int(image_id) >= self.train_size: continue
			if not is_train and int(image_id) < self.train_size: continue

			# add to ds
			self.add_image(self.source, image_id=image_id, path=image_path, annotation=annotation_path)
		
		if self.debug:
			print('-- Image info --')
			pprint(self.image_info)

	def extract_boxes(self, annotation_path):
		xml_tree = ElementTree.parse(annotation_path)
		annotation = xml_tree.getroot()

		boxes = []
		for box in annotation.iter('bndbox'):
			xmin = get_xml_int(box, 'xmin')
			ymin = get_xml_int(box, 'ymin')
			xmax = get_xml_int(box, 'xmax')
			ymax = get_xml_int(box, 'ymax')
			coordinates = [xmin, ymin, xmax, ymax]
			boxes.append(coordinates)
		width = get_xml_int(annotation, './/size/width')
		height = get_xml_int(annotation, './/size/height')

		if self.debug: 
			print(f'width: {width}, height: {height}, boxes: ')
			pprint(boxes)
		return boxes, width, height
	def load_mask(self,image_id): 
		info = self.image_info[image_id]
		annotation_path = info['annotation']

		boxes, w, h = self.extract_boxes(annotation_path)

		class_ids = []
		masks = np.zeros([h, w, len(boxes)], dtype=np.uint8)
		for i, (xmin, ymin, xmax, ymax) in enumerate(boxes):
			masks[ymin:ymax, xmin:xmax, i] = 1
			class_ids.append(self.class_names.index('kangaroo'))
		
		return masks, np.asarray(class_ids, dtype=np.int32)

	def image_reference(self, image_id):
		info = self.image_info[image_id]
		return info['path']
