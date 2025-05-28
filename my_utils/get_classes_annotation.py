import os
import sys

def list_subfolders_with_index():
    """
    列出文件夹路径下所有第一级子文件夹，并生成annotations.txt文件。
    如果没有子文件夹或存在文件，则报错退出。
    
    Returns:
        bool: 操作是否成功
    """
    
    
    # 获取当前.py文件的绝对路径
    current_file_path = os.path.abspath(__file__)  # 例如：/home/user/project/src/main.py

    # 获取当前.py文件的父目录（src的上一级目录）
    parent_dir = os.path.dirname(os.path.dirname(current_file_path))  # /home/user/project

    # 构建与父目录同级的datasets路径
    datasets_dir = os.path.join(parent_dir, "datasets")  # /home/user/project/datasets
    
    # datasets/train
    datasets_train_dir = os.path.join(datasets_dir, "train")
    
    # 构建与父目录同级的datas路径
    datas_dir = os.path.join(parent_dir, "datas")
    
    # 硬编码的文件夹路径（直接写死）
    folder_path = datasets_train_dir
    
    # 检查路径是否存在
    if not os.path.exists(folder_path):
        print(f"错误：路径 '{folder_path}' 不存在")
        return False
    
    # 检查是否是文件夹
    if not os.path.isdir(folder_path):
        print(f"错误：'{folder_path}' 不是文件夹")
        return False
    
    # 获取所有第一级条目
    entries = os.listdir(folder_path)
    
    # 检查是否存在文件
    has_files = any(os.path.isfile(os.path.join(folder_path, entry)) for entry in entries)
    if has_files:
        print("错误：文件夹下存在文件，请确保只包含子文件夹")
        return False
    
    # 获取所有子文件夹
    subfolders = [entry for entry in entries 
                 if os.path.isdir(os.path.join(folder_path, entry))]
    
    # 检查是否有子文件夹
    if not subfolders:
        print("错误：文件夹下没有子文件夹")
        return False
    
    # 按字母顺序排序并编号
    subfolders.sort()
    
    # 获取当前脚本所在目录
    # script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(datas_dir, "annotations.txt")
    
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            for idx, name in enumerate(subfolders):
                # 如果是最后一个元素，不添加换行符
                if idx == len(subfolders) - 1:
                    f.write(f"{name} {idx}")
                else:
                    f.write(f"{name} {idx}\n")
        
        print(f"成功生成 annotations.txt 文件，共写入 {len(subfolders)} 个子文件夹")
        print(f"文件路径: {output_file}")
        return True
    except Exception as e:
        print(f"写入文件时出错: {e}")
        return False

if __name__ == "__main__":
    # 直接调用函数，不再从命令行或输入获取路径
    if not list_subfolders_with_index():
        sys.exit(1)