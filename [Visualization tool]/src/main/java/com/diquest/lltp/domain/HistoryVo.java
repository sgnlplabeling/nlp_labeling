package com.diquest.lltp.domain;

import java.util.Date;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class HistoryVo extends CommonVo {
	
	/**
	 * 히스토리 고유 ID
	 */
	private Integer id;
	
	/**
	 * record 고유 ID
	 */
	private Integer recordId;
	
	/**
	 * record 시퀀스
	 */
	private Integer recordSeq;
	
	/**
	 * 작업 유형
	 */
	private String type;
	
	/**
	 * 작업 구분
	 */
	private String job;

	/**
	 * 비고
	 */
	private String regId;
	
	/**
	 * 등록 날짜
	 */
	private Date regDate;
	
	/**
	 * 제목
	 */
	private String subject;
	
	private String note;
}
