
__module_name__ = "_add_obs_var.py"
__author__ = ", ".join(["Michael E. Vinyard"])
__email__ = ", ".join(["vinyard@g.harvard.edu",])


# import packages #
# --------------- #
import numpy as np
import pandas as pd

        
def _add_obs(metadata, cell_names, str_col_keys=["CellNames"]):

    obs_dict = {}
    metadata_dict = {}
    cell_names = pd.DataFrame(cell_names[()].astype('U'), columns=['CellNames'])
    for key, value in metadata.items():
        if value is None:
            metadata_dict[key] = value
        elif value.shape[0] == 1:
            metadata_dict[key] = value[:][0].decode("utf-8")
        else:
            obs_dict[key] = value[:]

    obs_df = pd.DataFrame(obs_dict)

    for col in str_col_keys:
        if col in obs_df.columns:
            obs_df[col] = pd.Categorical(obs_df[col].str.decode("utf-8"))
            
    obs_df = obs_df[obs_df["CellNames"].isin(cell_names["CellNames"])]
    return obs_df, metadata_dict


def _add_var(feature_df, str_col_keys=["seqnames", "name"]):

    """return Feature_DF as var"""

    var_df = pd.DataFrame(np.array(feature_df))

    for col in str_col_keys:
        if col in var_df.columns:
            var_df[col] = pd.Categorical(var_df[col].str.decode("utf-8"))

    var_df = var_df.drop_duplicates(subset='name', keep='first')
    return var_df
             
def _add_obs_var(adata, metadata, feature_df, cell_names):
    
    adata.var = _add_var(feature_df)
    adata.obs, adata.uns['metadata_dict'] = _add_obs(metadata, cell_names)
    
    return adata