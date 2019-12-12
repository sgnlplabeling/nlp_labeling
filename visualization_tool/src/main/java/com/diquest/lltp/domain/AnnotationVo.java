package com.diquest.lltp.domain;

import java.text.NumberFormat;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class AnnotationVo extends CommonVo {
	
	/**
	 * annotation 고유 ID
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
	 * annotation 이름
	 */
	private String annId;
	
	/**
	 * entity 혹은 relation 이름
	 */
	private String name;
	
	/**
	 * 시작 지점
	 */
	private String startPoint;
	
	/**
	 * 끝 지점
	 */
	private String endPoint;
	
	/**
	 * 내용
	 */
	private String content;
	
	/**
	 * 카운트
	 */
	private Integer count;
	
	/**
	 * 
	 * BRAT에 들어가는 ann파일 내용.
	 * */
	private String bratContents;
	
	
	private double subCount;

	private String subCntFmt;
	
	public void setSubCount(Double subCount) {
		this.subCount = subCount;
		setSubCntFmt();
	}
	
	
	public void setSubCntFmt() {
		subCntFmt = NumberFormat.getInstance().format(subCount);
	}
	
	
	public String getSubCntFmt() {
		return subCntFmt;
	}
}
