# GPM
### Change Log

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
