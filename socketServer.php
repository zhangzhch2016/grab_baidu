<?php
$server = new swoole_websocket_server("0.0.0.0", 9501);

$server->on('open', function (swoole_websocket_server $server, $request) {
    echo "sucess websocketServer";
});

$server->on('message', function (swoole_websocket_server $server, $frame) {
    $getval = $frame->data;
    $valArr = [];
    $vals = explode('&', $getval);
    if(is_array($vals)) {
        foreach($vals as $items) {

            $item = explode('=', $items);
            $valArr[$item[0]] = $item[1];
        }
    }
    if(empty($valArr['search'])) {
        $server->push($frame->fd, "请输入关键字");
    }
    if(empty($valArr['page'])) {
        $valArr['page'] = 1;
    }
    $url = $valArr['isPhone']== 1 ? 'https://www.baidu.com/s?wd='.$valArr['search'] : 'https://www.baidu.com/from=844b/s?word='.$valArr['search'].'#ms=1';
    $data = array("crawl","baidu", "-a", "p={$valArr['page']}","-a","starurl=$url");
    $process = new swoole_process(function(swoole_process $worker)use($data){

	    $worker->exec('/usr/local/python3/bin/scrapy', $data);
	}, true);
    $pid = $process->start();
        while(true){
            echo $backinfo = $process->read();
            $server->push($frame->fd, $backinfo);
            if(strpos($backinfo, 'closed')) {
                 break;
            }
        }
        $filename = file_get_contents(dirname(__FILE__).'/filename');
        $server->push($frame->fd, $filename);
    $ret = swoole_process::wait();
});

$server->on('close', function ($ser, $fd) {

    echo "client {$fd} closed\n";
});

$server->start();