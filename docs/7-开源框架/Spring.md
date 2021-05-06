## Spring

### Spring IOC

#### IOC原理

* refresh()
* 创建BeanFactory
* 加载BeanDefinition
    * `Map<String, BeanDefinition> beanDefinitionMap`
    * 解析并注册BeanDefinition
* Bean预实例化(非lazy-init)
    * `createBeanInstance`: 实例化Bean
        * InstantiationAwareBeanPostProcessor.postProcessBeforeInstantiation()
        * 反射创建Bean
        * addSingletonFactory: 处理循环依赖
        * InstantiationAwareBeanPostProcessor.postProcessAfterInstantiation()
    * `populateBean`: ioc依赖注入
        * InstantiationAwareBeanPostProcessor.postProcessPropertyValues()
            * inject
    * `initializeBean`: 初始化Bean
        * Aware
            * Aware.setBeanName()
            * BeanClassLoaderAware.setBeanClassLoader()
            * BeanFactoryAware.setBeanFactory()
        * BeanPostProcessor.postProcessBeforeInitialization()
            * `@PostConstruct`
        * `afterPropertiesSet()`
        * `init-method`
        * BeanPostProcessor.postProcessAfterInitialization()

#### 扩展接口

* ```FactroyBean```
* ```BeanPostProcessor```
* ```InstantiationAwareBeanPostProcessor```
* ```BeanFactoryPostProcessor```
* ```Aware```
* ```InitializingBean```

#### @Autowired/@Resource

* @Autowired: AutowiredAnnotationBeanPostProcessor
    * byType
    * 有多个，@Primary
    * @Qualifier: byType + byName
* @Resource: CommonAnnotationBeanPostProcessor
    * @Resource(name, type): byName + byType
    * @Resource(name): byName
    * @Resource(type): byType
    * @Resource: 先fieldName，后classType

#### 循环依赖

* `构造器的循环依赖没法解决`
* 三级缓存: DefaultSingletonBeanRegistry
    * singletonObjects: Map<String, Object>: 单例Bean缓存
    * earlySingletonObjects: Map<String, Object>: 早期的单例Bean缓存
    * singletonFactories: Map<String, ObjectFactory<?>>: 单例工厂缓存

```java
protected Object getSingleton(String beanName, boolean allowEarlyReference) {
    Object singletonObject = this.singletonObjects.get(beanName);
    if (singletonObject == null && isSingletonCurrentlyInCreation(beanName)) {
        // 单例Bean当前在创建中
        synchronized (this.singletonObjects) {
            singletonObject = this.earlySingletonObjects.get(beanName);
            if (singletonObject == null && allowEarlyReference) {
                ObjectFactory<?> singletonFactory = this.singletonFactories.get(beanName);
                if (singletonFactory != null) {
                    singletonObject = singletonFactory.getObject();
                    this.earlySingletonObjects.put(beanName, singletonObject);
                    this.singletonFactories.remove(beanName);
                }
            }
        }
    }
    return (singletonObject != NULL_OBJECT ? singletonObject : null);
}
```

### Spring AOP

> Aspect Oriented Programming，面向切面编程

#### 切入点Pointcut

* execution: 方法
* args: 方法参数
* @args: 方法参数注解
* @annotation: 方法注解
* ...

```java
public interface Pointcut {

    // 类过滤器
    ClassFilter getClassFilter();

    // 方法匹配器
    MethodMatcher getMethodMatcher();

}
```

类过滤器，参考`AspectJExpressionPointcut`

```java
public interface ClassFilter {

    boolean matches(Class<?> clazz);

}
```

方法匹配器，参考`AspectJExpressionPointcut`

```java
public interface MethodMatcher {

    boolean isRuntime();

    boolean matches(Method method, Class<?> targetClass);

    boolean matches(Method method, Class<?> targetClass, Object... args);

}
```

#### 增强Advice

* 前置增强: MethodBeforeAdvice
* 环绕增强: MethodInterceptor
* 异常增强: ThrowsAdvice
* 后置增强: AfterReturningAdvice
* 引介增强: IntroductionInterceptor

#### 切面Aspect

```切面Aspect = 切入点Pointcut + 增强Advice```，即在哪些地方(切入点)执行哪些逻辑(增强)

#### AOP代理

* JDK动态代理: JdkDynamicAopProxy
* CGLib动态代理: ObjenesisCglibAopProxy

#### AOP代理实现

```java
public class ReflectiveMethodInvocation implements ProxyMethodInvocation, Cloneable {

    // 当前拦截器的索引
    private int currentInterceptorIndex = -1;
    // 拦截器列表(包括动态方法匹配器)
    protected final List<?> interceptorsAndDynamicMethodMatchers;

    @Override
    public Object proceed() throws Throwable {
        if (this.currentInterceptorIndex == this.interceptorsAndDynamicMethodMatchers.size() - 1) {
            // 拦截器列表调用完, 调用连接点的方法
            return invokeJoinpoint();
        }

        // currentInterceptorIndex自加1, 职责链模式
        Object interceptorOrInterceptionAdvice = this.interceptorsAndDynamicMethodMatchers.get(++this.currentInterceptorIndex);
        if (interceptorOrInterceptionAdvice instanceof InterceptorAndDynamicMethodMatcher) {
            // 动态方法匹配器的处理逻辑, 此处略过
        } else {
            // 调用拦截器
            return ((MethodInterceptor) interceptorOrInterceptionAdvice).invoke(this);
        }
    }

}
```

前置增强拦截器:

```java
public class MethodBeforeAdviceInterceptor implements MethodInterceptor, Serializable {

    private MethodBeforeAdvice advice;

    public MethodBeforeAdviceInterceptor(MethodBeforeAdvice advice) {
        this.advice = advice;
    }

    @Override
    public Object invoke(MethodInvocation invocation) throws Throwable {
        this.advice.before(invocation.getMethod(), invocation.getArguments(), invocation.getThis());
        return invocation.proceed();
    }

}
```

后置增强拦截器:

```java
public class AfterReturningAdviceInterceptor implements MethodInterceptor, AfterAdvice, Serializable {

    private final AfterReturningAdvice advice;

    public AfterReturningAdviceInterceptor(AfterReturningAdvice advice) {
        this.advice = advice;
    }

    @Override
    public Object invoke(MethodInvocation invocation) throws Throwable {
        Object result = invocation.proceed();
        this.advice.afterReturning(result, invocation.getMethod(), invocation.getArguments(), invocation.getThis());
        return result;
    }

}
```

异常增强拦截器:

```java
public class ThrowsAdviceInterceptor implements MethodInterceptor, AfterAdvice {

    private final Object throwsAdvice;

    @Override
    public Object invoke(MethodInvocation invocation) throws Throwable {
        try {
            return invocation.proceed();
        } catch (Throwable ex) {
            Method handlerMethod = getExceptionHandler(ex);
            if (handlerMethod != null) {
                invokeHandlerMethod(invocation, ex, handlerMethod);
            }
            throw ex;
        }
    }

}
```

### Spring中的设计模式

#### 工厂模式

BeanFactory

#### 单例模式

singleton bean

#### 模版方法模式

#### 观察者模式

Spring事件监听

#### 适配器模式

#### 装饰器模式


#### Spring事务传播机制

* 外部有事务，内部以单独事务方式执行，`PROPAGATION_REQUIRES_NEW`
* 外部有事务，内部以事务方式执行，`PROPAGATION_REQUIRED`
* 外部有事务，内部以非事务方式执行，挂起外部事务，`PROPAGATION_NOT_SUPPORTED`
* 外部有事务，内部以非事务方式执行，抛出异常，`PROPAGATION_NEVER`
* 外部无事务，内部以事务方式执行，`PROPAGATION_REQUIRED`


[<< 上一篇: MyBatis](7-开源框架/MyBatis.md)

[>> 下一篇: Spring-Boot](7-开源框架/Spring-Boot.md)
