package com.diquest.lltp.domain;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class CollectionVo extends CommonVo {
	
	/**
	 * collection 고유 ID
	 */
	private Integer colId;
	
	/**
	 * collection 이름
	 */
	private String name;
	
	/**
	 * 부모 collection 이름
	 */
	private String parentCol;
	
	/**
	 * 부모 collection ID
	 */
	private Integer parentId;
	
	/**
	 * 상위 collection 전체경로
	 */
	private String path;
}
