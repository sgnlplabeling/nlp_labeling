package com.diquest.lltp.domain;

import lombok.Data;

@Data
public class AnnotationVo extends CommonVo {
	private int id;
	private int recordId;
	private int recordSeq;
	private String annId;
	private String name;
	private String startPoint;
	private String endPoint;
	private String content;
	
	private String keyword;
	private int count;
}
