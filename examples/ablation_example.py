import keras
import numpy as np
import sys
sys.path.append('..')
from BioExp import spatial
from BioExp.helpers import utils
import SimpleITK as sitk
from keras.models import load_model
from BioExp.helpers.losses import *
from BioExp.helpers.metric import *


data_root_path = '../sample_vol/'

model_path = '../trained_models/U_resnet/ResUnet.h5'
weights_path = '../trained_models/U_resnet/ResUnet.40_0.559.hdf5'


model = load_model(model_path, custom_objects={'gen_dice_loss':gen_dice_loss,
                                        'dice_whole_metric':dice_whole_metric,
                                        'dice_core_metric':dice_core_metric,
                                        'dice_en_metric':dice_en_metric})
model.load_weights(weights_path)

infoclasses = {}
for i in range(1): infoclasses['class_'+str(i)] = (i,)
infoclasses['whole'] = (1,2,3)


data_root_path = '../sample_vol/'
layer_name = 'conv2d_3'
test_image, gt = utils.load_vol_brats('../sample_vol/Brats18_CBICA_ARZ_1', slicen=78)
A = spatial.Ablation(model = moedl, 
				weights_pth = weights_path, 
				metric      = dice_label_coef, 
				layer_name  = layer_name, 
				test_image  = test_image, 
				gt 	    = gt, 
				classes     = infoclasses, 
				nclasses    = 4)

df = A.ablate_filter(step = 1)
