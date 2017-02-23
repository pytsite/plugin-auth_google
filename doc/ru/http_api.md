# PytSite Google Authentication Driver HTTP API

## POST auth/access-token/google

Обмен Google ID Token на PytSite Access Token.  

- См. [PytSite Authentication HTTP API](https://github.com/pytsite/pytsite/blob/devel/pytsite/auth/doc/ru/http_api.md).
- См. [Google Sign-In](https://developers.google.com/identity/)


### Параметры

- *required* **str** `id_token`: токен, возвращаемый Google после успешной аутентификации на их стороне. 


### Формат ответа

Полностью совпадает с ответом метода [POST auth/access-token](https://github.com/pytsite/pytsite/blob/devel/pytsite/auth/doc/ru/http_api.md#post-authaccess-token)


### Примеры

Запрос:

```
curl -X POST -d id_token=123xyz https://test.com/api/1/auth/access-token/google
```

Ответ:

```
{
    "token": "e51081bc4632d8c2a31ac5bd8080af1b",
    "user_uid": "586aa6a0523af53799474d0d",
    "ttl": 86400,
    "created": "2017-01-25T14:04:35+0200",
    "expires": "2017-01-26T14:04:35+0200"
}
```
