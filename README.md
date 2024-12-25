# 通讯录管理系统

这是一个使用 PyQt6 构建的通讯录管理系统，支持添加、删除、查找和更新联系人信息。

## 功能特性

- 添加联系人
- 删除联系人
- 查找联系人
- 更新联系人信息
- 显示联系人列表
- 日志记录

## 安装

1. 克隆仓库到本地：

    ```bash
    git clone https://github.com/LogicShao/SimpleAddressBook.git
    cd SimpleAddressBook
    ```

2. 创建并激活虚拟环境：

    ```bash
    # macOS/Linux
    python3 -m venv .venv
    source .venv/bin/activate

    # Windows
    python -m venv .venv
    .venv\Scripts\activate
    ```

3. 安装依赖：

    ```bash
    pip install -r requirements.txt
    ```

## 使用

1. 运行主程序：

    ```bash
    python main.py
    ```

2. 在主窗口中，你可以通过工具栏按钮添加、删除、查找和更新联系人信息。

## 文件结构

- main.py：程序入口，初始化并运行主窗口。
- MainWindow.py：主窗口类，包含联系人表格和工具栏。
- DataHandler.py：数据处理类，负责加载和保存联系人数据。
- EventDialog.py：对话框类，包含添加联系人、显示联系人信息等功能。
- ContactPerson.py：联系人类，定义联系人数据结构。
- logConfig.py：日志配置文件，配置日志记录器。
- application.log：日志文件，记录程序运行日志。
- randContactPerson.py: 用于产生随机的联系人到 "addressbook.json"，使用方法为 `python randContactPerson.py Num`，将生成 `Num` 个随机联系人。若不指定则将生成 10 个。

## 日志

日志文件 application.log 会记录程序的运行日志，包括加载联系人、添加联系人、删除联系人等操作。日志文件的最大大小为 5MB，当超过大小时会自动清空。
