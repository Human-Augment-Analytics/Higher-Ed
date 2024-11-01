import deeplabcut
config_path = "/home/hice1/kcozart6/scratch/Copy of Successful Run on 10.28.2024/config.yaml"
deeplabcut.evaluate_network(config_path, snapshotindex='all')