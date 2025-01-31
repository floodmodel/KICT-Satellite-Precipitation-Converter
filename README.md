# KICT Satellite Precipitation Converter
* **2022년 12월 현재 제공하는 plug-in은 QGIS3.22(QGIS 3.22.14 LTR 기준)에서 시범운영중입니다..** <br/>

  
#### Update History
	KICT Satellite Precipitation Converter In QGIS 3

	v0.0.66
		: qgis 3.22 이상 버전에서 사용 가능하도록 코드 수정됨
		: data downlod 기능 - 날짜 형식을 고정시킴
		: network check 코드 수정

	v0.1.1 이후는 여기를 참고해 주십시요
		: https://github.com/floodmodel/Converter/releases

<details>
<summary>Last Change Log</summary>
<div markdown="1">
	
	v0.0.3 - progress bar 추가, hdf5 to convert 수정, Accum 기능, 체크박스로 ui 수정, Make CSV 기능 및 ui 수정
	v0.0.4 - 일부 output path 텍스트 박스 Enable 상태 변환(임의 경로 입력 방지)
	v0.0.5 - clip 메뉴, 파일 선택(TIFF) 기능 추가(기존 : 필수 HDF to convert 기능 수행 후 CLIP 사용, 변경 : 바로 CLIP 기능 사용 가능하도록 조치)
	v0.0.6
		TITLE 변경
		MAKE ASC 진행률 바 추가됨.
	
	v0.0.7
		CLIP ZONE 추가(KOREA TYPOON)
		csv fieldname 없으면 msg 출력 수행X
		clip 선택 실행 에러 있음. 그거는 csv 후에 진행
	
	v0.0.8
		gdal path 변경
	
	v0.0.9
		QgsMessageLog(CLIP) 추가
	v0.0.10
		clip 존 별 폴더 생성
		gdal.exe 미작동.. 패스 변경
		hdf5 메시지 오류 수정함.
	
	v0.0.11
		gdal_path 변경
	
	v0.0.12
		MAKE CSV - SHP FieldName 대소문자 구분제거
		gdal_path 오류 수정
	
	v0.0.13
		Data Download - default 날짜 변경,배치파일 생성 메시지 추가, 배치파일 날짜 이상 해소
		HDF5 To Convert - list 목록 선택 기능 제거, 생성결과 분리 폴더 생성(step1,step2)
		Accum - 계산 식 변경
		
	v0.0.14
		Make Image - make png files 저장 폴더 선택 가능, 리스트 오류 수정
		
	v0.0.15
		Data Download - user 명에 공백 문제를 위한 수행문 수정, 사용자 지정 폴더 추가
		Accum - 리스트 레이어 선택 기능 제거.(리스트에 있는 레이어 모두 수행), 오류 수정
		Satellitecorrection -csv 변경된 포맷으로 변경
		Make image - 글씨 크기 조절
	
	v0.0.16
		Accum - 오류 수정
		완료 파업창 추가 - make csv, Function
	
	v0.0.17
		Satellitecorrection - 오류 수정
		
	v0.0.18
		Make CSV - message 오류 수정
		Satellitecorrection - 플러그인 구동 확인
		
	v0.0.19
		CLIP - Shape FILE CLIP 추가, 사용자 지정 CLIP 추가, 사용자 clip 콤보 박스 추가 가능
	
	v0.0.20
		CLIP - Shape FILE clip 기능에서 polygon type만 허용되도록 수정.
		Make image - png 파일 배경 shape 추가
		
	v0.0.21
		Data Download - early --> late 사용으로 ftp 경로 수정
	
	v0.0.22
		Make image - png 파일 배경 shape 추가, 일부 수정
	
	v0.0.23
		Satellitecorrection - 일부 수정
	
	v0.0.24
		File selection window uniformity.
		ADD KICT Marker
		File select dir fixed("C://")
		Data Download - Add User ID/PW input text window
		CLIP - partial modification
		Satellitecorrection - partial modification
		
	v0.0.25
		TOTAL = Path 보완
		Accum - argument 보완
		
	v0.0.26
		Make Image - Base Shape layer 
		
	v0.0.27
		Data Download - cmorph 데이터 다운로드(0.25deg, 3hr), UI 변경
		
	v0.0.28
		Data Download - CMORPH 데이터 다운로드 경로 오류 수정.
		(https://ftp.cpc.ncep.noaa.gov/precip/CMORPH_V1.0/CRT/0.25deg-3HLY/)
		
	v0.0.29
		기능 명 변경 : HDF5_Convert --> Convert_to_TIFF
		
		Data Download - CMORPH 데이터 다운로드 날짜 오작동 수정
		Convert_to_TIFF - CMORPH 데이터 변환	
			
	v0.0.30
		Convert_to_TIFF - CMORPH 데이터 변환 일부 수정됨
		
	v0.0.31
		플러그인 Name 개명(GPM >>> Kict_Satellite_Precipitation_Converter)
		CLIP - clip zone [ korea ] 영역 범위 수정
		
	v0.0.32
		Data Download - 프로그레스 바 추가, batch 파일 실행 방식이 아닌 자동 다운로드 방식으로 변경
		CLIP - clip zone [North_korea] 추가
	
	v0.0.33
		Data Download - 다운받을 파일의 목록 .listing 파일 바탕화면에 생성
		Make image - step1 | step2 폴더 분리, step1은 일반 이미지,step2 는 shape 파일 중첩 이미지
		
	v0.0.34
		하단 로고 이미지 변경
		
	v0.0.35
		Convert To Tiff - CMORPH Converter 갱신
		Make image - PNG 이미지 배경 여백 축소
		
	v0.0.36
		Convert To Tiff - 기능 개선
		Accum - 인식 오류 문제 확인
	
	v0.0.37
		Convert To Tiff - CMORPH 변환 기능 Patch
		Make image - polygon 외곽선 색 변경 가능
		
	v0.0.38
		: Data Download -  ADD Data GSMap
		: Convert to TIFF - Convert GSMap to TIFF
		: Make CSV - Add ComboBox FieldName
		: Accum - ADD GSMap
		: Make Image - change color polygon, polyline, change symbol point 
	
	v0.0.39
		: Convert to TIFF - Normalize Convert HDF5 to TIFF 
		: Accum - (CMORPH, GSMap) Modification of Cumulative Rainfall Calculation
		
	v0.0.40
		: Make Image - Some modify, create GIF Filename
	
	v0.0.41
		: Accum - Modify Path (SAGA.cmd, OSGeo4W.bat)
</div>
</details>
