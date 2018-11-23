package com.diquest.lltp.modules.learning.service;

import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.Set;

import com.diquest.lltp.domain.DocumentVo;

public interface LearningService {
	public static final Map<String, Set<Integer>> LAERNING_THREAD = new HashMap<String, Set<Integer>>();
	public void learningStart(DocumentVo vo) throws Exception;
	public List<Integer> isRunningLearingThread(DocumentVo vo);
}
