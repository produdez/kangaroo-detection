from mrcnn.model import load_image_gt
from mrcnn.model import mold_image
from mrcnn.utils import compute_ap
import numpy as np

def evaluate_model(dataset, model, cfg):
    APs = list()
    for image_id in dataset.image_ids:
        image, _, gt_class_id, gt_bbox, gt_mask = load_image_gt(dataset, cfg, image_id)
        scaled_image = mold_image(image, cfg)
        sample = np.expand_dims(scaled_image, 0)
        yhat = model.detect(sample, verbose = 0)
        r = yhat[0]
        AP, _, _, _ = compute_ap(
            gt_bbox, gt_class_id, gt_mask, 
            r['rois'], r['class_ids'], r['scores'], r['masks'])
        
        APs.append(AP)
    
    meanAP = np.mean(APs)
    return meanAP
