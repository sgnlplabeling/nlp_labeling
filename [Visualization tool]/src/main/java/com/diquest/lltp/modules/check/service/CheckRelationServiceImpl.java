package com.diquest.lltp.modules.check.service;
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
import com.diquest.lltp.domain.RelationVo;
import com.diquest.lltp.modules.brat.service.BratService;
import com.diquest.lltp.modules.check.dao.CheckRelationDao;
import com.diquest.lltp.modules.data.service.DocumentService;

@Service("checkRelationService")
public class CheckRelationServiceImpl implements CheckRelationService{
	
	@Value("#{app['brat.dataPath']}") private String dataLocation;
	
	@Autowired public CheckRelationDao reltationDao;
	
	@Autowired public DocumentService documentService;

	@Autowired public BratService bratService;

	public List<RelationVo> getRelationList(CommonVo commonVo) {
		return reltationDao.getRelationList(commonVo);
	}
	
	public String relationJstreeHtml(String groupName) throws Exception {
		CommonVo commonVo = new CommonVo();
		commonVo.setGroupName(groupName);
		int num = 0;
		List<RelationVo> entityList = getRelationList(commonVo);
		
		if (!entityList.isEmpty()) {
			HashMap<String,String> map = new HashMap<String,String>();
			
			for (RelationVo vo :entityList) {
				map.put(vo.getName(),vo.getJstreeName());
			}
			
			for (RelationVo vo :entityList) {
				
				String name = "";
				vo.setJstreeId("rel"+String.valueOf(vo.getRelId()));
				
				if (!StringUtils.isEmpty(vo.getParentRel())) {
					String parentEnt[] = (vo.getParentRel()).split("/");
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

	public List<AnnotationVo> getKeywordStartPoint(String groupName, String relation, String searchTerm) {
		relation = relation.replaceAll("rel", "");
		String [] relIds = relation.split(",");
		
		HashMap <String,Object> map = new HashMap<>();
		map.put("groupName", groupName);
		map.put("relIds", relIds);
		map.put("searchTerm", searchTerm);
		
		List<AnnotationVo> list = reltationDao.getKeywordStartPoint(map);
		
		return list;
	}

	public List<AnnotationVo> getKeywordEndPoint(String groupName, String relation, String searchTerm) {
		relation = relation.replaceAll("rel", "");
		String [] relIds = relation.split(",");
		
		HashMap <String,Object> map = new HashMap<>();
		map.put("groupName", groupName);
		map.put("relIds", relIds);
		map.put("searchTerm", searchTerm);
		
		List<AnnotationVo> list = reltationDao.getKeywordEndPoint(map);
		
		return list;
	}
	
	public List<DocumentVo> getLabelingDocList(AnnotationVo vo) throws Exception {
		return reltationDao.getLabelingDocList(vo);
	}

	public List<DocumentVo> getUnlabelingList(List<DocumentVo> list) throws Exception {
		return reltationDao.getUnlabelingList(list);
	}
	
	public List<AnnotationVo> getKeywordList(RelationVo vo) throws Exception {
		return reltationDao.getKeywordList(vo);
	}

	public List<RelationVo> getRelationLoc(AnnotationVo vo) {
		return (List<RelationVo>)reltationDao.getRelationLoc(vo);
	}
}
