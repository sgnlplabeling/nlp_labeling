# 레이블링 과제 API

글쓴이: 우종성 (jongseong.w@diquest.com)

이 문서는 레이블링 과제(IITP 43세부과제)를 위해 개발한
관리도구-레이블링엔진 연동 API의 사용법에 관한 것입니다.


## 사용법

필요한 파일

1. labelproj_api.jar


### 1. 자동 레이블링

```java
Labeler.getInstance(RECORD_ID, RECORD_SEQ, DOC_ID).label();
```

#### 진행 단계별 DB 히스토리

1. JOB_HISTORY 테이블, 데이터 삽입.
2. RECORD 테이블, RABEL_STAT 필드값 "처리중"으로 변경.
3. ANNOTATION 테이블, 데이터 삽입.
4. RECORD 테이블
  1. RABEL_STAT 필드값 "자동"으로 변경.
  2. RECORD_SEQ 필드값 1 증가.
5. 1. JOB_HISTORY 테이블, 데이터 삽입.


### 2. 학습 데이터 생성

```java
TrainSetSaver saver = new TrainSetSaver(RECORD_ID, RECORD_SEQ);
saver.save();
```

#### 진행 단계별 DB 히스토리

1. JOB_HISTORY 테이블, 데이터 삽입.
2. RECORD 테이블, LEARN_STAT 필드값 "처리중"으로 변경.
3. RECORD 테이블, LEARN_DATA 업데이트. (생성된 학습데이터)
4. RECORD 테이블, LEARN_STAT 필드값 "자동"로 변경.
5. JOB_HISTORY 테이블, 데이터 삽입.
