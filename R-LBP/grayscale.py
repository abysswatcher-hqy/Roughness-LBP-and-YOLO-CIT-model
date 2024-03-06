from PIL import Image
import os

def convert_to_grayscale(input_path, output_path):
    # 打开图像
    original_image = Image.open(input_path)

    # 将图像转换为灰度
    grayscale_image = original_image.convert("L")

    # 保存灰度图像
    grayscale_image.save(output_path)

if __name__ == "__main__":
    # 输入图像的路径
    input_image_path = "../../杂项/阶段4分离.png"  # 替换为实际的图像路径

    # 获取图像文件名和扩展名
    image_name, image_extension = os.path.splitext(os.path.basename(input_image_path))

    # 输出灰度图像的路径
    output_image_path = f"{image_name}_grey{image_extension}"

    # 调用函数进行转换并保存
    convert_to_grayscale(input_image_path, output_image_path)

    print(f"转换完成，灰度图像保存为: {output_image_path}")
