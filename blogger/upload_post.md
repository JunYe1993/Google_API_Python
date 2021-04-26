!['Google.jpg'](https://junye1993.github.io/image/Google.jpg)

## Google Blogger API Table

其實找到好用的 Google API document 就完成 80% 了，這裡紀錄 [Python][blogger_api_python_table] 連結。再紀錄個 Google 給開發者用的 [Playground][google_dev_playground]，可以讓你先試試 API。

## Post article

這裡紀錄程式碼模擬平常的流程，但其實可以只用 insert 就完成所有事。

- **New Post**

    新增草稿。

``` python
    # Create a new draft post.
    # The return value (newpost) is dict contain all info of this draft
    newpost = service.posts().insert(blogId=BLOGID, isDraft=True).execute()
```

- **Update content**

    Update 好 content 後，要轉成 JSON object。以下若程式碼直接傳 JsonPost(str)，會回傳錯誤 Invalid JSON payload received. Unknown name “”: Root element must be a message，即使他們 print 出來一模一樣。

``` python
    # Update some content of the new draft post.
    newpost['title'] = "posted via python"
    newpost['content'] = "<div>hello world test</div>"
    JsonPost = json.dumps(newpost, indent=4, ensure_ascii=False)
    service.posts().update(blogId=BLOGID, postId=newpost['id'], 
        body=json.loads(JsonPost)).execute()
```

- **Publich**

    其實就只是把 Draft 的狀態改成 Publish。

``` python
    # Publish the new post.
    service.posts().publish(blogId=BLOGID, postId=newpost['id']).execute()
```

- **Insert 解決一切**

    可以直接用 insert 就好，上面的程式碼只是模擬。

``` python
    service.posts().insert(blogId=BLOGID, body=body).execute()
```
    
參考資料 :

1.[Google API Library][blogger_api_python_table]

[blogger_api_python_table]: https://developers.google.com/resources/api-libraries/documentation/blogger/v3/python/latest/index.html
[google_dev_playground]: https://developers.google.com/oauthplayground/