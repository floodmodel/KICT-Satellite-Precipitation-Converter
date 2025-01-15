# -*- coding: utf-8 -*-
import os
import re
import subprocess
from datetime import datetime, timedelta

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QApplication, QMessageBox

wget_path = (
    '"'
    + os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    + "/wget.exe"
    + '"'
)
kst_list = []


class GPM_download_Class:
    def __init__(
        self,
        userpass,
        userInfo,
        getFiledate_1,  # start
        getFiledate_2,  # end
        # j_date,
        gpm_type,
        donwload_folder,
        timeLabel_type,
        progressbar,
    ):
        # self.url = "https://jsimpsonhttps.pps.eosdis.nasa.gov/text"
        self.url = "https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3"
        self.userInfo = userInfo
        self.getFiledate_1 = getFiledate_1
        # self.j_date = j_date
        self.gpm_type = gpm_type
        self.donwload_folder = donwload_folder
        self.timeLabel_type = timeLabel_type.upper()
        self.days = 0
        self.getFiledate = ""
        self.userpass = userpass
        self.progressbar = progressbar
        # kst 단위

        if self.timeLabel_type == "KST":
            if getFiledate_1 == getFiledate_2:
                self.days = 0
            else:
                # self.days = str(
                #    (datetime.strptime(getFiledate_2, "%Y-%m-%d").date())
                #    - (datetime.strptime(getFiledate_1, "%Y-%m-%d").date())
                # ).split(" ")[0]

                self.days = (
                    datetime.strptime(getFiledate_2, "%Y-%m-%d").date()
                    - datetime.strptime(getFiledate_1, "%Y-%m-%d").date()
                ).days

                # for day in range(int(self.days) + 2):
                #    self.getFiledate = current_date = datetime.strptime(
                #        getFiledate_1, "%Y-%m-%d"
                #    ).date() + timedelta(day)

                # self.j_date = current_date.timetuple().tm_yday
                self.main()

        # UTC 단위
        file_list = []
        if self.timeLabel_type == "UTC":
            if getFiledate_1 == getFiledate_2:
                self.days = 0
            else:
                self.days = str(
                    (datetime.strptime(getFiledate_2, "%Y-%m-%d").date())
                    - (datetime.strptime(getFiledate_1, "%Y-%m-%d").date())
                ).split(" ")[0]

            for day in range(int(self.days) + 1):
                self.getFiledate = str(
                    datetime.strptime(getFiledate_1, "%Y-%m-%d").date() + timedelta(day)
                )
                self.year, self.month, self.day = self.getFiledate.split("-")
                file_list = file_list + self.get_file_list()
            self.main(file_list)

    def main(self, file_list):
        # self.year, self.month,self.day = self.getFiledate.split('-')
        # file_list = self.get_file_list()
        count = 0
        tiff_list = []

        # 변경 예정 240719-오
        if self.gpm_type == "GPM_3IMERGHHE.07":
            # if self.gpm_type == "imerg/gis" or self.gpm_type == "imerg/gis/early":
            for filename in file_list:
                if os.path.splitext(filename)[1] == ".tif":
                    if (("30min") in filename) is True:
                        tiff_list.append(filename)

            self.progressbar.setMaximum(len(tiff_list) - 1)
            QApplication.processEvents()
            for filename in tiff_list:
                if self.timeLabel_type == "UTC":
                    print("UTC")
                    self.progressbar.setValue(count)
                    self.get_file(filename)
                    count = count + 1
                    QApplication.processEvents()
            QMessageBox.information(
                None,
                "GPM Download ",
                " Download is complete. Please check the download folder",
            )

        if self.gpm_type == "GPM_3IMERGHHL.07":
            # if self.gpm_type == "imerg/late" or self.gpm_type == "imerg/early":
            self.progressbar.setMaximum(len(file_list) - 1)
            QApplication.processEvents()
            for filename in file_list:
                if self.timeLabel_type == "UTC":
                    self.get_file(filename)
                    self.progressbar.setValue(count)
                    count = count + 1
                    QApplication.processEvents()
            QMessageBox.information(
                None,
                "GPM Download ",
                " Download is complete. Please check the download folder",
            )

    # kst 단위 다운로드 방식
    def get_file_list_kst(self, filename):
        kst_list.append(filename)
        donwload_list = []
        dayfile = (
            (filename.split(".")[4]).split("-")[0]
            + "-"
            + (filename.split(".")[4]).split("-")[1]
        )
        filedate = re.search(r"\d{8}", filename).group()
        if filedate + "-S163000" in dayfile:
            num = kst_list.index(filename)
            for ii in range(num - 3):
                kst_list.pop(0)

        if len(kst_list) > 48:
            del kst_list[0:48]

        if len(kst_list) == 48:
            for count in kst_list:
                donwload_list.append(count)
        return donwload_list

    def get_file_list(self):
        if self.gpm_type == "GPM_3IMERGHHL.07" or self.gpm_type == "GPM_3IMERGHHE.07":
            # if self.gpm_type == "imerg/late" or self.gpm_type == "imerg/early":
            julian_date = self.__get_julian_date()
            server = "{0}/{1}/{2}/{3}".format(
                self.url,
                self.gpm_type,
                self.year,
                # self.j_date,
                # self.year + self.month,
                julian_date,
            )

        # if self.gpm_type == "GPM_3IMERGHHL.07" or self.gpm_type == "GPM_3IMERGHHE.07"
        if (
            self.gpm_type == "imerg/gis" or self.gpm_type == "imerg/gis/early"
        ):  # 이전 코드
            server = "{0}/{1}/{2}/{3}".format(
                self.url,
                self.gpm_type,
                self.year + "/" + self.month,
                self.year + self.month + self.day,
            )

        tmpmyPW = ""
        tmpmyPW = self.userpass
        cmd = "{0} --user={1} --password={2} -qO- {3}".format(
            wget_path, self.userInfo, tmpmyPW, server
        )

        QMessageBox.information(
            None,
            "GPM Download ",
            cmd,
        )

        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True
        )

        stdout = process.communicate()[0].decode()
        if stdout[0] == "<":
            print(stdout[0])
            print("No imerg files for the given date")
            return []
        file_list = stdout.split()
        return file_list

    def get_file(self, filenames):
        if self.gpm_type == "GPM_3IMERGHHL.07":
            # if self.gpm_type == "imerg/late":  # HHL
            # ftype은 그대로(저장경로...)
            ftype = "GPM/HDF5/late"
        elif self.gpm_type == "imerg/gis":  # tiff?
            ftype = "GPM/TIFF/late"

        if self.gpm_type == "GPM_3IMERGHHE.07":
            # if self.gpm_type == "imerg/early":  # HHE
            ftype = "GPM/HDF5/early"
        elif self.gpm_type == "imerg/gis/early":  # tiff 변환?
            ftype = "GPM/TIFF/early"

        cmd = "{0} -r -nd -P {1} --limit-rate=20000k --user={2} --password={3} --content-on-error {4}".format(
            wget_path,
            self.donwload_folder + "/" + ftype,
            self.userInfo,
            self.userpass,
            self.url + filenames,
        )
        QMessageBox.information(
            None,
            "get GPM file",
            cmd,
        )
        subprocess.call(cmd, shell=True)

    def __get_julian_date(self) -> str:
        # 주어진 연도, 월, 일로 날짜 객체 생성
        date = datetime(int(self.year), int(self.month), int(self.day))
        # 줄리안 날짜 계산: 1월 1일부터의 일 수
        julian_date = date.timetuple().tm_yday
        julian_date_str = str(julian_date).zfill(3)
        return julian_date_str
