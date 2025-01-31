# -*- coding: utf-8 -*-
"""
Created on 2018. 10. 6.

wget bat script class

change log =  2019-01-02 : ftp 경로 수정

@author: MH.CHO
"""

import ftplib
import getpass
import os
import sys
import urllib.request
from datetime import datetime, timedelta

import requests
from PyQt5.QtWidgets import QProgressBar

sys.path.insert(0, os.path.dirname(os.path.realpath(__file__)) + "/Lib/data_download")

username = getpass.getuser()
wget_path = os.path.dirname(os.path.abspath(__file__)) + "/Lib/wget.exe"
wget_path = wget_path.replace(username, '"' + username + '"')
output = "'"


def connected_to_internet(url, timeout=5):
    try:
        print(requests.get(url, timeout=timeout).status_code)
        if requests.get(url, timeout=timeout).status_code == 404:
            return False
        else:
            return True
    except requests.ConnectionError:
        return False


# 폴더 생성
def folder_create(path):
    if not os.path.exists(path):
        os.mkdir(path, exist_ok=True)


def ftp_filename_get(char, url, userid, userpw, start, fileFormat):
    #     output = os.getenv('USERPROFILE') + '\\Desktop\\' + "{0}_data_download.listing".format(str(char))
    #     print start]
    try:
        ftp = ftplib.FTP(url.split("/")[0])
        #     # ftp = ftplib.FTP_TLS()
        #     ftp.set_debuglevel(2)
        ftp.login(userid, userpw)

        dir = (
            (str(url.split("/")[1:]).replace("', '", "/")).replace("['", "")
        ).replace("']", "")
        ftp.cwd(dir)
        if char.lower() == "cmorph":
            #         print "{0}/{1}/".format(str(start.strftime('%Y')), str(start.strftime('%Y%m')))
            ftp.cwd(
                "{0}/{1}/".format(
                    str(start.strftime("%Y")), str(start.strftime("%Y%m"))
                )
            )
        #         ftp.cwd("{0}/{1}/".format("{0}/{1}/".format(str(start.strftime('%Y'))), str(start.strftime('%Y%m'))))
        elif char.lower() == "gpm":
            # HDF5
            ftp.cwd("{0}/".format((start.strftime("%Y%m"))))
            # ftp.cwd("{0}/{1}/.format((start.strftime))")
            # TIFF
        #         ftp.cwd("{0}/{1}/".format(str(start.strftime('%Y')),str(start.strftime('%m'))))
        elif char.lower() == "gsmap":
            ftp.cwd(
                "{0}/{1}/{2}/".format(
                    str(start.strftime("%Y")),
                    str(start.strftime("%m")),
                    str(start.strftime("%d")),
                )
            )

        data = []

        ftp.dir(data.append)

        #     file = open(output,'w+')
        filename = []
        for line in data:
            if start.strftime("%Y%m%d") in line.split()[8]:
                if fileFormat == "tif":
                    if "30min.tif" in line.split()[8]:
                        filename.append(line.split()[8])
                else:
                    #             file.write(line.split()[8])
                    # CMORPH, HDF5는 이거 사용함
                    filename.append(line.split()[8])
        #             break
        #         filename.append(line.split()[8])
        #     file.close()
        ftp.close()

        return filename
    except Exception as exc:
        print("exc", exc)
        return str(exc)


# NASA GPM DATA DOWNLOAD
def create_bat_script(Id, Pw, start, end, folder, fileFormat, dowload_type, HDForTiff):
    # def create_bat_script(Id,Pw,start,end):
    #     output = os.getenv('USERPROFILE') + '\\Desktop\\' + "GPM_data_download.bat"
    #     ftp_user = "jh-kim@kict.re.kr"
    #     ftp_pass = "jh-kim@kict.re.kr"
    ftp_user = str(Id)
    ftp_pass = str(Pw)

    # ==================
    # ftp_url ="ftp://jsimpson.pps.eosdis.nasa.gov/data/imerg/late/" #2018-12-26 메일에서 late 사용으로 변경됨.
    # ftp_url ="http://jsimpson.pps.eosdis.nasa.gov/data/imerg/late/" #2018-12-26 메일에서 late 사용으로 변경됨.

    # hdf5 , tif 둘 다 다운로드 경로가 맞는지 확인 바람... nasa에서 주소를 변경했음.
    # 이제 FTP 안되고 HTTP로만 가능함.
    # hdf5 format download
    # early
    # https://jsimpsonhttps.pps.eosdis.nasa.gov/imerg/early/

    # late
    # https://jsimpsonhttps.pps.eosdis.nasa.gov/imerg/late/

    # tif 포맷 다운로드 주소
    # late
    # https://jsimpsonhttps.pps.eosdis.nasa.gov/imerg/gis/

    # early
    # https://jsimpsonhttps.pps.eosdis.nasa.gov/imerg/gis/early/

    if HDForTiff == "HDF5":
        if dowload_type == "Early":
            # ftp_url = "https://jsimpsonhttps.pps.eosdis.nasa.gov/imerg/early/"
            # url = "jsimpsonhttps.pps.eosdis.nasa.gov/imerg/early/"
            ftp_url = (
                "https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHHE.07/"
            )
            url = "gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHHE.07/"
        else:  # late
            # ftp_url = "https://jsimpsonhttps.pps.eosdis.nasa.gov/imerg/late/"
            # url = "jsimpson.pps.eosdis.nasa.gov/data/imerg/late/"
            ftp_url = (
                "https://gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHHL.07"
            )
            url = "gpm1.gesdisc.eosdis.nasa.gov/data/GPM_L3/GPM_3IMERGHHL.07/"
    else:
        # TIFF file?
        if dowload_type == "Early":
            ftp_url = "https://jsimpsonhttps.pps.eosdis.nasa.gov/imerg/gis/early/"
            url = "jsimpsonhttps.pps.eosdis.nasa.gov/imerg/early/"
        else:
            ftp_url = "https://jsimpsonhttps.pps.eosdis.nasa.gov/imerg/gis/"
            url = "jsimpson.pps.eosdis.nasa.gov/data/imerg/late/"
    # url="jsimpson.pps.eosdis.nasa.gov/data/imerg/"
    # url="jsimpson.pps.eosdis.nasa.gov/data/imerg/late/"

    # ==================
    list = []
    arg = ""
    #     daylist = []
    start = datetime.strptime(start, "%Y-%m-%d").date()
    days = datetime.strptime(end, "%Y-%m-%d").date() - start

    #     output = os.getenv('USERPROFILE') + '\\Desktop\\' + "{0}_data_download.listing".format("gpm")
    # 박사님이 뭐 다운로드 됐는지 리스트 보고 싶다 하심.
    output = folder + "/{0}_data_download.listing".format("gpm")
    if os.path.exists(output):
        os.remove(output)
    file_listing = open(output, "w+")

    for i in range(days.days + 1):
        #         if len(str(start.month)) == 1:
        #             month = "0"+ str(start.month) # mm
        #         else:
        #             month =str(start.month)
        #         https://ftp.cpc.ncep.noaa.gov/precip/CMORPH_V1.0/CRT/0.25deg-3HLY/2011/201106/
        # file = ftp_filename_get("gpm", url, ftp_user, ftp_pass, start, fileFormat)
        file = ftp_filename_get("gpm", url, ftp_user, ftp_pass, fileFormat)

        for filename in file:
            file_listing.write(filename + "\n")

            #             #=============
            path = ftp_url + "{0}/".format(str(start.strftime("%Y%m"))) + filename
            path = ftp_url + "{0}/".format(str(start.strftime("%Y"))) + filename
            if os.path.exists(folder + "/GPM/" + filename):
                pass
            else:
                arg = (
                    wget_path
                    + ' -r -nd -P "' '{0}" '.format(folder + "/GPM/")
                    + "--limit-rate=20000k --ftp-user={0} --ftp-password={1} --content-on-error {2}".format(
                        ftp_user, ftp_pass, (path)
                    )
                )
                list.append(arg)

        start = start + timedelta(days=1)

    file_listing.close()
    return list


# Id,Pw,start,end
# create_bat_script("mhcho058@hermesys.co.kr","mhcho058@hermesys.co.kr","2019-05-22","2019-05-31","D:/Working/Gungiyeon/GPM/GPM_test/T20190723/0_download")


# CMORPH DATA DOWNLOAD
def cmorph_data_download(
    start: str, end: str, folder: str, time: str, progressbar: QProgressBar
):
    start = datetime.strptime(start, "%Y-%m-%d").date()
    days = datetime.strptime(end, "%Y-%m-%d").date() - start
    total_days = days.days + 1

    # Set base URL based on time resolution
    if time == "30min":
        base_url = "https://www.ncei.noaa.gov/data/cmorph-high-resolution-global-precipitation-estimates/access/30min/8km/"
        files_per_day = 24
        file_format = (
            "CMORPH_V1.0_ADJ_8km-30min_{year}{month:02d}{day:02d}{hour:02d}.nc"
        )
    else:  # 1hr
        base_url = "https://www.ncei.noaa.gov/data/cmorph-high-resolution-global-precipitation-estimates/access/hourly/0.25deg/"
        files_per_day = 24  # 24 files for hourly resolution
        file_format = (
            "CMORPH_V1.0_ADJ_0.25deg-HLY_{year}{month:02d}{day:02d}{hour:02d}.nc"
        )

    # Calculate total number of files for progress bar
    total_files = total_days * files_per_day
    progressbar.setMaximum(total_files)
    current_file = 0

    # Create folder if it doesn't exist
    folder_create(folder)

    current_date = start
    while current_date <= start + days:
        # Create year/month/day folder structure
        date_folder = (
            f"{current_date.year}/{current_date.month:02d}/{current_date.day:02d}"
        )
        full_url = f"{base_url}{date_folder}/"
        save_folder = folder + "/" + date_folder

        # print(save_folder)

        os.makedirs(save_folder, exist_ok=True)

        # Download files for each time step
        if time == "30min":
            for hour in range(24):
                filename = file_format.format(
                    year=current_date.year,
                    month=current_date.month,
                    day=current_date.day,
                    hour=hour,
                )
                file_url = f"{full_url}{filename}"
                save_path = os.path.join(save_folder, filename)

                try:
                    if not os.path.exists(save_path):
                        urllib.request.urlretrieve(file_url, save_path)
                except Exception as e:
                    print(f"Error downloading {filename}: {str(e)}")

                current_file += 1
                progressbar.setValue(current_file)
        else:  # 1hr
            for hour in range(24):
                filename = file_format.format(
                    year=current_date.year,
                    month=current_date.month,
                    day=current_date.day,
                    hour=hour,
                )
                file_url = f"{full_url}{filename}"
                save_path = os.path.join(save_folder, filename)

                try:
                    if not os.path.exists(save_path):
                        urllib.request.urlretrieve(file_url, save_path)
                except Exception as e:
                    print(f"Error downloading {filename}: {str(e)}")

                current_file += 1
                progressbar.setValue(current_file)

        current_date += timedelta(days=1)

    progressbar.setValue(total_files)


# GSMap DATA DOWNLOAD
def GSMap_data_download(Id, Pw, start, end, folder, fileformat):
    print(Id, Pw)
    ftp_url = "ftp://{0}:{1}@hokusai.eorc.jaxa.jp/standard/v8/hourly/".format(Id, Pw)
    url = "hokusai.eorc.jaxa.jp/standard/v8/hourly/"
    list = []
    arg = ""

    start = datetime.strptime(start, "%Y-%m-%d").date()
    days = datetime.strptime(end, "%Y-%m-%d").date() - start

    output = folder + "/{0}_data_download.listing".format("GSMap")
    file_listing = open(output, "w+")
    for i in range(days.days + 1):
        file = ftp_filename_get("gsmap", url, Id, Pw, start, fileformat)

        for filename in file:
            #             print (filename)
            file_listing.write(filename + "\n")
            path = ftp_url + "{0}/{1}/{2}/{3}".format(
                str(start.strftime("%Y")),
                str(start.strftime("%m")),
                str(start.strftime("%d")),
                filename,
            )
            if os.path.exists(folder + "/GSMap/" + filename):
                pass
            else:
                arg = wget_path + ' -r -nd -P "' '{0}" '.format(
                    folder + "/GSMap/"
                ) + "--limit-rate=20000k {0}".format(path)
            #                 print (arg)
            #                 os.system(arg)
            list.append(arg)
        #                 print (arg)
        #                 os.system(arg)
        start = start + timedelta(days=1)
    file_listing.close()
    return list
