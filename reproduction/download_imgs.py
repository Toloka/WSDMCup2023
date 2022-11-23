from joblib import Parallel, delayed
from tqdm.auto import tqdm
import pandas as pd
import wget
import os


df = pd.read_csv('sample_urls.csv')
os.mkdir('data/imgs')
img_paths = Parallel(
    n_jobs=100)(delayed(wget.download)(img_url, out='data/imgs') for img_url in tqdm(df.image)
)
