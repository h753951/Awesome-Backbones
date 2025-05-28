import os
import sys
import shutil

def generate_file_list(datasets_path, subset_name, class_to_label, output_dir):
    subset_path = os.path.join(datasets_path, subset_name)
    if not os.path.exists(subset_path):
        print(f"警告：{subset_name} 文件夹不存在，跳过处理")
        return
    
    output_lines = []
    prefix = f"datasets/{subset_name}"
    
    for class_name in os.listdir(subset_path):
        class_path = os.path.join(subset_path, class_name)
        if os.path.isdir(class_path):
            if class_name not in class_to_label:
                print(f"警告：发现未标注的类别 '{class_name}'，跳过处理")
                continue
            
            label = class_to_label[class_name]
            
            for image_file in os.listdir(class_path):
                image_full_path = os.path.join(class_path, image_file)
                if os.path.isfile(image_full_path):
                    output_line = f"{prefix}/{class_name}/{image_file} {label}\n"
                    output_lines.append(output_line)
    
    # 直接在目标目录生成文件
    output_file = os.path.join(output_dir, f"{subset_name}.txt")
    with open(output_file, 'w') as f:
        f.writelines(output_lines)
    
    print(f"成功生成 {output_file}，共处理 {len(output_lines)} 个图片")

def main():
    # 获取当前.py文件的绝对路径
    current_file_path = os.path.abspath(__file__)
    
    # 获取当前.py文件的父目录（src的上一级目录）
    parent_dir = os.path.dirname(os.path.dirname(current_file_path))
    
    # 构建与父目录同级的datasets文件夹路径
    datasets_dir = os.path.join(parent_dir, "datasets")
    
    # 构建与父目录同级的datas文件夹路径（用于存放生成的txt文件）
    datas_dir = os.path.join(parent_dir, "datas")
    
    # 确保datas目录存在
    os.makedirs(datas_dir, exist_ok=True)
    
    # 第一步：输入 datasets 文件夹路径
    datasets_path = datasets_dir
    
    if not os.path.exists(datasets_path):
        print(f"错误：路径 {datasets_path} 不存在")
        sys.exit(1)
    
    # 读取 annotations.txt 文件
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    annotations_path = os.path.join(datas_dir, "annotations.txt")
    
    class_to_label = {}
    try:
        with open(annotations_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    class_name, label = line.split()
                    class_to_label[class_name] = label
    except FileNotFoundError:
        print(f"错误：找不到标注文件 {annotations_path}")
        sys.exit(1)
    
    # 第二步和第三步：处理 train, val, test 三个子集
    for subset_name in ["train", "val", "test"]:
        generate_file_list(datasets_path, subset_name, class_to_label, datas_dir)

if __name__ == "__main__":
    main()