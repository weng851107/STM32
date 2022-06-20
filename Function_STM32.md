
# 目錄

- [Reference](#0)
- [GPIO](#1)
  - [[STM32G4系列] GPIO筆記 - CubeMX GPIO整理與應用](#1.1)
    - [設定GPIO output](#1.1.1)
    - [設定GPIO input](#1.1.2)
    - [STM32的HAL庫中GPIO有8種工作模式](#1.1.3)



<h1 id="0">Reference</h1>

- [初次學習的學習清單](https://ithelp.ithome.com.tw/articles/10281160)

- https://ithelp.ithome.com.tw/users/20141979/articles?page=4

<h1 id="1">GPIO</h1>

<h2 id="1.1">[STM32G4系列]GPIO筆記-CubeMX GPIO整理與應用</h2>

[Reference](https://ithelp.ithome.com.tw/articles/10282215)

<h3 id="1.1.1">設定GPIO output</h3>

- 以P2腳位PC13為例，設定為GPIO輸出腳位

- 在MCU接腳圖點選**GPIO_Output**，可在左邊**System Core**選項中開啟**GPIO視窗**，可顯現所設定腳位詳細資料

    ![STM32_img00](./doc/Function_STM32/[STM32G4系列]GPIO筆記-CubeMX%20GPIO整理與應用/STM32_img00.jpg)

- 可在User Label可自行定義名稱

    ![STM32_img01](./doc/Function_STM32/[STM32G4系列]GPIO筆記-CubeMX%20GPIO整理與應用/STM32_img01.jpg)

- 若沒有特殊要求，甚至User Label亦可選擇默認，即完成CubeMX中 GPIO的配置

**指令函數使用：**

1. 使GPIO輸出高電平或低電平：`void HAL_GPIO_WritePin(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin, GPIO_PinState PinState)`
   - **GPIOx** :其中x可以(A..G取決於所使用的裝置)來選擇GPIO外設
   - **GPIO_Pin** :指定要寫入的埠位。此引數可以是GPIO_PIN_x之一，其中x可以是( 0..15 )
   - **PinState** :指定要寫入選定位的值。此引數可以是GPIO_PinState列舉值之一:
     - **GPIO_PIN_RESET**:清除埠Pin,低電平
     - **GPIO_PIN_SET**:設定埠Pin，高電平

    ```C
    HAL_GPIO_WritePin(GPIOA, DONG_OUT_1_Pin|DONG_OUT_2_Pin, GPIO_PIN_RESET);//兩個設定為低電平
    HAL_Delay(1000);//1s
    HAL_GPIO_WritePin(GPIOA, DONG_OUT_1_Pin, GPIO_PIN_SET);//單獨設定為高電平
    HAL_GPIO_WritePin(GPIOA,DONG_OUT_2_Pin, 1);//單獨設定為高電平
    HAL_Delay(1000);//1s
    ```

2. Toggle指定的GPIO output：`void HAL_GPIO_TogglePin(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin)`
   - **GPIOx** :其中x可以(A..G取決於所使用的裝置)來選擇GPIO外設
   - **GPIO_Pin** :指定要寫入的埠位。此引數可以是GPIO_PIN_x之一，其中x可以是(0..15 )

    ```C
    HAL_GPIO_TogglePin(GPIOA, DONG_OUT_1_Pin|DONG_OUT_2_Pin);//兩個輸出電平取反
    HAL_Delay(1000);//1s
    HAL_GPIO_TogglePin(GPIOA, DONG_OUT_1_Pin);//單獨輸出電平取反
    HAL_GPIO_TogglePin(GPIOA,DONG_OUT_2_Pin);//單獨輸出電平取反
    HAL_Delay(1000);//1s
    ```

<h3 id="1.1.2">設定GPIO input</h3>

- GPIO intput使用可以分成兩種方式達成，分別是**輪詢**與**中斷**方式

**輪詢：**

- 使GPIO讀取腳位高電平或低電平：`GPIO_PinState HAL_GPIO_ReadPin(GPIO_TypeDef *GPIOx, uint16_t GPIO_Pin)`
  - **GPIOx** :其中x可以(A..G取決於所使用的裝置)來選擇GPIO外設
  - **GPIO_Pin** :指定要寫入的埠位。此引數可以是GPIO_PIN_x之一，其中x可以是(0..15 )

- 返回：

    ```C
    typedef enum
    {
        GPIO_PIN_RESET = 0u,    //低電平
        GPIO_PIN_SET            //高電平
    } 
    GPIO_PinState;
    ```

- 範例：

    ```C
    GPIO_PinState res=HAL_GPIO_ReadPin(DONG_IN_1_GPIO_Port,DONG_IN_1_Pin);          //讀取電平
    if(res==GPIO_PIN_RESET)
    {
        HAL_GPIO_WritePin(GPIOA, DONG_OUT_1_Pin|DONG_OUT_2_Pin, GPIO_PIN_SET);      //兩個設定為高電平
    }
    else
    {
        HAL_GPIO_WritePin(GPIOA, DONG_OUT_1_Pin|DONG_OUT_2_Pin, GPIO_PIN_RESET);    //兩個設定為低電平
    }
    ```

**中斷：**

- 以CubeMX設定GPIO

    ![STM32_img02](./doc/Function_STM32/[STM32G4系列]GPIO筆記-CubeMX%20GPIO整理與應用/STM32_img02.png)

    ![STM32_img03](./doc/Function_STM32/[STM32G4系列]GPIO筆記-CubeMX%20GPIO整理與應用/STM32_img03.png)

- GPIO mode:
  - 上升沿觸發檢測的外部中斷模式（External Interrupt Mode with Rising edge trigger detection）
  - 下降沿觸發檢測的外部中斷模式（External Interrupt Mode with Falling edge trigger detectiort）
  - 上升/下降沿觸發檢測的外部中斷模式（External Interrupt Mode with Risinq/Falling edge trigger detection）
  - 上升沿觸發檢測的外部事件模式（External Event Mode with Rising edge trigger detection）
  - 下降沿觸發檢測的外部事件模式（External Event Mode with Falling edge trigger detection）
  - 上升/下降沿觸發檢測的外部事件模式（External Event Mode with Rising/Falling edge trigger detectiont）

- 中斷和事件的區別：
  - **中斷**是當IO達到中斷條件後會向CPU產生中斷請求
  - **事件**是事先設定好的任務，當微控制器達到要求將通過硬體的方式處理事先設定好的任務，而不向CPU請求中斷，比如DMA、AD轉換等

- 範例：

    ```C
    //GPIO中斷回撥函式
    void HAL_GPIO_EXTI_Callback(uint16_t GPIO_Pin){
    //判斷進入中斷的GPIOs
    if(KEY1_Pin==GPIO_Pin){
            HAL_GPIO_TogglePin(GPIOA, DONG_OUT_1_Pin);      //單獨輸出電平取反
            HAL_GPIO_TogglePin(GPIOA,DONG_OUT_2_Pin);       //單獨輸出電平取反
        }
    }
    ```

<h3 id="1.1.3">STM32的HAL庫中GPIO有8種工作模式</h3>

![STM32_img04](./doc/Function_STM32/[STM32G4系列]GPIO筆記-CubeMX%20GPIO整理與應用/STM32_img04.png)

**4種輸入狀態**

1. 浮空輸入模式

   - STM32的引腳狀態是不確定的，此時STM32得到的電平狀態完全取決於GPIO外部的電平狀態，所以說在GPIO外部的引腳懸空時，讀取該埠的電平狀態是個不確定的值。

2. 模擬輸入模式

   - 最常用的場合是ADC模擬輸入，不像其他輸入模式只有0和1，模擬輸入模式可以讀取到很細微變化的值

3. 帶上拉、下拉輸入模式

   - 上下拉的電阻的介紹是電阻阻值都在30-50K之間

   - 因為浮空模式時，在GPIO外部連接的電路未工作時，STM32讀取的GPIO狀態是不確定的，所以可以採用帶上拉或者下拉輸入的模式先給MCU一個確定的狀態，當外部電路電平狀態發生變化時，易於MCU的判斷。

**4種輸出狀態**

1. 推輓輸出模式

   - 指兩個三極體分別受兩個互補信號的控制
   - 總是在一個三極體導通的時候另一個截止
   - 可以輸出高電平，也可以輸出低電平


2. 開漏輸出模式

   - 一般開漏輸出模式時，如果外部不接上拉電阻時，只能輸出低電平
   - 想輸出高電平必須要外接上拉電阻

3. 復用推挽、開漏輸出模式

   - 可以理解為把GPIO配置為第二功能使用的時候的配置，並非單純的用作IO輸入或輸出
   - 使用外設IIC時，我們需要把GPIO配置為復用推輓輸出，用於數據通信功能
   - 串口通信的TX、以及SPI外設的GPIO使用就要把引腳設置為復用開漏輸出



