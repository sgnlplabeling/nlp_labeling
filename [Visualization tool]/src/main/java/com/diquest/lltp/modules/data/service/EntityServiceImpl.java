package com.diquest.lltp.modules.data.service;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashMap;
import java.util.List;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import org.springframework.web.multipart.MultipartFile;

import com.diquest.lltp.common.utils.ExcelReadUtils;
import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.EntityVo;
import com.diquest.lltp.domain.RelationVo;
import com.diquest.lltp.modules.brat.service.BratService;
import com.diquest.lltp.modules.data.dao.EntityDao;

@Service("entityService")
public class EntityServiceImpl implements EntityService {

	@Autowired
	public EntityDao entityDao;
	@Autowired
	public BratService bratService;
	@Autowired
	public DocumentService documentService;

	public void excelUpload(CommonVo vo) throws Exception {
		MultipartFile file = vo.getFile()[0];
		List<EntityVo> entList = ExcelReadUtils.getSheetAt(file.getInputStream(), 0, 2, EntityVo.class);
		List<RelationVo> relList = ExcelReadUtils.getSheetAt(file.getInputStream(), 1, 2, RelationVo.class);
		String groupName = vo.getGroupName();

		// TODO 동일한 이름이 있을시에, id 반환하기.
		if (entList.size() > 0) {
			for (EntityVo ent : entList) {
				ent.setGroupName(groupName);
				insertEntity(ent);
			}
		}

		if (relList.size() > 0) {
			for (RelationVo rel : relList) {
				rel.setGroupName(groupName);
				insertRelation(rel);
			}
		}
	}

	public Integer insertEntity(EntityVo vo) {
		if (StringUtils.isEmpty(vo.getLabel())) {
			vo.setLabel(vo.getName());
		}
		return (Integer) entityDao.insertEntity(vo);
	}

	public EntityVo getEntityOne(EntityVo vo) throws Exception {
		return entityDao.getEntityOne(vo);
	}

	public void updateEntity(EntityVo vo) throws Exception {
		entityDao.updateEntity(vo);
	}

	public void deleteEntity(EntityVo vo) throws Exception {
		entityDao.deleteEntity(vo);
	}

	public List<DocumentVo> getEntityDocList(EntityVo vo) throws Exception {
		return (List<DocumentVo>) entityDao.getEntityDocList(vo);
	}

	public int getEntityDocListCount(EntityVo vo) throws Exception {
		return (int) entityDao.getEntityDocListCount(vo);
	}

	public void recordDelete(EntityVo vo) throws Exception {
		String[] recordIds = vo.getRecordIds();
		DocumentVo doc;
		for (String recordId : recordIds) {
			doc = new DocumentVo();
			doc.setRecordId(Integer.parseInt(recordId));
			doc.setName(vo.getName());

			List<AnnotationVo> list = entityDao.getAnnotationList(doc);
			documentService.updateRecord(doc);

			for (AnnotationVo ann : list) {
				bratService.insertAnnotation(ann);
			}
		}
	}

	public List<RelationVo> getRelationList(EntityVo vo) throws Exception {
		return (List<RelationVo>) entityDao.getRelationList(vo);
	}

	public List<EntityVo> getEntityList(EntityVo vo) throws Exception {
		return (List<EntityVo>) entityDao.getEntityList(vo);
	}

	public void updateRelation(RelationVo vo) throws Exception {

		HashMap<String, Object> relMap = new HashMap<String, Object>();

		String[] startRels = vo.getStartRels();
		String[] endRels = vo.getEndRels();
		String startRel, endRel = "";

		for (int i = 0; i < startRels.length; i++) {
			startRel = startRels[i];
			endRel = endRels[i];

			if (!StringUtils.isEmpty(startRel) && !StringUtils.isEmpty(endRel)) {
				String endRelArr = (String) relMap.get(startRel);

				if (endRelArr == null || endRelArr.isEmpty()) {
					endRelArr = endRel;
					relMap.put(startRel, endRelArr);
				} else {
					endRelArr += "|" + endRel;
					relMap.put(startRel, endRelArr);
				}

			}
		}

		List<String> id = new ArrayList<String>();

		for (String key : relMap.keySet()) {
			vo.setStartRel(key);
			vo.setEndRel((String) relMap.get(key));
			id.add(entityDao.updateRelation(vo));
		}
		vo.setRelIds(id.toArray(new String[id.size()]));
		entityDao.deleteRelation(vo);
	}

	public Integer insertRelation(RelationVo vo) throws Exception {

		if (StringUtils.isEmpty(vo.getLabel())) {
			vo.setLabel(vo.getName());
		}
		EntityVo entityVo = new EntityVo();
		entityVo.setGroupName(vo.getGroupName());
		if ("syntactic".equalsIgnoreCase(vo.getGroupName())) {
			setStartRel(vo, entityVo);
		} else if ("causation".equalsIgnoreCase(vo.getGroupName())) {
			setStartRel(vo, entityVo);
		} else if ("simentic".equalsIgnoreCase(vo.getGroupName())) {
			setStartRel(vo, entityVo);
		}

		return entityDao.insertRelation(vo);
	}

	private void setStartRel(RelationVo vo, EntityVo entityVo) {
		List<EntityVo> entityList = entityDao.getEntityList(entityVo);
		if (StringUtils.isEmpty(vo.getStartRel())) {
			vo.setStartRel(entityList.get(0).getName());
		}
	}

	public void deleteRelation(RelationVo vo) throws Exception {
		entityDao.deleteRelation(vo);
	}

	@Override
	public List<EntityVo> getEntityByEntId(String name) {
		String entity = name.replaceAll("ent", "");
		String[] entIds = entity.split(",");
		EntityVo vo = new EntityVo();
		vo.setSearchTagName(entIds);
		return entityDao.getEntityByEntId(vo);
	}
}
