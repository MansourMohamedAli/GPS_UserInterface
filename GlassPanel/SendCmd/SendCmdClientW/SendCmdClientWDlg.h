// SendCmdClientWDlg.h : header file
//

#if !defined(AFX_SENDCMDCLIENTWDLG_H__8279F820_F721_4DB2_820E_933964218F59__INCLUDED_)
#define AFX_SENDCMDCLIENTWDLG_H__8279F820_F721_4DB2_820E_933964218F59__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

/////////////////////////////////////////////////////////////////////////////
// CSendCmdClientWDlg dialog

class CSendCmdClientWDlg : public CDialog
{
// Construction
public:
	CSendCmdClientWDlg(CWnd* pParent = NULL);	// standard constructor

// Dialog Data
	//{{AFX_DATA(CSendCmdClientWDlg)
	enum { IDD = IDD_SENDCMDCLIENTW_DIALOG };
		// NOTE: the ClassWizard will add data members here
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CSendCmdClientWDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	//{{AFX_MSG(CSendCmdClientWDlg)
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	afx_msg void OnSend();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_SENDCMDCLIENTWDLG_H__8279F820_F721_4DB2_820E_933964218F59__INCLUDED_)
