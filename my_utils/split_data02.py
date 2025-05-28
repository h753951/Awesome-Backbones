import os
from shutil import copy, rmtree
import random
from tqdm import tqdm

def main():
    '''
    split_rate_val : 验证集占训练集的比例（从训练集中再划分）
    split_rate_test: 测试集划分比例
    init_dataset   : 未划分前的数据集路径
    new_dataset    : 划分后的数据集路径
    '''
    def makedir(path):
        if os.path.exists(path):
            rmtree(path)
        os.makedirs(path)
    
    split_rate_test = 0.1  # 测试集比例（占总数据）
    split_rate_val = 0.112   # 验证集比例（占剩余训练数据）
    init_dataset = ''      # 原始数据集路径
    new_dataset = 'datasets'
    random.seed(0)

    classes_name = [name for name in os.listdir(init_dataset)]

    makedir(new_dataset)
    training_set = os.path.join(new_dataset, "train")
    val_set = os.path.join(new_dataset, "val")
    test_set = os.path.join(new_dataset, "test")
    makedir(training_set)
    makedir(val_set)
    makedir(test_set)
    
    for cla in classes_name:
        makedir(os.path.join(training_set, cla))
        makedir(os.path.join(val_set, cla))
        makedir(os.path.join(test_set, cla))

    for cla in classes_name:
        class_path = os.path.join(init_dataset, cla)
        img_set = os.listdir(class_path)
        num = len(img_set)
        
        # 1. 先划分测试集
        test_set_index = random.sample(img_set, k=int(num * split_rate_test))
        remaining_imgs = [img for img in img_set if img not in test_set_index]
        
        # 2. 从剩余数据中划分验证集
        val_set_index = random.sample(
            remaining_imgs, 
            k=int(len(remaining_imgs) * split_rate_val)
        )
        
        # 3. 训练集 = 剩余数据 - 验证集
        train_set_index = [img for img in remaining_imgs if img not in val_set_index]
        
        # 复制文件到对应目录
        with tqdm(total=num, desc=f'Class : ' + cla, mininterval=0.3) as pbar:
            for img in img_set:
                init_img = os.path.join(class_path, img)
                if img in test_set_index:
                    new_img = os.path.join(test_set, cla)
                elif img in val_set_index:
                    new_img = os.path.join(val_set, cla)
                else:
                    new_img = os.path.join(training_set, cla)
                copy(init_img, new_img)
                pbar.update(1)
        print()

if __name__ == '__main__':
    main()