#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>
#include "handlers.h"

#define IP_ADDRESS "127.0.0.1"
#define TARGET_PORT 15050
#define LOCAL_PORT 8888
#define BUFF_SIZE 1024
#define HEADER_SIZE 0
#define PAYLOAD_SIZE (BUFF_SIZE - HEADER_SIZE)
#define sendrecvflag 0
#define FILE_PATH "/mnt/d/SEMESTER_2/PSIA/HW02/crc_count.c"

int main(int argc, char *argv[])
{
    int sockfd, nBytes, f_size;
    char buffer[BUFF_SIZE];
    char header[HEADER_SIZE];
    char payload[PAYLOAD_SIZE];
    char *filename;
    struct sockaddr_in addr_con;
    FILE *fp = NULL;

    int addr_conlen = sizeof(addr_con);
    addr_con.sin_family = AF_INET;
    addr_con.sin_port = htons(TARGET_PORT);
    addr_con.sin_addr.s_addr = inet_addr(IP_ADDRESS);

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    if (sockfd < 0)
        printf("\nfile descriptor not received!!\n");
    else
        printf("\nfile descriptor %d received\n", sockfd);

    printf("Sending the name of the file...\n");
    strcpy(buffer, "IMG_SENT_NEW.png");
    sendto(sockfd, buffer, BUFF_SIZE, 0, (struct sockaddr *)&addr_con, addr_conlen);
    printf("The file name has been successfully sent.\n\n");
    sleep(0.9);

    /* Sends the size of the file in bytes to the listener */
    printf("Sending the size of the file...\n");
    char fileSize[BUFF_SIZE];
    // int size = getFileSize(FILE_PATH);
    int size = 684686;
    itoa(size, fileSize);
    printf("The size of the file is [%s].\n", fileSize);
    sendto(sockfd, fileSize, BUFF_SIZE, 0, (struct sockaddr *)&addr_con, addr_conlen);
    printf("The size of the file has been successfully sent.\n\n");
    sleep(0.1);

    /* Sends START */
    printf("Sending the START keyword...\n");
    sendto(sockfd, "START", BUFF_SIZE, 0, (struct sockaddr *)&addr_con, addr_conlen);
    printf("The keyword START has been successfully sent.\n\n");

    printf("Now time for the file.\n\n");

    send_file(sockfd, (struct sockaddr *)&addr_con,
              addr_conlen, filename,
              payload, buffer, header, size);

    printf("It's sent.\n\n");

    return 0;
}