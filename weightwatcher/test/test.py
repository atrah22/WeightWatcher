import unittest

import weightwatcher as ww

class Test_VGG11(unittest.TestCase):

	@classmethod
	def setUpClass(cls):
		"""I run only once for this class
		"""
		import torchvision.models as models
		cls.model = models.vgg11(pretrained=True)
		cls.watcher = ww.WeightWatcher(model=cls.model, log=False)


	def setUp(self):
		"""I run before every test in this class
		"""
		pass


	def test_summary_is_dict(self)
		"""Test that get_summary() returns a valid python dict
		"""
		self.watcher.analyze()
		summary = self.watcher.get_summary()

		self.assertTrue(isinstance(summary, dict), "Summary is a dictionary")

		for key in ['norm', 'norm_compound', 'lognorm', 'lognorm_compound']:
			self.assertTrue(key in summary, "{} in summary".format(key))


	def test_pandas(self):
		"""Test that get_summary(pandas=True) returns a valid pandas dataframe
		"""
		import pandas as pd

		self.watcher.analyze()
		summary = self.watcher.get_summary(pandas=True)

		self.assertEqual(isinstance(summary, pd.DataFrame), True, "Summary is a pandas DataFrame")

		columns = ",".join(summary.columns)
		for key in ['norm', 'norm_compound', 'lognorm', 'lognorm_compound']:
			self.assertTrue(key in summary.columns, "{} in summary. Columns are {}".format(key, columns))


	def test_filter_dense_layer_types(self):
		"""Test that ww.LAYER_TYPE.DENSE filter is applied only to DENSE layers"
		"""
		import pandas as pd

		results = self.watcher.analyze(layers=ww.LAYER_TYPE.DENSE)
		d = self.watcher.get_details(results=results)

		denseLayers = d[d['layer_type']=="DENSE"]
		denseCount = len(denseLayers)

		self.assertTrue(denseCount > 0, "Non zero number of dense layers: {} found".format(denseCount))
			
		# Dense layers are analyzed
		self.assertTrue((denseLayers.N > 0).all(axis=None), "All {} dense layers have a non zero N".format(denseCount))
		self.assertTrue((denseLayers.M > 0).all(axis=None), "All {} dense layers have a non zero M".format(denseCount))

		nonDenseLayers = d[d['layer_type']!="DENSE"]
		nonDenseCount = len(nonDenseLayers)

		self.assertTrue(nonDenseCount > 0, "VGG11 has non dense layers: {} found".format(nonDenseCount))
		
		# Non Dense layers are NOT analyzed
		self.assertTrue((nonDenseLayers.N == 0).all(axis=None), "All {} NON dense layers have a zero N".format(nonDenseCount))
		self.assertTrue((nonDenseLayers.M == 0).all(axis=None), "All {} NON dense layers have a zero M".format(nonDenseCount))


	def test_filter_conv2D_layer_types(self):
		"""Test that ww.LAYER_TYPE.CONV2D filter is applied only to CONV2D layers"
		"""
		import pandas as pd

		results = self.watcher.analyze(layers=ww.LAYER_TYPE.CONV2D)
		d = self.watcher.get_details(results=results)

		conv2DLayers = d[d['layer_type']=="CONV2D"]
		conv2DCount = len(conv2DLayers)

		self.assertTrue(conv2DCount > 0, "Non zero number of conv2D layers: {} found".format(conv2DCount))
			
		# Conv2D layers are analyzed
		self.assertTrue((conv2DLayers.N > 0).all(axis=None), "All {} conv2D layers have a non zero N".format(conv2DCount))
		self.assertTrue((conv2DLayers.M > 0).all(axis=None), "All {} conv2D layers have a non zero M".format(conv2DCount))

		nonConv2DLayers = d[d['layer_type']!="CONV2D"]
		nonConv2DCount = len(nonConv2DLayers)

		self.assertTrue(nonConv2DCount > 0, "VGG11 has non conv2D layers: {} found".format(nonConv2DCount))
		
		# Non Conv2D layers are NOT analyzed
		self.assertTrue((nonConv2DLayers.N == 0).all(axis=None), "All {} NON conv2D layers have a zero N".format(nonConv2DCount))
		self.assertTrue((nonConv2DLayers.M == 0).all(axis=None), "All {} NON conv2D layers have a zero M".format(nonConv2DCount))


	def test_compare(self):
		"""End to end testing between resnet18 and resnet152
		"""
		import torchvision.models as models

		modelA = models.resnet18(pretrained=True)
		modelB = models.resnet152(pretrained=True)
		
		result = ww.WeightWatcher.compare(modelA, modelB)
		self.assertFalse(result, "resnet152 is better than resnet18 norm wise")

		result = ww.WeightWatcher.compare(modelA, modelB, compute_spectralnorms=True)
		self.assertFalse(result, "resnet152 is better than resnet18 spectralnorm wise")

		result = ww.WeightWatcher.compare(modelA, modelB, compute_softranks=True)
		self.assertFalse(result, "resnet152 is better than resnet18 spectralnorm wise")

		# slow (disabled for now)
		result = ww.WeightWatcher.compare(modelA, modelB, compute_alphas=True, multiprocessing=False)
		self.assertFalse(result, "resnet152 is better than resnet18 alpha wise")
		

if __name__ == '__main__':
	unittest.main()