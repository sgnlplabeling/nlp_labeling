package com.diquest.lltp.domain;

import java.util.Date;

import org.springframework.web.context.request.RequestAttributes;
import org.springframework.web.context.request.RequestContextHolder;

import lombok.Data;

@Data
public class HistoryVo extends CommonVo {
	private int id;
	private int recordId;
	private int recordSeq;
	private String type;
	private String job;
	private String note;
	private String regId;
	private Date regDate;
	private String subject;
}
