## Spring Security

### OAuth 2.0 Authorization Server

TokenEndpointAuthenticationFilter

AuthorizationEndpoint       /oauth/authorize
WhitelabelApprovalEndpoint  /oauth/confirm_access
WhitelabelErrorEndpoint     /oauth/error
TokenEndpoint               /oauth/token   
CheckTokenEndpoint          /oauth/check_token
TokenKeyEndpoint            /oauth/token_key

RedirectResolver

### OAuth 2.0 Resource Server

BasicAuthenticationFilter(Basic认证)                  Authorization: Basic QWxhZGRpbjpvcGVuIHNlc2FtZQ==
AbstractUserDetailsAuthenticationProvider

OAuth2AuthenticationProcessingFilter(OAuth2认证)      Authorization: Bearer 011bb863-f998-4285-8b8a-6ef62972d893
OAuth2AuthenticationManager

UsernamePasswordAuthenticationFilter

ResourceServerTokenServices                         RemoteTokenServices

DefaultLoginPageGeneratingFilter            默认登录页生成拦截器

FilterSecurityInterceptor
http://localhost:8081/oauth/authorize?response_type=code&client_id=client&scope=user&redirect_uri=http://www.baidu.com
LoginUrlAuthenticationEntryPoint

AbstractAuthenticationTargetUrlRequestHandler

FilterChainProxy

#### /oauth/authorize未登录

#### /oauth/authorize已登录

AuthorizationEndpoint.authorize()
AbstractRememberMeServices

SecurityContextPersistenceFilter

#### /login

Spring Security原理: http://blog.sina.com.cn/s/blog_5c0522dd0101doey.html

### Spring Security过滤器

FilterChainProxy

SecurityContextPersistenceFilter
LogoutFilter
UsernamePasswordAuthenticationFilter
DefaultLoginPageGeneratingFilter
DefaultLogoutPageGeneratingFilter
AnonymousAuthenticationFilter
SessionManagementFilter
FilterSecurityInterceptor

SavedRequestAwareAuthenticationSuccessHandler
RequestCacheAwareFilter

### OAuth2接口

#### /oauth/authorize

GET http://localhost:6700/oauth/authorize?response_type=code&client_id=client&scope=user&state=test&redirect_uri=http://www.baidu.com

https://www.baidu.com/?code=ZkaoN2&state=test

#### /oauth/token获取Token

POST /oauth/token

grant_type: authorization_code
client_id: client
client_secret: 111111
code: yD49kM
redirect_uri: http://www.baidu.com

#### /oauth/token刷新Token

POST /oauth/token

grant_type: refresh_token
client_id: client
client_secret: 111111
refresh_token: 264aa935-d257-47a5-bb9f-46190b24ab0f
scope: user

```json
{
  // token
 "access_token": "264aa935-d257-47a5-bb9f-46190b24ab0f",
  // token类型
 "token_type": "bearer",
  // refresh_token，用于刷新token
 "refresh_token": "28f3fd55-85f3-4091-9055-35eb430fd3da",
  // token有效期，单位秒
 "expires_in": 299,
  // 权限范围
 "scope": "user"
}
```

#### 请求资源

?access_token=b6e9d952-d5ba-481d-871a-5af43f8ee4fb

Authorization: Bearer 011bb863-f998-4285-8b8a-6ef62972d893

### Spring Security实战

* client
    * ClientDetailsService: ThreadLocal缓存 + redis缓存 + jdbc
* code
    * AuthorizationCodeServices: redis存储
* token
    * TokenStore: redis存储
* 上下文
    * SecurityContextRepository: 默认session实现，替换为cookie + redis实现
* 用户
    * UserDetailsService
* zuul网关
    * zuul.sensitiveHeaders: 设置为空，默认过滤Cookie、Set-Cookie、Authorization
* 自定义登录页
    * .formLogin().successHandler(): 用户认证成功处理，跳转/oauth/authorize
        * AuthenticationSuccessHandler: 解析header中的referer，跳转到referer参数指定的url
    * .formLogin().failureHandler(): 用户认证失败处理，跳转登录页面
        * AuthenticationFailureHandler: 解析header中的referer，跳转登录页带上referer参数
    * .exceptionHandling().authenticationEntryPoint(): /oauth/authorize，匿名用户无权限访问处理，跳转登录页面
        * AuthenticationEntryPoint: 自定义，跳转登录页带上referer参数

https://blog.csdn.net/ejinxian/article/details/47313539


[<< 上一篇: Spring-MVC](7-开源框架/Spring-MVC.md)

[>> 下一篇: Spring](7-开源框架/Spring.md)
