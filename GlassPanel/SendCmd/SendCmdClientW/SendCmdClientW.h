// SendCmdClientW.h : main header file for the SENDCMDCLIENTW application
//

#if !defined(AFX_SENDCMDCLIENTW_H__B0A3ED9E_90F3_4440_8D14_796C8161388D__INCLUDED_)
#define AFX_SENDCMDCLIENTW_H__B0A3ED9E_90F3_4440_8D14_796C8161388D__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#ifndef __AFXWIN_H__
	#error include 'stdafx.h' before including this file for PCH
#endif

#include "resource.h"		// main symbols

/////////////////////////////////////////////////////////////////////////////
// CSendCmdClientWApp:
// See SendCmdClientW.cpp for the implementation of this class
//

class CSendCmdClientWApp : public CWinApp
{
public:
	CSendCmdClientWApp();

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CSendCmdClientWApp)
	public:
	virtual BOOL InitInstance();
	//}}AFX_VIRTUAL

// Implementation

	//{{AFX_MSG(CSendCmdClientWApp)
		// NOTE - the ClassWizard will add and remove member functions here.
		//    DO NOT EDIT what you see in these blocks of generated code !
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};


/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_SENDCMDCLIENTW_H__B0A3ED9E_90F3_4440_8D14_796C8161388D__INCLUDED_)
