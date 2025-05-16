以下是为该激活工具编写的README文档：

# JetBrains激活工具 v3.0

![界面截图](screenshot.png) <!-- 建议添加实际界面截图 -->

## 📖 项目简介

一款基于PyQt6开发的Windows平台图形化工具，用于快速激活JetBrains全系列开发工具。提供简洁易用的界面和自动化激活流程，支持主流IDE的一键激活。

## ⚙️ 功能特性

- ✅ 支持产品：
  - CLion | DataGrip | GoLand | IDEA 
  - PhpStorm | PyCharm | Rider | WebStorm
- 🛡️ 管理员权限自动检测
- 📜 动态脚本加载与验证
- 📊 实时状态反馈与日志记录
- 🖥️ 高DPI显示支持
- 🚦 安全防护规避提示

## 📦 系统要求

- **操作系统**: Windows 10/11 (64位)
- **运行环境**: [.NET Framework 4.8+](https://dotnet.microsoft.com/download/dotnet-framework)
- **权限要求**: 必须使用管理员权限运行

## 🚀 快速开始

### 安装步骤
1. 安装Python依赖：
   ```bash
   pip install -r requirements.txt
   ```
2. 打包可执行文件（可选）：
   ```bash
   pyinstaller --onefile --add-data "scripts/*;scripts" --icon=jetbrains.ico activation.py
   ```

### 使用说明
1. 将程序添加到杀毒软件白名单
2. 右键选择"以管理员身份运行"
3. 仔细阅读并同意用户协议
4. 选择需要激活的开发工具
5. 等待执行结果提示（约10-30秒）

> ⚠️ 注意：首次运行前请确保：
> - 已关闭所有JetBrains产品
> - 系统时间设置正确
> - 计算机已连接互联网

## 🛠️ 技术细节

- **脚本验证机制**：
  ```python
  def check_script_valid(self, path):
      """ 增强型脚本验证 """
      return os.path.exists(path) and path.lower().endswith('.vbs')
  ```
- **进程管理**：
  ```python
  process = QProcess(self)
  process.start("wscript.exe", [script_path])
  ```
- **日志系统**：
  - 记录位置：`activation.log`
  - 包含：时间戳、操作记录、错误详情

## ⚠️ 注意事项

1. 部分安全软件可能误报为风险程序
2. 每个激活操作会生成独立日志记录
3. 激活有效期与服务器状态相关
4. 不支持批量激活操作

## 📜 免责声明

本工具仅供**学习研究**目的，开发者不承担以下责任：
- ❌ 用于商业用途造成的法律问题
- ❌ 长期使用导致的版权纠纷
- ❌ 系统环境差异引发的兼容性问题

根据用户协议，您应在使用后24小时内：
1. 删除本程序所有副本
2. 卸载通过本程序激活的软件
3. 购买JetBrains正版授权（[官网](https://www.jetbrains.com/)）

## 📄 许可证

本项目基于 [MIT License](LICENSE) 发布，请严格遵守开源协议使用。

---

**友情提示**：推荐开发者支持正版软件，获取完整功能与官方技术支持。[教育授权申请](https://www.jetbrains.com/community/education/#students)
