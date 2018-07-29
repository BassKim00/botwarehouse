# botwarehouse

간단히 작성하자면

virtualen 설치 및 가상환경 접속

virtualenv -p python3 venv 

source venv/bin/activate

필요한 라이브러리 설치

pip install requirements.txt

모델 마이그레이션 (디비 클라우드에 올려야 할듯 한번에 끝내려면)

python manage.py migrate

엑셀 데이터 디비 인서트(중복 체크 안하므로 한번에 올리던가 해야함)
(엑셀 타이틀 변경해서 한번씩 실행 할 것.)

python stock/data/excel_data.py
