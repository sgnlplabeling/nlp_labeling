package com.diquest.lltp.modules.brat.service;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.FileReader;
import java.io.OutputStreamWriter;
import java.io.Writer;
import java.text.SimpleDateFormat;
import java.util.Arrays;
import java.util.Date;
import java.util.HashMap;
import java.util.Iterator;
import java.util.List;
import java.util.Map;

import org.json.simple.JSONArray;
import org.json.simple.JSONObject;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Service;
import org.springframework.web.context.request.RequestAttributes;
import org.springframework.web.context.request.RequestContextHolder;

import com.diquest.lltp.domain.AnnotationVo;
import com.diquest.lltp.domain.DocumentVo;
import com.diquest.lltp.domain.EntityVo;
import com.diquest.lltp.domain.RelationVo;
import com.diquest.lltp.domain.UserVo;
import com.diquest.lltp.modules.brat.dao.BratDao;
import com.diquest.lltp.modules.check.service.CheckEntityService;
import com.diquest.lltp.modules.check.service.CheckRelationService;
import com.diquest.lltp.modules.data.service.DocumentService;
import com.diquest.lltp.modules.work.service.HistoryService;

@Service("bratService")
public class BratServiceImpl implements BratService{
    
	@Value("#{app['brat.dataPath']}") private String dataLocation;
	
	@Autowired public BratDao bratDao;
	
	@Autowired
	public DocumentService documentService;
	
	@Autowired
	public CheckEntityService checkEntityService;
	
	@Autowired
	public CheckRelationService checkRelationService;
	
	@Autowired 
	public HistoryService historyService;	
	   
	public List<AnnotationVo> getAnnotationList(DocumentVo documentVo) {
		return bratDao.getAnnotationList(documentVo);
	}

	@SuppressWarnings("unchecked")
	public HashMap<String,Object> getDocData(DocumentVo documentVo) throws Exception {
		HashMap<String,Object> map = new HashMap<>();
		
		List<AnnotationVo> annList = getAnnotationList(documentVo);
		DocumentVo doc = documentService.getDocOne(documentVo);
		
		JSONArray entityArr = new JSONArray();
		JSONArray relationArr = new JSONArray();
		
		JSONArray element;	
		
		JSONArray point;
		JSONArray pointArr;
		
		for (AnnotationVo ann : annList) {
			element = new JSONArray();
			String ann_id = ann.getAnnId();

			element.add(ann_id); //개체id
			element.add(ann.getName()); //개체명
			
			if (ann_id.startsWith("T")) {
				point = new JSONArray();
				pointArr = new JSONArray();
				point.add(ann.getStartPoint()); //포인트 시작지점
				point.add(ann.getEndPoint()); //포인트 끝지점
				pointArr.add(point);

				element.add(pointArr);
				entityArr.add(element);
				
			} else if (ann_id.startsWith("R")) {
				pointArr = new JSONArray();
				
				point = new JSONArray(); //시작지점
				point.add("Anaphor");
				point.add(ann.getStartPoint());
				pointArr.add(point);

				point = new JSONArray(); //끝지점
				point.add("Entity");
				point.add(ann.getEndPoint());
				pointArr.add(point);
				
				element.add(pointArr);
				relationArr.add(element);
			}
		}
		
		map.put("entities", entityArr);
		map.put("relations", relationArr);
		map.put("text", doc.getContent());
		
		return map;
	}	
	
	public String getIndextSubstring(String str, String index) {
		int idx = str.lastIndexOf(index);
		if (idx > 0) {
			str = str.substring(0, idx);
		}
		return str;
	}
	
	public HashMap<String,Object> getCollData(DocumentVo documentVo) throws Exception {
		List<EntityVo> entityList = checkEntityService.getEntityList(documentVo);
		List<RelationVo> relationList = checkRelationService.getRelationList(documentVo);

	    HashMap<String,Object> resultMap = new HashMap<String,Object>();
	      
		JSONArray elementArr = new JSONArray();
		JSONObject element, argsEle;
		JSONArray labelArr, argsArr;
		
		String [] searchTerm = {};
		String tmpSearchTerm = documentVo.getSearchTerm();
		
		if (tmpSearchTerm != null) {
			searchTerm = (tmpSearchTerm.replaceAll(" ", "")).split(",");
		}
		
		for (EntityVo entity : entityList) {
			labelArr = new JSONArray();
			element = new JSONObject();

			labelArr.add(entity.getLabel());
			
			element.put("type", entity.getName());
			element.put("labels", labelArr);
			element.put("bgColor", entity.getBgColor());
			
			if (searchTerm.length > 0) {
				if (!Arrays.asList(searchTerm).contains(entity.getName())) {
				//if (!Arrays.asList(searchTerm).contains("ent"+entity.getEntId())) {
					element.put("bgColor", "#ffffff");
				}
			}
			
			elementArr.add(element);
		}
	    resultMap.put("entities", elementArr);
	    
		elementArr = new JSONArray();
		
		for (RelationVo relation : relationList) {
			labelArr = new JSONArray();
			element = new JSONObject();
			
			argsArr = new JSONArray();
			
			labelArr.add(relation.getLabel());
			
			element.put("type", relation.getName());
			element.put("color", "#000000");

			element.put("labels", labelArr);
			if (searchTerm.length > 0) {
				if (!Arrays.asList(searchTerm).contains(relation.getName())) {
					element.put("color", "#ffffff");
				}
			}
			
			//시작 relation
			argsEle = new JSONObject();
			JSONArray endRels = new JSONArray();
			
			argsEle.put("role", "Anaphor");
			endRels.add(relation.getStartRel());
			argsEle.put("targets", endRels);
			
			argsArr.add(argsEle);
			
			//끝 relation
			String [] endRel = (relation.getEndRel()).split("\\|");
			argsEle = new JSONObject();
			endRels = new JSONArray();
			
			argsEle.put("role", "Entity");
			for (String rel : endRel) {
				endRels.add(rel);
			}
			argsEle.put("targets", endRels);
			
			argsArr.add(argsEle);
			
			element.put("args", argsArr);
			elementArr.add(element);
			
			}
		
		resultMap.put("relations", elementArr);
		
		return resultMap;
	}
	
	public HashMap<String,Object> bratReadOnly(DocumentVo documentVo) throws Exception {
		HashMap<String,Object> resultMap = new HashMap<>();
		String groupName = documentVo.getGroupName();
		documentVo = documentService.getDocOne(documentVo);
		documentVo.setGroupName(groupName);
		
		SimpleDateFormat dayTime = new SimpleDateFormat("yyyymmddhhmmss");
		String currentTime = dayTime.format(new Date(System.currentTimeMillis()));
		
		String fileName = dataLocation+currentTime;
		
    	resultMap.put("filePath", currentTime+"/"+documentVo.getSubject());
        
    	createFile(documentVo,fileName);
    	
        return resultMap;
	}
	
	public HashMap<String,Object> bratEdit(DocumentVo documentVo) throws Exception {
		HashMap<String,Object> resultMap = new HashMap<>();
		DocumentVo doc = documentService.getRecordOne(documentVo);
		
		if (doc == null) {
			documentVo.setRabelStat("수동");
			documentVo.setRecordId(documentService.insertRecord(documentVo));
			
			doc = documentService.getRecordOne(documentVo);
		} 
		doc.setUserId(documentVo.getUserId());
		
        String fileName = dataLocation+doc.getRecordId();
        File file = new File(fileName);

        if (file.exists()) {
        	String listFileName = "";
        	File[] list = file.listFiles();
        	for (int i=0; i<list.length; i++) {
        		listFileName = list[i].getName();
        		
        		if (listFileName.contains(".ann")) {
        			Date modifiedDate = new Date(list[i].lastModified());
        			Date currentDate = new Date();
        			SimpleDateFormat dateFormat = new SimpleDateFormat("yyyyMMddHHmm");
        			
        			modifiedDate = dateFormat.parse(dateFormat.format(modifiedDate));
        			currentDate = dateFormat.parse(dateFormat.format(currentDate));
        			
        			long minute = (currentDate.getTime() - modifiedDate.getTime())/60000;
        			
        			if (minute > 60) {
        				bratSave(doc);
        				deleteFile(""+doc.getRecordId());
        				resultMap.put("filePath", doc.getRecordId()+"/"+doc.getSubject());
        				break;
        			}
        		}
        		
        		if (listFileName.contains(".lock")) {
        			listFileName = listFileName.replaceAll(fileName, "");
        			listFileName = listFileName.replaceAll(".lock", "");
        			resultMap.put("userId", listFileName);

            		SimpleDateFormat dayTime = new SimpleDateFormat("yyyymmddhhmmss");
            		String currentTime = dayTime.format(new Date(System.currentTimeMillis()));
            		
            		fileName = dataLocation+currentTime;

                	resultMap.put("filePath", currentTime+"/"+doc.getSubject());
                	
        			break;
        		}
        	}
        	resultMap.put("labelGrade", doc.getLabelGrade());
        	
        } else {
        	resultMap.put("filePath", doc.getRecordId()+"/"+doc.getSubject());
        	resultMap.put("labelGrade", doc.getLabelGrade());
        }
        
        createFile(doc,fileName);
        return resultMap;
	}
	
	public void createFile(DocumentVo doc, String fileName) throws Exception {

		List<EntityVo> entityList = checkEntityService.getEntityList(doc);
		List<RelationVo> relationList = checkRelationService.getRelationList(doc);
		List<AnnotationVo> annList = getAnnotationList(doc);

		String text = "";
        
        File file = new File(fileName);
        
        file.mkdirs();
        
        // lock파일 생성
        String userId = ((UserVo) RequestContextHolder.getRequestAttributes().getAttribute("userLoginInfo", RequestAttributes.SCOPE_SESSION)).getUserId();
        
        file = new File(fileName+"/"+userId+".lock");
        file.createNewFile();
        
        //.txt파일 생성
        file = new File(fileName+"/"+doc.getSubject()+".txt");
        
        Writer fw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(file), "utf-8"));
        fw.write(doc.getContent());
        fw.flush();
        fw.close();
        
        //.ann파일 생성
        text = "";
        file = new File(fileName+"/"+doc.getSubject()+".ann");
        fw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(file), "utf-8"));
        for (AnnotationVo vo : annList) {
        	text += vo.getAnnId();
        	text += "\t";
        	text += vo.getName();
        	text += " ";
        	if (vo.getAnnId().startsWith("T")) {
        		text += vo.getStartPoint();
        		text += " ";
        		text += vo.getEndPoint();
        		text += "\t";
        		text += vo.getContent();
        	} else if (vo.getAnnId().startsWith("R")) {
        		text += "Arg1:";
        		text += vo.getStartPoint();
        		text += " ";
        		text += "Arg2:";
        		text += vo.getEndPoint();
        	}
        	text += "\n";
        }
        fw.write(text);
        fw.flush();
        fw.close();
        
        //annotation.conf파일 생성
        file = new File(fileName+"/"+"annotation.conf");
        fw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(file), "utf-8"));
        text = "";
    	text += "[entities]";
        for (EntityVo vo : entityList) {
        	text += "\n";
        	text += vo.getName();
        }
        text += "\n";
        text += "[relations]";
        for (RelationVo vo : relationList) {
        	text += "\n";
        	text += vo.getName();
        	text += " Arg1:";
        	text += vo.getStartRel();
        	text += ", Arg2:";
        	text += vo.getEndRel();
        }
        text += "\n";
        text += "[events]";
        text += "\n";
        text += "[attributes]";
        fw.write(text);
        fw.flush();
        fw.close();
        
        //visual.conf파일 생성
        HashMap drawingMap = new HashMap<String,String>();
    	HashMap labelMap = new HashMap<String,String>();
    	
    	for (EntityVo vo : entityList) {
    		labelMap.put(vo.getName(), " | "+vo.getLabel());
    		drawingMap.put(vo.getName(), "	bgColor:"+vo.getBgColor());
        }
    	for (RelationVo vo : relationList) {
    		labelMap.put(vo.getName(), " | "+vo.getLabel());
    		drawingMap.put(vo.getName(), "	color:"+vo.getColor());
        }
           
        file = new File(fileName+"/"+"visual.conf");
        fw = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(file), "utf-8"));
        
        text = "";
    	text += "[labels]";
    	
        Iterator<String> keys = labelMap.keySet().iterator();
        while( keys.hasNext() ){
            String key = keys.next();
        	text += "\n";
        	text += key;
        	text += labelMap.get(key);
        }
        text += "\n";
        
        text += "[drawing]";
        text += "\n";
        text += "SPAN_DEFAULT	borderColor:darken";
        
        keys = drawingMap.keySet().iterator();
        while( keys.hasNext() ){
            String key = keys.next();
        	text += "\n";
        	text += key;
        	text += drawingMap.get(key);
        }
        
        text += "\n";
        
        fw.write(text);
        fw.flush();
        fw.close();
        String cmd = "chmod 777 -R " + dataLocation; 
        Runtime rt = Runtime.getRuntime(); 
        Process p = rt.exec(cmd); 
        p.waitFor(); 
        
	}
	
	public DocumentVo bratSave(DocumentVo documentVo) throws Exception {
		documentVo = documentService.getRecordOne(documentVo);
		documentVo.setRabelStat("수동");
		
		//record 저장하기
		documentService.updateRecord(documentVo);
		
		//ann파일 파싱하여 저장
		String path = dataLocation+documentVo.getRecordId()+"/"+documentVo.getSubject()+".ann";
		BufferedReader in = new BufferedReader(new FileReader(path));
		String s;
		AnnotationVo AnnotationVo;
		
		while ((s = in.readLine()) != null) {
			AnnotationVo = new AnnotationVo();
			
			//record 아이디로 변경함
			AnnotationVo.setRecordId(documentVo.getRecordId());
			String ann[] = s.split("\t");
			
			if (s.startsWith("T")) {
				if (ann.length>2) { 
					AnnotationVo.setAnnId(ann[0]);
					AnnotationVo.setContent(ann[2]);
					
					String ent[] = ann[1].split(" ");
					AnnotationVo.setName(ent[0]);
					AnnotationVo.setStartPoint(ent[1]);
					AnnotationVo.setEndPoint(ent[2]);
				}
			}
			else if (s.startsWith("R")) {
				if (ann.length>1) { 
					AnnotationVo.setAnnId(ann[0]);
					String ent[] = ann[1].split(" ");
					AnnotationVo.setName(ent[0]);
					AnnotationVo.setStartPoint(ent[1].replace("Arg1:", ""));
					AnnotationVo.setEndPoint(ent[2].replace("Arg2:", ""));
				}
			} else continue; 
			
			insertAnnotation(AnnotationVo);
			
			}
		in.close();
		
		historyService.addHistoryRecord(historyService.makeLabelingHistory("수정", documentVo.getRecordId(), null));
		
		return documentVo;
	}
	
	public void insertAnnotation(AnnotationVo ann) {
		bratDao.insertAnnotation(ann);
	}
	
	public void deleteFile(String path) throws Exception {
		File file = new File(dataLocation+path);
		File[] tempFile = file.listFiles();
		
		if (tempFile != null) {
			for (int i=0; i<tempFile.length; i++) {
				tempFile[i].delete();
			}
			file.delete();
			
			int idx;
			while(true) {
				idx = path.lastIndexOf("/");
				if (idx < 1) break;
				
				path = path.substring(0,idx);
				
				file = new File(dataLocation+path);
				if ((file.listFiles()).length<1) {
					file.delete();
				} else {
					break;
				}
			}
		}
	}
}
