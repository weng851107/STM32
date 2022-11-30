```
Author: Antony_Weng <weng851107@gmail.com>

This file is only used for the record of the learning process, only used by myself and the file has never been leaked out.
If there is related infringement or violation of related regulations, please contact me and the related files will be deleted immediately. Thank you!
```

- [Note](#0)
- [Basic_STM32](#1)
- [Function_STM32](#2)




<h1 id="0">Note</h1>

[CubeIDE Note Content | CubeIDE 教學系列目錄](https://medium.com/stm32cubeide/cubeide-note-context-cubeide-%E6%95%99%E5%AD%B8%E7%B3%BB%E5%88%97%E7%9B%AE%E9%8C%84-4879670ddf4f)

content assist: 預設 Alt + /

- https://www.cnblogs.com/ramlife/p/12448674.html

STM32CubeIDE如何試調

- 使用Expression or live Expression：但只能用於全域變數

- STM32 Cube IDE 下實現printf
    - [STM32 Cube IDE 下實現串口printf](http://ibotx.com/?p=198)
    - [STM32 Cube IDE 下实现 SWO printf](http://ibotx.com/?p=236)

- STM32 Uart接至 Ambarella SoC Uart：STM32 Uart送，用Ambarella SoC Uart去接，顯示在TeraTerm

  - [stm32_uart.py](./code/uart/stm32_uart.py)：Tx完接收之後的RX
  - [stm32_uart_rx.py](./code/uart/stm32_uart_rx.py)：一個程序在Rx, [stm32_uart_tx.py](./code/uart/stm32_uart_tx.py)：另一個程序在Tx，透過mutex且判斷某file數值作為是否在Tx，Tx時disable Rx
  - [stm32_uart_rx.c](./code/uart/stm32_uart_rx.py)：一個程序在Rx, [stm32_uart_tx.c](./code/uart/stm32_uart_tx.py)：另一個程序在Tx，透過mutex且判斷某file數值作為是否在Tx，Tx時disable Rx，但目前Rx會掉字，尚未處理，大致用法已完成

STM32CubeMonitor試調

- 基本變數試調: [新一代神器STM32CubeMonitor介紹、下載、安裝和使用教程](https://www.twblogs.net/a/5e6c165dbd9eee211685f5b5)

GPIO state 設置

- high
- low
- high impedance: means that the stm32 microcontroller won't be trying to drive the pin either high or low.
  - 設為input + No Pull

    ```C
    GPIO_InitStruct.Pin = GPIO_PIN_12; 
    GPIO_InitStruct.Mode = GPIO_MODE_INPUT; 
    GPIO_InitStruct.Pull = GPIO_NOPULL;
    ```

調配Zoom馬達，Focus馬達會自動對焦

- 透過Python把motor trace設置為struct的形式

    [README](./code/excel/README)

    [get_data_from_excel.py](./code/excel/get_data_from_excel.py)


<h1 id="1">Basic_STM32</h1>

[Basic_STM32.md](./Basic_STM32.md)

<h1 id="2">Function_STM32</h1>

[Function_STM32](./Function_STM32.md)





