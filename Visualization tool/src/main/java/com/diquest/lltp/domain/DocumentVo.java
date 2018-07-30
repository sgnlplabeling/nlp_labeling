package com.diquest.lltp.domain;

import java.util.Date;
import java.util.List;

import org.springframework.web.multipart.MultipartFile;

import lombok.Data;

@Data
public class DocumentVo extends CommonVo {
	private int docId;
	private int colId;
	
	private String path;
	private String subject;
	private String content;
	private String regId;
	private Date regDate;
	private Date lastDate;
	
	private int recordId;
	private String recordSeq;
	private String lastRecordSeq;
	
	private String confId;
	private Date confDate;
	private String rabelStat;
	private String labelGrade;
	private String learnStat;
	private String learnData;
	
	private int count;
	private MultipartFile [] file;
	private List<DocumentVo> recordList;
	
	private String keyword;
}
