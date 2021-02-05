# MicroCloudChip
<img src="app/static/app/img/logo.png" width="200"><br>
![language](https://img.shields.io/badge/python-3.9.0-blue?style=flat-square)
![framework](https://img.shields.io/badge/django-3.1.4-yellowgreen?style=flat-square)
![os](https://img.shields.io/badge/OS-Debian-blueviolet?style=flat-square)
![platform](https://img.shields.io/badge/platform-Docker-informational?style=flat-square)
![GitHub](https://img.shields.io/github/license/SweetCase-BakHwa-Project/MicroCloudChip?style=flat-square)<br>
![GitHub release (latest by date)](https://img.shields.io/github/v/release/SweetCase-BakHwa-Project/MicroCloudChip?style=flat-square)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/SweetCase-BakHwa-Project/MicroCloudChip?include_prereleases&label=pre-release&style=flat-square)
![status](https://img.shields.io/badge/status-Alpha1-important?style=flat-square)

<br>

딱 최소한의 기능을 갖춘 NAS Cloud Web Application
* * *
![example](example.PNG)
* * *
## 주요 기능
* 최소한의 클라우드 기능
    * 파일 업로드/다운로드
    * 여러 파일이나 디렉토리를 zip으로 묶어 다운로드 가능
    * 디렉토리 생성 가능
* 계정
    * admin의 권한 하에 계정 관리 가능
* 최초 부팅시 admin의 아이디와 비밀번호는 admin, admin
* * *
## How To run
### As User 
* Docker Container
    * ```shell
        $ sudo docker run -it -d -p 8000:8000 --name [아무거나] -e IP=0.0.0.0 -e PORT=8000 recomadock/microcloudchip:0.2.0
        ```
    * 정상적으로 완료되었으면 chrome으로 hostname:8000/microcloudchip로 접속하면 사용 가능합니다.
    * [참고](https://hub.docker.com/r/recomadock/microcloudchip/tags?page=1&ordering=last_updated)
* Run By Source Code 
    * ```shell
        $ sudo apt install -y vim gcc make zlib1g-dev zlib1g
        $ git clone https://github.com/SweetCase-BakHwa-Project/MicroCloudChip.git
        $ cd MicroCloudChip/bin
        $ perl install.pl
        $ perl run.pl
    ```

* IP, PORT는 선택이며 설정을 하지 않았을 경우의 default값은 0.0.0.0:8000이 됩니다.
### As Developer
* Localhost에서 개발하는 케이스를 위주로 설명하였습니다.
* As User처럼 Linux환경(또는 wsl)에서만 가능합니다.
```shell
$ git clone https://github.com/SweetCase-BakHwa-Project/MicroCloudChip.git
$ cd MicroCloudChip/app/app
$ vim config.json
```
 config.json은 최상위 루트를 정할 때 사용되므로 원하는 루트로 수정합니다.
 <br>수정을 마쳤으면 아래와 같이 명령어를 입력합니다.
```shell
$ cd .. (in ~/MicroCloudChip/app)
$ sh refresh.sh
$ python manage.py runserver
```
* 정상적으로 작동이 되었으면 chrome으로 localhost:8000/microcloudchip으로 접속이 가능합니다.
* * *
## 업데이트 예정인 항목
* v 0.3.0
    * User 항목 추가
        * 새로 생성된 디렉토리 및 파일에 유저 이름 생성
    * deb/rpm 패키지 설치 가능
    * 메인 루트를 사용자가 직접 정할 수 있다.
        * Docker를 이용해 설치 할 경우
* v0.4.0
    * User 정책 도입
        * Linux 처럼 user, other로 나뉜다.
        * 파일일 경우 download, delete 권한이 있으며
        * 디렉토리일 경우 download, upload, delete 세 가지의 권한이 존재하게 된다.
* * *
* 아직 Alpha Version이라 bug가 많습니다. 오류 발생시 issue탭에 추가해 주시면 차기 업데이트에 해당 항목을 추가하겠습니다.
