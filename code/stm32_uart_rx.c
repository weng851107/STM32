#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <fcntl.h>
#include <termios.h>
#include <errno.h>
#include <stdint.h>
#include <pthread.h>

#define DISPLAY_STRING      (1)
#define BLOCKING_MODE       (1)

#define PORT                "/dev/ttyS1"
#define R_BUFFER            (64)

pthread_mutex_t mutex;

static int __set_uart_env(int fd, int speed, int databits, int stopbits, int parity)
{
    struct termios options;

    if(tcgetattr( fd,&options)  !=  0)
    {
    perror("setEnv error-1");
    return(-1);
    }

    //tcgetattr(fd, &options);

    tcflush(fd, TCIOFLUSH);
    cfsetispeed(&options, speed);
    cfsetospeed(&options, speed);
    tcsetattr(fd, TCSANOW, &options);

    options.c_cflag &= ~CSIZE;
    switch (databits)
    {
    case 7:
        options.c_cflag |= CS7;
        break;

    case 8:
        options.c_cflag |= CS8;
        break;

    default:
        fprintf(stderr,"Unsupported data bits\n");
        return (-1);
    }

    switch(parity)
    {
    case 'n':
    case 'N':
        options.c_cflag &= ~PARENB;
        options.c_iflag &= ~INPCK;
        break;

    case 'o':
    case 'O':
        options.c_cflag |= (PARODD | PARENB);
        options.c_iflag |= INPCK;
        break;

    case 'e':
    case 'E':
        options.c_cflag |= PARENB;
        options.c_cflag &= ~PARODD;
        options.c_iflag |= INPCK;
        break;

    case 'S':
    case 's':  /*as no parity*/
        options.c_cflag &= ~PARENB;
        options.c_cflag &= ~CSTOPB;
        break;

    default:
        fprintf(stderr,"Unsupported parity\n");
        return (-1);

    }


    switch (stopbits)
    {
    case 1:
        options.c_cflag &= ~CSTOPB;
        break;

    case 2:
        options.c_cflag |= CSTOPB;
        break;

    default:
        fprintf(stderr,"Unsupported stop bits\n");
        return (-1);
    }

    /* Set input parity option */
    if (parity != 'n')
        options.c_iflag |= INPCK;

    options.c_cc[VTIME] = 150; // 15 seconds
    options.c_cc[VMIN] = 0;


    options.c_lflag  &= ~(ICANON | ECHO | ECHOE | ISIG);  /*Input*/
    options.c_oflag  &= ~OPOST;   /*Output*/

    tcflush(fd,TCIFLUSH);
    if (tcsetattr(fd,TCSANOW,&options) != 0)
    {
        perror("%setEnv error-2");
        return (-1);
    }

    return (0);
}

// refer to http://gaiger-programming.blogspot.com/2015/03/simple-linux-serial-port-programming-in.html
int __set_uart_env_nonblock(int fd, int speed, int parity)
{
    struct termios tty;

    memset(&tty, 0, sizeof tty);
    if (tcgetattr(fd, &tty) != 0) /* save current serial port settings */
    {
        printf("__LINE__ = %d, error %s\n", __LINE__, strerror(errno));
        return -1;
    }

    cfsetospeed(&tty, speed);
    cfsetispeed(&tty, speed);

    tty.c_cflag = (tty.c_cflag & ~CSIZE) | CS8;
    tty.c_iflag &= ~IGNBRK;
    tty.c_lflag = 0;
    tty.c_oflag = 0;
    tty.c_cc[VMIN] = 0;
    tty.c_cc[VTIME] = 0;

    tty.c_iflag &= ~(IXON | IXOFF | IXANY);
    tty.c_cflag |= (CLOCAL | CREAD);
    tty.c_cflag &= ~(PARENB | PARODD);
    tty.c_cflag |= parity;
    tty.c_cflag &= ~CSTOPB;
    tty.c_cflag &= ~CRTSCTS;

    if (tcsetattr(fd, TCSANOW, &tty) != 0)
    {
        printf("__LINE__ = %d, error %s\n", __LINE__, strerror(errno));
        return -1;
    }

    return 0;
} 

int _cec_internal_open_uart(const char *tty)
{
    int fd = (-1);

    if(!tty)
    {
        printf("%s: invalid tty\n", __func__);
        return (-1);
    }

    //fd = open(tty, O_RDWR | O_NOCTTY | O_NONBLOCK | O_NDELAY);    /*non-blocking*/
    fd = open(tty, O_RDWR | O_NOCTTY);                              /*blocking*/
    if(fd <= 0)
    {
        perror("Cant open ttyS1");
        return (-1);
    }

#if BLOCKING_MODE
	if (__set_uart_env(fd, B115200, 8, 1, 'N') < 0)
	{
		printf("Set ENV Error\n");
		close(fd);
		return (-1);
	}	
#else
    __set_uart_env_nonblock(fd, B115200, 0);
    printf("%s: done\n", __func__);
#endif
	return fd;
}

int _cec_internal_cfg_uart_115200(int fd)
{
	if(fd <= 0)
		return (-1);

	return __set_uart_env(fd, B115200, 8, 1, 'N');
}


void _cec_internal_close_uart(int fd)
{
	if(fd > 0)
	{
		close(fd);
		fd = (-1);
	}
}

/*
 * /usr/local/linaro-aarch64-2020.09-gcc10.2-linux5.4/bin/aarch64-linux-gnu-gcc -o stm32_uart_rx stm32_uart_rx.c -lpthread
 *
 * Note: 目前Rx收數值看起來有時候會漏字，和Rx速度有關??? 待修正
*/
int main(int argc, char *argv[])
{  
    int ret = 0;
    int fd;
    char flag = '0';

    pthread_mutex_lock(&mutex);
    system("echo 0 > /tmp/.stm32_uart_flag");
    pthread_mutex_unlock(&mutex);

    fd = _cec_internal_open_uart(PORT);
    if (fd < 0) {
        printf("Error opening %s: %s\n", PORT, strerror(errno));
        return -1;
    }

    /* simple noncanonical input */
    do {
        unsigned char buf[R_BUFFER];
        int rdlen;
        
        FILE *fp = popen("cat /tmp/.stm32_uart_flag", "r");
        flag = fgetc(fp);
        //printf("flag = %c\n", flag);
        pclose(fp);

        if (flag == '0') {
            rdlen = read(fd, buf, sizeof(buf) - 1);
            if (rdlen > 0) {
#ifdef DISPLAY_STRING
                buf[rdlen] = '\0';
                printf("Read %d: %s", rdlen, buf);
                //printf("\n");
#else /* display hex */
                unsigned char   *p;
                printf("Read %d:", rdlen);
                for (p = buf; rdlen-- > 0; p++)
                    printf(" 0x%x", *p);
                //printf("\n");
#endif
            } else if (rdlen < 0) {
                printf("Error from read: %d: %s\n", rdlen, strerror(errno));
            } else {  /* rdlen == 0 */
                printf("Timeout from read\n");
            }               
            /* repeat read to get full message */
            }
        else {

        }     

    } while (1);

    _cec_internal_close_uart(fd);

    return ret;
}

