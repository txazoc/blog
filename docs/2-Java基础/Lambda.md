## Lambda

### Lambda实现原理

```java
public class LambdaGenarateTest {

    public static void main(String[] args) {
        // 导出生成的内部类到指定目录
        System.setProperty("jdk.internal.lambda.dumpProxyClasses", "/Users/txazo/TxazoProject/java/target/classes");
        // Lambda表达式
        Calculater left = (a, b) -> a;
        left.calculate(1, 2);
        // 方法引用
        Calculater right = LambdaGenarateTest::right;
        right.calculate(1, 2);
    }

    private static int right(int a, int b) {
        return b;
    }

    @FunctionalInterface
    private interface Calculater {

        int calculate(int a, int b);

    }

}
```

Lambda表达式`(a, b) -> a`对应的内部类:

```java
final class LambdaGenarateTest$$Lambda$1 implements LambdaGenarateTest.Calculater {

    @LambdaForm.Hidden
    public int calculate(int var1, int var2) {
        return LambdaGenarateTest.lambda$main$0(var1, var2);
    }

}
```

方法引用`LambdaGenarateTest::right`对应的内部类:

```java
final class LambdaGenarateTest$$Lambda$2 implements LambdaGenarateTest.Calculater {

    @LambdaForm.Hidden
    public int calculate(int var1, int var2) {
        return LambdaGenarateTest.right(var1, var2);
    }

}
```

反编译`LambdaGenarateTest`:

```linux
javap -p LambdaGenarateTest.class
```

```console
Compiled from "LambdaGenarateTest.java"
public class org.txazo.jdk8.lambda.LambdaGenarateTest {
  public org.txazo.jdk8.lambda.LambdaGenarateTest();
  public static void main(java.lang.String[]);
  private static int right(int, int);
  private static int lambda$main$0(int, int);
}
```

可以看到，`LambdaGenarateTest`类多了一个`lambda$main$0`方法

继续反编译:

```linux
javap -v LambdaGenarateTest.class
```

```console
public class org.txazo.jdk8.lambda.LambdaGenarateTest

  public static void main(java.lang.String[]);
    Code:
         8: invokedynamic #5,  0              // InvokeDynamic #0:calculate:()Lorg/txazo/jdk8/lambda/LambdaGenarateTest$Calculater;
        17: invokeinterface #6,  3            // InterfaceMethod org/txazo/jdk8/lambda/LambdaGenarateTest$Calculater.calculate:(II)I
        23: invokedynamic #7,  0              // InvokeDynamic #1:calculate:()Lorg/txazo/jdk8/lambda/LambdaGenarateTest$Calculater;
        32: invokeinterface #6,  3            // InterfaceMethod org/txazo/jdk8/lambda/LambdaGenarateTest$Calculater.calculate:(II)I

BootstrapMethods:
  0: #41 invokestatic java/lang/invoke/LambdaMetafactory.metafactory:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;
    Method arguments:
      #42 (II)I
      #43 invokestatic org/txazo/jdk8/lambda/LambdaGenarateTest.lambda$main$0:(II)I
      #42 (II)I
  1: #41 invokestatic java/lang/invoke/LambdaMetafactory.metafactory:(Ljava/lang/invoke/MethodHandles$Lookup;Ljava/lang/String;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodType;Ljava/lang/invoke/MethodHandle;Ljava/lang/invoke/MethodType;)Ljava/lang/invoke/CallSite;
    Method arguments:
      #42 (II)I
      #46 invokestatic org/txazo/jdk8/lambda/LambdaGenarateTest.right:(II)I
      #42 (II)I
```

可以看到，Lambda表达式和方法引用的字节码指令为`invokedynamic`，然后`invokedynamic`指令执行时会调用`LambdaMetafactory`的`metafactory`方法

```java
public class LambdaMetafactory {

    public static CallSite metafactory(
            MethodHandles.Lookup caller,
            String invokedName,
            MethodType invokedType,
            MethodType samMethodType,
            MethodHandle implMethod,
            MethodType instantiatedMethodType)
            throws LambdaConversionException {
        AbstractValidatingLambdaMetafactory mf;
        mf = new InnerClassLambdaMetafactory(caller, invokedType,
                invokedName, samMethodType,
                implMethod, instantiatedMethodType,
                false, EMPTY_CLASS_ARRAY, EMPTY_MT_ARRAY);
        mf.validateMetafactoryArgs();
        return mf.buildCallSite();
    }

}
```

* caller: 调用类
* invokedName: 函数式接口的方法名
* implMethod: Lambda表达式生成的内部方法`org/txazo/jdk8/lambda/LambdaGenarateTest.lambda$main$0`或方法引用对应的方法`org/txazo/jdk8/lambda/LambdaGenarateTest.sub`

经过上面的分析，Lambda的等价形式如下:

```java
public class LambdaGenarateTest {

    public static void main(String[] args) {
        // 导出生成的内部类到指定目录
        System.setProperty("jdk.internal.lambda.dumpProxyClasses", "/Users/txazo/TxazoProject/java/target/classes");
        // Lambda表达式
        Calculater left = new LambdaGenarateTest$$Lambda$1();
        left.calculate(1, 2);
        // 方法引用
        Calculater right = new LambdaGenarateTest$$Lambda$2();
        right.calculate(1, 2);
    }

    private static int lambda$main$0(int a, int b) {
        return a;
    }

    private static int right(int a, int b) {
        return b;
    }

    @FunctionalInterface
    private interface Calculater {

        int calculate(int a, int b);

    }

    final static class LambdaGenarateTest$$Lambda$1 implements LambdaGenarateTest.Calculater {

        @LambdaForm.Hidden
        public int calculate(int var1, int var2) {
            return LambdaGenarateTest.lambda$main$0(var1, var2);
        }

    }

    final static class LambdaGenarateTest$$Lambda$2 implements LambdaGenarateTest.Calculater {

        @LambdaForm.Hidden
        public int calculate(int var1, int var2) {
            return LambdaGenarateTest.right(var1, var2);
        }

    }

}
```

最后，总结下Lambda表达式的执行过程:

* javac编译时将Lambda表达式转换为内部方法，方法引用略过
* 执行`invokedynamic`指令
* 调用`LambdaMetafactory`的`metafactory`方法
    * `asm`生成匿名内部类，实现对应的函数式接口
    * 匿名内部类实例化
* 调用匿名内部类对象的函数式接口方法
    * Lambda表达式: 调用Lambda表达式转换后的内部方法
    * 方法引用: 调用方法引用对应的方法
