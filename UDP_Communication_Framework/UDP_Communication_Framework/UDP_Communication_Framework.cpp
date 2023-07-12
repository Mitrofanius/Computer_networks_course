// UDP_Communication_Framework.cpp : Defines the entry point for the console application.

#pragma comment(lib, "ws2_32.lib")
#include "stdafx.h"
#include <winsock2.h>
#include "ws2tcpip.h"

#define TARGET_IP "192.168.30.56"

#define FOLDER_PATH "C:\\Users\\demom\\urok\\"
#define FILE_NAME "new.jpg"
#define FILE_PATH FOLDER_PATH FILE_NAME
#define SAVE_FOLDER_PATH "C:\\Users\demom\\urok\\"

#define FILE_OPENING_ERROR 1

#define PACKET_LEN 1024
#define FLAGS_NUM 0
#define DIGITS_NUM 100
#define MODULO_NUM 100
#define START "START"
#define STOP "STOP"
#define STR_LEN 100

//#define SENDER
#define RECEIVER

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



void retrieve_word(char* destination, char* from) {
	int i = 0;
	while ((from[i] > 32 && from[i] < 127)) {
		destination[i] = from[i];
		i++;
	}
	destination[i] = '\0';
}


/* Converts integer to string */
void itoa(long number, char string[])
{
	long i, remainder, length = 0, n;

	n = number;
	while (n != 0)
	{
		length++;
		n /= 10;
	}
	for (i = 0; i < length; i++)
	{
		remainder = number % 10;
		number = number / 10;
		string[length - (i + 1)] = remainder + '0';
	}
	if (length == 0 && number == 0)
	{
		string[length] = '0';
		length++;
	}

	string[length] = '\0';
}

/* Writes a size of a file into given string */
long getFileSize(char const* path) {
	FILE* file = fopen(path, "rb");
	if (!file)
	{
		fprintf(stderr, "ERROR: attempt of opening FILE %s has been failed. In FILE %s in LINE %d.\n", FILE_PATH, __FILE__, __LINE__);
		exit(FILE_OPENING_ERROR);
	}

	fseek(file, 0L, SEEK_END);
	long size = ftell(file);

	return size;
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

	printf("Trying to create a new socket...\n");
	socketS = socket(AF_INET, SOCK_DGRAM, 0);
	if (bind(socketS, (sockaddr*)&local, sizeof(local)) != 0) {
		printf("Binding error!\n");
		getchar(); //wait for press Enter
		return 1;
	}
	printf("The socket has been successfully created.\n\n");

	char buffer_tx[PACKET_LEN];
	char buffer_rx[PACKET_LEN];

#ifdef SENDER
	sockaddr_in addrDest;
	addrDest.sin_family = AF_INET;
	addrDest.sin_port = htons(TARGET_PORT);
	InetPton(AF_INET, _T(TARGET_IP), &addrDest.sin_addr.s_addr);

	/* Opens the file */
	printf("Trying to open the file...\n");
	FILE* file = fopen(FILE_PATH, "rb");
	if (!file)
	{
		fprintf(stderr, "ERROR: attempt of opening FILE %s has been failed. In FILE %s in LINE %d.\n", FILE_PATH, __FILE__, __LINE__);
		exit(FILE_OPENING_ERROR);
	}
	printf("The file has been successfully opened.\n\n");

	/* Sends the name of the file ti the listener */
	printf("Sending the name of the file...\n");
	printf("Length of the file name is [%i]\n", strlen(FILE_NAME));
	sendto(socketS, FILE_NAME, strlen(FILE_NAME), FLAGS_NUM, (sockaddr*)&addrDest, sizeof(addrDest));
	printf("The file name has been successfully sent.\n\n");

	/* Sends the size of the file in bytes to the listener */
	printf("Sending the size of the file...\n");
	char fileSize[DIGITS_NUM];
	long size = getFileSize(FILE_PATH);
	itoa(size, fileSize);
	printf("The size of the file is [%s].\n", fileSize);
	sendto(socketS, fileSize, strlen(fileSize), FLAGS_NUM, (sockaddr*)&addrDest, sizeof(addrDest));
	printf("The size of the file has been successfully sent.\n\n");

	/* Sends START */
	printf("Sending the START keyword...\n");
	sendto(socketS, START, strlen(START), FLAGS_NUM, (sockaddr*)&addrDest, sizeof(addrDest));
	printf("The keyword START has been successfully sent.\n\n");

	/* Sends the file in loop piece by piece, BUFFERS_LEN each time */
	printf("The sending process has been started.\n\n");
	long i = 0;
	long bytesCount = 0;
	do
	{
		if (i % MODULO_NUM == 0)
		{
			printf("Sending packet [#%i]...\n", i);
		}

		if (size >= PACKET_LEN)
		{
			fread(buffer_tx, sizeof(BYTE) * PACKET_LEN, 1, file);
			bytesCount += PACKET_LEN;
		}
		else
		{
			fread(buffer_tx, sizeof(BYTE) * size, 1, file);
			bytesCount += size;
		}

		sendto(socketS, buffer_tx, PACKET_LEN, FLAGS_NUM, (sockaddr*)&addrDest, sizeof(addrDest));

		size -= PACKET_LEN;
		i++;
	} while (size > 0);
	printf("\n[%i] bytes has been sent.\n", bytesCount);
	printf("The file has been successfully sent.\n\n");

	/* Sends STOP */
	printf("Sending the STOP keyword...\n");
	sendto(socketS, STOP, strlen(STOP), FLAGS_NUM, (sockaddr*)&addrDest, sizeof(addrDest));
	printf("The keyword STOP has been successfully sent.\n\n");

	/* End of the SENDER side */
	printf("End.\n");
	closesocket(socketS);
	fclose(file);

#endif // SENDER


#ifdef RECEIVER

	char filepath[100] = "C:\\Users\\demom\\psia\\";


	/* Receives a name of the file */
	printf("Trying to receive a file name...");
	char fileName[STR_LEN];
	if (recvfrom(socketS, buffer_rx, sizeof(buffer_rx), 0, (sockaddr*)&from, &fromlen) == SOCKET_ERROR) {
		printf("Socket error!\n");
		getchar();
		return 1;
	}




	retrieve_word(fileName, buffer_rx);

	printf("%s\n", fileName);


	printf("The file name has been successfully received.\n\n");

	/* Creates/opens the file */
	printf("Trying to open the file...\n");
	//char filePath[STR_LEN] = SAVE_FOLDER_PATH;
	strcat(filepath, fileName);
	printf("%s\n", filepath);
	FILE* file = fopen(filepath, "wb");
	if (!file)
	{
		fprintf(stderr, "ERROR: opening FILE %s failed. In FILE %s in LINE %d.", filepath, __FILE__, __LINE__);
		exit(FILE_OPENING_ERROR);
	}
	printf("The file has been successfully opened.\n\n");

	/* Receives the size of the file in bytes*/
	printf("Receiving the size of the file...\n");
	char fileSize[DIGITS_NUM];
	if (recvfrom(socketS, fileSize, sizeof(fileSize), FLAGS_NUM, (sockaddr*)&from, &fromlen) == SOCKET_ERROR) {
		printf("Socket error!\n");
		getchar();
		return 1;
	}
	long size = atoi(fileSize);
	printf("The size of the file is [%ld].\n", size);
	printf("The size of the file has been successfully sent.\n\n");

	/* Waits for START keyword */
	printf("Receiving the START keyword...\n");
	char start[STR_LEN];
	if (recvfrom(socketS, buffer_rx, sizeof(buffer_rx), FLAGS_NUM, (sockaddr*)&from, &fromlen) == SOCKET_ERROR) {
		printf("Socket error!\n");
		getchar();
		return 1;
	}
	retrieve_word(start, buffer_rx);
	if (strcmp(start, START))
	{
		printf("The keyword START has been successfully received.\n\n");
	}

	/* Gets the file in loop piece by piece, BUFFERS_LEN each time */
	printf("The reveiving process has been started.\n\n");
	long bytesCount = 0;
	long i = 0;
	do
	{
		if (i % MODULO_NUM == 0)
		{
			printf("Receiving packet [#%i]...\n", i);
		}

		if (recvfrom(socketS, buffer_rx, PACKET_LEN, FLAGS_NUM, (sockaddr*)&from, &fromlen) == SOCKET_ERROR) {
			printf("Socket error!\n");
			getchar();
			return 1;
		}

		if (size >= PACKET_LEN)
		{
			fwrite(buffer_rx, sizeof(BYTE) * PACKET_LEN, 1, file);
			bytesCount += PACKET_LEN;
		}
		else
		{
			fwrite(buffer_rx, sizeof(BYTE) * size, 1, file);
			bytesCount += size;
		}

		size -= PACKET_LEN;
		i++;
	} while (size >= 0);
	printf("\n[%i] bytes has been received.\n", bytesCount);
	printf("The file has been successfully received.\n\n");


	/* Waits for STOP keyword */
	printf("Receiving the STOP keyword...\n");
	char stop[STR_LEN];
	if (recvfrom(socketS, buffer_rx, sizeof(buffer_rx), FLAGS_NUM, (sockaddr*)&from, &fromlen) == SOCKET_ERROR) {
		printf("Socket error!\n");
		getchar();
		return 1;
	}

	retrieve_word(stop, buffer_rx);

	if (strcmp(stop, STOP))
	{
		printf("The keyword STOP has been successfully received.\n\n");
	}

	/* End of the RECEIVER side */
	printf("End.\n");
	closesocket(socketS);
	fclose(file);
#endif
	//**********************************************************************

	getchar(); //wait for press Enter
	return 0;
}
