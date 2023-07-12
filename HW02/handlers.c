#include "handlers.h"
#include <unistd.h>

char *get_filename(char *buffer, char *filename)
{
    int i = HEADER_SIZE;
    while ((buffer[i] > 32 && buffer[i] < 127))
    {
        *(filename + i) = *(buffer + i);
        i++;
    }
    *(filename + i) = '\0';
    return filename;
}

long getFileSize(char const *path)
{
    FILE *file = fopen(path, "rb");
    if (!file)
    {
        fprintf(stderr, "ERROR: attempt of opening FILE.\n");
        exit(1);
    }

    fseek(file, 0L, SEEK_END);
    long size = ftell(file);

    return size;
}

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

char *get_payload(char *buffer, char *payload)
{
    for (int i = HEADER_SIZE; i <= BUFF_SIZE; i++)
    {
        *(payload + i) = *(buffer + i);
        i++;
    }
    return payload;
}

char *get_header(char *buffer, char *header)
{
    for (int i = 0; i <= HEADER_SIZE; i++)
    {
        *(header + i) = *(buffer + i);
        i++;
    }
    return header;
}

void receive_file(int sockfd, struct sockaddr *from,
                  socklen_t *fromlen, char *filename,
                  char *payload, char *local_buffer, char *header, int f_size)
{
    // char *local_buffer = (char *)malloc(1024);
    FILE *fp = NULL;
    fp = fopen(filename, "wb");
    if (fp == NULL)
        printf("\nFile open failed!\n");
    else
    {
        printf("\nFile Successfully opened!\n");
    }
    printf("Allright");

    int nBytes;
    int ff_size = f_size;
    printf("%d", f_size);
    int counter = 0;
    while (ff_size > 0)
    {
        // recieve message
        nBytes = recvfrom(sockfd, local_buffer,
                          BUFF_SIZE, 0,
                          (struct sockaddr *)&from, fromlen);
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
        fwrite(local_buffer, BUFF_SIZE, 1, fp);

        ff_size -= BUFF_SIZE;
        if (counter % 10 == 0)
            printf("%s\n", local_buffer);
        counter += 1;
    }
    fclose(fp);
}

void send_file(int sockfd, struct sockaddr *from,
               socklen_t fromlen, char *filename,
               char *payload, char *buffer, char *header, int f_size)
{
    FILE *fp = NULL;
    fp = fopen(FILE_PATH, "rb");
    if (fp == NULL)
        printf("\nFile open failed!\n");
    else
    {
        printf("\nFile Successfully opened!\n");
    }
    int counter = 0;
    int ff_size = f_size;
    while (ff_size > 0)
    {
        int nBytes;

        // reading from file
        fread(buffer, BUFF_SIZE, 1, fp);

        // sending message
        sendto(sockfd, buffer,
               BUFF_SIZE, 0,
               (struct sockaddr *)&from, fromlen);

        // sleep(0.1);

        // nBytes = recvfrom(sockfd, buffer,
        //                   BUFF_SIZE, 0,
        //                   (struct sockaddr *)&from, &fromlen);

        // // get header
        // header = get_header(buffer, header);
        // // get payload
        // payload = get_payload(buffer, payload);

        // // write payload to file
        // fwrite(payload, f_size, 1, fp);

        ff_size -= BUFF_SIZE;
        if (counter % 10 == 0)
            printf("%d\n", ff_size);
        counter += 1;
    }
    fclose(fp);
}
