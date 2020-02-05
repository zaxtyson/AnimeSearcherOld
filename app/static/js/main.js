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

function playVideo(video_hash) {
    let video_type = 'auto';
    let dialog = document.getElementById("video_loading");
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

    const player = new DPlayer({
        container: document.getElementById('player'),
        screenshot: true,
        preload: true,
        autoplay: true,
        audio: 100,
        video: {
            'url': '/video/' + video_hash + '/data',
            'type': video_type
        }
    });

    player.on("loadeddata", function () {
        console.log("视频加载成功~");
        dialog.close();
    });

    player.on("error", function () {
        console.log("视频加载失败 :(");
        prompt("网页端无法播放该视频，请尝试离线播放(或使用支持 URL 播放的本地播放器播放), 视频格式: " + video_type,
            "http://127.0.0.1:5000/video/" + video_hash + "/data");
        dialog.close();
    })


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