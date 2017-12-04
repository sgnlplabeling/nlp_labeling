
package com.diquest.lltp.common.utils.file;

import java.io.BufferedOutputStream;
import java.io.File;
import java.io.FileInputStream;
import java.io.FileOutputStream;
import java.util.ArrayList;
import java.util.List;

import org.apache.commons.compress.archivers.zip.ZipArchiveEntry;
import org.apache.commons.compress.archivers.zip.ZipArchiveInputStream;
import org.apache.commons.fileupload.FileItem;
import org.apache.commons.lang.RandomStringUtils;
import org.apache.commons.lang.StringUtils;
import org.springframework.web.multipart.MultipartFile;

public class FileUpload {
	/**
	 * 단일 파일 업로드
	 * 
	 * @param item
	 * @param savePath
	 * @param requestMap
	 * @return
	 * @throws Exception
	 */
	public static FileInfo fileUpload(FileItem item, String savePath) throws Exception{
		return fileUpload(item, savePath, false);
	}

	/**
	 * 단일 파일 업로드
	 * 
	 * @param item
	 * @param savePath
	 * @param isAppendExt
	 * @param requestMap
	 * @return
	 * @throws Exception
	 */
	public static FileInfo fileUpload(FileItem item, String savePath, boolean isAppendExt) throws Exception{
		FileInfo fileInfo = null;
		
		if (!item.isFormField()) {
			String fileName = item.getName();
			
			if(!StringUtils.defaultString(fileName, "").equals("")){
				String saveFileName = RandomStringUtils.randomAlphanumeric(25);
				if(isAppendExt){
					saveFileName += StringUtils.right(fileName, fileName.length() - fileName.lastIndexOf("."));
				}
				
				java.io.File save_path = new java.io.File(savePath);
				save_path.mkdirs();
				
				java.io.File uploadedFile = null;
				if(StringUtils.right(savePath, 1).equals("/")){
					uploadedFile = new java.io.File( savePath + saveFileName );
				}else{
					uploadedFile = new java.io.File( savePath + "/" + saveFileName );
				}

				item.write(uploadedFile);
				fileName = fileName.substring(fileName.lastIndexOf("\\") + 1 );
				
				fileInfo = new FileInfo();
				fileInfo.setOrgn_file_nm(fileName);
				fileInfo.setSave_file_nm(saveFileName);
				fileInfo.setSave_path(savePath);
			}
		}
		return fileInfo;
	}

	/**
	 * 단일 파일 업로드
	 * 
	 * @param item
	 * @param savePath
	 * @param requestMap
	 * @return
	 * @throws Exception
	 */
	public static FileInfo fileUpload(MultipartFile item, String savePath) throws Exception{
		return fileUpload(item, savePath, false);
	}

	/**
	 * 단일 파일 업로드
	 * 
	 * @param item
	 * @param savePath
	 * @param isAppendExt
	 * @param requestMap
	 * @return
	 * @throws Exception
	 */
	public static FileInfo fileUpload(MultipartFile item, String savePath, boolean isAppendExt) throws Exception{
		FileInfo fileInfo = null;
		
		if (!item.isEmpty()) {
			String fileName = item.getOriginalFilename();
			
			if(!StringUtils.defaultString(fileName, "").equals("")){
				String saveFileName = RandomStringUtils.randomAlphanumeric(25);
				if(isAppendExt){
					saveFileName += StringUtils.right(fileName, fileName.length() - fileName.lastIndexOf("."));
				}

				java.io.File save_path = new java.io.File(savePath);
				save_path.mkdirs();
				
				item.transferTo(new File(savePath, saveFileName));
				fileName = fileName.substring(fileName.lastIndexOf("\\") + 1 );
				
				fileInfo = new FileInfo();
				fileInfo.setOrgn_file_nm(fileName.substring(0,fileName.lastIndexOf(".")));
				fileInfo.setSave_file_nm(saveFileName);
				fileInfo.setSave_path(savePath);
				fileInfo.setGubun(fileName.substring(fileName.lastIndexOf(".")+1));
			}
		}
		return fileInfo;
	}
	
	/**
	 * 복수 파일 업로드
	 * 
	 * @param item
	 * @param savePath
	 * @param requestMap
	 * @return
	 * @throws Exception
	 */
	public static List<FileInfo> fileUpload(MultipartFile[] item, String savePath) throws Exception{
		return fileUpload(item, savePath, false);
	}

	/**
	 * 복수 파일 업로드
	 * 
	 * @param item
	 * @param savePath
	 * @param isAppendExt
	 * @param requestMap
	 * @return
	 * @throws Exception
	 */
	public static List<FileInfo> fileUpload(MultipartFile[] item, String savePath, boolean isAppendExt) throws Exception{
		List<FileInfo> itemList = new ArrayList<FileInfo>();
		savePath += RandomStringUtils.randomAlphanumeric(25);
		savePath += "/";
		if(item != null && item.length>0){
			
			for(int i=0; i<item.length; i++){
				FileInfo fileInfo = fileUpload(item[i], savePath, isAppendExt);
				if(fileInfo != null){
					if (fileInfo.getGubun().equals("zip")) {
						itemList.addAll(unZipFile(fileInfo.getSave_path()+fileInfo.getSave_file_nm(),savePath));
					} else {
						itemList.add(fileInfo);
					}
				}
			}
		}
		return itemList;
	}
	
	public static List<FileInfo> unZipFile(String targetZip, String completeDir) throws Exception {
		List<FileInfo> itemList = new ArrayList<FileInfo>();
		File zippedFile = new File(targetZip);
		
		FileInfo fileInfo;		
		ZipArchiveInputStream zis;
		ZipArchiveEntry entry;
		String fileName;
		File target;
		int nWritten = 0;
		BufferedOutputStream bos ;
		byte [] buf = new byte[1024 * 8];
		
		zis = new ZipArchiveInputStream(new FileInputStream(zippedFile), "EUC-KR", false);
		while ((entry = zis.getNextZipEntry()) != null) {
			fileName = entry.getName();
			fileName = fileName.substring(fileName.lastIndexOf("/")+1);
			
			if (fileName.lastIndexOf(".")<1) continue;
			
			String gubun = fileName.substring(fileName.lastIndexOf(".")+1);
			fileName = fileName.substring(0, fileName.lastIndexOf("."));
			
			String saveFileName = RandomStringUtils.randomAlphanumeric(25);
			
			target = new File (zippedFile.getParentFile(), saveFileName);
			if ( entry.isDirectory() ){
				target.mkdirs();
			} else {
				target.createNewFile();
				bos = new BufferedOutputStream(new FileOutputStream(target));
				while ((nWritten = zis.read(buf)) >= 0 ){
					bos.write(buf, 0, nWritten);
				}
				bos.close();
				
				fileInfo = new FileInfo();
				fileInfo.setOrgn_file_nm(fileName);
				fileInfo.setSave_file_nm(saveFileName);
				fileInfo.setSave_path(target.getPath().replaceAll(saveFileName, ""));
				fileInfo.setGubun(gubun);
				itemList.add(fileInfo);
			}
		}
		zis.close();
		
		return itemList;
    }  
	
}
