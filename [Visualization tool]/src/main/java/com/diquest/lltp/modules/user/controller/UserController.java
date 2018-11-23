package com.diquest.lltp.modules.user.controller;

import java.util.List;

import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpSession;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.servlet.ModelAndView;

import com.diquest.lltp.common.utils.Pagination;
import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.UserVo;
import com.diquest.lltp.modules.user.service.UserService;

@Controller
public class UserController {
	
	@Autowired
	public UserService userService;
	
	@RequestMapping(value="/work/user/list.do")
    public ModelAndView userList(HttpServletRequest request, UserVo vo) throws Exception{
		ModelAndView mv = new ModelAndView();
		
		CommonVo commonvo = new CommonVo();
		commonvo.setUserId(vo.getUserId());
		
		int count = userService.selectUserListCount(commonvo);
		List<UserVo> userList = userService.selectUserList(commonvo);
		
		mv.addObject("list", userList);
        mv.addObject("count", count);
        mv.addObject("pagination", new Pagination(request, count));
        mv.addObject("param", vo);
		
        mv.setViewName("work/user/list");
        return mv;
    }
    
    @RequestMapping(value="/work/user/add.do")
    public ModelAndView userAdd() throws Exception{
        ModelAndView mv = new ModelAndView();
        mv.setViewName("work/user/add");
        return mv;
    }
    
    @RequestMapping(value="/work/user/edit.do")
    public ModelAndView user(HttpServletRequest request, UserVo vo) throws Exception{
        ModelAndView mv = new ModelAndView();
        
        String userId = vo.getUserId();
        UserVo user = null;
        
        if(userId != null && userId != "") {
        	user = userService.selectUser(userId);
        }
        
        HttpSession session = request.getSession();
        if(!"SUPER".equals(((UserVo)session.getAttribute("userLoginInfo")).getType()) &&
				!user.getUserId().equals(((UserVo)session.getAttribute("userLoginInfo")).getUserId())){
        	mv = new ModelAndView("redirect:/work/user/list.do");
		}
        
        mv.addObject("user", user);
        mv.addObject("param", vo);
        
        mv.setViewName("work/user/edit");
        return mv;
    }
    
    @RequestMapping(value="/work/user/chkUserId.do")
    public ModelAndView chkUserId(HttpServletRequest request, UserVo vo) throws Exception{
    	ModelAndView mv = new ModelAndView("jsonView");
		
		CommonVo commonvo = new CommonVo();
		commonvo.setUserId(vo.getUserId());
		
		int count = userService.selectUserListCount(commonvo);
        mv.addObject("count", count);
		
        return mv;
    }
    
    @RequestMapping(value="/work/user/deleteUser.do")
    public ModelAndView deleteUser(HttpServletRequest request, UserVo vo) throws Exception{
    	ModelAndView mv = new ModelAndView("jsonView");
		
		String userId = vo.getUserId();
		
		if(userId != null && userId != "") {
			if("super".equals(userId)) {
				mv.addObject("result", "fail");
				mv.addObject("message", "super계정은 삭제할 수 없습니다.");
			} else {
				userService.deleteUser(userId);
				mv.addObject("result", "success");
			}
        } else {
        	mv.addObject("result", "fail");
        }
		
        return mv;
    }
    
    @RequestMapping(value="/work/user/insertUser.do")
    public ModelAndView insertUser(HttpServletRequest request, UserVo vo) throws Exception{
    	ModelAndView mv = new ModelAndView("jsonView");
    	
    	HttpSession session = request.getSession();
    	
    	if(!"SUPER".equals(((UserVo)session.getAttribute("userLoginInfo")).getType())) {
    		mv.addObject("result", "fail");
			mv.addObject("message", "저장 권한이 없습니다.");
			return mv;
    	}
    	
    	CommonVo commonvo = new CommonVo();
		commonvo.setUserId(vo.getUserId());
		
		int count = userService.selectUserListCount(commonvo);
		
		mv.addObject("result", "success");
		
		if(count > 0) {
			mv.addObject("result", "fail");
			mv.addObject("message", "이미 등록이 되어 있는 아이디입니다.");
		} else {
			userService.insertUser(vo, mv);
		}
		
        return mv;
    }
    
    @RequestMapping(value="/work/user/updateUser.do")
    public ModelAndView updateUser(HttpServletRequest request, UserVo vo) throws Exception{
    	ModelAndView mv = new ModelAndView("jsonView");
    	
    	CommonVo commonvo = new CommonVo();
		commonvo.setUserId(vo.getUserId());
		
		UserVo resultVO = userService.selectUser(vo.getUserId());
		
		HttpSession session = request.getSession();
		
		mv.addObject("result", "success");
		
		if(resultVO == null) {
			mv.addObject("result", "fail");
			mv.addObject("message", "수정할 사용자가 없습니다.");
		} else if(!"SUPER".equals(((UserVo)session.getAttribute("userLoginInfo")).getType()) &&
				!resultVO.getUserId().equals(((UserVo)session.getAttribute("userLoginInfo")).getUserId())){
			mv.addObject("result", "fail");
			mv.addObject("message", "수정 권한이 없습니다.");
		} else {
			if(!"SUPER".equals(((UserVo)session.getAttribute("userLoginInfo")).getType())) {
				vo.setAuthConfMng(null);
				vo.setAuthDocMng(null);
				vo.setAuthDomainMng(null);
				vo.setAuthEntityMng(null);
				vo.setAuthLabelMng(null);
				vo.setAuthLearnMng(null);
				vo.setAuthRelationMng(null);
				vo.setAuthTagMng(null);
				vo.setType(null);
			}
			
			userService.updateUser(vo, mv);
		}
		
        return mv;
    }
    
    @RequestMapping(value="/work/user/updateUserPwd.do")
    public ModelAndView updateUserPwd(HttpServletRequest request, UserVo vo) throws Exception{
    	ModelAndView mv = new ModelAndView("jsonView");
    	
		UserVo resultVO = userService.selectUser(vo.getUserId());
		
		HttpSession session = request.getSession();
		
		mv.addObject("result", "success");
		
		if(resultVO == null || resultVO.getUserId() == null || "".equals(resultVO.getUserId())) {
			mv.addObject("result", "fail");
			mv.addObject("message", "수정할 사용자가 없습니다.");
		} else if(!"SUPER".equals(((UserVo)session.getAttribute("userLoginInfo")).getType()) &&
				!resultVO.getUserId().equals(((UserVo)session.getAttribute("userLoginInfo")).getUserId())){
			mv.addObject("result", "fail");
			mv.addObject("message", "수정 권한이 없습니다.");
		} else if(!vo.getPassword().equals(resultVO.getPassword())){
			mv.addObject("result", "fail");
			mv.addObject("message", "현재 비밀번호가 틀립니다.");
		} else {
			userService.updateUserPwd(vo, mv);
		}
		
        return mv;
    }
}
