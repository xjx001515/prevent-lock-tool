from PIL import Image, ImageDraw, ImageFont
import os

def create_icon():
    # 创建一个 256x256 的图像，使用 RGBA 模式支持透明度
    size = 256
    image = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    draw = ImageDraw.Draw(image)
    
    # 绘制圆形背景
    margin = 20
    draw.ellipse([margin, margin, size-margin, size-margin], 
                 fill='#0071e3')
    
    # 绘制鼠标图标
    cursor_color = 'white'
    cursor_points = [
        (size//2-40, size//2-40),  # 左上
        (size//2+20, size//2+20),  # 右下
        (size//2-40, size//2+20),  # 左下
    ]
    draw.polygon(cursor_points, fill=cursor_color)
    
    # 保存为 ICO 文件
    image.save('prevent_lock.ico', format='ICO', sizes=[(256, 256)])

if __name__ == '__main__':
    create_icon() 