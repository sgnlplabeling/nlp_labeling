package com.diquest.lltp.modules.check.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import com.diquest.lltp.common.utils.JsTree;
import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.EntityVo;
import com.diquest.lltp.modules.brat.service.BratService;
import com.diquest.lltp.modules.check.dao.CheckEntityDao;
import com.diquest.lltp.modules.data.service.DocumentService;
import com.diquest.lltp.modules.work.service.HistoryService;

@Service("checkEntityService")
public class CheckEntityServiceImpl implements CheckEntityService {
	
	@Value("#{app['brat.dataPath']}") private String dataLocation;
	
	@Autowired public CheckEntityDao entityDao;
	
	@Autowired public DocumentService documentService;

	@Autowired public BratService bratService;
	
	@Autowired public HistoryService historyService;	
	
	public List<EntityVo> getEntityList(CommonVo commonVo) {
		List<EntityVo> list = new ArrayList<>();
		if (!StringUtils.isEmpty(commonVo.getGroupName())) {
			list = entityDao.getEntityList(commonVo);
		}
		return list;
	}
	
	public String entityJstreeHtml(String groupName) throws Exception {
		CommonVo commonVo = new CommonVo();
		commonVo.setGroupName(groupName);
		int num = 0;
		List<EntityVo> entityList = getEntityList(commonVo);
		
		if (!entityList.isEmpty()) {
			HashMap<String,String> map = new HashMap<String,String>();
			
			for (EntityVo vo :entityList) {
				map.put(vo.getName(),vo.getJstreeName());
			}
			
			for (EntityVo vo :entityList) {
				
				String name = "";
				vo.setJstreeId("ent"+String.valueOf(vo.getEntId()));
				
				if (!StringUtils.isEmpty(vo.getParentEnt())) {
					String parentEnt[] = (vo.getParentEnt()).split("/");
					for (int i=0; i<parentEnt.length; i++) {
						name += map.get(parentEnt[i]);
						name += "/";
					}
				}
				name += vo.getJstreeName();
				vo.setJstreeName(name);
				entityList.set(num, vo);
				num++;
			}
		}
		
		return new JsTree.Mapper("jstreeId","jstreeName").parseAsHtml(entityList);
	}

	public List<AnnotationVo> getKeywordList(String groupName, String entity, String searchTerm, String orderField, String orderOpt) throws Exception {
		entity = entity.replaceAll("ent", "");
		String [] entIds = entity.split(",");
		
		HashMap <String,Object> map = new HashMap<>();
		map.put("groupName", groupName);
		map.put("entIds", entIds);
		map.put("searchTerm", searchTerm);
		map.put("orderField", orderField);
		map.put("orderOpt", orderOpt);
		
		return entityDao.getKeywordList(map);
	}
	
	public List<DocumentVo> getLabelingDocList(AnnotationVo vo) throws Exception {
		return entityDao.getLabelingDocList(vo);
	}

	public List<DocumentVo> getUnlabelingList(List<DocumentVo> list) throws Exception {
		return entityDao.getUnlabelingList(list);
	}

	public void unlabelingDoc(String[] docId, String groupName, String[] keyword) throws Exception {
		DocumentVo vo;
		
		for (int i=0; i<docId.length; i++) {
			vo = new DocumentVo();
			vo.setGroupName(groupName);
			vo.setDocId(Integer.parseInt(docId[i]));
			
			List<AnnotationVo> annList = bratService.getAnnotationList(vo);
			
			vo.setKeywords(keyword);
			List<AnnotationVo> keywordList = bratService.getAnnotationList(vo);
			
			List<AnnotationVo> resultList = new ArrayList<>();
			
			for (AnnotationVo ann : annList) {
				boolean result = true;
				
				for (AnnotationVo key : keywordList) {
					if ((ann.getAnnId()).equals(key.getAnnId())) {
						result = false;
						break;
					} else if ((ann.getStartPoint()).equals(key.getAnnId()) || (ann.getEndPoint()).equals(key.getAnnId())) {
						result = false;
						break;
					}
				}
				if (result) resultList.add(ann);
			}
			documentService.updateRecord(vo);
			
			for (AnnotationVo ann : resultList) {
				bratService.insertAnnotation(ann);
			}
			historyService.addHistoryRecord(historyService.makeLabelingHistory("언레이블링", annList.get(0).getRecordId(), keyword[0]));
		}
	}
}
