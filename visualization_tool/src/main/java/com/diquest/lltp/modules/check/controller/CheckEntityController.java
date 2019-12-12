package com.diquest.lltp.modules.check.controller;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.EntityVo;
import com.diquest.lltp.modules.brat.service.BratService;
import com.diquest.lltp.modules.check.service.CheckEntityService;
import com.diquest.lltp.modules.data.service.EntityService;

@Controller
public class CheckEntityController {

	@Autowired
	public CheckEntityService checkEntityService;

	@Autowired
	public EntityService entityService;

	@Autowired
	public BratService bratService;

	@RequestMapping(value = "/check/entity/list.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView getEntityList(DocumentVo documentVo) throws Exception {
		ModelAndView mv = new ModelAndView();
		mv.setViewName("check/entity/list");

		String namedentityJstreeHtml = checkEntityService.entityJstreeHtml("namedentity");
		String syntacticJstreeHtml = checkEntityService.entityJstreeHtml("syntactic");
		String causationJstreeHtml = checkEntityService.entityJstreeHtml("causation");
		String simenticJstreeHtml = checkEntityService.entityJstreeHtml("simentic");
		String speechJstreeHtml = checkEntityService.entityJstreeHtml("speech");

		mv.addObject("namedentityJstreeHtml", namedentityJstreeHtml);
		mv.addObject("syntacticJstreeHtml", syntacticJstreeHtml);
		mv.addObject("causationJstreeHtml", causationJstreeHtml);
		mv.addObject("simenticJstreeHtml", simenticJstreeHtml);
		mv.addObject("speechJstreeHtml", speechJstreeHtml);
		return mv;
	}

	@RequestMapping(value = "/check/entity/keywordList.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView getKeywordList(String groupName, String entity, String searchTerm, String orderField, String orderOpt) throws Exception {
		ModelAndView mv = new ModelAndView("jsonView");
		List<EntityVo> seletedEnt = entityService.getEntityByEntId(entity);
		List<AnnotationVo> keywordList = checkEntityService.getKeywordList(groupName, entity, searchTerm, orderField, orderOpt);
		mv.addObject("selectEntityDesc", seletedEnt);
		mv.addObject("keywordList", keywordList);
		mv.addObject("keywordListCount", keywordList.size());
		return mv;
	}

	@RequestMapping(value = "/check/entity/docList.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView getLabelingDocList(AnnotationVo vo) throws Exception {
		ModelAndView mv = new ModelAndView("jsonView");

		List<DocumentVo> labelingList = checkEntityService.getLabelingDocList(vo);
		List<DocumentVo> unlabelingList = checkEntityService.getUnlabelingList(labelingList);
		long labelingCnt = 0;
		for (DocumentVo v : labelingList) {
			labelingCnt += v.getCount();
		}
		mv.addObject("labelingList", labelingList);
		mv.addObject("labelingListCount", labelingList.size());
		mv.addObject("labelingCnt", labelingCnt);
		mv.addObject("unlabelingList", unlabelingList);
		mv.addObject("unlabelingListCount", unlabelingList.size());
		return mv;
	}

	@RequestMapping(value = "/check/entity/bratDetailView.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView bratDetailView(DocumentVo documentVo) throws Exception {
		ModelAndView mv = new ModelAndView("jsonView");
		mv.addObject("map", bratService.bratReadOnly(documentVo));
		return mv;
	}

	@RequestMapping(value = "/check/entity/unlabeling.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView unlabeling(String docId, String groupName, String[] keyword) throws Exception {
		ModelAndView mv = new ModelAndView("jsonView");
		checkEntityService.unlabelingDoc(docId.split(","), groupName, keyword);
		return mv;
	}
}
