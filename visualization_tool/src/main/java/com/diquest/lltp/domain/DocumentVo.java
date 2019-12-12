package com.diquest.lltp.domain;

import java.sql.Timestamp;
import java.util.List;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class DocumentVo extends CommonVo {
	
	/**
	 * 문서 고유 ID
	 */
	private int docId;
	
	/**
	 * collection 고유 ID
	 */
	private int colId;
	
	/**
	 * record 고유 ID
	 */
	private int recordId;
	
	/**
	 * 경로
	 */
	private String path;
	
	/**
	 * 문서 제목
	 */
	private String subject;
	
	/**
	 * 문서 내용
	 */
	private String content;
	
	/**
	 * 등록자 ID
	 */
	private String regId;
	
	/**
	 * record 시퀀스
	 */
	private String recordSeq;
	
	/**
	 * 최근 record 시퀀스
	 */
	private String lastRecordSeq;
	
	/**
	 * 작업 확인자 ID
	 */
	private String confId;
	
	/**
	 * 레이블링 상태
	 */
	private String rabelStat;
	
	/**
	 * 레이블링 등급
	 */
	private String labelGrade;
	
	/**
	 * 학습 상태
	 */
	private String learnStat;
	
	/**
	 * 학습 데이터
	 */
	private String learnData;
	
	/**
	 * 문서 갯수
	 */
	private int count;
	
	/**
	 * record 리스트
	 */
	private List<DocumentVo> recordList;

	/**
	 * 작업 확인 날짜
	 */
	private Timestamp confDate;
	
	/**
	 * 등록 날짜
	 */
	private Timestamp regDate;
	
	/**
	 * 최종 작업 날짜
	 */
	private Timestamp lastDate;
	
	private String date;
	
}
