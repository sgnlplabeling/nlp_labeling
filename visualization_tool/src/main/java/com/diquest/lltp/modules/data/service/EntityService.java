package com.diquest.lltp.modules.data.service;


import java.util.List;

import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.EntityVo;
import com.diquest.lltp.domain.RelationVo;

public interface EntityService {
	
	public void excelUpload(CommonVo commonVo) throws Exception;
	
	public EntityVo getEntityOne(EntityVo vo) throws Exception;

	public void updateEntity(EntityVo vo) throws Exception;

	public Integer insertEntity(EntityVo vo) throws Exception;

	public void deleteEntity(EntityVo vo) throws Exception;

	public List<DocumentVo> getEntityDocList(EntityVo vo) throws Exception;

	public int getEntityDocListCount(EntityVo vo) throws Exception;

	public void recordDelete(EntityVo vo) throws Exception;

	public List<RelationVo> getRelationList(EntityVo vo) throws Exception;

	public List<EntityVo> getEntityList(EntityVo vo) throws Exception;

	public void updateRelation(RelationVo vo) throws Exception;

	public Integer insertRelation(RelationVo vo) throws Exception;

	public void deleteRelation(RelationVo vo) throws Exception;

	List<EntityVo> getEntityByEntId(String name);
	
}
