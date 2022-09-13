# RaRe
RaRe: Universal module to work with RabbitMQ for multiple task repetitions with time delays between repetitions.

## What does this package do?

- It allows you to repeat a task from the queue N times (or with a time limit) with delays between retries.
- Delays between retries can be adjusted both "manually" and according to different algorithms (log, fibo, linear, etc.).
- If the task was NOT executed successfully N times - redirects the task to a bug queue for searching for the bug
- Execution of a task in accordance with a "queue chain": when a task gets to one queue, then to the second and so on, as long as required.
- Delayed start of task execution
- Easily and simply add and maintain final "handlers" for task execution, depending on "payloads"
- Start the vorker (via command line) with a "subscribe" to the queue. The name of the queue is passed through a parameter:

`$ python run_worker.py -q queue_name`

## Why is the package written for?

This package (in the next version will be available as a module through PyPi), is written for tasks where you need guaranteed execution of various queries or calculations that are relevant for a limited time.

If it fails N-times (or before a expired-time), the task is automatically redirected to a bug queue. Where testers can already figure out why the problem occurred.

Bug-logging is on developers' conscience :)

First of all, this solution was written for mailing lists (sms, email, push, telegram, etc.) and critical HTTP requests to external servers.


> ### Example:
>
> __Task:__
>
> One task uses the service DeepL (HTTP POST Request) to automatically translate texts.
>
> __Problem:__
>
> In the process of work it turned out that DeepL servers often fail to respond. Failures could last from 1 to 30 minutes.
>
> If tasks were sent to repeat each time without delay, they would pile up quickly and keep sending requests to the "lying" servers.
>
> __Solution:__
>
> As a solution, DLX queues (about the same as in Celary) were used, with varying time delays between attempts to process the request.
>
> The first 3 minutes requests were sent frequently, and then less and less frequently, but until the task was executed or its "shelf life" expired.
>
> __Result:__
>
> In the end, the problem was completely solved. Everything is translated steadily, and the servers are not overloaded with unnecessary work.

This module allows you to flexibly adjust the time delay between retries.

> ### Example two:
> 
> Tracking regular service payments with a subscription.
> 
> __Task:__
> 
> Make regular charges to subscribers' cards.
> 
> __Problem:__
> 
> At the time of attempting to debit funds, there were crashes for various reasons: not enough funds on the card, server request crashes, third-party server crashes (less often), etc.
> 
> __Solution:__
> 
> The debit attempt was repeated several times at increasing intervals, up to once every three days.
> 
> The time limit was a week, and in case of unsuccessful completion, the task was placed in the "SENDER queue", after which the user was sent messages to disconnect the services.
> 
> __Result:__
> 
> As a result, payment problems decreased to the minimum values for the entire period of operation. The LTV indicator increased and the load on the support service decreased.

## Documentation coming soon :)

WBR, Dmitry
dmaevsky@gmail.com
