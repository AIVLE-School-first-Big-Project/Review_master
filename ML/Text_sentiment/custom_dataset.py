import torch
from torch.nn import functional as F
from torch.utils.data import Dataset
from transformers import AutoTokenizer

import re

class NSMCDataset(Dataset):
  def __init__(self, df):
    self.tokenizer = AutoTokenizer.from_pretrained("monologg/koelectra-base-v3-discriminator")
    self.p = re.compile("밓")
    self.text = df['context']

  def __len__(self):
    return len(self.text)
  
  def __getitem__(self, idx):
    text = self.text.values[idx]
    text = self.p.sub("미",text)

    inputs = self.tokenizer(
        text, 
        return_tensors='pt',
        truncation=True,
        max_length=256,
        pad_to_max_length=True,
        add_special_tokens=True
        )
    
    input_ids = inputs['input_ids'][0]
    attention_mask = inputs['attention_mask'][0]

    return input_ids, attention_mask
