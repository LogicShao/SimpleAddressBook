from ContactPerson import ContactPerson
from logConfig import logger

import json
import os
import atexit


class DataHandler:
    def __init__(self, path: str):
        self.path = path
        self.addressbook = self.load_addressbook()
        self.is_saved = False

        logger.info("从 %s 加载通讯录，共 %d 个联系人",
                    self.path, len(self.addressbook))
        # 当addressbook太大打印head和tail
        if len(self.addressbook) > 10:
            contacts = self.getContacts()
            logger.info("展示前 5 个联系人: %s", contacts[:5])
            logger.info("展示后 5 个联系人: %s", contacts[-5:])
        elif len(self.addressbook) > 0:
            logger.info("联系人: %s", self.getContacts())

        atexit.register(self.save_addressbook)

    def __del__(self):
        self.save_addressbook()

    def save_addressbook(self):
        if self.is_saved:
            return
        self.is_saved = True

        # 保存通讯录数据
        with open(self.path, "w", encoding="utf-8") as file:
            try:
                data = [contact.__dict__
                        for contact in self.addressbook.values()]
                json.dump(data, file, ensure_ascii=False, indent=4)
                logger.info("数据保存至 %s", self.path)
            except Exception as e:
                logger.error("数据保存至 %s 失败", e)

    def load_addressbook(self) -> dict[str, ContactPerson]:
        if not self.path.endswith(".json"):
            raise RuntimeError("仅支持json文件")

        # 读取通讯录数据
        if not os.path.exists(self.path):
            # 创建一个空文件并返回空字典
            with open(self.path, "w", encoding="utf-8") as file:
                file.write("[]")
            return {}

        # 判断文件是否为空
        if os.path.getsize(self.path) == 0:
            return {}

        with open(self.path, "r", encoding="utf-8") as file:
            data: list[dict] = json.load(file)
        return {item["name"]: ContactPerson(**item) for item in data}

    def getContacts(self) -> list[ContactPerson]:
        # 获取所有联系人
        return sorted(self.addressbook.values(), key=lambda x: x.name)

    def addContact(self, contact: ContactPerson):
        name = contact.name
        if name in self.addressbook:
            raise ValueError(f"联系人{name}已存在")
        self.addressbook[name] = contact

    def removeContact(self, name: str):
        if name not in self.addressbook:
            raise ValueError(f"联系人{name}不存在")
        del self.addressbook[name]

    def updateContact(self, name: str, contact: ContactPerson):
        if name not in self.addressbook:
            raise ValueError(f"联系人{name}不存在")
        self.addressbook[name] = contact

    def getContact(self, name: str) -> ContactPerson:
        if name not in self.addressbook:
            raise ValueError(f"联系人{name}不存在")
        return self.addressbook[name]

    def existContact(self, name: str) -> bool:
        return name in self.addressbook
