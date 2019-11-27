package com.diquest.lltp.modules.auto.dao;

import java.util.List;

import org.springframework.stereotype.Repository;

import com.diquest.lltp.common.dao.CommonDAO;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.HistoryVo;


@Repository("AutoLabelingDao")
public class AutoLabelingDao extends CommonDAO {

	public List<HistoryVo> getAutoLabelingStat(DocumentVo vo) {
		return selectList("auto.getAutoLabelingStat" , vo);
	}

}
