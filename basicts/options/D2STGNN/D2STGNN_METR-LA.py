import os
from easydict import EasyDict
import torch
# architecture 
from basicts.archs.D2STGNN_arch import D2STGNN
# runner
from basicts.runners.D2STGNN_runner import D2STGNNRunner
from basicts.data.base_dataset import BaseDataset
from basicts.metrics.mae import masked_mae
from basicts.metrics.mape import masked_mape
from basicts.metrics.rmse import masked_rmse
from basicts.losses.losses import l1_loss
from basicts.utils.serialization import load_adj

CFG = EasyDict()

# ================= general ================= #
CFG.DESCRIPTION = 'D2STGNN model configuration'
CFG.RUNNER  = D2STGNNRunner
CFG.DATASET_CLS   = BaseDataset
CFG.DATASET_NAME  = "METR-LA"
CFG.DATASET_TYPE  = 'Traffic speed'
CFG.GPU_NUM = 1
CFG.SEED    = 1
CFG.CUDNN_ENABLED = True
CFG.METRICS = {
    "MAE": masked_mae,
    "RMSE": masked_rmse,
    "MAPE": masked_mape
}

# ================= model ================= #
CFG.MODEL = EasyDict()
CFG.MODEL.NAME  = 'D2STGNN'
CFG.MODEL.ARCH  = D2STGNN
adj_mx, _ = load_adj("datasets/" + CFG.DATASET_NAME + "/adj_mx.pkl", "doubletransition")
CFG.MODEL.PARAM = {
    "num_feat"  : 1,
    "num_hidden": 32,
    "dropout"   : 0.1,
    "seq_length": 12,
    "k_t"       : 3,
    "k_s"       : 2,
    "gap"       : 3,
    "num_nodes" : 207,
    "adjs"      : [torch.tensor(adj) for adj in adj_mx],
    "num_layers": 5,
    "num_modalities": 2,
    "node_hidden"   : 10,
    "time_emb_dim"  : 10,
}
CFG.MODEL.FROWARD_FEATURES = [0, 1, 2]            # traffic speed, time in day
CFG.MODEL.TARGET_FEATURES  = [0]                # traffic speed

# ================= optim ================= #
CFG.TRAIN = EasyDict()
CFG.TRAIN.LOSS = l1_loss
CFG.TRAIN.OPTIM = EasyDict()
CFG.TRAIN.OPTIM.TYPE = "Adam"
CFG.TRAIN.OPTIM.PARAM= {
    "lr":0.002,
    "weight_decay":1.0e-5,
    "eps":1.0e-8
}
CFG.TRAIN.LR_SCHEDULER = EasyDict()
CFG.TRAIN.LR_SCHEDULER.TYPE = "MultiStepLR"
CFG.TRAIN.LR_SCHEDULER.PARAM= {
    "milestones":[1, 30, 38, 46, 54, 62, 70, 80],
    "gamma":0.5
}

# ================= train ================= #
CFG.TRAIN.CLIP       = 5
CFG.TRAIN.NUM_EPOCHS = 100
CFG.TRAIN.CKPT_SAVE_DIR = os.path.join(
    'checkpoints',
    '_'.join([CFG.MODEL.NAME, str(CFG.TRAIN.NUM_EPOCHS)])
)
# train data
CFG.TRAIN.DATA          = EasyDict()
CFG.TRAIN.NULL_VAL      = 0.0
## read data
CFG.TRAIN.DATA.DIR      = 'datasets/' + CFG.DATASET_NAME
## dataloader args, optional
CFG.TRAIN.DATA.BATCH_SIZE   = 32
CFG.TRAIN.DATA.PREFETCH     = False
CFG.TRAIN.DATA.SHUFFLE      = True
CFG.TRAIN.DATA.NUM_WORKERS  = 2
CFG.TRAIN.DATA.PIN_MEMORY   = False
## curriculum learning
CFG.TRAIN.CL    = EasyDict()
CFG.TRAIN.CL.WARM_EPOCHS    = 0
CFG.TRAIN.CL.CL_EPOCHS      = 6
CFG.TRAIN.CL.PREDICTION_LENGTH  = 12

# ================= validate ================= #
CFG.VAL = EasyDict()
CFG.VAL.INTERVAL = 1
# validating data
CFG.VAL.DATA = EasyDict()
## read data
CFG.VAL.DATA.DIR      = 'datasets/' + CFG.DATASET_NAME
## dataloader args, optional
CFG.VAL.DATA.BATCH_SIZE     = 32
CFG.VAL.DATA.PREFETCH       = False
CFG.VAL.DATA.SHUFFLE        = False
CFG.VAL.DATA.NUM_WORKERS    = 2
CFG.VAL.DATA.PIN_MEMORY     = False

# ================= test ================= #
CFG.TEST = EasyDict()
CFG.TEST.INTERVAL = 1
# validating data
CFG.TEST.DATA = EasyDict()
## read data
CFG.TEST.DATA.DIR      = 'datasets/' + CFG.DATASET_NAME
## dataloader args, optional
CFG.TEST.DATA.BATCH_SIZE    = 32
CFG.TEST.DATA.PREFETCH      = False
CFG.TEST.DATA.SHUFFLE       = False
CFG.TEST.DATA.NUM_WORKERS   = 2
CFG.TEST.DATA.PIN_MEMORY    = False
