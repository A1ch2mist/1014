from PIL import Image

# 定义输入和输出文件路径
input_image_path = r"C:\Users\60361\Desktop\篮球 (2).png"
output_icon_path = r"C:\Users\60361\Desktop\篮球 (2).ico"

# 打开 PNG 图像文件
image = Image.open(input_image_path)

# 将图像保存为 ICO 格式
image.save(output_icon_path)

print("转换完成！")
