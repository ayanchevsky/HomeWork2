# -*- coding: utf-8 -*-
import datetime
import re
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, Table, Column, Integer, String, DateTime, Float, MetaData, ForeignKey
from sqlalchemy.orm import Session
import os


Base = declarative_base()


class DataTable(Base):
    __tablename__ = 'noutsdata'
    id = Column(Integer, primary_key=True)
    url = Column(String(256))
    visited_at = Column(DateTime)

    name = Column(String(256))
    cpu_hhz = Column(Float)
    ram_gb = Column(Integer)
    ssd_gb = Column(Integer)
    price_rub = Column(Integer)
    rank = Column(Float)

    def __init__(self, url, visited_at, name, cpu_hhz, ram_gb, ssd_gb, price_rub, rank):
        self.url = url
        self.visited_at = visited_at
        self.name = name
        self.cpu_hhz = cpu_hhz
        self.ram_gb = ram_gb
        self.ssd_gb = ssd_gb
        self.price_rub = price_rub
        self.rank = rank

    def __repr__(self):
        return "<Data %s, %s, %s, %s, %s, %s, %s>" % \
               (self.name, self.cpu_hhz, self.ram_gb, self.ssd_gb, self.price_rub, self.url, self.rank)


class NoutsPipeline(object):
    def __init__(self):
        basename = 'data_scraped'
        self.engine = create_engine("sqlite:///%s" % basename, echo=False)
        if not os.path.exists(basename):
            Base.metadata.create_all(self.engine)

    def re_search(self, find, item):
        result = re.search(find, item)
        if result:
            return int(result.group(1))
        else:
            return 0

    def process_item(self, item, spider):
        cpu_hhz = float(self.re_search(r".+(\d\d\d\d) М", str(item['description'])))
        ram_gb = self.re_search(r" (\d{1,2}) G", str(item['description']))
        disk_ssd = self.re_search(r"SSD /? ?(\d{1,4})", str(item['description']))
        disk_emmc = self.re_search(r"eMMC / (\d{1,4})", str(item['description']))
        # disk_hdd = self.re_search(r"HDD / (\d{1,4})", str(item['description']))
        # hdd_disk = disk_ssd + disk_emmc + disk_hdd
        visited_at = datetime.datetime.now()
        #rank = cpu_hhz * 0.3 + ram_gb * 2.9 + disk_ssd * 1.5 + disk_emmc * 1.5 + disk_hdd * 1 + int(item['price']) * -0.01
        rank = cpu_hhz * 0.09 + ram_gb * 5.9 + disk_ssd * 0.5 + disk_emmc * 0.5 + item['price'] * -0.002
        rank = float("{0:.2f}".format(rank))
        disk = disk_ssd if disk_ssd else disk_emmc
        # dt = DataTable(url=item['item'], visited_at=datetime.datetime.now(), name=item['name'], cpu_hhz=cpu_hhz,
        #                ram_gb=ram_gb, ssd_gb=hdd_disk, price_rub=item['price'], rank=rank)
        #print(f"{item['url']}\n{visited_at}\n{item['name']}\n{cpu_hhz}\n{ram_gb}\n{disk}\n{item['price']}\n{rank}")
        dt = DataTable(item['url'], visited_at, item['name'], cpu_hhz, ram_gb, disk, item['price'], rank)
        self.session.add(dt)
        return item

    def close_spider(self, spider):
        self.session.commit()
        self.session.close()

    def open_spider(self, spider):
        self.session = Session(bind=self.engine)
