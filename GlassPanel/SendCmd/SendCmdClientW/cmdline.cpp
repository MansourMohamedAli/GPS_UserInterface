//
//  MODULE:   cmdline.cpp
//
//	AUTHOR: Carlos Antollini 
//
//  mailto: cantollini@hotmail.com
//
//	Date: 09/29/2001
//
//	Version 1.01
// 

#include <afxwin.h>
#include "cmdline.h"


CCommandLine::CCommandLine()
{
	m_strCommandLine = _T("");
	m_strAppName = _T("");
	m_strAppPath = _T("");
	m_strLastToken = _T("");
	string = NULL;
	ParseCommandLine();
}

CCommandLine::~CCommandLine()
{
	m_strCommandLine = _T("");
	m_strAppName = _T("");
	m_strAppPath = _T("");
	m_strLastToken = _T("");

	if(string != NULL)
		free(string);
}

BOOL CCommandLine::GetFirstParameter(CString& strFlag, CString& strParam)
{
	int nParam = 0;
	char seps[] = " ";
	BOOL bRet = FALSE;
	
	strFlag = _T("");
	strParam = _T("");

	if(string != NULL)
		free(string);
	string = (char*)malloc(m_strCommandLine.GetLength() * sizeof(char) + 1);
	memset(string, 0, m_strCommandLine.GetLength() * sizeof(char));

	strcpy(string, m_strCommandLine.GetBuffer(0));
	
	token = strtok(string, seps );
	while(token != NULL && nParam < 2)
	{

		CString strToken = (LPCTSTR)token;

		if(nParam > 0)
		{	
			if(strToken.Left(1).FindOneOf("/-") != -1)
			{
				strFlag = strToken.Mid(1);
				token = strtok(NULL, seps);
				strToken = (LPCTSTR)token;
				if(strToken.Left(1).FindOneOf("/-") != -1)
				{
					m_strLastToken = strToken;
					strToken.Empty();
				}
				else
					m_strLastToken.Empty();
			}

			strParam = strToken;
			bRet = TRUE;
		}
		if (m_strLastToken.IsEmpty())
			token = strtok(NULL, seps);
		else
			token = m_strLastToken.GetBuffer(0);
		nParam++;	
	}

	return bRet;	
}

BOOL CCommandLine::GetNextParameter(CString& strFlag, CString& strParam)
{
	char seps[] = " ";
	strFlag = _T("");
	strParam = _T("");

	if(token != NULL)
	{
		CString strToken = (LPCTSTR)token;

		if(strToken.Left(1).FindOneOf("/-") != -1)
		{
			strFlag = strToken.Mid(1);
			token = strtok(NULL, seps);
			strToken = (LPCTSTR)token;
			if(strToken.Left(1).FindOneOf("/-") != -1)
			{
				m_strLastToken = strToken;
				strToken.Empty();
			}
			else
				m_strLastToken.Empty();
		}
		strParam = strToken;
		if (m_strLastToken.IsEmpty())
			token = strtok( NULL, seps );
		else
			token = m_strLastToken.GetBuffer(0);
		return TRUE;
	}

	return FALSE;
}

void CCommandLine::ParseCommandLine()
{
	CString strParam;
	CString strFlag;
	int nParam = 0;
	char seps[] = " ";
	BOOL bRet = FALSE;
	
	strFlag = _T("");
	strParam = _T("");

	m_strCommandLine = ::GetCommandLine();
	m_strCommandLine.TrimLeft();
	m_strCommandLine.TrimRight();
	m_strAppName = AfxGetAppName(); 

	if(string != NULL)
		free(string);
	string = (char*)malloc(m_strCommandLine.GetLength() * sizeof(char) + 1);
	memset(string, 0, m_strCommandLine.GetLength() * sizeof(char));

	strcpy(string, m_strCommandLine.GetBuffer(0));
	
	token = strtok(string, seps );
	while(token != NULL)
	{
		bRet = TRUE;

		CString strToken = (LPCTSTR)token;

		if(nParam == 0)
		{
			m_strAppPath = strToken;
			m_strAppPath.TrimLeft();
			m_strAppPath.TrimRight();
		}
		else
		{			
			if(strToken.Left(1).FindOneOf("/-") != -1)
			{
				strFlag = strToken.Mid(1);
				token = strtok(NULL, seps);
				strToken = (LPCTSTR)token;
				if(strToken.Left(1).FindOneOf("/-") != -1)
				{
					m_strLastToken = strToken;
					strToken.Empty();
				}
				else
					m_strLastToken.Empty();
			}
			strParam = strToken;
		}
		if (m_strLastToken.IsEmpty())
			token = strtok(NULL, seps);
		else
			token = m_strLastToken.GetBuffer(0);

		if(nParam > 0)
		{
			ParseParam(strFlag, TRUE, strtok == NULL);
			ParseParam(strParam, FALSE, strtok == NULL);
		}
		nParam++;	
	}
}

