# -*- coding: utf-8 -*-
import http.cookiejar
import os
import re
import subprocess
import urllib.request
from datetime import datetime, timedelta

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
        gpm_type,
        donwload_folder,
        timeLabel_type,
        progressbar,
    ):
        self.url = "https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3"
        self.userInfo = userInfo
        self.getFiledate_1 = getFiledate_1
        self.gpm_type = gpm_type
        self.donwload_folder = donwload_folder
        self.timeLabel_type = timeLabel_type.upper()
        self.days = 0
        self.getFiledate = ""
        self.userpass = userpass
        self.progressbar = progressbar

        # Split username and password
        self.username, self.password = userInfo, userpass

        if self.timeLabel_type == "KST":
            if getFiledate_1 == getFiledate_2:
                self.days = 0
            else:
                self.days = (
                    datetime.strptime(getFiledate_2, "%Y-%m-%d").date()
                    - datetime.strptime(getFiledate_1, "%Y-%m-%d").date()
                ).days
                self.main()

        # UTC 단위
        if self.timeLabel_type == "UTC":
            if getFiledate_1 == getFiledate_2:
                self.days = 0
            else:
                self.days = (
                    datetime.strptime(getFiledate_2, "%Y-%m-%d").date()
                    - datetime.strptime(getFiledate_1, "%Y-%m-%d").date()
                ).days

            # Convert dates to required format (YYYYMMDD)
            start_date = datetime.strptime(getFiledate_1, "%Y-%m-%d").strftime("%Y%m%d")
            end_date = datetime.strptime(getFiledate_2, "%Y-%m-%d").strftime("%Y%m%d")

            # Generate URLs for the date range
            urls = self.generate_gpm_urls(start_date, end_date)
            self.main(urls)

    def generate_gpm_urls(self, start, end):
        """
        Generate URLs for GPM files between start and end dates
        """
        # TODO: type에 따라 URL 나누기
        base_url = f"{self.url}/{self.gpm_type}"
        urls = []

        # Convert string dates to datetime objects
        start = datetime.strptime(start, "%Y%m%d")
        end = datetime.strptime(end, "%Y%m%d")

        current_date = start
        while current_date <= end:
            # GPM data is available every 30 minutes (48 files per day)
            index = 0  # Start index for each day (0000, 0030, 0060, ...)

            for hour in range(24):
                for minute in [0, 30]:
                    # Format the date and time components
                    year = current_date.strftime("%Y")
                    doy = current_date.strftime("%j")
                    date_str = current_date.strftime("%Y%m%d")

                    # Create the filename
                    start_time = f"{hour:02d}{minute:02d}00"

                    # Calculate end time properly
                    if minute == 0:
                        end_hour = hour
                        end_minute = 29
                    else:
                        end_hour = hour
                        end_minute = 59

                    end_time = f"{end_hour:02d}{end_minute:02d}59"

                    # Format index as 4 digits (0000, 0030, 0060, ...)
                    index_str = f"{index:04d}"
                    postfix = (
                        ""
                        if self.gpm_type == "GPM_3IMERGHH.07"
                        else "-E"
                        if self.gpm_type == "GPM_3IMERGHHE.06"
                        else "-L"
                    )

                    filename = f"3B-HHR{postfix}.MS.MRG.3IMERG.{date_str}-S{start_time}-E{end_time}.{index_str}.V07B.HDF5"

                    # Construct the full URL
                    url = f"{base_url}/{year}/{doy}/{filename}"
                    urls.append(url)

                    # Increment index by 30 for next file
                    index += 30

            current_date += timedelta(days=1)

        return urls

    def download_gpm_file(self, url):
        """
        Download GPM file from NASA GESDISC using urllib with cookie handling
        """
        if not os.path.exists(self.donwload_folder):
            os.makedirs(self.donwload_folder)

        filename = url.split("/")[-1]
        output_path = os.path.join(self.donwload_folder, filename)

        try:
            # Create a password manager and cookie jar
            password_mgr = urllib.request.HTTPPasswordMgrWithDefaultRealm()
            password_mgr.add_password(
                None, "https://urs.earthdata.nasa.gov", self.username, self.password
            )

            # Create cookie jar and handlers
            cookie_jar = http.cookiejar.CookieJar()
            cookie_handler = urllib.request.HTTPCookieProcessor(cookie_jar)
            password_handler = urllib.request.HTTPBasicAuthHandler(password_mgr)

            # Build opener with both handlers
            opener = urllib.request.build_opener(cookie_handler, password_handler)

            # Install the opener
            urllib.request.install_opener(opener)

            # Download the file
            print(f"Downloading {filename}...")
            request = urllib.request.Request(url)
            with opener.open(request) as response:
                with open(output_path, "wb") as out_file:
                    out_file.write(response.read())
            print(f"Downloaded {filename} successfully")
            return True

        except Exception as e:
            print(f"Error downloading file: {str(e)}")
            return False

    def main(self, urls):
        count = 0
        total_files = len(urls)
        self.progressbar.setMaximum(total_files - 1)
        QApplication.processEvents()

        for index, url in enumerate(urls):
            if self.timeLabel_type == "UTC":
                self.progressbar.setValue(index)
                success = self.download_gpm_file(url)
                if success:
                    count += 1
                QApplication.processEvents()

        QMessageBox.information(
            None,
            "GPM Download ",
            f"Download Complete. {count} files downloaded. {total_files - count} files failed to download.",
        )

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
