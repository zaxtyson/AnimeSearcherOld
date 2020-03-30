// 获取搜索结果列表
function getVideos(animeName) {
    console.log("正在搜索: " + animeName);
    let dialog = document.getElementById("search_loading");
    if (!dialog.showModal) {
        dialogPolyfill.registerDialog(dialog);
    }
    dialog.show();
    $.ajax({
        type: "GET",
        url: "/search/" + animeName,
        success: function (ret) {
            dialog.close();
            document.getElementById("page-content").innerHTML = ret;    // 更新网站主体页面
        }
    });
    return false;   // 禁止表单跳转
}

// 点开某集视频后再显示弹幕搜索按钮
function showDanmakuList() {
    $.ajax({
        type: "GET",
        async: false,
        url: "/danmaku_list/" + $.cookie("video_list"),
        success: function (ret) {
            document.getElementById("danmaku_list").innerHTML = ret;
        }
    });
}

let player = null;  // 全局播放器对象

function playVideo(video_hash, danmaku_cid = 0) {
    let video_type = 'auto';
    let dialog = document.getElementById("video_loading");

    if (video_hash != null) {
        $.cookie("playing", video_hash);    // 保存当前视频 hash, 加载弹幕需要重新创建播放器
        $("#search_danmaku_bt").show();
    } else {
        video_hash = $.cookie("playing");   // 仅提供弹幕 cid 播放视频
    }

    // 切换视频前先销毁，否则弹幕无法正常加载
    if (player) {
        player.destroy();
    }

    // 显示加载框
    if (!dialog.showModal) {
        dialogPolyfill.registerDialog(dialog);
    }
    dialog.showModal();

    $.ajax({
        type: "GET",
        async: false,
        url: "/video/" + video_hash + "/type",
        success: function (ret) {
            console.log("视频格式检测: " + ret + ' -> ' + video_hash);
            video_type = ret;
        }
    });


    console.log("加载弹幕 cid: " + danmaku_cid);
    player = new DPlayer({
        container: document.getElementById('player'),
        screenshot: true,
        preload: true,
        autoplay: true,
        video: {
            'url': '/video/' + video_hash + '/data',
            'type': video_type
        },
        danmaku: {
            id: danmaku_cid,
            api: '/video/danmaku/'
        }
    });


    // 加载成功关闭加载框
    player.on("loadeddata", function () {
        console.log("视频加载成功~");
        dialog.close();
    });

    player.on("destroy", function () {
        console.log("播放器销毁");
    });

    // 某些格式视频无法播放，此时显示映射的 URL
    player.on("error", function () {
        if (player.video.error) {   // DPlayer Bug,destroy 事件会重复触发 error 事件
            console.log("视频加载失败 :(");
            prompt("网页端无法播放该视频，请尝试离线播放(或使用支持 URL 播放的本地播放器播放), 视频格式: " + video_type,
                "http://127.0.0.1:5000/video/" + video_hash + "/data");
            dialog.close();
        }
    });
}


// 关于页面
function showAbout() {
    let dialog = document.getElementById("about");
    if (!dialog.showModal) {
        dialogPolyfill.registerDialog(dialog);
    }
    dialog.showModal();
    dialog.querySelector('.close').addEventListener('click', function () {
        dialog.close();
    });
}


// 网页全屏
function openFullscreen() {
    let element = document.documentElement;
    if (element.requestFullscreen) {
        element.requestFullscreen();
    } else if (element.mozRequestFullScreen) {
        element.mozRequestFullScreen();
    } else if (element.msRequestFullscreen) {
        element.msRequestFullscreen();
    } else if (element.webkitRequestFullscreen) {
        element.webkitRequestFullScreen();
    }
    let screen_status = document.getElementById("screen_status");
    screen_status.onclick = exitFullScreen;
    screen_status.firstElementChild.textContent = "fullscreen_exit";
}

// 退出全屏
function exitFullScreen() {
    if (document.exitFullscreen) {
        document.exitFullscreen();
    } else if (document.mozCancelFullScreen) {
        document.mozCancelFullScreen();
    } else if (document.msExitFullscreen) {
        document.msExiFullscreen();
    } else if (document.webkitCancelFullScreen) {
        document.webkitCancelFullScreen();
    } else if (document.webkitExitFullscreen) {
        document.webkitExitFullscreen();
    }
    let screen_status = document.getElementById("screen_status");
    screen_status.onclick = openFullscreen;
    screen_status.firstElementChild.textContent = "fullscreen";
}