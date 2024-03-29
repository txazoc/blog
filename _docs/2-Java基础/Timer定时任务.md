## Timer定时任务

#### TimerTask

定时任务

```java
public abstract class TimerTask implements Runnable {

    // 锁
    final Object lock = new Object();
    // 任务状态
    int state;
    // 下一次执行时间
    long nextExecutionTime;
    /**
     * 重复任务的间隔时间
     *
     * period = 0, 不重复
     * period > 0, 固定频率执行的间隔时间
     * period < 0, 固定延迟执行的间隔时间
     */
    long period = 0;

}
```

#### TaskQueue

任务队列，最小堆实现的优先级队列

```java
class TaskQueue {

    // 队列中元素数量
    private int size = 0;
    // 堆
    private TimerTask[] queue = new TimerTask[128];

    /**
     * 返回下一次要执行的任务, 即队头
     */
    TimerTask getMin() {
        return queue[1];
    }

    /**
     * 上浮
     */
    private void fixUp(int k) {
        while (k > 1) {
            int j = k >> 1;
            if (queue[j].nextExecutionTime <= queue[k].nextExecutionTime)
                break;
            TimerTask tmp = queue[j];
            queue[j] = queue[k];
            queue[k] = tmp;
            k = j;
        }
    }

    /**
     * 下沉
     */
    private void fixDown(int k) {
        int j;
        while ((j = k << 1) <= size && j > 0) {
            // 选择较小的子节点
            if (j < size && queue[j].nextExecutionTime > queue[j + 1].nextExecutionTime)
                j++;
            if (queue[k].nextExecutionTime <= queue[j].nextExecutionTime)
                break;
            TimerTask tmp = queue[j];
            queue[j] = queue[k];
            queue[k] = tmp;
            k = j;
        }
    }
}
```

#### TimerThread

定时任务执行线程，单线程执行

* TimerThread主循环
* queue为空，则wait()
* task = queue.getMin()
* 比较System.currentTimeMillis()和nextExecutionTime
    * nextExecutionTime > System.currentTimeMillis()，wait()两者之差的时间
    * nextExecutionTime <= System.currentTimeMillis()
        * period == 0，从队列中删除task
        * period != 0，重新计算并设置task的nextExecutionTime，然后执行下沉
        * task.run()
