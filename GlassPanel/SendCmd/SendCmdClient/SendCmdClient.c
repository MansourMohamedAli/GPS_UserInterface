/* SendCmdClient.c */
/* A simple UDP client that send a command to execute on a remote computer */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <time.h>
#include <winsock2.h>
#include "ctypes.h"


#define SIZE 500
#define DEFAULT_PORT	(52000)
#define EXECUTE_TAG		"Execute:"
#define BIND_TO_IP		"SENDCMDCLIENT_BIND_IP"

void usage(void);
char** str_split(char* a_str, const char a_delim);

int send_cmd(char* py_string)
{
	WSADATA w;								/* Used to open Windows connection */
	unsigned short port_number;				/* The port number to use */
	SOCKET sd;								/* The socket descriptor */
	int server_length;						/* Length of server struct */
	char send_buffer[SIZE] = EXECUTE_TAG;   /* Data to send */
	struct hostent* hp;						/* Information about the server */
	struct sockaddr_in server;				/* Information about the server */
	struct sockaddr_in client;				/* Information about the client */
	//	char host_name[256];					/* Host name of this computer */
	char Server_name[256];					/* Server name */
	char* pColon;
	char* pBindIP;
	char** command;

	command = str_split(py_string, ' ');
	/* Make sure command line is correct */
	//if ((num_words < 2) || (num_words > 3))
	//{
	//	usage();
	//}
	port_number = DEFAULT_PORT;
	// Look for embedded port number
	pColon = strstr(command[0], ":");
	if (pColon)
	{
		int nLen;
		nLen = pColon - command[0];
		strncpy(Server_name, command[0], nLen);
		Server_name[nLen] = 0;
		// Port
		port_number = atoi(pColon + 1);
	}
	else
	{
		strcpy(Server_name, command[0]);
	}
	if (strlen(command[1]) == 0)
	{
		usage();
	}
	strcat(send_buffer, command[1]);

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
	memset((void*)&server, '\0', sizeof(struct sockaddr_in));

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

	// Get the login name from the environment
	pBindIP = getenv(BIND_TO_IP);
	if ((pBindIP = getenv(BIND_TO_IP)) != NULL)
	{
		/* Clear out client struct */
		memset((void*)&client, '\0', sizeof(struct sockaddr_in));

		/* Set family and port */
		client.sin_family = AF_INET;
		client.sin_port = htons(0);

		/* Get the IP address */
		hp = gethostbyname(pBindIP);

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

		/* Bind local address to socket */
		if (bind(sd, (struct sockaddr*)&client, sizeof(struct sockaddr_in)) == -1)
		{
			fprintf(stderr, "Error: Cannot bind address [%d.%d.%d.%d] to socket.\n",
				client.sin_addr.S_un.S_un_b.s_b1, client.sin_addr.S_un.S_un_b.s_b2,
				client.sin_addr.S_un.S_un_b.s_b3, client.sin_addr.S_un.S_un_b.s_b4);
			closesocket(sd);
			WSACleanup();
			exit(0);
		}
	}

	/* Tranmsit remote command */
	server_length = sizeof(struct sockaddr_in);
	if (sendto(sd, send_buffer, (int)strlen(send_buffer) + 1, 0, (struct sockaddr*)&server, server_length) == -1)
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

// Function to split a string into tokens
char** str_split(char* a_str, const char a_delim) {
	char** result = NULL;
	size_t count = 0;
	char* tmp = a_str;
	char* last_delim = NULL;
	char delim[2];
	delim[0] = a_delim;
	delim[1] = '\0';

	// Count how many elements will be extracted
	while (*tmp) {
		if (a_delim == *tmp) {
			count++;
			last_delim = tmp;
		}
		tmp++;
	}

	// Add space for trailing token
	count += (last_delim < (a_str + strlen(a_str) - 1));

	// Add space for terminating null string
	count++;
	result = (char**)malloc(sizeof(char*) * count);

	if (result) {
		size_t idx = 0;
		char* token = strtok(a_str, delim);

		while (token) {
			result[idx++] = strdup(token);
			token = strtok(NULL, delim);
		}

		result[idx] = NULL;
	}

	return result;
}

char* extract_between(const char* str, const char* p1, const char* p2) {
	const char* i1 = strstr(str, p1);
	if (i1 != NULL) {
		const size_t pl1 = strlen(p1);
		const char* i2 = strstr(i1 + pl1, p2);
		if (i2 != NULL) {
			const size_t mlen = i2 - (i1 + pl1);
			char* ret = malloc(mlen + 1);
			if (ret != NULL) {
				memcpy(ret, i1 + pl1, mlen);
				ret[mlen] = '\0';
				return ret;
			}
		}
	}
	return NULL;
}

#include <stdio.h>
#include <string.h>

int extract_between_quotes(const char* str, const char* p1, const char* p2) {
	const char* input = "SetVariables \"a\" \"b\" \"c\"";
	const char* start = "\"";
	const char* end = "\"";

	char* substring_start = strstr(input, start);
	if (substring_start) {
		substring_start += strlen(start); // Move past the opening quote
		char* substring_end = strstr(substring_start, end);
		if (substring_end) {
			size_t length = substring_end - substring_start;
			char extracted[length + 1];
			strncpy(extracted, substring_start, length);
			extracted[length] = '\0'; // Null-terminate the extracted string
			printf("Extracted substring: %s\n", extracted);
		}
		else {
			printf("Closing quote not found.\n");
		}
	}
	else {
		printf("Opening quote not found.\n");
	}

	return 0;
}


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
