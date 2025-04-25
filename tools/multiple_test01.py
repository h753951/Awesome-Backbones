import os
import sys
sys.path.insert(0, os.getcwd())
import torch

from utils.inference import inference_model, init_model, show_result_pyplot, save_result_pyplot
from utils.train_utils import get_info, file2dict
from models.build import BuildNet

def process_image(img_path, model, val_pipeline, classes_names, label_names, output_dir):
    """处理单张图片并保存结果"""
    # 获取原始文件名
    original_filename = os.path.basename(img_path)
    # 去掉扩展名
    filename_without_ext = os.path.splitext(original_filename)[0]
    # 生成输出文件名
    save_path = os.path.join(output_dir, f"output_{filename_without_ext}.jpg")
    
    # 处理图片
    result = inference_model(model, img_path, val_pipeline, classes_names, label_names)
    
    # 保存结果
    save_result_pyplot(model, img_path, result, out_file=save_path)
    print(f"已处理: {img_path} -> 保存到: {save_path}")

def main():
    # ===== 配置参数 =====
    img_folder = r"d:\bishe\complete apple photos\val"
    config = r"D:\bishe\Awesome-Backbones-main\models\efficientnet\efficientnet_b0.py"
    classes_map = r"D:\bishe\Awesome-Backbones-main\datas\annotations.txt"
    device = "cuda" if torch.cuda.is_available() else "cpu"
    output_dir = "output_results"  # 输出文件夹
    
    # 创建输出文件夹
    os.makedirs(output_dir, exist_ok=True)

    # ===== 初始化模型 =====
    classes_names, label_names = get_info(classes_map)
    model_cfg, train_pipeline, val_pipeline, data_cfg, lr_config, optimizer_cfg = file2dict(config)
    model = BuildNet(model_cfg)
    model = init_model(model, data_cfg, device=device, mode='eval')
    
    # ===== 遍历图片文件夹 =====
    # 支持的图片格式
    supported_formats = ('.jpg', '.jpeg', '.png', '.bmp', '.tif', '.tiff', '.JPG', '.JPEG')
    
    # 遍历文件夹
    for filename in os.listdir(img_folder):
        if filename.endswith(supported_formats):
            img_path = os.path.join(img_folder, filename)
            try:
                process_image(img_path, model, val_pipeline, classes_names, label_names, output_dir)
            except Exception as e:
                print(f"处理图片 {filename} 时出错: {str(e)}")
    
    print("所有图片处理完成！")

if __name__ == '__main__':
    main()