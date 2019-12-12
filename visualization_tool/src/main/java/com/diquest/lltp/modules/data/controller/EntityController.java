package com.diquest.lltp.modules.data.controller;

import java.text.SimpleDateFormat;
import java.util.Date;
import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

import org.apache.commons.lang3.StringUtils;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.ResponseBody;
import org.springframework.web.servlet.ModelAndView;

import com.diquest.lltp.common.utils.ExcelView;
import com.diquest.lltp.common.utils.Pagination;
import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.EntityVo;
import com.diquest.lltp.domain.RelationVo;
import com.diquest.lltp.modules.check.service.CheckEntityService;
import com.diquest.lltp.modules.check.service.CheckLabelingService;
import com.diquest.lltp.modules.check.service.CheckRelationService;
import com.diquest.lltp.modules.data.service.EntityService;

@Controller
public class EntityController {
	
	@Autowired
	public CheckLabelingService checkLabelingService;
	
	@Autowired
	public CheckEntityService checkEntityService;
	
	@Autowired
	public CheckRelationService checkRelationService;

	@Autowired
	public EntityService entityService;
	
    @RequestMapping(value="/data/entity/list.do")
    public ModelAndView entity(HttpServletRequest request, EntityVo vo, String[] selIds) throws Exception {
		ModelAndView mv = new ModelAndView();
		
        String namedentityJstreeHtml = checkLabelingService.elementJstreeHtml("namedentity", selIds);
        String syntacticJstreeHtml = checkLabelingService.elementJstreeHtml("syntactic", selIds);
        String causationJstreeHtml = checkLabelingService.elementJstreeHtml("causation", selIds);
        String simenticJstreeHtml = checkLabelingService.elementJstreeHtml("simentic", selIds);
        String speechJstreeHtml = checkLabelingService.elementJstreeHtml("speech", selIds);
        mv.addObject("namedentityJstreeHtml", namedentityJstreeHtml);
        mv.addObject("syntacticJstreeHtml", syntacticJstreeHtml);
        mv.addObject("causationJstreeHtml", causationJstreeHtml);
        mv.addObject("simenticJstreeHtml", simenticJstreeHtml);
        mv.addObject("speechJstreeHtml", speechJstreeHtml);
        mv.addObject("common", vo);
        mv.addObject("selIds",selIds);
        
        if (selIds != null && vo.getGroupName()!=null) {
    		EntityVo entity = entityService.getEntityOne(vo);
    		List<RelationVo> relation = entityService.getRelationList(vo);
    		
    		if (relation != null && relation.size() > 0) {
    			mv.addObject("relation", relation);
    			
    			List<EntityVo> entList = entityService.getEntityList(vo);
    			mv.addObject("entList", entList);
    		} else if (entity != null) {
    			mv.addObject("entity", entity);
    		}
        }
        
        if (StringUtils.isEmpty(vo.getGroupName())) {
        	vo.setGroupName("namedentity");
        }
        
		List<DocumentVo> docList = entityService.getEntityDocList(vo);
		int count = entityService.getEntityDocListCount(vo);
		
		mv.addObject("docList", docList);
		mv.addObject("count", count);
		mv.addObject("pagination", new Pagination(request, count));
		
        mv.setViewName("data/entity/list");
        return mv;
    }

	@RequestMapping(value = "/data/entity/excelDown.do")
	public ModelAndView excelDown(CommonVo commonVo) throws Exception {
	
		SimpleDateFormat dateFormat = new SimpleDateFormat("yyyyMMddHHmmss");
		String currentDate = dateFormat.format(new Date());
		
		List<EntityVo> entityList = checkEntityService.getEntityList(commonVo);
		List<RelationVo> relationList = checkRelationService.getRelationList(commonVo);
		
		ExcelView excelView = new ExcelView();
		excelView.setPrefix("/WEB-INF/excel");
		excelView.setTemplateFilename("entity_excel.xlsx");
		excelView.setDownloadFilename("데이터_" + currentDate + ".xlsx");

		ModelAndView modelAndView = new ModelAndView(excelView);
		modelAndView.addObject("entList", entityList);
		modelAndView.addObject("relList", relationList);
		
		return modelAndView;
	}
	
	@ResponseBody
	@RequestMapping(value = "/data/entity/upload.do", produces = "text/json; charset=UTF-8")
	public String upload(HttpServletResponse response, CommonVo commonVo) throws Exception {
		entityService.excelUpload(commonVo);
		return "";
	}    
	
	@RequestMapping(value = "/data/entity/select.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView select(EntityVo vo) throws Exception {
		ModelAndView modelAndView = new ModelAndView("jsonView");
		
		EntityVo entity = entityService.getEntityOne(vo);
		List<RelationVo> relation = entityService.getRelationList(vo);
		
		if (relation != null) {
			modelAndView.addObject("relation", relation);
			
			List<EntityVo> entList = entityService.getEntityList(vo);
			modelAndView.addObject("entList", entList);
		} else if (entity != null) {
			modelAndView.addObject("entity", entity);
		}
		return modelAndView;
	}

	@RequestMapping(value = "/data/entity/entityList.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView entityList(EntityVo vo) throws Exception {
		
		ModelAndView modelAndView = new ModelAndView("jsonView");
		List<EntityVo> entList = entityService.getEntityList(vo);
		modelAndView.addObject("entList", entList);
		return modelAndView;
	}
	
	@RequestMapping(value = "/data/entity/doclist.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView doclist(HttpServletRequest request, EntityVo vo) throws Exception {
		List<DocumentVo> docList = entityService.getEntityDocList(vo);
		int count = entityService.getEntityDocListCount(vo);
		
		ModelAndView modelAndView = new ModelAndView("jsonView");
		modelAndView.addObject("list", docList);
		modelAndView.addObject("count", count);
		modelAndView.addObject("pagination", new Pagination(request, count));
		return modelAndView;
	}
	
	@RequestMapping(value = "/data/entity/update.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView updateEntity(EntityVo vo) throws Exception {
		entityService.updateEntity(vo);
		
		ModelAndView modelAndView = new ModelAndView("jsonView");
		return modelAndView;
	}

	@RequestMapping(value = "/data/relation/update.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView updateRelation(RelationVo vo) throws Exception {
		entityService.updateRelation(vo);
		ModelAndView modelAndView = new ModelAndView("jsonView");
		return modelAndView;
	}
	
	@RequestMapping(value = "/data/entity/insert.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView insert(EntityVo vo) throws Exception {
		entityService.insertEntity(vo);
		
		ModelAndView modelAndView = new ModelAndView("jsonView");
		return modelAndView;
	}

	@RequestMapping(value = "/data/relation/insert.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView insert(RelationVo vo) throws Exception {
		Integer relId = entityService.insertRelation(vo);
		
		ModelAndView modelAndView = new ModelAndView("jsonView");
		modelAndView.addObject("relId", relId);
		return modelAndView;
	}
	
	@RequestMapping(value = "/data/entity/recordDelete.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView recordDelete(EntityVo vo) throws Exception {
		entityService.recordDelete(vo);
		ModelAndView modelAndView = new ModelAndView("jsonView");
		return modelAndView;
	}
	
	@RequestMapping(value = "/data/entity/delete.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView delete(EntityVo vo) throws Exception {
		entityService.deleteEntity(vo);
		ModelAndView modelAndView = new ModelAndView("jsonView");
		return modelAndView;
	}

	@RequestMapping(value = "/data/relation/delete.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView delete(RelationVo vo) throws Exception {
		entityService.deleteRelation(vo);
		ModelAndView modelAndView = new ModelAndView("jsonView");
		return modelAndView;
	}
}
