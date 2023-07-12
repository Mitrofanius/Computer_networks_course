// UDP_Communication_Framework.cpp : Defines the entry point for the console application.
//
#pragma comment(lib, "ws2_32.lib")
#include "stdafx.h"
#include <winsock2.h>
#include "ws2tcpip.h"
#define TARGET_IP "192.168.30.15"
#define FILE_PATH "C:\\Users\\Bablos\\Desktop\\Andy.jpg"
#define SAVE_PATH "something here must be written"
#define FILE_OPENING_ERROR 1
//#define BUFFERS_LEN 1024
#define BUFFERS_LEN 4
#define SENDER
//#define RECEIVER
#ifdef SENDER
#define TARGET_PORT 5555
#define LOCAL_PORT 8888
#endif // SENDER
#ifdef RECEIVER
#define TARGET_PORT 8888
#define LOCAL_PORT 5555
#endif // RECEIVER
void InitWinsock()
{
	WSADATA wsaData;
	WSAStartup(MAKEWORD(2, 2), &wsaData);
}
//**********************************************************************
int main()
{
	SOCKET socketS;
	InitWinsock();
	struct sockaddr_in local;
	struct sockaddr_in from;
	int fromlen = sizeof(from);
	local.sin_family = AF_INET;
	local.sin_port = htons(LOCAL_PORT);
	local.sin_addr.s_addr = INADDR_ANY;
	socketS = socket(AF_INET, SOCK_DGRAM, 0);
	if (bind(socketS, (sockaddr*)&local, sizeof(local)) != 0) {
		printf("Binding error!\n");
		getchar(); //wait for press Enter
		return 1;
	}
	//**********************************************************************
	char buffer_rx[BUFFERS_LEN];
	char buffer_tx[BUFFERS_LEN];
#ifdef SENDER
	sockaddr_in addrDest;
	addrDest.sin_family = AF_INET;
	addrDest.sin_port = htons(TARGET_PORT);
	InetPton(AF_INET, _T(TARGET_IP), &addrDest.sin_addr.s_addr);
	FILE* file = fopen(FILE_PATH, "rb");
	if (!file)
	{
		fprintf(stderr, "ERROR: opening FILE %s failed. In FILE %s in LINE %d.", FILE_PATH, FILE, __LINE__);
		exit(FILE_OPENING_ERROR);
	}
	while (fread(buffer_tx, sizeof(BYTE) * 4, 1, file))
	{
		printf("Sending packet...\n");
		sendto(socketS, buffer_tx, strlen(buffer_tx), 0, (sockaddr*)&addrDest, sizeof(addrDest));
	}
	printf("End.\n");
	//strncpy(buffer_tx, "Hello!\n", BUFFERS_LEN); //put some data to buffer
	//printf("Sending packet...\n");
	//sendto(socketS, buffer_tx, strlen(buffer_tx), 0, (sockaddr*)&addrDest, sizeof(addrDest)); 
	closesocket(socketS);
	fclose(file);
#endif // SENDER
#ifdef RECEIVER
	FILE* file = fopen(FILE_PATH, "wb");
	if (!file)
	{
		fprintf(stderr, "ERROR: opening FILE %s failed. In FILE %s in LINE %d.", SAVE_PATH, FILE, __LINE__);
		exit(FILE_OPENING_ERROR);
	}
	//strncpy(buffer_rx, "No data received.\n", BUFFERS_LEN);
	printf("Waiting for datagram ...\n");
	while (true)
	{
		if (recvfrom(socketS, buffer_rx, sizeof(buffer_rx), 0, (sockaddr*)&from, &fromlen) == SOCKET_ERROR) {
			printf("Socket error!\n");
			getchar();
			return 1;
		}
		else
			printf("Datagram: %s", buffer_rx);
		fwrite(buffer_rx, sizeof(BYTE) * 4, 1, file);
	}
	printf("End.\n");
	closesocket(socketS);
	fclose(file);
#endif
	//**********************************************************************
	getchar(); //wait for press Enter
	return 0;
}