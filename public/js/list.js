$(function() {
	var weixinInfos = {
		"oIWsFtzlRvsDVd2e69iSjjYcTbW8": '舟山广电',
		"oIWsFt_90Pc5J5qYypXzgI9E11Rs": '讲拨侬听',
		"oIWsFt0JFB3-dVvN7xqgLwG7lTZQ": '汪大姐来了',
		"oIWsFt5bh4aAeUwAgsLrGjBke2A0": '新闻综合频道',
		"oIWsFt1OUb1JyTvY7AVBizjd4F-w": '公共生活频道',
		"oIWsFtyXxULy9FfmEMrpYoo0Rxu4": '群岛旅游频道',
		"oIWsFt8cgf4W8lutaRBM-4jC0nEA": "新闻998频率",
		"oIWsFt-QtI5IGCGtE1Uc46aj0WZI": '交通97频率',
		"oIWsFt_HcL1-Bt57PtLs3NZbAYo8": '汽车音乐频率',
		"oIWsFt232h6j4SHUooOXzc1wcaXs": '电视新周报'
	};

	var genTmpl = function(d) {
		var key;
		d.data.forEach(function(r) {
			var tmpl = "";
			for (var k in r) {
				var times = k.split("-"),
						y = times[0],
						m = times[1],
						d = times[2];
				tmpl += '<div class="list-frame"><div class="list-time align-center text-white"><time>'+y+'年'+m+'月'+d+'日'+'</time></div><div class="list-content bg-white">';
				r[k].forEach(function(i) {
					tmpl += '<div class="flag flag--reversed"><a href="'+i.href.split("#")[0]+'"><div class="flag__body"><p>'+i.title+'</p></div><div class="flag__item" style="background-image:url(img/'+i.img+')"><img src="img/icon.png" width="90px"></div></a></div>';
					if (!key) key = i.key;
				});
				tmpl += '</div></div>';
				$(".list-getmore").before(tmpl);
			}
		});
		if (!!key) document.title = weixinInfos[key];
	};

	$.hg_h5app({
		"needUserInfo": function(d) {
			var _callAjax = _genCallAjax("http://develop.zsgd.com:11011/dlm/"),
					key = _getPar("key");
			_callAjax({
				"cmd":"getWeixins",
				"key":key,
			}, function(d) {
				// document.title = d.name;
				genTmpl(d);
				$(".list-getmore").click(function() {
					var k = $(".list-frame:last time").text().match(/\d+/g).join("-")
					var dt = new Date(k),
							m = dt.getMonth()+1,
							dd = dt.getDate(dt.setDate(dt.getDate()-1));
					if (m < 10) m = "0"+m;
					if (dd < 10) dd = "0"+dd;
					_callAjax({
						"cmd":"getWeixins",
						"date":dt.getFullYear()+"-"+m+'-'+dd,
						"key":key
					}, function(d) { genTmpl(d); });
				});

				$(".list-content a").click(function() {
					window.location.href = $(this).attr("href");
				});
			});
		}
	});
});
