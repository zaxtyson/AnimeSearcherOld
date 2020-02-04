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

// 获取视频播放列表页面数据
function getPlayList(list_hash) {
    console.log("获取视频播放列表:" + list_hash);
    $.ajax({
        type: "GET",
        url: "/playlist/" + list_hash,
        success: function (ret) {
            document.getElementById("page-content").innerHTML = ret;
        },
    });
}

function playVideo(video_hash, video_type) {
    console.log("播放视频 [" + video_type + "]: " + video_hash);
    new DPlayer({
        container: document.getElementById('player'),
        screenshot: true,
        preload: true,
        autoplay: true,
        audio: 100,
        video: {
            'url': '/video/' + video_hash,
            'type': video_type
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