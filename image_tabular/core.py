# AUTOGENERATED! DO NOT EDIT! File to edit: 00_core.ipynb (unless otherwise specified).

__all__ = ['get_valid_index', 'normalize_funcs_image_tab']

# Cell
from fastai.vision import *
from fastai.tabular import *
from typing import *
from torch import *
from typing import Tuple,Callable
from torch import Tensor,FloatTensor
from functools import partial


# Cell
def get_valid_index(df, valid_pct:float=0.2, seed:int=0):
    """generate valid index that will be used to split both image and tabular data"""
    np.random.seed(seed)
    rand_idx = np.random.permutation(range_of(df))
    cut = int(valid_pct * len(df))
    val_idx = rand_idx[:cut]
    return val_idx

# Cell
def _normalize_batch_image_tab(b:Tuple[Tensor,Tensor],
                               mean:FloatTensor,
                               std:FloatTensor,
                               do_x:bool=True,
                               do_y:bool=False)->Tuple[Tensor,Tensor]:
    "`b` = `x`,`y` - normalize `x` array of imgs and `do_y` optionally `y`."
    x,y = b
    # only normalize image not tabular data
    mean,std = mean.to(x[0].device),std.to(x[0].device)
    if do_x: x[0] = normalize(x[0],mean,std)
    return x,y

def normalize_funcs_image_tab(mean:FloatTensor,
                              std:FloatTensor, do_x:bool=True,
                              do_y:bool=False)->Tuple[Callable,Callable]:
    "Create normalize/denormalize func using `mean` and `std`, can specify `do_y` and `device`."
    mean,std = tensor(mean),tensor(std)
    # use custom _normalize_batch_image_tab function to accommodate (image_data, tabular_data)
    return (partial(_normalize_batch_image_tab, mean=mean, std=std, do_x=do_x, do_y=do_y),
            partial(denormalize,      mean=mean, std=std, do_x=do_x))
