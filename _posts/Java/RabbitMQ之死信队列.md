# RabbitMQ之死信队列

> 一 进入死信队列(进入死信的三个条件)
> - 1.消息被拒绝（basic.reject or basic.nack）并且requeue=false
> - 2.消息TTL过期过期时间
> - 3.队列达到最大长度

DLX也是一下正常的Exchange同一般的Exchange没有区别，它能在任何的队列上被指定，实际上就是设置某个队列的属性，当这个队列中有死信时，RabbitMQ就会自动的将这个消息重新发布到设置的Exchange中去，进而被路由到另一个队列， publish可以监听这个队列中消息做相应的处理， 这个特性可以弥补R abbitMQ 3.0.0以前支持的immediate参数中的向publish确认的功能。

> rabbitmq的三种模式：

> - 1. Fanout Exchange  广播

所有发送到Fanout Exchange的消息都会被转发到与该Exchange 绑定(Binding)的所有Queue上。Fanout Exchange  不需要处理RouteKey 。只需要简单的将队列绑定到exchange 上。这样发送到exchange的消息都会被转发到与该交换机绑定的所有队列上。类似子网广播，每台子网内的主机都获得了一份复制的消息。所以，Fanout Exchange 转发消息是最快的。

> - 2. Direct Exchange  点对点

所有发送到Direct Exchange的消息被转发到RouteKey中指定的Queue。Direct模式,可以使用rabbitMQ自带的Exchange：default Exchange 。所以不需要将Exchange进行任何绑定(binding)操作 。消息传递时，RouteKey必须完全匹配，才会被队列接收，否则该消息会被抛弃。

> - 3. Topic Exchange  模糊匹配

所有发送到Topic Exchange的消息被转发到所有关心RouteKey中指定Topic的Queue上，Exchange 将RouteKey 和某Topic 进行模糊匹配。此时队列需要绑定一个Topic。可以使用通配符进行模糊匹配，符号“#”匹配一个或多个词，符号“*”匹配不多不少一个词。因此“log.#”能够匹配到“log.info.oa”，但是“log.*” 只会匹配到“log.error”。所以，Topic Exchange 使用非常灵活。