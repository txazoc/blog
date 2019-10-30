## 四数相加

给定四个包含整数的数组列表 A , B , C , D ,计算有多少个元组 (i, j, k, l) ，使得 A[i] + B[j] + C[k] + D[l] = 0。

```java
public class FourSumCount {

    public static int fourSumCount(int[] a, int[] b, int[] c, int[] d) {
        Map<Integer, Integer> map = new HashMap<>();

        int sum = 0;
        for (int i : a) {
            for (int j : b) {
                sum = i + j;
                if (map.containsKey(sum)) {
                    map.put(sum, map.get(sum) + 1);
                } else {
                    map.put(sum, 1);
                }
            }
        }

        int count = 0;
        for (int i : c) {
            for (int j : d) {
                sum = -(i + j);
                if (map.containsKey(sum)) {
                    count += map.get(sum);
                }
            }
        }

        return count;
    }

    public static void main(String[] args) {
        System.out.println(fourSumCount(array(20, false), array(20, false), array(20, true), array(20, true)));
    }

    private static int[] array(int n, boolean nagv) {
        int[] arrs = new int[n];
        for (int i = 0; i < arrs.length; i++) {
            arrs[i] = nagv ? RandomUtils.nextInt(0, 100) : -RandomUtils.nextInt(0, 100);
        }
        return arrs;
    }

}
```

[上一篇 IM消息系统](13-项目经验/IM消息系统.md)

[下一篇 LRU缓存机制](13-项目经验/za.md)


[下一篇 LRU缓存机制](1-数据结构与算法/LRU缓存机制.md)
