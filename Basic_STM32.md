

# 目錄

- [Note](#0)
- [初識STM32](#1)
  - [STM32與Arduino的差異](#1.1)
    - [單晶片](#1.1.1)
  - [STM32 命名方法](#1.2)
- [STM32CubeIDE安裝以及環境設定](#2)
  - [CubeIDE簡介](#2.1)
  - [下載+安裝流程](#2.2)
  - [IDE閱覽](#2.3)
- [使用STM32CubeIDE](#3)
  - [程式碼導讀](#3.1)
  - [好用小工具 - 現場表達式 (live expression)](#3.2)
  - [好用小工具 - Memory](#3.3)
- [GPIO輸入輸出(上)](#4)
  - [腳位](#4.1)
  - [ioc檔](#4.2)
- [GPIO輸入輸出(中)](#5)




<h1 id="0">Note</h1>

- https://ithelp.ithome.com.tw/users/20141525/ironman/4839

<h1 id="1">初識STM32</h1>

- STM32系列是專為需要高效能、低功耗的嵌入式系統所專門設計的**ARM Cortex核心**

<h2 id="1.1">STM32與Arduino的差異</h2>

- STM32與Arduino都是屬於**單晶片**

- STM32擁有更多的功能：
  - STM32的TIMER有encoder mode，可以將方波直接做處理，對於馬達控制非常方便
  - Arduino是一個開源的電子開發原型平台。其包含硬體開發版和軟體IDE和各種開發生態。所以Arduino是一個集合了硬件和軟件的綜合體。而它上面的微控器是ATmega328p

- 兩者的定位不同：
  - Arduino對**硬體底層做了大量的封裝**，適合給初學者使用：
    - 例如機器人的開發測試：你要測試氣壓感測器的輸出值時，使用Arduino 的analogRead()，會比你用STM32的ADC功能來的快多了
  - 當需求更大時，包括對計算速度以及硬體操縱的要求更嚴苛的時候，STM32就會比Arduino更適合你。

<h3 id="1.1.1">單晶片</h3>

- 單晶片，全稱**單晶片微電腦**，又稱**微控制器單元（microcontroller unit）**，是把中央處理器、儲存器、定時/計數器（timer/counter）、各種輸入輸出介面等都整合在一塊積體電路晶片上的微型計算機。

- 與應用在個人電腦中的通用型微處理器相比，它更強調自供應（不用外接硬體）和節約成本。

- 它的最大優點是體積小，可放在儀表內部，但儲存量小，輸入輸出介面簡單，功能較低。

- 由於單晶片微電腦常用於當控制器故又名single chip microcontroller。台灣稱為「單晶片」；中國則主要採用「單片機」，英文縮寫為**MCU (Microcontroller Unit)**。

<h2 id="1.2">STM32 命名方法</h2>

- STM32F429ZI 開發版

    ![STM32_img00](./doc/初識STM32/STM32_img00.jpg)

- 命名表

    ![STM32_img01](./doc/初識STM32/STM32_img01.jpg)

  - Code size - 快閃記憶體(Flash memory)大小

<h1 id="2">STM32CubeIDE安裝以及環境設定</h1>

<h2 id="2.1">CubeIDE簡介</h2>

- STM32CubeIDE可以自動的幫你把腳位的配置生成程式碼，只要用圖形化的介面點一點，就不用自己打一堆，而且他還有很棒的變數監看的功能以及直接更改記憶體值的方式，總之對於新手來說是很方便的。

<h2 id="2.2">下載+安裝流程</h2>

[下載與安裝流程](https://ithelp.ithome.com.tw/articles/10265758#:~:text=%E9%81%8E%E5%85%B6%E4%BB%96%E7%9A%84...-,%E4%B8%8B%E8%BC%89%2B%E5%AE%89%E8%A3%9D%E6%B5%81%E7%A8%8B,-%E8%BB%9F%E9%AB%94%E7%9A%84%E5%AE%89%E8%A3%9D)

[Integrated Development Environment for STM32](https://www.st.com/en/development-tools/stm32cubeide.html)

- 必須在英文路徑下才能執行安裝檔(.exe)

<h2 id="2.3">IDE閱覽</h2>

- 開啟STM32CubeIDE，點擊左上角開啟新的STM32專案

    ![STM32_img00](./doc/STM32CubeIDE安裝/STM32_img00.jpg)

- 搜尋使用的開發版

    ![STM32_img01](./doc/STM32CubeIDE安裝/STM32_img01.jpg)

- 設定你的專案名稱

    ![STM32_img02](./doc/STM32CubeIDE安裝/STM32_img02.jpg)

- 如果有跳出這個畫面，就放心的按Yes，然後就會開始初始化，準備開啟檔案了，可能需要一下子

    ![STM32_img03](./doc/STM32CubeIDE安裝/STM32_img03.jpg)

- 左邊的Project Elplorer就是我們進行專案管理的地方，點擊 Core -> Src -> main.c 打開這個.c檔，以後我們就要在這裡寫程式

- 如果開啟後沒有出現可以從上面Window -> Short View -> Project Elplorer打開這個小視窗，其他有些視窗如果不小心手殘被關掉，也可以在這裡打開畫面右邊和底下是程式碼大綱以及一些監控視窗

    ![STM32_img04](./doc/STM32CubeIDE安裝/STM32_img04.jpg)

<h1 id="3">使用STM32CubeIDE</h1>

<h2 id="3.1">程式碼導讀</h2>

- CubeIDE可以把我們對於腳位的配置自動生成程式碼，我們只需要在filename.ioc(filename為專案名稱)點一點，儲存後他就會自動生成程式碼了。

- IDE怎麼知道要將自動生成的程式碼放在哪呢?實際上程式已經將程式碼做初步的分類，以下是程式碼最上面的幾行：

    ```C
    /* Includes ------------------------------------------------------------------*/
    #include "main.h"

    /* Private includes ----------------------------------------------------------*/
    /* USER CODE BEGIN Includes */

    /* USER CODE END Includes */

    /* Private typedef -----------------------------------------------------------*/
    /* USER CODE BEGIN PTD */

    /* USER CODE END PTD */

    /* Private define ------------------------------------------------------------*/
    /* USER CODE BEGIN PD */
    /* USER CODE END PD */
    ```

  - 每個類別的開頭都會有長長的虛線，由上到下依序是**Includes**、**Private Includes**、**Private typedef**、**Private define**。
  - 只要該類別是Private開頭的話，後面一定會有**USER CODE BEGIN**與**USER CODE END**這兩個註解，我們的程式碼就需要寫在這裡，而生成程式碼時就會安插在這個區間以外的地方。
  - 很重要的就是你的程式碼一定要放在BEGIN和END之間，否則只要你一生成程式碼，那你的程式碼就會不見了。

    ```C
    /* Private define ------------------------------------------------------------*/
    /* USER CODE BEGIN PD */
    #define PI 3.14159265358
    /* USER CODE END PD */
    ```

<h2 id="3.2">好用小工具 - 現場表達式 (live expression)</h2>

- 變數監測的小視窗，但他只能對**全域變數**(沒有被任何大括號框住的變數)進行監測

- 是一個debug的工具，因此正常執行的情況下式是不能使用的，需要點選工具列那排小蟲蟲的圖示以debug的方式執行(快捷鍵為F11)，執行的時候可能會產生一些視窗提醒，都按Yes即可。

- 在上面工具列那排的Window->Short View->現場表達式，就會出現在右邊的小視窗

    ![STM32_img00](./doc/使用STM32CubeIDE/STM32_img00.jpg)

- 接下來你會看到你的程式碼停在main函式裡面的第一行，在我這裡的情況下是`HAL_Init()`這一行

    ![STM32_img01](./doc/使用STM32CubeIDE/STM32_img01.jpg)

- 非常重要!!!這個時候你的程式碼還沒有開始執行，需要**按F8才會開始執行**

**實際使用看看這個功能：**

- 要記得在全域的地方新增變數 i, HAL_Delay()，單位為ms

- 用debug的方式執行，並在現場表達式的視窗內增加新表達式，就可以看到 i 每隔一秒增加1了

- 可以直接打上&var(var為你要監測的變數)，這樣可以直接獲取這個變數的記憶體位置

    ```C
    /* Infinite loop */
    /* USER CODE BEGIN WHILE */
    while (1)
    {
    /* USER CODE END WHILE */

    /* USER CODE BEGIN 3 */
        i++;
        HAL_Delay(1000);

    }
    /* USER CODE END 3 */
    ```

<h2 id="3.3">好用小工具 - Memory</h2>

- 這個工具的目的是取代Arduino的序列阜的功能，由於STM32並沒有提供人和單晶片溝通的介面，我們在測試的過程中經常會需要調整參數，因此就需要頻繁的上傳程式，而用這個功能就可以直接更改變數的值。

- **變數是存放在RAM當中，因此我們這個動作就是直接更改RAM的數值**

- 一樣是在debug的模式下才可以使用，預設會在底下的視窗，若沒有出現一樣可以從 `Window->Short View->Memory` 裡面找到。

- 首先點綠色的+新增一個你要監測的記憶體位置

    ![STM32_img02](./doc/使用STM32CubeIDE/STM32_img02.jpg)

    ![STM32_img03](./doc/使用STM32CubeIDE/STM32_img03.jpg)

- 接著右邊就會跑出許多框框，預設會是用Hex(十六進位)來表達記憶體的值。右邊New Renderings的地方新增你要解讀這個記憶體的方式

**實際使用看看這個功能：**

- 在全域的地方宣告一個變數x，並用現場表達式的方式獲取他的記憶體位置，以我來說，x這個變數放在0x20000028這個位置(不過實際上是0x20000028~0x2000002B，因為int是四個bytes嘛)

    ![STM32_img04](./doc/使用STM32CubeIDE/STM32_img04.jpg)

- 接著就按照上面的步驟新增要監看的記憶體位置

    ![STM32_img05](./doc/使用STM32CubeIDE/STM32_img05.jpg)

- 選擇Signed Integer作為解讀的方式

    ![STM32_img06](./doc/使用STM32CubeIDE/STM32_img06.jpg)

- 就可以順利看到0x20000028~0x2000002B的值啦，並且會以int的方式解讀

    ![STM32_img07](./doc/使用STM32CubeIDE/STM32_img07.jpg)

- 我們可以直接更改這個位置的值，直接點你要更改的記憶體位置，輸入新的值就OK了，順便使用現場表達式來確認這個值是否順利地被更動了。我順利的將x更改為31415926~

    ![STM32_img08](./doc/使用STM32CubeIDE/STM32_img08.jpg)

<h1 id="4">GPIO輸入輸出(上)</h1>

- GPIO全稱為General-purpose input/output，通用型之輸入輸出的簡稱，可以供使用者**對腳位進行輸入輸出的操作**。

<h2 id="4.1">腳位</h2>

- 單晶片不外乎就是對各個腳位做輸入輸出來控制馬達、接收訊號等

- 針腳分成內側與外側兩個部分，外側的腳位比較簡單，直接翻到板子的背面就可以看到每個腳位的編號了，而內側的腳位名稱需要查表，看的是紅色箭頭所標示的名稱，未標示的為Arduino的腳位，因為這塊開發版是一塊兼容Arduino的板子，因此他也寫上了對應到Arduino的腳位。

    ![STM32_img00](./doc/GPIO輸入輸出(上)/STM32_img00.jpg)

    ![STM32_img01](./doc/GPIO輸入輸出(上)/STM32_img01.jpg)

<h2 id="4.2">ioc檔</h2>

- 設定**腳位配置的圖形化介面**，在左側檔案管理的地方找到filename.ioc(filename為專案名稱)，點擊兩下就會打開。打開後一出現的就是STM32F429ZI單晶片的樣子，我們可以看到他總共有144個腳位

- 右下角的放大鏡可以輸入腳位名稱搜尋，例如輸入PB8對應到的腳位就會閃黑色

    ![STM32_img02](./doc/GPIO輸入輸出(上)/STM32_img02.jpg)

- 點擊選擇**GPIO_Output**這個模式，就順利的將這個腳位設為輸出模式了

- 如果想要復原，則可以選擇**Reset_State**這個模式，這也有可能需要一點時間，看到腳位就會變綠色就代表成功設定完成

    ![STM32_img03](./doc/GPIO輸入輸出(上)/STM32_img03.jpg)

- 只要有更動，且還沒有儲存，上面檔案這邊就會顯示" * "，這個時候按ctrl+s就可以順利儲存

    ![STM32_img04](./doc/GPIO輸入輸出(上)/STM32_img04.jpg)

- 如果有遇到詢問的視窗都一律按Yes，可以打勾，下次就不會再出現提醒了。

    ![STM32_img05](./doc/GPIO輸入輸出(上)/STM32_img05.jpg)

    ![STM32_img06](./doc/GPIO輸入輸出(上)/STM32_img06.jpg)

- 最後回到main.c檔案，往下滑我們可以發現自動新增一些程式碼，這段程式碼的功能是將GPIO初始化，這也就是STMCubeIDE這個IDE好用的地方，可以自動產生代碼

    ```C
    /**
    * @brief GPIO Initialization Function
    * @param None
    * @retval None
    */
    static void MX_GPIO_Init(void)
    {
        GPIO_InitTypeDef GPIO_InitStruct = {0};

        /* GPIO Ports Clock Enable */
        __HAL_RCC_GPIOB_CLK_ENABLE();

        /*Configure GPIO pin Output Level */
        HAL_GPIO_WritePin(GPIOB, GPIO_PIN_8, GPIO_PIN_RESET);

        /*Configure GPIO pin : PB8 */
        GPIO_InitStruct.Pin = GPIO_PIN_8;
        GPIO_InitStruct.Mode = GPIO_MODE_OUTPUT_PP;
        GPIO_InitStruct.Pull = GPIO_NOPULL;
        GPIO_InitStruct.Speed = GPIO_SPEED_FREQ_LOW;
        HAL_GPIO_Init(GPIOB, &GPIO_InitStruct);

    }
    ```

<h1 id="5">GPIO輸入輸出(中)</h1>



