# MicroCloudChip
<img src="app/static/app/img/logo.png" width="200"><br>
![language](https://img.shields.io/badge/python-3.9.0-blue?style=flat-square)
![framework](https://img.shields.io/badge/django-3.1.4-yellowgreen?style=flat-square)
![os](https://img.shields.io/badge/OS-Linux-blueviolet?style=flat-square)
![platform](https://img.shields.io/badge/platform-Docker-informational?style=flat-square)<br>
![GitHub release (latest by date)](https://img.shields.io/github/v/release/SweetCase-BakHwa-Project/MicroCloudChip?style=flat-square)
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/SweetCase-BakHwa-Project/MicroCloudChip?label=pre-release&style=flat-square)
![status](https://img.shields.io/badge/status-Alpha_Test-important?style=flat-square)

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
>   ### As User 
>   * 반드시 Linux 환경에 Docker가 설치되어있어야 합니다.(Windows에도 작동이 가능하나 일부 기능에 Root관련 문제로 에러가 발생할 수 있습니다.)
>   >```shell
>   >$ sudo docker run -it -d -p 8000:8000 --name [아무거나] recomadock/microcloudchip:0.0.2
>   [참고](https://hub.docker.com/r/recomadock/microcloudchip/tags?page=1&ordering=last_updated)
>   * 정상적으로 완료되었으면 chrome으로 hostname:8000/microcloudchip로 접속하면 사용 가능합니다.
* 
>   ### As Developer
>   * Localhost에서 개발하는 케이스를 위주로 설명하였습니다.
>   * As User처럼 Linux환경(또는 wsl)에서만 가능합니다.
>   >```shell
>   >$ git clone https://github.com/SweetCase-BakHwa-Project/MicroCloudChip.git
>   >$ cd MicroCloudChip/app/app
>   >$ vim config.json
>   >```
> config.json은 최상위 루트를 정할 때 사용되므로 원하는 루트로 수정합니다.
> <br>수정을 마쳤으면 아래와 같이 명령어를 입력합니다.
>   >```shell
>   >$ cd .. (in ~/MicroCloudChip/app)
>   >$ sh refresh.sh
>   >$ python manage.py runserver
>   >```
>   * 정상적으로 작동이 되었으면 chrome으로 localhost:8000/microcloudchip으로 접속이 가능합니다.
* * *
## 업데이트 예정인 항목
* v0.1.0
    * docker run으로 어플리케이션을 실행 할 때 최상위 루트를 사용자가 직접 정의할 수 있게 구현
    * port나 ip범위도 docker run으로 실행할 때 수정할 수 있게 구현
* v0.2.0
    * 시스템 정보 추가(Watcher 기능)
        * 전체 사용중인 용량 확인
        * 최대로 사용할 수 있는 용량 확인
        * 현재 로그인 되어 있는 User 확인
* v0.3.0
    * 파일 접근 권한 규칙 도입
        * Linux 처럼 user, other로 나뉜다.
        * 파일일 경우 download, delete 권한이 있으며
        * 디렉토리일 경우 download, upload, delete 세 가지의 권한이 존재하게 된다.
* * *
* 아직 Alpha Version이라 bug가 많습니다. 오류 발생시 issue탭에 추가해 주시면 차기 업데이트에 해당 항목을 추가하겠습니다.
