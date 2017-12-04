package com.diquest.lltp.domain;

import lombok.Data;

@Data
public class CollectionVo extends CommonVo {
	private Integer colId;
	private String name;
	private String parentCol;
	private Integer parentId;
	private String path;
}
