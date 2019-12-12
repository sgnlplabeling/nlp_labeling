package com.diquest.lltp.modules.learning.controller;

import java.util.List;

import javax.servlet.http.HttpServletRequest;

import org.apache.commons.lang3.StringUtils;
import org.apache.log4j.Logger;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.MediaType;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

import com.diquest.lltp.common.utils.Pagination;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.modules.data.service.CollectionService;
import com.diquest.lltp.modules.data.service.DocumentService;
import com.diquest.lltp.modules.learning.service.LearningService;

@Controller
public class LearningController {
	Logger log = Logger.getLogger(this.getClass());

	@Autowired
	public DocumentService documentService;

	@Autowired
	public CollectionService collectionService;

	@Autowired
	public LearningService learningService;

	@RequestMapping(value = "/learning/list.do")
	public ModelAndView getLearningList(HttpServletRequest request, DocumentVo vo) throws Exception {
		ModelAndView mv = new ModelAndView();
		if (StringUtils.isEmpty(vo.getGroupName())) {
			vo.setGroupName("namedentity");
		}

		Integer colId = vo.getColId();
		String domainJstreeHtml = collectionService.domainJstreeHtml(colId);

		List<DocumentVo> list = documentService.getDocRecordList(vo);
		int count = documentService.getDocRecordListCount(vo);

		mv.addObject("domainJstreeHtml", domainJstreeHtml);
		mv.addObject("list", list);
		mv.addObject("count", count);
		mv.addObject("pagination", new Pagination(request, count));
		mv.addObject("doc", vo);

		mv.setViewName("learning/list");
		return mv;
	}

	@RequestMapping(value = "/learning/start.do")
	public ModelAndView learningStart(DocumentVo vo) throws Exception {
		ModelAndView mv = new ModelAndView("jsonView");
		learningService.learningStart(vo);
		return mv;
	}

	@RequestMapping(value = "/learning/checkLearning.do", produces = MediaType.APPLICATION_JSON_VALUE)
	public ModelAndView checkAutoLabel(DocumentVo vo) throws Exception {
		ModelAndView mv = new ModelAndView("jsonView");
		List<Integer> checked = learningService.isRunningLearingThread(vo);
		if (!checked.isEmpty()) {
			mv.addObject("docId", checked);
		}
		return mv;
	}
}
