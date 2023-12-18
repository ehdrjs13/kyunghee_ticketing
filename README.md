
# 서울고등학교 경희제 외부인 통합 관리 체계
### (Integrated Visitor Management System, IVMS)


서울고등학교 경희제 외부인 통합 관리 체계(이하 IVMS)는 
입장객 수요를 관리하여 안전사고 방지 등의 효과를 얻기 위해 제작되었습니다.


IVMS는 입장객의 티켓을 스캔하여 데이터를 출력하는 FrontEnd와 
입장객들의 개인정보 데이터베이스를 기반으로 실질적인 데이터 처리를 담당하는 BackEnd,
그리고 엑셀 데이터를 가공하여 필요한 형식으로 변환하고 티켓을 생성하는 데이터 전처리 파트로 나뉘어 구성됩니다.

이 문서에서는 파트별로 각각 나누어 매뉴얼을 작성하도록 하겠습니다.


## 데이터 전처리


> 포맷에 맞게 신청자 명단을 ` Ticket ` 폴더 내에 ` visitorList.xlsx `(대소문자 주의)로 저장해주세요.



### 티켓 생성


` TicketMaker.py `


실행하면 ` Ticket/saverImg ` 폴더에 티켓 이미지가 저장됩니다.(파일명은 개인 순번으로 저장)


### DB 생성(중요)


` getSQLdb.py `

실행하면 입장객 리스트가 ` visitorlist.db `로 저장됩니다.



## FrontEnd


> 시작 전 API 서버의 ip주소를 확인하고, 이에 맞게 ` requests.get() `의 url을 수정해주세요.


` init.py `


해당 파일을 실행하게 되면 OpenCV 카메라 창이 열리며 QR스캔이 가능한 상태가 됩니다. 
입장권의 QR코드를 스캔하고, 만약 해당 코드가 유효하다면 알림음과 함께 해당 학생의 학적과 개인 코드가 콘솔로 출력됩니다.


입장객의 코드가 유효하지 않은 경우에는 긴 비프음이 울리며 붉은 글씨의 에러 메시지가 뜨게 됩니다.

` ERROR:이미 사용된 입장권입니다. `  : 티켓이 이미 입장 처리되어 중복 입장 처리되는 경우
 
` ERROR:올바른 형태의 데이터가 아닙니다. ` : QR코드의 데이터 형식이 올바른 형식(GateNumSchool)이 아닌 경우


중복 입장 에러가 DB오류로 비정상적으로 발생한 경우, BackEnd 부분의 중복 처리 복구 매뉴얼을 참조하시면 됩니다.


` init(legacy).py `


레거시 버전을 사용하면 서버와의 네트워크 문제가 발생했을 때 내장 데이터베이스만을 이용해 데이터를 처리합니다.
이때는 티켓 중복처리확인이 불가하므로, 상단의 ` init.py `가 서버 문제로 사용 불능 상태가 되었을 때의 최후의 수단으로서만 이용하시기 바랍니다.



## BackEnd


> 데이터 전처리의 DB생성 매뉴얼을 참고해서 ` visitorlist.db `를 생성하세요.

### 서버 가동


` server.py `


실행하면 API 서버가 가동됩니다. 


(모든 입장/복구는 ` Server.Log/app.log `에 요청 발생 시간과 함께 기록됩니다.)

### 입장 처리


` /mainEntrial/<id>(개인 코드) `


해당 id에 해당하는 학생의 개인정보를 ` json ` 형식으로 반환하고, 해당 학생에 입장 처리를 하여 중복 입장을 방지합니다.


### 중복 처리 복구(중요)


` /recovery/<id>(개인 코드) `


비정상적인 입장 처리가 발생할 경우 해당 학생의 중복 입장 방지 인디케이터(Check)를 0으로 초기화합니다.
외부인 입장 과정 중 명의 도용 등으로 인해 실제 신청된 사람이 입장에 어려움을 겪을 수 있습니다. 

이때 학생회나 지도 교사는 해당 복구 엔드포인트를 사용하여 해당 학생의 중복 입장 값을 초기화할 수 있습니다.



## Memo (Issue)
> 학교노트북에서 init.py 실행시 zbar 모듈서 libzbar-64.dll 누락 문제 해결 필요---c++2013ver 설치
>
> Linux 기반 pc에서 frontend 실행시 실행 도중 카메라 오류로 server에서 none 반환 오류--> nonetype 예외처리로 해결예정, frontend는 무조건 윈도우로 구성하기
