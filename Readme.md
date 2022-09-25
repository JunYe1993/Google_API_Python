!['Google.jpg'](https://junye1993.github.io/image/Google.jpg)

## Google API - python ver.

紀錄一些使用 python 呼叫 Google API 的心得

## 基本前置作業

- **Google Account**

    首先你要有 [google][Create_Account] 帳號。

- **Google Cloud Platform project**

    想要使用 Google Cloud Platform (GCP) 的 service，你需要創建一個 [GCP project][Create_GCP_Project]。左上角 project name 右邊的倒三角按下去新增。

- **Enable API**

    旁邊的 API&Services => Library => 新增你想要的服務。不過我當初沒有用這步，應該是我用 Oauth 而非 API Keys 的關係 ( [完整介紹][Guides_Create_Project] )。

- **Credentials**

    產生金鑰，我是選 Desktop App，然後下載其 json 檔就樣就好。雖然 [Google Guide][Guides_Create_Credentials] 其實有給很多講解及步驟，但我沒做也能運行。

## 安裝 google python api library

- **安裝 google api python**

    首先安裝 [google-api-python-client][Google_API_python_Git]，點進去有安裝方法，這裡用 Linux 做些紀錄。基本上是安裝一個 virtualenv，讓他新增一個獨立且乾淨的 python 執行環境，然後利用這虛擬環境去下載他門的 library。

``` bash
    # 安裝虛擬 python 環境和 google-api-python-client
    pip install virtualenv
    virtualenv <your-env>
    source <your-env>/bin/activate
    <your-env>/bin/pip install google-api-python-client
```

``` bash
    # windows (2022/09/25 note)
    pip install virtualenv
    python -m virtualenv <your-env>
    <your-env>\Scripts\activate
    <your-env>\Scripts\pip.exe install google-api-python-client
```

- **安裝 google_auth_oauthlib**

    再來安裝 [Oauth 2.0][Google_API_Oauth_Git]。

``` bash
    <your-env>/bin/pip install google_auth_oauthlib
```

## 安裝 google python api library

我寫這篇的主因，因為 google python api library 已經不再更新，有些 sample code 已經過時不能使用所以在這裡紀錄一些可用的 sample code。

- **Sample Code - flow**

    這是 [Google Oauth API Scope][Google_API_Oauth_Scope] 我拿 blogger 做測試。完整的程式碼在 [sample.py](/sample.py)，輸出結果在 [output.json](/output.json)。這裡擷取片段，順序還要參考完整的程式碼。

``` python
    # 首先是連線設置，Flow 這個 class 是用來讀取你的 Credentials 來認證你的程式。
    # client_secrets.json = 你下載的 Oauth json file。
    # SCOPES = 你宣告要使用哪些功能 ( ex. gmail, blogger... )
    from google_auth_oauthlib.flow import InstalledAppFlow
    SCOPES = ['https://www.googleapis.com/auth/blogger']
    flow = InstalledAppFlow.from_client_secrets_file(
        'client_secrets.json', SCOPES)

    # 用 port 0 連線 GCP，這裡會用預設瀏覽器去做認證，結束後會跟你說可以關閉網頁
    creds = flow.run_local_server(port=0)
```

- **Sample Code - token**

    這裡回傳值 creds，是 GCP 給的暫時性 token，若你的 token 還在且未過期，你就可以用此 token 直接連線而不用再透過瀏覽器認證。

``` python
    # 如果你有儲存 token，可以直接用 token 重新連線
    # token expired 的話且沒過太就的話可以用 creds.refresh(Request()) 做 refresh token
    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds.valid:
        if creds.expired and creds.refresh_token:
            creds.refresh(Request())
```

- **Sample Code - build**

    這裡依照 [Blogger API Guide][Google_API_Blogger_Guide] 去做取資料。

``` python
    # 先依照 scope 取得服務，再依照 api 的格式去取得資料
    # posts() 跟 list() 都是依照 Blogger API Guide 去填寫的，最後執行 execute()
    # 回傳會是 dict，要自己轉 json
    from googleapiclient.discovery import build
    service = build('blogger', 'v3', credentials=creds)
    posts = service.posts().list(blogId=BLOGID,maxResults=3).execute()
```

參考資料 :

1.我跟Google官網

[Create_Account]: https://www.google.com/account/about/
[Create_GCP_Project]: https://console.cloud.google.com/
[Guides_Create_Project]: https://developers.google.com/workspace/guides/create-project
[Guides_Create_Credentials]: https://developers.google.com/workspace/guides/create-credentials
[Google_API_python_Git]: https://github.com/googleapis/google-api-python-client
[Google_API_Oauth_Git]: https://github.com/googleapis/google-api-python-client/blob/master/docs/oauth.md
[Google_API_Oauth_Scope]: https://developers.google.com/identity/protocols/oauth2/scopes
[Google_API_Blogger_Guide]: https://developers.google.com/blogger/docs/3.0/getting_started