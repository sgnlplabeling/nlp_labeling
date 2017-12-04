package com.diquest.lltp.domain;

import lombok.Data;

@Data
public class RelationVo extends CommonVo{
	private String relId;
	private String name;
	private String groupName;
	private String parentRel;
	private String startRel;
	private String endRel;
	private String option;
	private String color;
	private String label;
}
