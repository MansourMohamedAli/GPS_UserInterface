/* SendCmdClient.c */
/* A simple UDP client that send a command to execute on a remote computer */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <winsock2.h>
#if _MSC_VER <= 1200 // MSVC 6.0 or earlier
#else
#include <Iphlpapi.h>
#pragma comment(lib,"Iphlpapi.lib") /* Need to add Iphlpapi.lib library to enumerate network cards */
#endif // _MSC_VER <= 1200 // MSVC 6.0 or earlier

#define SIZE 500
#define DEFAULT_PORT	(52000)
#define EXECUTE_TAG		"Execute:"
#define BIND_TO_IP		"SENDCMDCLIENT_BIND_IP"

void usage(void);
char *GetBindIP(ULONG saddr);

int main(int argc, char **argv)
{
	WSADATA w;								/* Used to open Windows connection */
	unsigned short port_number;				/* The port number to use */
	SOCKET sd;								/* The socket descriptor */
	int server_length;						/* Length of server struct */
	char send_buffer[SIZE] = EXECUTE_TAG;   /* Data to send */
	struct hostent *hp;						/* Information about the server */
	struct sockaddr_in server;				/* Information about the server */
	struct sockaddr_in client;				/* Information about the client */
#if _MSC_VER <= 1200 // MSVC 6.0 or earlier
	char host_name[256];					/* Host name of this computer */
#else
	char *pBindIP;
#endif // _MSC_VER <= 1200 // MSVC 6.0 or earlier
	char Server_name[256];					/* Server name */
	char *pColon;

	/* Make sure command line is correct */
	if ((argc < 2) || (argc > 3))
	{
		usage();
	}
	port_number = DEFAULT_PORT;
	// Look for embedded port number
	pColon = strstr(argv[1], ":");
	if (pColon)
	{
		int nLen;
		nLen = pColon - argv[1];
		strncpy(Server_name, argv[1], nLen);
		Server_name[nLen] = 0;
		// Port
		port_number = atoi(pColon + 1); 
	}
	else
	{
		strcpy(Server_name, argv[1]);
	}
	if (strlen(argv[2]) == 0)
	{
		usage();
	}
	strcat(send_buffer, argv[2]);

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

	/* Bind the to the network card */
	/* Get the login name from the environment */
#if _MSC_VER <= 1200 // MSVC 6.0 or earlier
#else
	pBindIP = getenv(BIND_TO_IP);
#endif // _MSC_VER <= 1200 // MSVC 6.0 or earlier
	/* Clear out client struct */
	memset((void *)&client, '\0', sizeof(struct sockaddr_in));
	/* Set family and port */
	client.sin_family = AF_INET;
	client.sin_port = htons(0);
#if _MSC_VER <= 1200 // MSVC 6.0 or earlier
#else
	if ((pBindIP = getenv(BIND_TO_IP)) == NULL)
	{
		/* Find a network card to bind to */
		pBindIP = GetBindIP(server.sin_addr.S_un.S_addr);
	}
#endif // _MSC_VER <= 1200 // MSVC 6.0 or earlier
	if ((argc >= 2) && (argc <= 4))
	{
		/* Get the IP address */
#if _MSC_VER <= 1200 // MSVC 6.0 or earlier
		gethostname(host_name, sizeof(host_name));
		hp = gethostbyname(host_name);
#else
		hp = gethostbyname(pBindIP);
#endif // _MSC_VER <= 1200 // MSVC 6.0 or earlier

		/* Check for NULL pointer */
		if (hp == NULL)
		{
			int dwError = WSAGetLastError();
			if (dwError != 0)
			{
				if (dwError == WSAHOST_NOT_FOUND)
					fprintf(stderr, "Error: Host not found.\n");
				else if (dwError == WSANO_DATA) 
					fprintf(stderr, "Error: No data record found.\n");
				else
					fprintf(stderr, "Error: Function failed with error: %ld\n", dwError);
			}
			else
				fprintf(stderr, "Error: gethostbyname() failed with unknown error.\n");
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
//	fprintf(stderr, "bind address [%d.%d.%d.%d]\n",
//			client.sin_addr.S_un.S_un_b.s_b1, client.sin_addr.S_un.S_un_b.s_b2,
//			client.sin_addr.S_un.S_un_b.s_b3, client.sin_addr.S_un.S_un_b.s_b4);
	if (bind(sd, (struct sockaddr *)&client, sizeof(struct sockaddr_in)) == -1)
	{
		fprintf(stderr, "Error: Cannot bind address [%d.%d.%d.%d] to socket.\n",
			client.sin_addr.S_un.S_un_b.s_b1, client.sin_addr.S_un.S_un_b.s_b2,
			client.sin_addr.S_un.S_un_b.s_b3, client.sin_addr.S_un.S_un_b.s_b4);
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

	return 0;
}

#if _MSC_VER <= 1200 // MSVC 6.0 or earlier
#else
/* See if sendto address is attached to network card */
char *GetBindIP(ULONG saddr)
{
	char *pBindIP = INADDR_ANY;	/* default to any address */
	PIP_ADAPTER_INFO pIpAdapterInfo = (PIP_ADAPTER_INFO)malloc(sizeof(IP_ADAPTER_INFO));
	/* Get structure size, used for GetAdaptersInfo parameter */
	unsigned long stSize = sizeof(IP_ADAPTER_INFO);
	/* Call the GetAdaptersInfo function to fill the pIpAdapterInfo pointer variable; where the stSize parameter is both an input and an output */
	int nRel = GetAdaptersInfo(pIpAdapterInfo,&stSize);
	if (ERROR_BUFFER_OVERFLOW == nRel)
	{
		free(pIpAdapterInfo);
		/* Reapply memory space to store all network card information */
		pIpAdapterInfo = (PIP_ADAPTER_INFO)malloc(stSize);
		/* Call the GetAdaptersInfo function again to fill the pIpAdapterInfo pointer variable */
		nRel = GetAdaptersInfo(pIpAdapterInfo,&stSize);    
 	}
	if (ERROR_SUCCESS == nRel)
	{
		BOOL bValid = FALSE;
		/* Output network card information */
		/* There may be multiple network cards */
		while (pIpAdapterInfo)
		{
			DWORD i = 0;
			IP_ADDR_STRING *pIpAddrString;
			switch(pIpAdapterInfo->Type)
			{
			case MIB_IF_TYPE_ETHERNET:
				bValid = TRUE;
				break;
			case MIB_IF_TYPE_OTHER:
			case MIB_IF_TYPE_TOKENRING:
			case MIB_IF_TYPE_FDDI:
			case MIB_IF_TYPE_PPP:
			case MIB_IF_TYPE_LOOPBACK:
			case MIB_IF_TYPE_SLIP:
			default:
				bValid = FALSE;
				break;
			}
			if (!bValid)
				continue;
			for (i = 0; i < pIpAdapterInfo->AddressLength; i++)
			{
				/* Maybe the network card has multiple IPs, so loop */
				pIpAddrString = &(pIpAdapterInfo->IpAddressList);
				do 
				{
					IP_ADDRESS_STRING CardAddr = pIpAddrString->IpAddress;
					IP_MASK_STRING CardMask = pIpAddrString->IpMask;
					struct sockaddr_in laddr;				/* Information about the local address */
					struct sockaddr_in lmask;				/* Information about the local mask */
					/* See if the server address is part of this network card */
				    laddr.sin_addr.s_addr = inet_addr((char *)&CardAddr);
				    lmask.sin_addr.s_addr = inet_addr((char *)&CardMask);
					if ((laddr.sin_addr.s_addr != INADDR_ANY) && (lmask.sin_addr.s_addr != INADDR_ANY))
					{
						/* Valid network */
						if (((laddr.sin_addr.S_un.S_addr ^ saddr) & lmask.sin_addr.s_addr) == 0)
						{
							/* The server address is on this network card */
							pBindIP = (char *)&CardAddr;
							return (pBindIP);
						}
					}
					/* Move to next address on card */
					pIpAddrString = pIpAddrString->Next;
				} while (pIpAddrString);
				/* Move to next card */
				pIpAdapterInfo = pIpAdapterInfo->Next;
				if (pIpAdapterInfo == NULL) /* Finished */
					break;
			}
		}
		/* Free up memory space */
		if (pIpAdapterInfo)
		{
			free(pIpAdapterInfo);
		}
	}
	return (pBindIP);
}
#endif // _MSC_VER <= 1200 // MSVC 6.0 or earlier

void usage(void)
{
	fprintf(stderr, "Corys Thunder Inc. - Remote Command Executive\n");
	fprintf(stderr, "Usage: SendCmdClient server_address:[port(Default=%d)] remote_command\n", DEFAULT_PORT);
	fprintf(stderr, "       server_address: nnn.nnn.nnn.nnn:port or COMPUTER:port\n");
	fprintf(stderr, "       remote_command: Quoted command to execute on remote machine, use \";\"\n");
	fprintf(stderr, "                       to separate multiple commands.\n");
	fprintf(stderr, "                       i.e. \"cd \\TRex\\Lightning;ThunderView.exe control.thd\"\n\n");
	fprintf(stderr, "Note: To bind to a specific ethernet card set the environment variable\n");
	fprintf(stderr, "      [%s] to the cards IP address.\n\n", BIND_TO_IP);
	exit(0);
}