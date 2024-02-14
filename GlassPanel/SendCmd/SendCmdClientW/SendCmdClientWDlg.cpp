// SendCmdClientWDlg.cpp : implementation file
//

#include "stdafx.h"
#include "SendCmdClientW.h"
#include "SendCmdClientWDlg.h"
#include "cmdline.h"
#include <time.h>
#include <winsock.h>

#define SIZE 500
#define DEFAULT_PORT	(52000)
#define EXECUTE_TAG		"Execute:"

#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif

/////////////////////////////////////////////////////////////////////////////
// CAboutDlg dialog used for App About

class CAboutDlg : public CDialog
{
public:
	CAboutDlg();

// Dialog Data
	//{{AFX_DATA(CAboutDlg)
	enum { IDD = IDD_ABOUTBOX };
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CAboutDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	//{{AFX_MSG(CAboutDlg)
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
	//{{AFX_DATA_INIT(CAboutDlg)
	//}}AFX_DATA_INIT
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CAboutDlg)
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
	//{{AFX_MSG_MAP(CAboutDlg)
		// No message handlers
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CSendCmdClientWDlg dialog

CSendCmdClientWDlg::CSendCmdClientWDlg(CWnd* pParent /*=NULL*/)
	: CDialog(CSendCmdClientWDlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(CSendCmdClientWDlg)
		// NOTE: the ClassWizard will add member initialization here
	//}}AFX_DATA_INIT
	// Note that LoadIcon does not require a subsequent DestroyIcon in Win32
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CSendCmdClientWDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CSendCmdClientWDlg)
		// NOTE: the ClassWizard will add DDX and DDV calls here
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CSendCmdClientWDlg, CDialog)
	//{{AFX_MSG_MAP(CSendCmdClientWDlg)
	ON_WM_SYSCOMMAND()
	ON_WM_PAINT()
	ON_WM_QUERYDRAGICON()
	ON_BN_CLICKED(IDC_SEND, OnSend)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CSendCmdClientWDlg message handlers

BOOL CSendCmdClientWDlg::OnInitDialog()
{
	CDialog::OnInitDialog();

	// Add "About..." menu item to system menu.

	// IDM_ABOUTBOX must be in the system command range.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);

	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		CString strAboutMenu;
		strAboutMenu.LoadString(IDS_ABOUTBOX);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}

	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon
	
	// TODO: Add extra initialization here
	// Command line stuff
	CString strParam, strValue;
	CCommandLine pCmd;
	CString strRemoteHost, strCmd;
	BOOL bCmd = false;
	BOOL bAddress = false;
	CString strFlag = _T("");
	BOOL bRet = pCmd.GetFirstParameter(strFlag, strParam);
	while (bRet)
	{
		// Check for "address"
		if (strFlag.CollateNoCase(_T("address")) == 0)
		{
			strRemoteHost = strParam;
			bAddress = true;
		}
		// "cmd" - command to run remotely
		if (strFlag.CollateNoCase(_T("cmd")) == 0)
		{
			strCmd = strParam;
			bCmd = true;
		}
		// "cmd" - command to run remotely
		if (strFlag.IsEmpty() && bCmd)
		{
			strCmd += _T(" ") + strParam;
		}
		bRet = pCmd.GetNextParameter(strFlag, strParam);
	}
	// Check for close
	if (bCmd && bAddress)
	{
		SetDlgItemText(IDC_REMOTE_HOST, strRemoteHost);
		SetDlgItemText(IDC_CMD, strCmd);
		OnSend();
		EndDialog(0);
//		exit(0);
	}

	return TRUE;  // return TRUE  unless you set the focus to a control
}

void CSendCmdClientWDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialog::OnSysCommand(nID, lParam);
	}
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void CSendCmdClientWDlg::OnPaint() 
{
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting

		SendMessage(WM_ICONERASEBKGND, (WPARAM) dc.GetSafeHdc(), 0);

		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;

		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialog::OnPaint();
	}
}

// The system calls this to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR CSendCmdClientWDlg::OnQueryDragIcon()
{
	return (HCURSOR) m_hIcon;
}

void CSendCmdClientWDlg::OnSend() 
{
	// Send the command
	WSADATA w;								/* Used to open Windows connection */
	CString strRemoteHost;
	CString strCmd;
	unsigned short port_number;				/* The port number to use */
	SOCKET sd;								/* The socket descriptor */
	int server_length;						/* Length of server struct */
	char send_buffer[SIZE] = EXECUTE_TAG;   /* Data to send */
	struct hostent *hp;						/* Information about the server */
	struct sockaddr_in server;				/* Information about the server */
	struct sockaddr_in client;				/* Information about the client */
	char host_name[256];					/* Host name of this computer */
	char Server_name[256];					/* Server name */
	char *pColon;

	GetDlgItemText(IDC_REMOTE_HOST, strRemoteHost);
	GetDlgItemText(IDC_CMD, strCmd);
	/* Make sure command line is correct */
	port_number = DEFAULT_PORT;
	// Look for embedded port number
//	pColon = strstr(strRemoteHost, ":");
	pColon = strstr(strRemoteHost.GetBuffer(0), ":");
	if (pColon)
	{
		int nLen;
		nLen = pColon - strRemoteHost;
		strncpy(Server_name, strRemoteHost, nLen);
		Server_name[nLen] = 0;
		// Port
		port_number = atoi(pColon + 1); 
	}
	else
	{
		strcpy(Server_name, strRemoteHost);
	}
	strcat(send_buffer, strCmd);

	/* Open windows connection */
	if (WSAStartup(0x0202, &w) != 0)
	{
		fprintf(stderr, "Error: Could not open Windows connection.\n");
		exit(0);
	}

	/* Open a datagram socket */
	sd = socket(AF_INET, SOCK_DGRAM, 0);
	if (sd == INVALID_SOCKET)
	{
		fprintf(stderr, "Error: Could not create socket.\n");
		WSACleanup();
		exit(0);
	}

	/* Clear out server struct */
	memset((void *)&server, '\0', sizeof(struct sockaddr_in));

	/* Set family and port */
	server.sin_family = AF_INET;
	server.sin_port = htons(port_number);

	/* Set server address */
    server.sin_addr.s_addr = inet_addr(Server_name);
	//If the address is not dotted notation, then do a DNS 
	//lookup of it.
	if (server.sin_addr.s_addr == INADDR_NONE)
	{
		hp = gethostbyname(Server_name);
		if (hp == NULL)
		{
			fprintf(stderr, "Error: gethostbyname(%s).\n", Server_name);
			WSACleanup();
			exit(0);
		}
		else
		{
			server.sin_addr.S_un.S_un_b.s_b1 = hp->h_addr_list[0][0];
			server.sin_addr.S_un.S_un_b.s_b2 = hp->h_addr_list[0][1];
			server.sin_addr.S_un.S_un_b.s_b3 = hp->h_addr_list[0][2];
			server.sin_addr.S_un.S_un_b.s_b4 = hp->h_addr_list[0][3];
		}
	}

	/* Clear out client struct */
	memset((void *)&client, '\0', sizeof(struct sockaddr_in));

	/* Set family and port */
	client.sin_family = AF_INET;
	client.sin_port = htons(0);

	if (strlen(Server_name))
	{
		/* Get host name of this computer */
		gethostname(host_name, sizeof(host_name));
		hp = gethostbyname(host_name);

		/* Check for NULL pointer */
		if (hp == NULL)
		{
			fprintf(stderr, "Error: Could not get host name.\n");
			closesocket(sd);
			WSACleanup();
			exit(0);
		}

		/* Assign the address */
		client.sin_addr.S_un.S_un_b.s_b1 = hp->h_addr_list[0][0];
		client.sin_addr.S_un.S_un_b.s_b2 = hp->h_addr_list[0][1];
		client.sin_addr.S_un.S_un_b.s_b3 = hp->h_addr_list[0][2];
		client.sin_addr.S_un.S_un_b.s_b4 = hp->h_addr_list[0][3];
	}

	/* Bind local address to socket */
	if (bind(sd, (struct sockaddr *)&client, sizeof(struct sockaddr_in)) == -1)
	{
		fprintf(stderr, "Error: Cannot bind address to socket.\n");
		closesocket(sd);
		WSACleanup();
		exit(0);
	}

	/* Tranmsit remote command */
	server_length = sizeof(struct sockaddr_in);
	if (sendto(sd, send_buffer, (int)strlen(send_buffer) + 1, 0, (struct sockaddr *)&server, server_length) == -1)
	{
		fprintf(stderr, "Error transmitting data.\n");
		closesocket(sd);
		WSACleanup();
		exit(0);
	}

	closesocket(sd);
	WSACleanup();

	return;
}
