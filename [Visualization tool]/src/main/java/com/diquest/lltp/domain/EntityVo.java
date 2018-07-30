package com.diquest.lltp.domain;

import lombok.Data;

@Data
public class EntityVo extends CommonVo {
	private String entId;
	private String name;
	private String groupName;
	private String label;
	private String bgColor;
	private String parentEnt;
	
}
