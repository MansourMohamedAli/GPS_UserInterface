/* SendCmdServer.c */
/* A simple UDP server that executes a command sent from a client */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <winsock.h>
#include <time.h>
#include <process.h>
#include <direct.h>
#include <conio.h>

#define BUFFER_SIZE		(4096)
#define EXECUTE_TAG		"Execute:"
#define DEFAULT_PORT	(52000)
#define DEFAULT_ADDR	"INADDR_ANY"

void usage(void);
void RunCommand(struct sockaddr_in client, char *pCmd);
char *trim(char *str);

int main(int argc, char **argv)
{
	WSADATA w;							/* Used to open windows connection */
	unsigned short port_number;			/* Port number to use */
	int client_length;					/* Length of client struct */
	int bytes_received;					/* Bytes received from client */
	SOCKET sd;							/* Socket descriptor of server */
	struct sockaddr_in server;			/* Information about the server */
	struct sockaddr_in client;			/* Information about the client */
	char buffer[BUFFER_SIZE];			/* Where to store received data */
	struct hostent *hp;					/* Information about this computer */
	char host_name[256];				/* Name of the server */
	char *pstrColon;					/* Addresss:port separator */
    HWND hwnd = GetConsoleWindow();
    HMENU hmenu = GetSystemMenu(hwnd, FALSE);

	/* Interpret command line */
	switch (argc)
	{
	case 1:
		port_number = DEFAULT_PORT;
		host_name[0] = 0;
		break;
	case 2:
		/* Extract the address:port */
		pstrColon = strstr(argv[1], ":");
		if (pstrColon == NULL)	// No port
		{
			port_number = DEFAULT_PORT;
			strcpy(host_name, argv[1]);
		}
		else					// Address and port
		{
			int nHostLen = (int)(pstrColon - argv[1]);
			strncpy(host_name, argv[1], nHostLen);
			host_name[nHostLen] = 0;	// Terminate it
			if (sscanf(pstrColon + 1, "%hu", &port_number) != 1)
			{
				usage();
			}
		}
		break;
	default:
		usage();
		break;
	}

	/* Disable Close Button */
    EnableMenuItem(hmenu, SC_CLOSE, MF_GRAYED);

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

	/* Set address automatically if desired */
	switch (argc)
	{
	case 1:
		/* Get host name of this computer */
		gethostname(host_name, sizeof(host_name));
	case 2:
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
		server.sin_addr.S_un.S_un_b.s_b1 = hp->h_addr_list[0][0];
		server.sin_addr.S_un.S_un_b.s_b2 = hp->h_addr_list[0][1];
		server.sin_addr.S_un.S_un_b.s_b3 = hp->h_addr_list[0][2];
		server.sin_addr.S_un.S_un_b.s_b4 = hp->h_addr_list[0][3];
		break;
	default:
		break;
	}

	/* Bind address to socket */
	if (bind(sd, (struct sockaddr *)&server, sizeof(struct sockaddr_in)) == -1)
	{
		fprintf(stderr, "Error: Could not bind name to socket.\n");
		closesocket(sd);
		WSACleanup();
		exit(0);
	}

	/* Print out server information */
	printf("Command Server running on %u.%u.%u.%u:%u\n", (unsigned char)server.sin_addr.S_un.S_un_b.s_b1,
											  (unsigned char)server.sin_addr.S_un.S_un_b.s_b2,
											  (unsigned char)server.sin_addr.S_un.S_un_b.s_b3,
											  (unsigned char)server.sin_addr.S_un.S_un_b.s_b4,
											  port_number);
	printf("Press CTRL + C to quit\n");

	/* Loop and get data from clients */
	while (1)
	{
		client_length = (int)sizeof(struct sockaddr_in);

		/* Receive bytes from client */
		bytes_received = recvfrom(sd, buffer, BUFFER_SIZE, 0, (struct sockaddr *)&client, &client_length);
		if (bytes_received < 0)
		{
			fprintf(stderr, "Error: Could not receive datagram.\n");
			closesocket(sd);
			WSACleanup();
			exit(0);
		}

		/* Check for time request */
		if (strnicmp(buffer, EXECUTE_TAG, strlen(EXECUTE_TAG)) == 0)
		{
			// Extract the parts of the buffer, path and command
			char *pCmd = buffer + strlen(EXECUTE_TAG);
			// Nothing to do if no command
			if (pCmd != NULL)
			{
				char *pSemiColon;
				char strCmd[1024];
				// Find the ;
				while (pSemiColon = strstr(pCmd, ";"))
				{
					// Process multiple commands separated by ";"
					if (pSemiColon != NULL)
					{
						int nLen = pSemiColon - pCmd;
						strncpy(strCmd, pCmd, pSemiColon - pCmd);
						strCmd[nLen] = 0;
						// Command
						RunCommand(client, strCmd);
						pCmd += nLen + 1;
					}
					else
						break;
				}
				// Last command
				RunCommand(client, pCmd);
			}
		}
	}
	closesocket(sd);
	WSACleanup();

	return 0;
}

// Execute command from client
void RunCommand(struct sockaddr_in client, char *pCmd)
{
	int nLen = strlen(pCmd);
	char strCmd[1024];
	char *pCmdBuffer = NULL;
	// Copy the command buffer
	if (strlen(pCmd))
		pCmdBuffer = strdup(pCmd);
	if (pCmdBuffer == NULL)
		return;
	// Check for special commands
	trim(pCmdBuffer);
	// cd - change directory
	if (nLen > 2)
	{
		if (strnicmp(pCmdBuffer, "cd ", 3) == 0)
		{
			strcpy(strCmd, pCmdBuffer + 3);
			// Change the directory
			_chdir(strCmd);
			// Display the client and cmd
			fprintf(stderr, "[%d.%d.%d.%d]: %s\n",  
				client.sin_addr.S_un.S_un_b.s_b1,
				client.sin_addr.S_un.S_un_b.s_b2,
				client.sin_addr.S_un.S_un_b.s_b3,
				client.sin_addr.S_un.S_un_b.s_b4,
				pCmdBuffer);
			// Free the buffer
			free(pCmdBuffer);
			return;
		}
	}
	// w: - change drive
	if (nLen > 1)
	{
		if (strnicmp(pCmdBuffer + 1, ":", 1) == 0)
		{
			int nDrive = 0;
			// Change the directory
			pCmdBuffer[0] = toupper(pCmdBuffer[0]);
			nDrive = pCmdBuffer[0] - 'A' + 1;
			_chdrive(nDrive);
			// Display the client and cmd
			fprintf(stderr, "[%d.%d.%d.%d]: %s\n",  
				client.sin_addr.S_un.S_un_b.s_b1,
				client.sin_addr.S_un.S_un_b.s_b2,
				client.sin_addr.S_un.S_un_b.s_b3,
				client.sin_addr.S_un.S_un_b.s_b4,
				pCmdBuffer);
			// Free the buffer
			free(pCmdBuffer);
			return;
		}
	}
	// Display the client and cmd
	fprintf(stderr, "[%d.%d.%d.%d]: %s\n",  
		client.sin_addr.S_un.S_un_b.s_b1,
		client.sin_addr.S_un.S_un_b.s_b2,
		client.sin_addr.S_un.S_un_b.s_b3,
		client.sin_addr.S_un.S_un_b.s_b4,
		pCmdBuffer);
	// Process everything else
	system(pCmdBuffer);
	free(pCmdBuffer);
	return;
}

char *trim(char *str)
{
    size_t len = 0;
    char *frontp = str - 1;
    char *endp = NULL;

    if( str == NULL )
            return NULL;

    if( str[0] == '\0' )
            return str;

    len = strlen(str);
    endp = str + len;

    /* Move the front and back pointers to address
     * the first non-whitespace characters from
     * each end.
     */
    while( isspace(*(++frontp)) );
    while( isspace(*(--endp)) && endp != frontp );

    if( str + len - 1 != endp )
            *(endp + 1) = '\0';
    else if( frontp != str &&  endp == frontp )
            *str = '\0';

    /* Shift the string so that it starts at str so
     * that if it's dynamically allocated, we can
     * still free it on the returned pointer.  Note
     * the reuse of endp to mean the front of the
     * string buffer now.
     */
    endp = str;
    if( frontp != str )
    {
            while( *frontp ) *endp++ = *frontp++;
            *endp = '\0';
    }
    return str;
}

void usage(void)
{
	fprintf(stderr, "Corys Thunder Inc. - Remote Command Executive\n");
	fprintf(stderr, "Usage: SendCmdServer [localaddr:port(Default=INADDR_ANY:%d)]\n", DEFAULT_PORT);
	fprintf(stderr, "Examples:\n");
	fprintf(stderr, "SendCmdServer                   <-- default IP address and port %d (Default)\n", DEFAULT_PORT);
	fprintf(stderr, "SendCmdServer :6900             <-- default IP address and port 6900\n");
	fprintf(stderr, "SendCmdServer 192.168.25.5      <-- IP address and port %d (Default)\n", DEFAULT_PORT);
	fprintf(stderr, "SendCmdServer 192.168.25.5:6900 <-- IP address and port 6900\n");
	exit(0);
}
