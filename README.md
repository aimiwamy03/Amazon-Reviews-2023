---
configs:
- config_name: raw_meta_All_Beauty
  data_files:
  - split: full
    path: "raw/meta_categories/All_Beauty.jsonl"
- config_name: 0core_last_out_w_his_All_Beauty
  data_files:
  - split: train
    path: "benchmark/0core/last_out_w_his/All_Beauty.train.csv"
  - split: validation
    path: "benchmark/0core/last_out_w_his/All_Beauty.valid.csv"
  - split: test
    path: "benchmark/0core/last_out_w_his/All_Beauty.test.csv"
---
