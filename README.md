# GeoExcelProcessor

`GeoExcelProcessor` 是一个通过高德地图API获取地理位置和计算距离，并处理Excel文件的工具。

## 功能

- 通过地址获取经纬度和详细地址。
- 计算两个地点之间的距离和行驶时间。
- 处理Excel文件并将结果存入新的Excel文件。

## 配置文件

在 `config.ini` 文件中配置以下参数：

```ini
[settings]
api_key = YOUR_AMAP_API_KEY
address_prefix = YOUR_ADDRESS_PREFIX
input_file = path/to/your/input.xlsx
output_file = path/to/your/output.xlsx
```

## 运行方法
1. 安装依赖库：
pip install -r requirements.txt
2. 运行脚本：
python run.py
3. 打包为可执行文件：
pyinstaller --onefile .\run.py 
