### **프로젝트 실행 방법**

#### **1. 깃허브 저장소 클론**
아래 명령어를 사용하여 프로젝트를 클론합니다.
```bash
git clone https://github.com/appjam-29th/app-pick-server.git
cd app-pick-server
```


#### **2. Docker Desktop 설치 및 로그인**
1. [Docker 공식 사이트](https://www.docker.com/products/docker-desktop/)에서 Docker Desktop을 설치합니다.
2. 설치 후 터미널에서 Docker에 로그인합니다.
```bash
docker login
```


#### **3. 프로젝트 빌드 (.jar 생성)**
아래 명령어를 실행하여 `.jar` 파일을 빌드합니다.
```bash
./gradlew build
```
> 📌 Windows 환경에서는 `gradlew.bat build` 실행


#### **4. Docker 이미지 빌드**
Dockerfile이 있는 디렉토리에서 아래 명령어를 실행합니다.
```bash
docker build -t apppick-server:latest .
```


#### **5. Docker Compose 빌드**
Docker Compose를 사용하여 애플리케이션을 빌드합니다.
```bash
docker-compose build
```

#### **6. Docker Compose 실행**
컨테이너를 실행합니다.
```bash
docker-compose up -d
```
> 📌 `-d` 옵션은 백그라운드에서 실행되도록 설정합니다.


### **API 명세서**
- [API 문서 확인](https://educated-drifter-2d6.notion.site/998bf018e107493cb9fc6c687cd245ce?v=40a1d0b5ac7d4e259604854079c506bf&pvs=4)

> 📌 API 사용 방법 및 상세 내용은 명세서를 참고하세요.
