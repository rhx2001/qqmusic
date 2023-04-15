(function() {
	// 获取窗口dom
	var domScrollDiv = document.getElementById('id-scroll-div');
  var domScrollItem1 = document.getElementById('id-scroll-item1');
  var scrollTimer = null;
  var rollingType = 'smooth';
  var deviationY = 10;
  var rowHeight = 40;
  var interval = 50;
  var funRun = function() {
    clearInterval(scrollTimer);
    scrollTimer = null;
    if (rollingType === 'smooth') {
			interval = 50;
    } else {
    	interval = 1500;
    }
  	scrollTimer = setInterval(()=>{
        funScrollDiv();
      }, interval)
  };
  var funScrollDiv = function() {
		if (domScrollDiv.offsetHeight >= domScrollItem1.offsetHeight) {
      return;
    }
    switch (rollingType) {
      case 'oneWay': {
        if (domScrollDiv.scrollTop >= domScrollItem1.scrollHeight) {
          // 滚动到顶部
          domScrollDiv.scrollTop = 0;
          domScrollDiv.scrollTo({
            // 从顶部滚动到第一行
            top: rowHeight + deviationY,
            behavior: "smooth",
          });
        } else {
          domScrollDiv.scrollBy({
            // 相对于当前位置每次向下滚动一个项目高度
            top: rowHeight + deviationY,
            behavior: "smooth",
          });
        }
        break;
      }
      case 'page': {
        if (domScrollDiv.scrollTop + domScrollDiv.offsetHeight >= domScrollItem1.scrollHeight) {
          // 复位
          domScrollDiv.scrollTop = 0;
        } else {
          domScrollDiv.scrollBy({
            top: domScrollDiv.offsetHeight,
            behavior: "smooth",
          });
        }
        break;
      }
      default:
      	// 判断滚动位置是否超出窗口
        if (domScrollDiv.scrollTop >= domScrollItem1.scrollHeight + deviationY) {
        	// 关键操作，超出窗口时 重置位置，由于是瞬发，刚好与下一帧衔接。
          domScrollDiv.scrollTop = 0;
        } else {
          domScrollDiv.scrollTop ++;
        }
        break;
    }
  }
  funRun();
})()
