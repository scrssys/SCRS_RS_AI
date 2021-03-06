from collections import namedtuple


Config = namedtuple("Config", [
  "train_data_path",
  "img_w",
  "img_h",
  "im_bands",
  "band_list",
  "im_type",
  "target_name",
  "val_rate",
  "augment",
  "label_nodata",
  "network",
  "BACKBONE",
  "activation",
  "encoder_weights",
  "dropout",
  "nb_classes",
  "sample_per_img",
  "batch_size",
  "epochs",
  "optimizer",
  "loss",
  "class_weights",
  "metrics",
  "lr",
  "lr_steps",
  "lr_gamma",
  "lr_scheduler",
  "nb_epoch",
  "old_epoch",
  "test_pad",
  "model_dir",
  "base_model",
  "monitor",
  "save_best_only",
  "mode",
  "factor",
  "patience",
  "epsilon",
  "cooldown",
  "min_lr",
  "log_dir",
  "img_input",
  "strategy",
  "window_size",
  "subdivisions",
  "slices",
  "block_size",
  "nodata",
  "tovector",
  "model_path",
  "mask_dir"
])


