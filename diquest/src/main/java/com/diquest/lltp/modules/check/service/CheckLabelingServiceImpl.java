package com.diquest.lltp.modules.check.service;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;

import com.diquest.lltp.common.utils.JsTree;
import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.EntityVo;
import com.diquest.lltp.domain.RelationVo;
import com.diquest.lltp.modules.brat.service.BratService;

@Service("checkLabelingService")
public class CheckLabelingServiceImpl implements CheckLabelingService{
    
	@Value("#{app['brat.dataPath']}") private String dataLocation;
	
	@Autowired 
	public BratService bratService;	
	
	@Autowired
	public CheckEntityService checkEntityService;
	
	@Autowired
	public CheckRelationService checkRelationService;
	
	public String elementJstreeHtml(String groupName) {
		CommonVo commonVo = new CommonVo();
		commonVo.setGroupName(groupName);
		
		List<CommonVo> elementList = new ArrayList<CommonVo>();
		
		List<EntityVo> entityList = checkEntityService.getEntityList(commonVo);
		List<RelationVo> relationList = checkRelationService.getRelationList(commonVo);
		
		if (!entityList.isEmpty()) {
			HashMap<String,String> map = new HashMap<String,String>();
			
			for (EntityVo vo :entityList) {
				map.put(vo.getName(),vo.getJstreeName());
			}
			
			for (EntityVo vo :entityList) {
				commonVo = new CommonVo();
				String name = "객체/";
				commonVo.setJstreeId(vo.getName());
				//commonVo.setJstreeId("ent"+String.valueOf(vo.getEntId()));
				
				if (!StringUtils.isEmpty(vo.getParentEnt())) {
					String parentEnt[] = (vo.getParentEnt()).split("/");
					for (int i=0; i<parentEnt.length; i++) {
						name += map.get(parentEnt[i]);
						name += "/";
					}
				}
				name += vo.getJstreeName();
				commonVo.setJstreeName(name);
				elementList.add(commonVo);
			}
		}
		
		if (!relationList.isEmpty()) {
			HashMap<String,String> map = new HashMap<String,String>();
			
			for (RelationVo vo :relationList) {
				map.put(vo.getName(),vo.getJstreeName());
			}
			
			for (RelationVo vo :relationList) {
				commonVo = new CommonVo();
				String name = "관계/";
				commonVo.setJstreeId(vo.getName());
				//commonVo.setJstreeId("rel"+String.valueOf(vo.getRelId()));
				
				if (!StringUtils.isEmpty(vo.getParentRel())) {
					String parentRel[] = (vo.getParentRel()).split("/");
					for (int i=0; i<parentRel.length; i++) {
						name += map.get(parentRel[i]);
						name += "/";
					}
				}
				name += vo.getJstreeName();
				commonVo.setJstreeName(name);
				elementList.add(commonVo);
			}
		}
		return new JsTree.Mapper("jstreeId","jstreeName").parseAsHtml(elementList);
	}
	
	
	public String getIndextSubstring(String str, String index) {
		int idx = str.lastIndexOf(index);
		if (idx > 0) {
			str = str.substring(0, idx);
		}
		return str;
	}
	

}
