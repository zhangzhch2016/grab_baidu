<?php
if($_SERVER['REQUEST_METHOD'] == 'POST'){
    header("Access-Control-Allow-Origin: *");
    ini_set('max_execution_time', '0');
    $search = !empty($_POST['search']) ? trim($_POST['search']) : exit("<script>history.go(-1)</script>");
    $isPhone = $_POST['isPhone'];
    $search = urlencode($search);
    $url = $isPhone == 1 ? 'https://www.baidu.com/s?wd='.$search : 'https://www.baidu.com/from=844b/s?word='.$search.'#ms=1';

    $page = isset($_POST['page']) ? (int)$_POST['page'] : 5;

    if ($page > 20 ) { $page = 20; }

    $cmd = "/usr/local/python3/bin/scrapy crawl baidu -a p={$page} -a starurl={$url}";
    exec($cmd, $info, $start);
    $fieldir = dirname(__FILE__).'/data/'.date('Ymd',time());
    $data = array();
    if($start == 0) {
        if(file_exists($fieldir)){
            $d = dir($fieldir);
            while(false !== ($filename = $d->read())) {
                if ($filename == '.' || $filename == '..'){
                    continue;
                }
                $data[$filename] = filemtime($fieldir.'/'.$filename);
            }
            $newFilename = array_search(max($data), $data);

            if(file_exists($fieldir.'/'.$filename)) {
                $response = array();
                $response['url'] = 'http://114.215.71.127:8888/baidu/data/'.date('Ymd',time())."/".$newFilename;
                $response['code'] = 200;
                echo json_encode($response);die;
            } else {
                echo "未找到文件";
            }
        }else{
            echo "爬取失败";exit();
        }
    }else{
        echo "命令执行失败 错误代码".$start;
    }
}




?>
<html>
    <head>
        <title>爬取百度列表</title>
        <meta charset='utf-8' />
        <link href="//cdn.bootcss.com/bootstrap/4.0.0-alpha.6/css/bootstrap.css" rel="stylesheet">
        <scriptsrc="https://code.jquery.com/jquery-2.2.4.js" integrity="sha256-iT6Q9iMJYuQiMWNd9lDyBUStIq/8PuOW33aOqmvFpqI="crossorigin="anonymous"></script>

    </head>
    <body style="margin:0 auto">
        <div class="text-center" style="background-color: #27ae60;width:100%">
            <form id="spider" style="padding-top:50px;">
                <input style="width:30%;display:inline;" type="text" class="form-control" name="search"  id="inputPassword2" placeholder="关键词">
                <select id='page' class="btn btn-success dropdown-toggle" name="page">
                    <option selected = "selected" value='1'>1</option>
                    <option value='2'>2页</option>
                    <option value='3'>3页</option>
                    <option value='4'>4页</option>
                    <option value='5'>5页</option>
                    <option value='6'>6页</option>
                    <option value='7'>7页</option>
                    <option value='8'>8页</option>
                    <option value='9'>9页</option>
                    <option value='10'>10页</option>
                    <option value='1'>1页</option>
                    <option value='12'>12页</option>
                    <option value='13'>13页</option>
                    <option value='14'>14页</option>
                    <option value='15'>15页</option>
                    <option value='16'>16页</option>
                    <option value='17'>17页</option>
                    <option value='18'>18页</option>
                    <option value='19'>19页</option>
                    <option value='20'>20页</option>

                </select>
                <select id='isPhone' class="btn btn-default dropdown-toggle" name="isPhone">
                    <option selected = "selected" value='1'>PC</option>
                    <option value='2'>手机端</option>
                </select>
                <input type="submit" value="抓取" class="btn btn-primary" name="sub" onclick="request_post(); return false;" />

            </form>
            <a id="address" onclick="display_none()"; href="#" class="btn btn-primary" style="display:none;">下载</a>

                    <textarea id="connect" style="color:#ccc;background-color: #000;width:100%; height: 33%;border: 1px #ccc solid; resize:none;"></textarea>

            <script>
                function display_none(){
                    $("#address").css("display","none");
                     $("input[name=sub]").attr("disabled","");
                }
                $(function(){
                    var diffHeight= $("body").height() - $("#connect").height() - $("#spider").height() -70;
                    $("#connect").css("margin-top",diffHeight+'px')
                    var connect = document.getElementById('connect');
                });
                function request_post(){
                    $("input[name=sub]").attr("disabled","disabled");
                    var search = $("input[name=search]").val().trim();
                    var page = $("#page").find("option:selected").val();
                    var isPhone = $("#isPhone").find("option:selected").val();

                    if (search.length == 0 ) {
                        alert("请输入要搜索的关键词");
                        return false;
                    }
                    var get_val = 'search=' + search + '&page=' + page + '&isPhone=' + isPhone
                    websockt(get_val);
                }

                function websockt(data){
                    var wsServer = 'ws://114.215.71.127:9501';
                    var websocket = new WebSocket(wsServer);
                    websocket.onopen = function (evt) {
                        websocket.send(data);
                        console.log("Connected to WebSocket server.");
                    };
                    websocket.onclose = function (evt) {

                        console.log("Disconnected");
                    };

                    websocket.onmessage = function (evt) {
                        console.log(evt.data);
                        if(evt.data.indexOf('xlsx') >=0) {
                            var date = new Date
                            Y = date.getFullYear();
                            M = (date.getMonth()+1 < 10 ? '0'+(date.getMonth()+1) : date.getMonth()+1);
                            D = date.getDate();
                            var addr = window.location.origin+'/baidu/data/'+Y+M+D+'/'+evt.data;
                            $("#address").attr("href",addr);
                            $("#address").css("display","inline");
                        } else{

                            $("#connect").append(evt.data);
                        }
                        var scrollTop = $("#connect")[0].scrollHeight;
                        $("#connect").scrollTop(scrollTop);

                    };


                    websocket.onerror = function (evt, e) {

                        console.log('Error occured: ' + evt.data);
                    };
                }

            </script>
        </div>
    </body>
</html>



