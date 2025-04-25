import os
import sys
sys.path.insert(0, os.getcwd())
import torch

from utils.inference import inference_model, init_model, show_result_pyplot, save_result_pyplot
from utils.train_utils import get_info, file2dict
from models.build import BuildNet

def main():
    # ===== 硬编码参数（替换成你的实际参数） =====
    img = r"D:/bishe/complete apple photos/val/ce_image (272).JPG"
    config = r"D:\bishe\Awesome-Backbones-main\models\efficientnet\efficientnet_b0.py"
    classes_map = r"D:\bishe\Awesome-Backbones-main\datas\annotations.txt"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    
    # save_path = "output.jpg"
    
    
    # 获取 ce_image (275).JPG
    original_filename = os.path.basename(img)
    # 去掉扩展名
    filename_without_ext = os.path.splitext(original_filename)[0]
      # 生成 output_ce_image (275).jpg
    save_path = f"output_{filename_without_ext}.jpg"

    # ===== 以下逻辑保持不变 =====
    classes_names, label_names = get_info(classes_map)
    model_cfg, train_pipeline, val_pipeline, data_cfg, lr_config, optimizer_cfg = file2dict(config)
    
    model = BuildNet(model_cfg)
    model = init_model(model, data_cfg, device=device, mode='eval')
    
    # 测试单张图片
    result = inference_model(model, img, val_pipeline, classes_names, label_names)
    
    # 显示结果
    # show_result_pyplot(model, img, result, out_file=save_path)
    
    # 仅保持结果
    save_result_pyplot(model, img, result, out_file=save_path)
    
    

if __name__ == '__main__':
    main()