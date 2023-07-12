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
#define TARGET_PORT 8888
#define LOCAL_PORT 15050
#define BUFF_SIZE 1024
#define HEADER_SIZE 0
#define PAYLOAD_SIZE (BUFF_SIZE - HEADER_SIZE)
#define sendrecvflag 0

int main(int argc, char *argv[])
{
    int sockfd, nBytes, f_size;
    char buffer[BUFF_SIZE];
    char header[HEADER_SIZE];
    char payload[PAYLOAD_SIZE];
    char filename[1024];
    char *name;
    struct sockaddr_in local;
    struct sockaddr_in from;
    FILE *fp = NULL;

    int fromlen = sizeof(from);

    local.sin_family = AF_INET;
    local.sin_port = htons(LOCAL_PORT);
    local.sin_addr.s_addr = inet_addr(IP_ADDRESS);

    sockfd = socket(AF_INET, SOCK_DGRAM, 0);

    if (bind(sockfd, (struct sockaddr *)&local, sizeof(local)) == 0)
        printf("\nSuccessfully binded!\n");
    else
    {
        printf("\nBinding Failed!\n");
        getchar(); //wait for press Enter
        return 1;
    }

    printf("\nWaiting for file name...\n");

    // receive file name

    nBytes = recvfrom(sockfd, buffer,
                      BUFF_SIZE, sendrecvflag,
                      (struct sockaddr *)&from, &fromlen);
    printf("OK");
    name = get_filename(buffer, filename);
    strcpy(filename, name);
    printf("\nFile Name Received: %s\n", filename);

    // receive file size
    // nBytes = recvfrom(sockfd, buffer,
    //                   BUFF_SIZE, sendrecvflag,
    //                   (struct sockaddr *)&from, &fromlen);

    // f_size = atoi(buffer);
    f_size = 686684;

    printf("\nFile size Received: %d\n", f_size);
    f_size = 686684;

    nBytes = recvfrom(sockfd, buffer,
                      BUFF_SIZE, sendrecvflag,
                      (struct sockaddr *)&from, &fromlen);
    printf("%s", buffer);

    // receiving the file
    // receive_file(sockfd, (struct sockaddr *)&from, &fromlen,
    //              filename, payload, buffer, header, f_size);

    int ff_size = 666846;
    printf("%d", f_size);
    int counter = 0;
    fp = fopen(filename, "wb");

    while (ff_size > 0)
    {
        // recieve message
        nBytes = recvfrom(sockfd, buffer,
                          BUFF_SIZE, 0,
                          (struct sockaddr *)&from, &fromlen);
        // sendto(sockfd, buffer,
        //        BUFF_SIZE, 0,
        //        (struct sockaddr *)&from, *fromlen);
        printf("fuck");
        /*
        // get header
        // header = get_header(buffer, header);
        // get payload
        // payload = get_payload(buffer, payload);
        */
        // write payload to file
        fwrite(buffer, 1024, 1, fp);

        ff_size -= BUFF_SIZE;
        if (counter % 10 == 0)
            printf("%s\n", buffer);
        counter += 1;
    }
    fclose(fp);

    printf("end\n");

    return 0;
}
