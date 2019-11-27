package com.diquest.lltp.domain;

import lombok.Getter;
import lombok.Setter;
import lombok.ToString;

@Getter
@Setter
@ToString
public class RelationVo extends CommonVo {

	/**
	 * 관계 고유 ID
	 */
	private String relId;

	/**
	 * 관계 이름
	 */
	private String name;

	/**
	 * 그룹 이름
	 */
	private String groupName;

	/**
	 * 부모 관계 이름
	 */
	private String parentRel;

	/**
	 * 시작 지점
	 */
	private String startRel;

	/**
	 * 끝 지점
	 */
	private String endRel;

	/**
	 * 옵션
	 */
	private String option;

	/**
	 * 글자 색상(default : black)
	 */
	private String color;

	/**
	 * 라벨 이름
	 */
	private String label;

	/**
	 * 시작 지점(배열)
	 */
	private String[] startRels;

	/**
	 * 끝 지점(배열)
	 */
	private String[] endRels;

	private String type;
}
