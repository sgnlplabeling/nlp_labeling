package com.diquest.lltp.modules.user.dao;


import java.util.List;

import org.springframework.stereotype.Repository;

import com.diquest.lltp.common.dao.CommonDAO;
import com.diquest.lltp.domain.CommonVo;
import com.diquest.lltp.domain.HistoryVo;
import com.diquest.lltp.domain.UserVo;

@Repository("UserDao")
public class UserDao extends CommonDAO {

	public int getUserListCount(CommonVo vo) {
		return (int)selectOne("user.selectUserListCount" , vo);
	}

	public List<UserVo> getUserList(CommonVo vo) {
		return (List<UserVo>)selectList("user.selectUserList" , vo);
	}
	
	public UserVo getUser(String userId) {
		return (UserVo)selectOne("user.selectUserView" , userId);
	}
	
	public UserVo deleteUser(String userId) {
		return (UserVo)selectOne("user.deleteUser" , userId);
	}
	
	public void insertUser(UserVo vo) {
		insert("user.insertUser" , vo);
	}
	
	public void updateUser(UserVo vo) {
		update("user.updateUser" , vo);
	}
	
	public void updateUserPwd(UserVo vo) {
		update("user.updateUserPwd" , vo);
	}
}
