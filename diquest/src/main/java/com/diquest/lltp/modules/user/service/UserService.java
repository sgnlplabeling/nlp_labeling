package com.diquest.lltp.modules.user.service;

import java.util.ArrayList;
import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;
import org.springframework.stereotype.Service;
import org.springframework.web.servlet.ModelAndView;

import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.UserVo;
import com.diquest.lltp.modules.user.dao.UserDao;

@Service
public class UserService  {
	
	@Autowired public UserDao userDao;
	
	public int selectUserListCount(CommonVo vo) {
		return userDao.getUserListCount(vo);
	}
	
	public List<UserVo> selectUserList(CommonVo vo) {
		return userDao.getUserList(vo);
	}
	
	public UserVo selectUser(String userId) {
		return userDao.getUser(userId);
	}
	
	public void deleteUser(String userId) {
		userDao.deleteUser(userId);
	}
	
	public void insertUser(UserVo vo, ModelAndView mv) {
		String userId = vo.getUserId();
		String username = vo.getUsername();
		String newPwd = vo.getNewPwd();
		String newPwdConf = vo.getNewPwdConf();
		String type = vo.getType();
		
		if(userId == null || "".equals(userId)){
			mv.addObject("result", "fail");
			mv.addObject("message", "아이디가 입력되지 않았습니다.");
	    	return;
	    } 
	    
	    if(userId.length() < 3){
	    	mv.addObject("result", "fail");
			mv.addObject("message", "아이디는 최소 4자까지 입력돼야 합니다.");
	        return;
	    }
	    
	    if(userId.length() > 15){
	    	mv.addObject("result", "fail");
			mv.addObject("message", "아이디는 최대 15까지 입력할 수 있습니다.");
	        return;
	    }
	    
	    if(username == null || "".equals(username)){
	    	mv.addObject("result", "fail");
			mv.addObject("message", "이름이 입력되지 않았습니다.");
	    	return;
	    }
	    
//	    if(userId.match("[^A-Z가-힣0-9a-z]/gi)" != null){
//	    	alert('아이디에는 공백과 특수문자를 입력할 수 없습니다.');
//	    	$('#userId').select();
//	        $('#userId').focus();
//	        return;
//	    }
	    
	    if("".equals(newPwd)){
	    	mv.addObject("result", "fail");
			mv.addObject("message", "비밀번호가 입력되지 않았습니다.");
            return;
        }
        
        if(newPwd.length() < 4){
        	mv.addObject("result", "fail");
			mv.addObject("message", "비밀번호는 최소 4자까지 입력돼야 합니다.");
            return;
        }
        
        if(newPwd.length() > 12){
        	mv.addObject("result", "fail");
			mv.addObject("message", "비밀번호 최대 12자리까지 입력할 수 있습니다.");
            return;
        }
        
//        if(newPwd.match(/\s/gi)){
//        	alert('비밀번호에는 공백이 포함될 수 없습니다.');
//        	$('#newPwd').select();
//            $('#newPwd').focus();
//            return;
//        }
        
        if(!newPwd.equals(newPwdConf)){
        	mv.addObject("result", "fail");
			mv.addObject("message", "입력한 비밀번호가 서로 일치하지 않습니다.");
            return;
        }
        
        if(type != null && !("SUPER".equals(type) || "ADMIN".equals(type) || "USER".equals(type))) {
        	mv.addObject("result", "fail");
			mv.addObject("message", type+" 구분은 잘못된 값입니다.");
	    	return;
        }
		
		userDao.insertUser(vo);
	}
	
	public void updateUser(UserVo vo, ModelAndView mv) {
		String userId = vo.getUserId();
		String username = vo.getUsername();
		String type = vo.getType();
		
		if(userId == null || "".equals(userId)){
			mv.addObject("result", "fail");
			mv.addObject("message", "수정할 대상이 업습니다.");
	    	return;
	    } 
	    
	    if(username == null || "".equals(username)){
	    	mv.addObject("result", "fail");
			mv.addObject("message", "이름이 입력되지 않았습니다.");
	    	return;
	    }
	    
        if(type != null && !("SUPER".equals(type) || "ADMIN".equals(type) || "USER".equals(type))) {
        	mv.addObject("result", "fail");
			mv.addObject("message", type+" 구분은 잘못된 값입니다.");
	    	return;
        }
		
		userDao.updateUser(vo);
	}
	
	public void updateUserPwd(UserVo vo, ModelAndView mv) {
		String userId = vo.getUserId();
		String password = vo.getPassword();
		String newPassword = vo.getNewPassword();
		String newPwd = vo.getNewPwd();
		String newPwdConf = vo.getNewPwdConf();
		
		if(userId == null || "".equals(userId)){
			mv.addObject("result", "fail");
			mv.addObject("message", "아이디가 입력되지 않았습니다.");
	    	return;
	    }
		
		if("".equals(password)){
	    	mv.addObject("result", "fail");
			mv.addObject("message", "현재 비밀번호가 입력되지 않았습니다.");
            return;
        }
		
	    if("".equals(newPwd) || "".equals(newPassword)){
	    	mv.addObject("result", "fail");
			mv.addObject("message", "새 비밀번호가 입력되지 않았습니다.");
            return;
        }
        
        if(newPwd.length() < 4){
        	mv.addObject("result", "fail");
			mv.addObject("message", "새 비밀번호는 최소 4자까지 입력돼야 합니다.");
            return;
        }
        
        if(newPwd.length() > 12){
        	mv.addObject("result", "fail");
			mv.addObject("message", "새 비밀번호 최대 12자리까지 입력할 수 있습니다.");
            return;
        }
        
//        if(newPwd.match(/\s/gi)){
//        	alert('비밀번호에는 공백이 포함될 수 없습니다.');
//        	$('#newPwd').select();
//            $('#newPwd').focus();
//            return;
//        }
        
        if(!newPwd.equals(newPwdConf)){
        	mv.addObject("result", "fail");
			mv.addObject("message", "입력한 새 비밀번호가 서로 일치하지 않습니다.");
            return;
        }
        
		userDao.updateUserPwd(vo);
	}

}
