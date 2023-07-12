#ifndef __HANDLERS_H__
#define __HABDLERS_H__

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <netinet/in.h>
#include <arpa/inet.h>
#include <sys/socket.h>
#include <sys/types.h>
#include <unistd.h>

#define BUFF_SIZE 1024
#define HEADER_SIZE 0
#define PAYLOAD_SIZE (BUFF_SIZE - HEADER_SIZE)
#define FILE_PATH "/mnt/d/SEMESTER_2/PSIA/HW02/crc_count.c"

void receive_file(int sockfd, struct sockaddr *from,
                  socklen_t *fromlen, char *filename,
                  char *payload, char *buffer, char *header, int f_size);

void send_file(int sockfd, struct sockaddr *from,
               socklen_t fromlen, char *filename,
               char *payload, char *buffer, char *header, int f_size);

char *get_payload(char *buffer, char *payload);

char *get_filename(char *buffer, char *filename);

char *get_header(char *buffer, char *header);

void itoa(long number, char string[]);

long getFileSize(char const *path);

#endif